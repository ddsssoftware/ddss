<section class="list">
    <h3>{{ __('ddss.symptoms_suggestions_title') }}</h3>
    @if(isset($suggestedSymptoms))
        @forelse ($suggestedSymptoms as $symptom)
            @include('symptoms.item')
        @empty
            @include('symptoms.noitem')
        @endforelse    
    @endif
</section>