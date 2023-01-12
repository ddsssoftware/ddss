<section id="conditions_suggestions">
    <h3>{{ __('ddss.conditions_suggestions_title') }}</h3>
    @if(isset($suggestedConditions))
        @forelse($suggestedConditions as $result)
            @include('conditions.item')
        @empty
            @include('conditions.noitem')
        @endforelse
    @endif
</section>