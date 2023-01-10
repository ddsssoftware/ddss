@extends('layout')

@section('header') 
<nav>
    <form action="{{ route('case.index') }}">
        <button>{{ __('ddss.index_header_new') }}</button>
    </form>
</nav>
@endsection

@section('content')
<article id="case">
    @include('case.index')
    @include('symptoms.index')
    @include('conditions.index')
</article>
@endsection