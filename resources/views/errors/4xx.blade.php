@extends('errors.layout')

@section('title', __('Error'))
@section('code', $exception->getStatusCode())
@section('message', __('Error'))
