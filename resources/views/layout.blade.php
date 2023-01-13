@include('header')

<header>
    <h1 title="{{ __('ddss.index_header_title') }}">DDSS</h1>
    @yield('header')
</header>

@yield('content')

@include('footer')