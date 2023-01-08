@extends('layout')

@section('header') 
<nav>
    <button>{{ __('ddss.index_header_new') }}</button>
    <button>{{ __('ddss.index_header_load') }}</button>
</nav>
@endsection

@section('content')
<article id="case">
    @include('case.index')
    @include('symptoms.index')
    @include('conditions.index')
</article>
@endsection