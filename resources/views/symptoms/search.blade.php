<section id="symptoms_search">
    <h3>{{ __('ddss.symptoms_search_title') }}</h3>
    <form id="symptoms_search_form"
          method="POST"
          action="{{ route('case.symptom.search') }}"
          data-form-needs-case="true">
        <input type="hidden" name="case" value="{{ $savedCase }}" />
        <input name="term" required>
        <button>{{ __('ddss.symptoms_search_form_search') }}</button>
    </form>
    @if(isset($symptomSearchResult))
        @forelse ($symptomSearchResult as $result)
            @include('symptoms.item')
        @empty
            @include('symptoms.noitem')
        @endforelse    
    @endif
</section>