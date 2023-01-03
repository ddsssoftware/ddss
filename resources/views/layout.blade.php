@include('header')

<header>
    <h1>{{ __('ddss.index_header_title') }}</h1>
    @yield('header')
</header>

@yield('content')

@include('footer')