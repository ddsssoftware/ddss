<div class="symptom_item">
    <span id="symptom_item_name_{{ $result->id }}"
          class="symptom_item_name"
          data-has-collapsed-details="true">{{ $result->name }}</span>
    <div id="symptom_item_details_{{ $result->id }}" 
        class="symptom_item_details"
        style="display: none;">

        <a id="symptom_item_details_factsheet_{{ $result->id }}"
            href="{{ route('factsheet.symptom', [$result->id])}}"
            target="_blank">{{ __('ddss.symptom_item_details_factsheet')}}</a>
    
            <div id="symptom_item_details_presence_{{ $result->id }}" class="symptom_item_details_presence">
            <form id="symptom_item_details_presence_form_{{ $result->id }}"
                  method="POST"
                  action="{{ route('case.symptom.present') }}">
                <input type="hidden" name="c" value="{{ $savedCase }}" />
                <input type="hidden" name="symptom" value="{{ $result->id }}">
                <button id="symptom_item_details_presence_form_submit_{{ $result->id }}"
                        type="button"
                        data-has-notes="symptom_item_details_notes_text_{{ $result->id }}"
                        class="symptom_item_details_presence_form_submit">{{ __('ddss.symptom_item_details_presence_present') }}</button>
            </form>
            <form id="symptom_item_details_presence_form_{{ $result->id }}"
                  method="POST"
                  action="{{ route('case.symptom.notpresent') }}">
                <input type="hidden" name="c" value="{{ $savedCase }}" />
                <input type="hidden" name="symptom" value="{{ $result->id }}">
                <button id="symptom_item_details_presence_form_submit_{{ $result->id }}"
                        type="button"
                        data-has-notes="symptom_item_details_notes_text_{{ $result->id }}"
                        class="symptom_item_details_presence_form_submit">{{ __('ddss.symptom_item_details_presence_not-present') }}</button>
            </form>
        </div>


        <div id="symptom_item_details_tests_{{ $result->id }}" class="symptom_item_details_tests">
            @foreach($result->tests as $test)
                <form method="POST"
                      action="{{ route('case.test.add') }}"
                      id="symptom_item_details_tests_form_{{ $test->id }}"
                      class="symptom_item_details_tests_form">
                    <input type="hidden" name="c" value="{{ $savedCase }}" />
                    <input type="hidden" name="test" value="{{ $test->id }}">
                    <button type="button" 
                        data-has-notes="symptom_item_details_notes_text_{{ $result->id }}" >{{ $test->name }}</button>
                </form>
            @endforeach
        </div>

        <div id="symptom_item_details_notes_{{ $result->id }}" class="symptom_item_details_notes">
            <textarea id="symptom_item_details_notes_text_{{ $result->id }}" placeholder="Notes"></textarea>
        </div>
    </div>
</div>