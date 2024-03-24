@extends('layout')

@section('content')

@if($errors->any())
    {!! implode('', $errors->all('<div>:message</div>')) !!}
@endif

    <section id="conditions.edit" class="main">
        <form method="POST" action="{{ route('conditions.update', $condition) }}">
            @csrf
            @method('PATCH')
            @include('conditions.form')
            <x-forms.submit />
        </form>
        <nav>
            <x-nav.delete :url="route('conditions.destroy', $condition)" :text="__('ddss.condtions_edit__nav_delete')" />
        </nav>
    </section>

@endsection