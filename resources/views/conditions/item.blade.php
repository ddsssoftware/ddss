<div class="condition_item">
    <span id="condition_item_name_{{ $result->id }}"
          class="condition_item_name">{{ $result->name }}</span>
    <div id="condition_item_details_{{ $result->id }}" 
        class="condition_item_details"
        style="display: none;">

        <a id="condition_item_details_factsheet_{{ $result->id }}"
            href="{{ route('factsheet.condition', [$result->id])}}"
            target="_blank">{{ __('ddss.condition_item_details_factsheet')}}</a>
    
        <div id="condition_item_details_presence_{{ $result->id }}" class="condition_item_details_presence">
            <form id="condition_item_details_presence_form_{{ $result->id }}" method="POST" action="{{ route('case.condition.present') }}">
                <input type="hidden" name="condition" value="{{ $result->id }}">
                <button id="condition_item_details_presence_form_button_{{ $result->id }}" class="condition_item_details_presence_form_button" type="button">{{ __('ddss.condition_item_details_presence_present') }}</button>
            </form>
            <button>{{ __('ddss.condition_item_details_presence_not-present') }}</button>
        </div>

        <div id="condition_item_details_notes_{{ $result->id }}" class="condition_item_details_notes">
            <textarea id="condition_item_details_notes_text_{{ $result->id }}" placeholder="Notes"></textarea>
        </div>
    </div>
</div>