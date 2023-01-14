<section class="list">
    <h3>{{ __('ddss.conditions_suggestions_title') }}</h3>
    @if(isset($suggestedConditions))
        @forelse($suggestedConditions as $condition)
            @include('conditions.item')
        @empty
            @include('conditions.noitem')
        @endforelse
    @endif
</section>