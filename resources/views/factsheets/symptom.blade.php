@extends('layout')

@section('content')

    <article id="factsheet">
        <section id="factsheet_symptom">
            <h2>{{ __('ddss.factsheet_symptom_title') }}</h2>
            <section id="factsheet_symptom_details">
                <h3>{{ $symptom->name }}</h3>
                <p>{{ $symptom->desc }}</p>
            </section>
            <section id="factsheet_condition_test">
                <h4>{{ __('ddss.factsheet_condition_test_title') }}</h4>
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