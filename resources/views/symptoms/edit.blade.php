@extends('layout')

@section('content')

@if($errors->any())
    {!! implode('', $errors->all('<div>:message</div>')) !!}
@endif

    <section id="symptoms-edit" class="main">
        <form method="POST" action="{{ route('symptoms.update', $symptom) }}">
            @csrf
            @method('PATCH')
            @include('symptoms.form')
            <x-forms.submit />
        </form>
        <nav>
            <x-nav.delete :url="route('symptoms.destroy', $symptom)" :text="__('ddss.symptoms_edit__nav_delete')" />
        </nav>
    </section>

@endsection