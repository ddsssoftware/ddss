@extends('layout')

@section('content')

@if($errors->any())
    {!! implode('', $errors->all('<div>:message</div>')) !!}
@endif

    <section id="conditions.store" class="main">
        <form method="POST" action="{{ route('conditions.store') }}">
            @csrf
            @include('conditions.form')
            <x-forms.submit />
        </form>
    </section>

@endsection