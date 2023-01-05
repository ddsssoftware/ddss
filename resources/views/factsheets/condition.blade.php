@extends('layout')

@section('content')

    <article id="factsheet">
        <section id="factsheet_condition">
            <h2>{{ __('ddss.factsheet_condition_title') }}</h2>
            <section id="factsheet_condition_details">
                <h3>{{ $condition->name }}</h3>
                <p>{{ $condition->desc }}</p>
            </section>
            <section id="factsheet_condition_symptoms">
                <h4>{{ __('ddss.factsheet_condition_symptoms_title') }}</h4>
                <ul>
                @forelse ($symptoms as $symptom)
                    <li><a href="{{ route('factsheet.symptom', [$symptom->id]) }}">{{ $symptom->name }}</a></li>
                @empty
                    <p>{{ __('ddss.factsheet_no-data') }}</p>
                @endforelse
                </ul>
            </section>
            <section id="factsheet_condition_tests">
                <h4>{{ __('ddss.factsheet_condition_tests_title') }}</h4>
                <ul>
                @forelse ($tests as $test)
                    <li><a href="{{ route('factsheet.test', [$test->id]) }}">{{ $test->name }}</a></li>
                @empty
                    <p>{{ __('ddss.factsheet_no-data') }}</p>
                @endforelse
                </ul>
            </section>
        <section>
    </article>

@endsection