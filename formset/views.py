import json

from django.http.response import HttpResponseBadRequest, JsonResponse
from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.edit import FormView as GenericFormView
from django.views.generic.detail import SingleObjectMixin

from formset.upload import FileUploadMixin
from formset.widgets import Selectize, DualSelector


class IncompleSelectResponseMixin:
    """
    Add this mixin class to views classes using forms with incomplete fields. These fields
    usually are of type ChoiceField referring to a foreign model and using one of the widgets
    :class:`formset.widgets.Selectize`, :class:`formset.widgets.SelectizeMultiple` or
    :class:`formset.widgets.DualSelector`.
    """
    def get(self, request, **kwargs):
        if request.accepts('application/json') and 'field' in request.GET:
            if 'query' in request.GET or 'offset' in request.GET:
                return self._fetch_options(request)
        return super().get(request, **kwargs)

    def _fetch_options(self, request):
        field_path = request.GET['field']
        try:
            field = self.get_field(field_path)
        except KeyError:
            return HttpResponseBadRequest(f"No such field: {field_path}")
        assert isinstance(field.widget, (Selectize, DualSelector))
        try:
            offset = int(request.GET.get('offset'))
        except TypeError:
            offset = 0
        if query := request.GET.get('query'):
            data = {'query': query}
            queryset = field.widget.search(query)
            incomplete = None  # incomplete state unknown
        else:
            data = {}
            queryset = field.widget.choices.queryset
            incomplete = queryset.count() - offset > field.widget.max_prefetch_choices
        limited_qs = queryset[offset:offset + field.widget.max_prefetch_choices]
        to_field_name = field.to_field_name if field.to_field_name else 'pk'
        items = [{'id': getattr(item, to_field_name), 'label': str(item)} for item in limited_qs]
        data.update(
            count=len(items),
            total_count=field.widget.choices.queryset.count(),
            incomplete=incomplete,
            items=items,
        )
        return JsonResponse(data)


class FormsetResponseMixin:
    @cached_property
    def _request_body(self):
        if self.request.content_type == 'application/json':
            return json.loads(self.request.body)

    def get_extra_data(self):
        """
        When submitting a form, one can additionally add extra parameters via the button's ``submit()`` action.
        Use this method to access that extra data.
        """
        if self._request_body:
            return self._request_body.get('_extra')


class FormViewMixin(FormsetResponseMixin):
    def get_success_url(self):
        """
        In **django-formset**, the success_url may be None and set inside the templates.
        """
        return str(self.success_url) if self.success_url else None

    def form_valid(self, form):
        response = super().form_valid(form)
        assert response.status_code == 302
        return JsonResponse({'success_url': self.get_success_url()})

    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse(form.errors, status=422, safe=False)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self._request_body:
            kwargs['data'] = self._request_body.get('formset_data')
        return kwargs

    def get_field(self, path):
        field_name = path.split('.')[-1]
        return self.form_class.base_fields[field_name]


class FormView(IncompleSelectResponseMixin, FileUploadMixin, FormViewMixin, GenericFormView):
    """
    FormView class used as controller for handling a single Django Form. The purpose of this View
    is to render the provided Form, when invoked as a standard GET-request using the provided Django
    Template.
    This View also acts as endpoint for POST-requests submitting files, as endpoint for GET-requests
    querying for autocomplete Select-Fields and as endpoint for Form submissions.

    It can be used directly inside the URL routing:

    .. code-block:: python

        from django.urls import path
        from formset.views import FormView

        ...
        urlpatterns = [
            ...
            path('my-uri', FormView.as_view(
                form_class=MyForm,
                template_name='my-form.html',
                success_url='/success',
            )),
            ...
        ]

    """


class FormCollectionViewMixin(FormsetResponseMixin):
    collection_class = None
    success_url = None
    initial = {}

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate blank versions of the forms in the collection."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, **kwargs):
        form_collection = self.get_form_collection()
        if form_collection.is_valid():
            return self.form_collection_valid(form_collection)
        else:
            return self.form_collection_invalid(form_collection)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_collection'] = self.get_form_collection()
        return context

    def get_field(self, path):
        return self.form_collection.get_field(path)

    def get_form_collection(self):
        collection_class = self.get_collection_class()
        kwargs = {
            'initial': self.get_initial(),
        }
        if self.request.method in ('POST', 'PUT') and self.request.content_type == 'application/json':
            body = json.loads(self.request.body)
            kwargs.update(data=body.get('formset_data'))
        return collection_class(**kwargs)

    def get_collection_class(self):
        return self.collection_class

    def get_initial(self):
        """Return the initial data to use for collections of forms on this view."""
        return self.initial.copy()

    def get_success_url(self):
        return str(self.success_url) if self.success_url else None

    def form_collection_valid(self, form_collection):
        return JsonResponse({'success_url': self.get_success_url()})

    def form_collection_invalid(self, form_collection):
        return JsonResponse(form_collection.errors, status=422, safe=False)


class FormCollectionView(IncompleSelectResponseMixin, FileUploadMixin, FormCollectionViewMixin, ContextMixin, TemplateResponseMixin, View):
    pass


class EditCollectionView(IncompleSelectResponseMixin, FileUploadMixin, FormCollectionViewMixin, SingleObjectMixin, TemplateResponseMixin, View):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            collection_class = self.get_collection_class()
            initial.update(collection_class().model_to_dict(self.object))
        return initial

    def form_collection_valid(self, form_collection):
        form_collection.construct_instance(self.object, form_collection.cleaned_data)
        return super().form_collection_valid(form_collection)
