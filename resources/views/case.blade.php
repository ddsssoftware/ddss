<script>
    @if(isset($case))
        document.ddsscase = '@php echo serialize($case); @endphp';
    @else
        document.ddsscase = 'new';
    @endif
</script>