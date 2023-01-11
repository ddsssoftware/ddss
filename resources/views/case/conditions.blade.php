<section id="case_conditions">
    <h3>{{ __('ddss.case_conditions_title') }}</h3>
    @foreach ($case[Diagnosis::CONDITIONS] as $condition)
        @include('case.condition_item')
    @endforeach
</section>