<div class="case_symptom_item">
    <div class="case_symptom_item_header">
        <span id="case_symptom_item_name_{{ $symptom->id }}" class="case_symptom_item_name" data-has-collapsed-details="true">{{ $symptom->name }}</span>
        <span class="case_symptom_item_presence">{{ __($symptom->present ? 'ddss.case_symptom_item_presence_present' : 'ddss.case_symptom_item_presence_not-present') }}</span>
    </div>
    <div id="case_symptom_item_details_{{ $symptom->id }}" class="case_symptom_item_details" style="display: none;">
        <a id="symptom_item_details_factsheet_{{ $symptom->id }}"
            href="{{ route('factsheet.symptom', [$symptom->id])}}"
            target="_blank">{{ __('ddss.case_symptom_item_details_factsheet')}}</a>
        <p>{{ $symptom->notes }}</p>
        <form action="{{ route('case.symptom.remove') }}"
            method="POST">
            <input type="hidden" name="symptom" value="{{ $symptom->id }}">
            <input type="hidden" name="case" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_symptom_item_details_remove') }}</button>
        </form>
    </div>
</div>