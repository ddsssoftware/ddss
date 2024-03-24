<form method="POST" class="nav-delete" action="{{ $url }}">
    @csrf
    @method('DELETE')
    <a href="#" onclick="this.closest('form').submit();return false;">{{ $text }}</a>
</form>