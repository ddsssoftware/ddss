<section id="case_symptoms">
    <h3>{{ __('ddss.case_symptoms_title')}}</h3>
    @foreach ($case['symptoms'] as $symptom)
        @include('case.symptom_item')
    @endforeach
</section>