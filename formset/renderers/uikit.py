from formset.renderers.default import FormRenderer as DefaultFormRenderer


class FormRenderer(DefaultFormRenderer):
    _template_mapping = dict(DefaultFormRenderer._template_mapping, **{
        'django/forms/default.html': 'formset/uikit/form.html',
        'django/forms/widgets/checkbox.html': 'formset/uikit/widgets/checkbox.html',
        'django/forms/widgets/radio.html': 'formset/uikit/widgets/multiple_input.html',
        'formset/default/widgets/file.html': 'formset/uikit/widgets/file.html',
        'django/forms/widgets/checkbox_select.html': 'formset/uikit/widgets/multiple_input.html',
    })

    def _amend_input(self, context):
        context['widget']['attrs']['class'] = 'uk-input'
        return context

    def _amend_label(self, context):
        context = super()._amend_label(context, hide_checkbox_label=True)
        if not isinstance(context['attrs'], dict):
            context['attrs'] = {}
        css_classes = []
        if css_class := context['attrs'].pop('class', None):
            css_classes.append(css_class)
        css_classes.append('uk-form-label')
        context['attrs']['class'] = ' '.join(css_classes)
        return context

    def _amend_textarea(self, context):
        context['widget']['attrs']['class'] = 'uk-textarea'
        return context

    def _amend_select(self, context):
        context['widget']['attrs']['class'] = 'uk-select'
        return context

    def _amend_multiple_input(self, context):
        context = super()._amend_multiple_input(context)
        for _, optgroup, _ in context['widget']['optgroups']:
            for option in optgroup:
                option['template_name'] = 'formset/uikit/widgets/input_option.html'
        return context

    _context_modifiers = dict(DefaultFormRenderer._context_modifiers, **{
        'django/forms/label.html': _amend_label,
        'django/forms/widgets/text.html': _amend_input,
        'django/forms/widgets/email.html': _amend_input,
        'django/forms/widgets/date.html': _amend_input,
        'django/forms/widgets/number.html': _amend_input,
        'django/forms/widgets/password.html': _amend_input,
        'django/forms/widgets/textarea.html': _amend_textarea,
        'django/forms/widgets/select.html': _amend_select,
        'django/forms/widgets/checkbox_select.html': _amend_multiple_input,
        'django/forms/widgets/radio.html': _amend_multiple_input,
        'formset/default/widgets/selectize.html': _amend_select,
    })
