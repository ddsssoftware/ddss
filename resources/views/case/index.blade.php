<section id="case">
    <h2>{{ __('ddss.case_title') }}</h2>
    @include('case.description')
    @include('case.presentation')
    @include('case.tests')
    @include('case.eliminated')
    @include('case.summary')
</section>