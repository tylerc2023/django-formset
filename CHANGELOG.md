## Changes

- 0.10.2
  * In sortable form collections, add a CSS ghost class to make moved item more opaque. This is for
    a better usability experience.
  * In sortable form collections, change the form name after moving a collection. This fixes a
    problem with form validation.
  * Fix: On forms created from a model, method `IncompleteSelectResponseMixin.fetch_options()`
    raised an AttributeError.
  * Class `FormCollection` and class `Fieldset` accept an optional help text which is rendered at
    the bottom of a `<django-form-collection>` or `<fieldset>`.
  * Some rendering templates remove whitespace using templatetag `{% spaceless %}`.
  * Django-4.1 now is officially supported.

- 0.10.1
  * The HTML tags for `<select is="django-selectize">` and `<select is="django-dual-selector">`
    declare their own webcomponents which now add their own HTML elements in front of themselves,
    before hiding. Instead of hiding via `display: none;` they now "conceal" so that the browser
    can set focus on input fields not validating.
  * Replace `uglify` against `terser` to minify JavaScript files.
  * In webcomponent `<select is="django-dual-selector">`, replace `elem.getValue()` against
    `elem.value`.
  * Simplify the way events handlers are called.
  * Remove the CSRF-Token from the request header of webcomponents `<select is="django-selectize">`
    and `<select is="django-dual-selector">`, since they exclusively use GET requests.
  * The right selector box of the webcomponent `<select is="django-dual-selector" required …>`
    highlights as invalid (by rendering a red border), if input data is missing.

- 0.10
  * The right part of the widget `DualSelector` optionally is sortable now. Views accepting forms
    with this widget can rely upon that sorting order and store it.
  * Form collections with siblings can optionally be declared as sortable. A drag handle is then
    rendered above the collection, which can be used for sorting.
  * Add Germans translations text readable by the end user.

- 0.9.1
  * The optional URL parameter passed into button action `proceed(...)` now takes precedence over
    the `success_url` returned inside the response object.
  * Allow wrapping HTML elements between a `<django-formset>` and its immediate
    `<django-form-collection>`-elements.
  * Add German translations.

- 0.9
  * Fixed problems when resetting a formset containing multiple collections with siblings: All just
    added collections are removed on reset.
  * Distinguish while removing a collection: A just added collection is removed, while existing
    collections are marked for removal.
  * On cleaning post data while processing collections, one can choose whether to keep existig but
    removed colections for further processing, or ignore them.
  * Allow extra label to be added inside the "Add collection" button.
  * Handle CSRF token via attribute to `<django-formset csrf-token="…">` rather than using a cookie.
  * Fix typo: Rename  `IncompleSelectResponseMixin` -> `IncompleteSelectResponseMixin`.
  * Fix some issues with `FormCollection`-s: Invoking `replicate` now creates a deep copy of all
    children.
  * Fix in widget `FileInput`: On reloading the form, the provided value is kept to its initial
    state.

- 0.8.8
  * Use a simpler and semantically more correct HTML representation for the file uploader widget.

- 0.8.7
  * Fix: If an uploaded image has an EXIF orientation tag, that image that is transposed accordingly.
  * On file upload, fill the progressbar to only 90%. The remaining 10% of the progressbar are
    filled after successful image transformation.
  * Rename Event "submit" to "submitted", because otherwise FireFox triggers a page reload.

- 0.8.6
  * Fix: Files uploaded into collections with siblings, are not duplicated anymore.
  * Fix: Clear `cleaned_data` during form validation to prevent duplicate content.
  * Fix occasionally occuring MRO-TypeError when instantiating checkbox widget.
  * Remove tag "_marked_for_removal_" while submitting form. Use Array with holes instead.
  * In Collections with siblings, do not extend number of siblings, if maximum is reached.

- 0.8.5
  * Fix: Form collections with empty siblings, on submission now create an empty array.

- 0.8.4
  * Add optional argument for delay in milliseconds to button actions `okay` and `bummer`. 
  * Resetting a django-formset removes all just added sibling collections and unmarks all
    collections for removal.
  * Fields beeing hidden on the client using `show-if`/`hide-if` also are disabled to prevent
    validation – which wouldn't make sense anyway.
  * Add parameter `legend` to Form Collection so that a collection can have an optional title.

- 0.8.3
  * Fix: For ``field_css_classes``, fall back to form name rather than its prefix.

- 0.8.2
  * Fix: Set empty dropbox item on upload widget during form reset.
  * Fix: Collections with siblings on root level generated invalid form data.
  * Add special placeholder to render errors for collections with siblings.
  * Add additional actions to button: Spinner, Okay, Bummer and Reload.
  * In Button's proceed action, print a warning, if neither a success-, nor a
    fallback-URL is given to proceed.
  * In `FormCollectionView` handle response of posting formsets analogous to the way
    Django handles forms.

- 0.8.1
  * Adopt `DualSelector` for Tailwind.css.
  * Hide `calendar-picker-indicator` in touched input date fields.
  * Fix: Expecting path for base location as Path object.
  * Fix: Updating of existing object failed.
  * Add method `get_extra_data` to class `FormView`.
  * Increase max filename length to 250 characters.
  * Fix: Abort silently if input field is missing.
  * Replace `<div>`-based progress bar against proper HTML element `<progress>`.

- 0.8
  * Add widget `DualSelector` which accepts multiple values and is the form field counterpart
    to Django's `ManyToManyField`. This is an alternative widget to `SelectizeMultiple`.

- 0.7
  * Add widget `SelectizeMultiple` which accepts multiple values and is the form field counterpart
    to Django's `ManyToManyField`.
  * Bugfix in UploadWidget: Do not delete existing file on form update.

- 0.6
  * Content from `FileUploadWidget` can be transfered to a Django model and vice versa.

- 0.4
  * It is possible to control every aspect of the feedback, given to the user while he fills the
    input fields.
  * Templatetag `render_form` and `formsetify` accepts parameters `form_classes` and
    `collection_classes` for finer styling control.

- 0.3
  * Add `show-if`, `hide-if` and `disable-if` attribute parsing to fields and fieldsets.
  * Add class `Fieldset` to handle forms with legends and the possibility for hiding and disabling.
  * Form Collections may have siblings and can be extended.

- 0.2
  * Refactored to work for Django>4 only.
  * Added Form Collections.

- 0.1
  * Initial release.
