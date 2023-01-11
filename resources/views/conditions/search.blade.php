<section id="conditions_search">
    <h3>{{ __('ddss.conditions_search_title') }}</h3>
    <form id="conditions_search_form"
          action="{{ route('case.condition.search') }}"
          data-form-needs-case="true">
        <input type="hidden" name="c" value="{{ $savedCase }}" />
        <input name="term" required>
        <button>{{ __('ddss.conditions_search_form_search') }}</button>
    </form>
    @if(isset($conditionSearchResult))
        @forelse($conditionSearchResult as $result)
            @include('conditions.item')
        @empty
            @include('conditions.noitem')
        @endforelse
    @endif
</section>