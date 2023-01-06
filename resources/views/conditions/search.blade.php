<section id="conditions_search">
    <h3>{{ __('ddss.conditions_search_title') }}</h3>
    <form id="conditions_search_form" method="POST" action="{{ route('case.condition.search') }}">
        <input name="term" id="conditions_search_form_text">
        <button id="conditions_search_form_search">{{ __('ddss.conditions_search_form_search') }}</button>
    </form>
    @if(isset($conditionSearchResult))
        @each('conditions.item', $conditionSearchResult, 'result', 'conditions.noitem')
    @endif
</section>