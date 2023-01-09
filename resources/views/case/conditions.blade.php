<section id="case_conditions">
    <h3>{{ __('ddss.case_conditions_title') }}</h3>
    @foreach ($case['conditions'] as $condition)
        @include('case.condition_item')
    @endforeach
</section>