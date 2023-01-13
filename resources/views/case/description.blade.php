<section>
    <h3>{{ __('ddss.case_description_title') }}</h3>
    <form id="case_description_form" method="POST"
          action="{{ route('case.description.update') }}">
        <input type="hidden" name="c" value="{{ $savedCase }}" />
        <textarea id="case_description_form_textarea" name="description">{{ ($case[Diagnosis::DESCRIPTION] ?? '') }}</textarea>
        <button id="case_description_form_submit">{{ __('ddss.case_description_form_save') }}</button>
    </form>
</section>