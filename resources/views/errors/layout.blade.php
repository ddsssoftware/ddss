@include('header')

<article id="error">
    <h1>@yield('title')</h1>
    <h2>@yield('code')</h2>
    <h3>@yield('message')</h3>
</article>

@include('footer')