<div class="item">
    <header>
        <span data-has-details="symptom_item_{{ $symptom[Diagnosis::ID] }}">{{ $symptom[Diagnosis::NAME] }}</span>
        <span>{{ __($symptom[Diagnosis::PRESENCE] ? 'ddss.case_symptom_item_presence_present' : 'ddss.case_symptom_item_presence_not-present') }}</span>
    </header>
    <section id="symptom_item_{{ $symptom[Diagnosis::ID] }}" style="display: none;">
        <a href="{{ route('factsheet.symptom', [$symptom[Diagnosis::ID]])}}"
            target="_blank">{{ __('ddss.case_symptom_item_details_factsheet')}}</a>
        <p>{{ $symptom[Diagnosis::NOTES] }}</p>
        <form action="{{ route('case.symptom.remove') }}" method="POST">
            <input type="hidden" name="symptom" value="{{ $symptom[Diagnosis::ID] }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button>{{ __('ddss.case_symptom_item_details_remove') }}</button>
        </form>
    </section>
</div>