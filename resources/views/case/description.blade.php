<section id="case_description">
    <h3>{{ __('ddss.case_description_title') }}</h3>
    <form id="case_description_form"
          method="POST"
          action="{{ route('case.updatedescription') }}"
          data-form-needs-case="true">
        <textarea id="case_description_form_text" name="description">{{ ($case['description'] ?? '') }}</textarea>
        <button id="case_description_form_submit">{{ __('ddss.case_description_form_save') }}</button>
    </form>
</section>