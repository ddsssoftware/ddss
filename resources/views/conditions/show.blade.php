@include('header')

<section id="condition-show" class="main">
    <h2>{{ __('ddss.conditions_show__title') }}</h2>
    <section id="details">
        <h3>{{ $condition->name }}</h3>
        <p>{{ $condition->desc }}</p>
    </section>
    <section id="symptoms">
        <h4>{{ __('ddss.conditions_show__symptom_title') }}</h4>
        <ul>
            @foreach ($condition->symptoms()->select('id', 'name')->orderBy('name')->get() as $symptom)
                <li><a href="{{ route('symptoms.show', [$symptom->id])}}">{{ $symptom->name }}</a></li>
            @endforeach
        </ul>
    <section>
    <section id="tests">
        <h4>{{ __('ddss.conditions_show__test_title') }}</h4>
        <ul>
            @foreach ($condition->tests()->distinct()->select('tests.id', 'tests.name')->orderBy('tests.name')->get() as $test)
                <li><a href="{{ route('tests.show', [$test->id])}}">{{ $test->name }}</a></li>
            @endforeach
        </ul>
    <section>
    <nav>
        <a href="{{ route('conditions.edit', $condition) }}">{{ __('ddss.conditions_show__nav_edit') }}</a>
        <a href="{{ route('conditions.index') }}">{{ __('ddss.conditions_show__nav_browse') }}</a>
    <nav>
</section>

@include('footer')