<div class="item">
    <header>
        <span data-has-details="condition_item_details_{{ $condition->id }}">{{ $condition->name }}</span>
    </header>
    <section id="condition_item_details_{{ $condition->id }}" style="display: none;">
        <a href="{{ route('factsheet.condition', [$condition->id])}}" target="_blank">{{ __('ddss.condition_item_details_factsheet')}}</a>
        <form method="POST" action="{{ route('case.condition.present') }}">
            <input type="hidden" name="condition" value="{{ $condition->id }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <button data-has-notes="condition_item_notes_{{ $condition->id }}" type="button">{{ __('ddss.condition_item_details_presence_present') }}</button>
        </form>
        <form method="POST" action="{{ route('case.condition.notpresent') }}">
            <input type="hidden" name="c" value="{{ $savedCase }}" />
            <input type="hidden" name="condition" value="{{ $condition->id }}">
            <button data-has-notes="condition_item_notes_{{ $condition->id }}" type="button">{{ __('ddss.condition_item_details_presence_not-present') }}</button>
        </form>
        <form>
            <textarea id="condition_item_notes_{{ $condition->id }}" placeholder="Notes"></textarea>
        </form>
    </section>
</div>