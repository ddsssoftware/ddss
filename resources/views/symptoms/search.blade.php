<section class="list">
    <h3>{{ __('ddss.symptoms_search_title') }}</h3>
    <form id="symptoms_search_form"
          action="{{ route('case.symptom.search') }}"
          data-form-needs-case="true">
        <input type="hidden" name="c" value="{{ $savedCase }}" />
        <input name="term" required>
        <button>{{ __('ddss.symptoms_search_form_search') }}</button>
    </form>
    <section class="list">
        @if(isset($symptomSearchResult))
            @forelse ($symptomSearchResult as $symptom)
                @include('symptoms.item')
            @empty
                @include('symptoms.noitem')
            @endforelse    
        @endif
    </section>
</section>