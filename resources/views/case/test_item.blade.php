<div class="case_test_item">
    <div class="case_test_item_header">
        <span id="case_test_item_name_{{ $test[Diagnosis::ID] }}" class="case_test_item_name" data-has-collapsed-details="true">{{ $test[Diagnosis::NAME] }}</span>
    </div>
    <div id="case_test_item_details_{{ $test[Diagnosis::ID] }}" class="case_test_item_details" style="display: none;">
        <a id="test_item_details_factsheet_{{ $test[Diagnosis::ID] }}"
            href="{{ route('factsheet.test', [$test[Diagnosis::ID]])}}"
            target="_blank">{{ __('ddss.case_test_item_details_factsheet')}}</a>
        <p>{{ $test[Diagnosis::NOTES] }}</p>
        <form action="{{ route('case.test.remove') }}"
            method="POST">
            <input type="hidden" name="test" value="{{ $test[Diagnosis::ID] }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_test_item_details_remove')}}</button>
        </form>
    </div>
</div>