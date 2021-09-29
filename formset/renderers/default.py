from django.forms.renderers import DjangoTemplates


class FormRenderer(DjangoTemplates):
    template_mapping = {
        'django/forms/errors/list/default.html': 'formset/default/field_errors.html',
        'django/forms/default.html': 'formset/default/form.html',
        'django/forms/label.html': 'formset/default/label.html',
        'django/forms/widgets/text.html': 'formset/default/widgets/input.html',
        'django/forms/widgets/radio.html': 'formset/default/widgets/radio.html',
        'django/forms/widgets/email.html': 'formset/default/widgets/input.html',
        'django/forms/widgets/file.html': 'formset/default/widgets/file.html',
        'django/forms/widgets/checkbox.html': 'formset/default/widgets/input.html',
        'django/forms/widgets/date.html': 'formset/default/widgets/input.html',
        'django/forms/widgets/select.html': 'formset/default/widgets/select.html',
        'django/forms/widgets/number.html': 'formset/default/widgets/input.html',
        'django/forms/widgets/checkbox_select.html': 'formset/default/widgets/checkbox_select.html',
        #'django/forms/widgets/textarea.html': 'formset/default/widgets/textarea.html',
        'django/forms/widgets/password.html': 'formset/default/widgets/input.html',
        'django/forms/widgets/hidden.html': 'formset/default/widgets/input.html',
    }

    def get_template(self, template_name):
        template_name = self.template_mapping.get(template_name, template_name)
        return super().get_template(template_name)

    def render(self, template_name, context, request=None):
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()
