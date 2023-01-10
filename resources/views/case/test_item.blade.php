<div class="case_test_item">
    <div class="case_test_item_header">
        <span id="case_test_item_name_{{ $test->id }}" class="case_test_item_name" data-has-collapsed-details="true">{{ $test->name }}</span>
    </div>
    <div id="case_test_item_details_{{ $test->id }}" class="case_test_item_details" style="display: none;">
        <a id="test_item_details_factsheet_{{ $test->id }}"
            href="{{ route('factsheet.test', [$test->id])}}"
            target="_blank">{{ __('ddss.case_test_item_details_factsheet')}}</a>
        <p>{{ $test->notes }}</p>
        <form action="{{ route('case.test.remove') }}"
            method="POST">
            <input type="hidden" name="test" value="{{ $test->id }}">
            <input type="hidden" name="case" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_test_item_details_remove')}}</button>
        </form>
    </div>
</div>