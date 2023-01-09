<div class="case_condition_item">
    <div class="case_condition_item_header">
        <span id="case_condition_item_name_{{ $condition->id }}" class="case_condition_item_name" data-has-collapsed-details="true">{{ $condition->name }}</span>
    </div>
    <div id="case_condition_item_details_{{ $condition->id }}" class="case_condition_item_details" style="display: none;">
        <a id="condition_item_details_factsheet_{{ $condition->id }}"
            href="{{ route('factsheet.condition', [$condition->id])}}"
            target="_blank">{{ __('ddss.case_condition_item_details_factsheet')}}</a>
        <p>{{ $condition->notes }}</p>
        <button>{{ __('ddss.case_condition_item_details_remove')}}</button>
    </div>
</div>