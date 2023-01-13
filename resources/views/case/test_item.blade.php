<div class="item">
    <header>
        <span data-has-details="test_item_details_{{ $test[Diagnosis::ID] }}">{{ $test[Diagnosis::NAME] }}</span>
    </header>
    <section id="test_item_details_{{ $test[Diagnosis::ID] }}" class="case_test_item_details" style="display: none;">
        <a href="{{ route('factsheet.test', [$test[Diagnosis::ID]])}}" target="_blank">{{ __('ddss.case_test_item_details_factsheet')}}</a>
        <p>{{ $test[Diagnosis::NOTES] }}</p>
        <form action="{{ route('case.test.remove') }}" method="POST">
            <input type="hidden" name="test" value="{{ $test[Diagnosis::ID] }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_test_item_details_remove')}}</button>
        </form>
    </section>
</div>