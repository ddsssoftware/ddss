@extends('layout')

@section('content')

    <article id="factsheet">
        <section id="factsheet_test">
            <h2>{{ __('ddss.factsheet_test_title') }}</h2>
            <section id="factsheet_test_details">
                <h3>{{ $test->name }}</h3>
                <p>{{ $test->desc }}</p>
            </section>
            <section id="factsheet_test_symptoms">
                <h4>{{ __('ddss.factsheet_test_symptoms_title') }}</h4>
                <ul>
                @forelse ($symptoms as $symptom)
                    <li><a href="{{ route('factsheet.symptom', [$symptom->id]) }}">{{ $symptom->name }}</a></li>
                @empty
                    <p>{{ __('ddss.factsheet_no-data') }}</p>
                @endforelse
                </ul>
            </section>
        <section>
    </article>

@endsection