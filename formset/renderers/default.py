import copy
import types

from django.forms.renderers import DjangoTemplates


class FormRenderer(DjangoTemplates):
    max_options_per_line = 4

    _template_mapping = {
        'django/forms/errors/list/default.html': 'formset/default/field_errors.html',
        'django/forms/default.html': 'formset/default/form.html',
        'django/forms/widgets/radio.html': 'formset/default/widgets/multiple_input.html',
        'django/forms/widgets/file.html': 'formset/default/widgets/file.html',
        'django/forms/widgets/checkbox_select.html': 'formset/default/widgets/multiple_input.html',
    }

    def __init__(self, field_css_classes=None, label_css_classes=None, control_css_classes=None,
                 form_css_classes=None, max_options_per_line=None):
        self.field_css_classes = field_css_classes
        self.label_css_classes = label_css_classes
        self.control_css_classes = control_css_classes
        self.form_css_classes = form_css_classes
        if max_options_per_line is not None:
            self.max_options_per_line = max_options_per_line
        super().__init__()

    def get_template(self, template_name):
        template_name = self._template_mapping.get(template_name, template_name)
        return super().get_template(template_name)

    def _amend_form(self, context):
        context.update(
            control_css_classes=self.control_css_classes,
            form_css_classes=self.form_css_classes,
        )
        return context

    def _amend_label(self, context, hide_checkbox_label=False):
        if self.label_css_classes:
            if not isinstance(context['attrs'], dict):
                context['attrs'] = {}
            context['attrs']['class'] = self.label_css_classes
        if hide_checkbox_label and context['field'].widget_type == 'checkbox':
            # label is rendered by {{ field }}, so remove it to prevent double rendering
            context['use_tag'] = False
            context.pop('label', None)
        return context

    def _amend_multiple_input(self, context):
        """
        Inlines a small number of radio/checkbox fields to render them on one line.
        """
        max_options = 0
        for group, options, index in context['widget']['optgroups']:
            if group is None:
                max_options = len(context['widget']['optgroups'])
                break
            max_options = max(max_options, len(options))
        context['widget']['inlined_options'] = max_options <= self.max_options_per_line
        return context

    _context_modifiers = {
        'django/forms/default.html': _amend_form,
        'django/forms/label.html': _amend_label,
        'django/forms/widgets/checkbox_select.html': _amend_multiple_input,
        'django/forms/widgets/radio.html': _amend_multiple_input,
    }

    def render(self, template_name, context, request=None):
        context = copy.deepcopy(context)
        context_modifier = self._context_modifiers.get(template_name)
        if callable(context_modifier):
            context = types.MethodType(context_modifier, self)(context)
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()
