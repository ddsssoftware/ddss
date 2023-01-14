<section class="list">
    <h3>{{ __('ddss.case_conditions_title') }}</h3>
    @foreach ($case[Diagnosis::CONDITIONS] as $id => $condition)
        @include('case.condition_item')
    @endforeach
</section>