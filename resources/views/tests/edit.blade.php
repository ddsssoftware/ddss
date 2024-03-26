@extends('layout')

@section('content')

@if($errors->any())
    {!! implode('', $errors->all('<div>:message</div>')) !!}
@endif

    <section id="tests-edit" class="main">
        <form method="POST" action="{{ route('tests.update', $test) }}">
            @csrf
            @method('PATCH')
            @include('tests.form')
            <x-forms.submit />
        </form>
        <nav>
            <x-nav.delete :url="route('tests.destroy', $test)" :text="__('ddss.tests_edit__nav_delete')" />
        </nav>
    </section>

@endsection