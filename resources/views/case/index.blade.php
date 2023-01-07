<section id="case">
    <h2>{{ __('ddss.case_title') }}</h2>
    @include('case.description')
    @include('case.symptoms')
    @include('case.tests')
    @include('case.conditions')
    @include('case.summary')
</section>