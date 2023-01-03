<section id="symptoms_search">
    <h3>{{ __('ddss.symptoms_search_title') }}</h3>
    <form id="symptoms_search_form" method="POST" action="{{ route('case.symptom.search') }}">
        <input name="term" id="symptoms_search_form_text" required>
        <button id="symptoms_search_form_search">{{ __('ddss.symptoms_search_form_search') }}</button>
    </form>
    @if(isset($symptomSearchResult))
        @each('symptoms.item', $symptomSearchResult, 'result', 'symptoms.noitem')
    @endif
</section>