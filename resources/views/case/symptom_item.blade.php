<div class="case_symptom_item">
    <div class="case_symptom_item_header">
        <span id="case_symptom_item_name_{{ $symptom[Diagnosis::ID] }}" class="case_symptom_item_name" data-has-collapsed-details="true">{{ $symptom[Diagnosis::NAME] }}</span>
        <span class="case_symptom_item_presence">{{ __($symptom[Diagnosis::PRESENCE] ? 'ddss.case_symptom_item_presence_present' : 'ddss.case_symptom_item_presence_not-present') }}</span>
    </div>
    <div id="case_symptom_item_details_{{ $symptom[Diagnosis::ID] }}" class="case_symptom_item_details" style="display: none;">
        <a id="symptom_item_details_factsheet_{{ $symptom[Diagnosis::ID] }}"
            href="{{ route('factsheet.symptom', [$symptom[Diagnosis::ID]])}}"
            target="_blank">{{ __('ddss.case_symptom_item_details_factsheet')}}</a>
        <p>{{ $symptom[Diagnosis::NOTES] }}</p>
        <form action="{{ route('case.symptom.remove') }}"
            method="POST">
            <input type="hidden" name="symptom" value="{{ $symptom[Diagnosis::ID] }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_symptom_item_details_remove') }}</button>
        </form>
    </div>
</div>