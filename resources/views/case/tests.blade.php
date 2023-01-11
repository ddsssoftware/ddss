<section id="case_tests">
    <h3>{{ __('ddss.case_tests_title') }}</h3>
    @foreach ($case[Diagnosis::TESTS] as $test)
        @include('case.test_item')
    @endforeach
</section>