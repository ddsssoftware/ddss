<div class="symptom_item">
    <span id="symptom_item_name_{{ $result->symptom_id }}"
          class="symptom_item_name"
          data-has-collapsed-details="true">{{ $result->symptom_name }}</span>
    <div id="symptom_item_details_{{ $result->symptom_id }}" 
        class="symptom_item_details"
        style="display: none;">

        <a id="symptom_item_details_factsheet_{{ $result->symptom_id }}"
            href="{{ route('factsheet.symptom', [$result->symptom_id])}}"
            target="_blank">{{ __('ddss.symptom_item_details_factsheet')}}</a>
    
            <div id="symptom_item_details_presence_{{ $result->symptom_id }}" class="symptom_item_details_presence">
            <form id="symptom_item_details_presence_form_{{ $result->symptom_id }}"
                  method="POST"
                  action="{{ route('case.symptom.present') }}">
                <input type="hidden" name="case" value="{{ $savedCase }}" />
                <input type="hidden" name="symptom" value="{{ $result->symptom_id }}">
                <button id="symptom_item_details_presence_form_submit_{{ $result->symptom_id }}"
                        class="symptom_item_details_presence_form_submit">{{ __('ddss.symptom_item_details_presence_present') }}</button>
            </form>
            <form id="symptom_item_details_presence_form_{{ $result->symptom_id }}"
                  method="POST"
                  action="{{ route('case.symptom.notpresent') }}">
                <input type="hidden" name="case" value="{{ $savedCase }}" />
                <input type="hidden" name="symptom" value="{{ $result->symptom_id }}">
                <button id="symptom_item_details_presence_form_submit_{{ $result->symptom_id }}"
                        class="symptom_item_details_presence_form_submit">{{ __('ddss.symptom_item_details_presence_not-present') }}</button>
            </form>
        </div>


        <div id="symptom_item_details_tests_{{ $result->symptom_id }}" class="symptom_item_details_tests">
            @foreach($result->tests as $test)
                <button>{{ $test->test_name }}</button>
            @endforeach
        </div>

        <div id="symptom_item_details_notes_{{ $result->symptom_id }}" class="symptom_item_details_notes">
            <textarea id="symptom_item_details_notes_text_{{ $result->symptom_id }}" placeholder="Notes"></textarea>
        </div>
    </div>
</div>