@include('header')

<section id="symptoms-show" class="main">
    <h2>{{ __('ddss.symptoms_show__title') }}</h2>
    <section id="details">
        <h3>{{ $symptom->name }}</h3>
        <p>{{ $symptom->desc }}</p>
    </section>
    <section id="conditons">
        <h4>{{ __('ddss.symptoms_show__conditions_title') }}</h4>
        <ul>
            @foreach ($symptom->conditions()->select('id', 'name')->orderBy('name')->get() as $condition)
                <li><a href="{{ route('conditions.show', [$condition->id])}}">{{ $condition->name }}</a></li>
            @endforeach
        </ul>
    <section>
    <section id="tests">
        <h4>{{ __('ddss.symptoms_show__tests_title') }}</h4>
        <ul>
            @foreach ($symptom->tests()->select('id', 'name')->orderBy('name')->get() as $test)
                <li><a href="{{ route('tests.show', [$test->id])}}">{{ $test->name }}</a></li>
            @endforeach
        </ul>
    <section>
    <nav>
        <a href="{{ route('symptoms.edit', $symptom) }}">{{ __('ddss.symptoms_show__nav_edit') }}</a>
        <a href="{{ route('symptoms.index') }}">{{ __('ddss.symptoms_show__nav_browse') }}</a>
    <nav>
<section>


@include('footer')