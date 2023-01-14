<section class="list">
    <h3>{{ __('ddss.case_tests_title') }}</h3>
    @foreach ($case[Diagnosis::TESTS] as $id => $test)
        @include('case.test_item')
    @endforeach
</section>