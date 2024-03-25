@extends('layout')

@section('content')

@if($errors->any())
    {!! implode('', $errors->all('<div>:message</div>')) !!}
@endif

    <section id="symptoms-create" class="main">
        <form method="POST" action="{{ route('symptoms.store') }}">
            @csrf
            @include('symptoms.form')
            <x-forms.submit />
        </form>
    </section>

@endsection