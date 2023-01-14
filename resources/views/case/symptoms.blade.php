<section class="list">
    <h3>{{ __('ddss.case_symptoms_title')}}</h3>
    @foreach ($case[Diagnosis::SYMPTOMS] as $id => $symptom)
        @include('case.symptom_item')
    @endforeach
</section>