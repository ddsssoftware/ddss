<section id="case_description">
    <h3>{{ __('ddss.case_description_title') }}</h3>
    <form id="case_description_form"
          method="POST"
          action="{{ route('case.updatedescription') }}">
        <input type="hidden" name="case" value="{{ $savedCase }}" />
        <textarea name="description">{{ ($case['description'] ?? '') }}</textarea>
        <button>{{ __('ddss.case_description_form_save') }}</button>
    </form>
</section>