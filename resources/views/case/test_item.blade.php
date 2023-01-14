<div class="item">
    <header>
        <span data-has-details="test_item_details_{{ $id }}">{{ $test[Diagnosis::NAME] }}</span>
    </header>
    <section id="test_item_details_{{ $id }}" class="case_test_item_details" style="display: none;">
        <a href="{{ route('factsheet.test', [$id])}}" target="_blank">{{ __('ddss.case_test_item_details_factsheet')}}</a>
        <p>{{ $test[Diagnosis::NOTES] }}</p>
        <form action="{{ route('case.test.remove') }}" method="POST">
            <input type="hidden" name="test" value="{{ $id }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_test_item_details_remove')}}</button>
        </form>
    </section>
</div>