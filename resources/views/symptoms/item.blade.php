<div class="item">
    <header>
        <span data-has-details="symptom_item_details_{{ $symptom->id }}">{{ $symptom->name }}</span>
    </header>
    <section id="symptom_item_details_{{ $symptom->id }}" style="display: none;">
        <a href="{{ route('factsheet.symptom', [$symptom->id])}}" target="_blank">{{ __('ddss.symptom_item_details_factsheet')}}</a>
        <form method="POST" action="{{ route('case.symptom.present') }}">
            <input type="hidden" name="symptom" value="{{ $symptom->id }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button data-has-notes="symptom_item_notes_{{ $symptom->id }}" type="button">{{ __('ddss.symptom_item_details_presence_present') }}</button>
        </form>
        <form method="POST" action="{{ route('case.symptom.notpresent') }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <input type="hidden" name="symptom" value="{{ $symptom->id }}">
            <button data-has-notes="symptom_item_notes_{{ $symptom->id }}" type="button">{{ __('ddss.symptom_item_details_presence_not-present') }}</button>
        </form>
        @foreach($symptom->tests as $test)
            <form method="POST" action="{{ route('case.test.add') }}">
                <input type="hidden" name="c" value="{{ $savedCase }}" />
                <input type="hidden" name="test" value="{{ $test->id }}">
                <button type="button" data-has-notes="symptom_item_notes_{{ $symptom->id }}" >{{ $test->name }}</button>
            </form>
        @endforeach
        <form>
            <textarea id="symptom_item_notes_{{ $symptom->id }}" placeholder="Notes"></textarea>
        </form>
    </section>
</div>
