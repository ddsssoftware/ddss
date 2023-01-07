<section id="conditions_search">
    <h3>{{ __('ddss.conditions_search_title') }}</h3>
    <form id="conditions_search_form"
          method="POST"
          action="{{ route('case.condition.search') }}"
          data-form-needs-case="true">
        <input name="term" id="conditions_search_form_text" required>
        <button id="conditions_search_form_submit" type="button">{{ __('ddss.conditions_search_form_search') }}</button>
    </form>
    @if(isset($conditionSearchResult))
        @each('conditions.item', $conditionSearchResult, 'result', 'conditions.noitem')
    @endif
</section>