@extends('layout')

@section('content')

@if($errors->any())
    {!! implode('', $errors->all('<div>:message</div>')) !!}
@endif

    <section id="tests-create" class="main">
        <form method="POST" action="{{ route('tests.store') }}">
            @csrf
            @include('tests.form')
            <x-forms.submit />
        </form>
    </section>

@endsection