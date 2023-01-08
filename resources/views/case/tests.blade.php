<section id="case_tests">
    <h3>{{ __('ddss.case_tests_title') }}</h3>
    @foreach ($case['tests'] as $test)
        {{ $test->name }}
    @endforeach
</section>