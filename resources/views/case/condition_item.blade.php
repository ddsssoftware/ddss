<div class="item">
    <header>
        <span data-has-details="condition_item_{{ $condition[Diagnosis::ID] }}">{{ $condition[Diagnosis::NAME] }}</span>
        <span>{{ __($condition[Diagnosis::PRESENCE] ? 'ddss.case_condition_item_presence_present' : 'ddss.case_condition_item_presence_not-present') }}</span>
    </header>
    <section id="condition_item_{{ $condition[Diagnosis::ID] }}" style="display: none;">
        <a href="{{ route('factsheet.condition', [$condition[Diagnosis::ID]])}}"
           target="_blank">{{ __('ddss.case_condition_item_details_factsheet')}}</a>
        <p>{{ $condition[Diagnosis::NOTES] }}</p>
        <form action="{{ route('case.condition.remove') }}" method="POST">
            <input type="hidden" name="condition" value="{{ $condition[Diagnosis::ID] }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_condition_item_details_remove') }}</button>
        </form>
    </section>
</div>