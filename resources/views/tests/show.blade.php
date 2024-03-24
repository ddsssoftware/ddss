@include('header')

<section id="tests-show" class="main">
    <h2>{{ __('ddss.tests_show__title') }}</h2>
    <section id="details">
        <h3>{{ $test->name }}</h3>
        <p>{{ $test->desc }}</p>
    </section>
    <section id="symptoms">
        <h4>{{ __('ddss.tests_show__symptom_title') }}</h4>
        <ul>
            @foreach ($test->symptoms()->select('symptoms.id', 'symptoms.name')->orderBy('symptoms.name')->get() as $symptom)
                <li><a href="{{ route('symptoms.show', [$symptom->id])}}">{{ $symptom->name }}</a></li>
            @endforeach
        </ul>
    <section>
    <section id="conditions">
        <h4>{{ __('ddss.tests_show__condition_title') }}</h4>
        <ul>
            @foreach ($test->conditions()->distinct()->select('conditions.id', 'conditions.name')->orderBy('conditions.name')->get() as $condition)
                <li><a href="{{ route('conditions.show', [$condition->id])}}">{{ $condition->name }}</a></li>
            @endforeach
        </ul>
    <section>
<section>


@include('footer')