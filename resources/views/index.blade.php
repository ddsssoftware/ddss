<!doctype html>
<html class="no-js" lang="">
<head>
    <meta charset="utf-8">
    <title>{{ __('ddss.index_head_title') }}</title>
    <meta name="description" content="{{ __('ddss.index_head_description') }}">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <link rel="stylesheet" href="/reset.css">
    <link rel="stylesheet" href="/css.css">
</head>

<body>
    
    @include('nav') 

    <article id="case">
        @include('case.index')
        @include('symptoms.index')
        @include('conditions.index')
    </article>

    <script src="/js.js"></script>

    <footer>
        <p>DDSS - Differential Diagnose Support System</p>
        <p>Copyright - 2022-2023</p>
        <p>Licensed under <a href="https://www.gnu.org/licenses/gpl-3.0.html">GPLv3</a></p>
    </footer>
</body>

</html>