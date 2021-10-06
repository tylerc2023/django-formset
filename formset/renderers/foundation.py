from formset.renderers.default import FormRenderer as DefaultFormRenderer


class FormRenderer(DefaultFormRenderer):
    _template_mapping = dict(DefaultFormRenderer._template_mapping, **{
        'django/forms/default.html': 'formset/foundation/form.html',
        'django/forms/widgets/radio.html': 'formset/foundation/widgets/multiple_input.html',
        'formset/default/widgets/file.html': 'formset/foundation/widgets/file.html',
        'django/forms/widgets/checkbox_select.html': 'formset/foundation/widgets/multiple_input.html',
    })

    def _amend_multiple_input(self, context):
        context = super()._amend_multiple_input(context)
        if context['widget'].get('inlined_options'):
            for _, optgroup, _ in context['widget']['optgroups']:
                for option in optgroup:
                    option['template_name'] = 'formset/foundation/widgets/inlined_input_option.html'
        return context

    _context_modifiers = dict(DefaultFormRenderer._context_modifiers, **{
        'django/forms/widgets/checkbox_select.html': _amend_multiple_input,
        'django/forms/widgets/radio.html': _amend_multiple_input,
    })