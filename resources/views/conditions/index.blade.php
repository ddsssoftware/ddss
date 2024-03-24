@include('header')


<section id="conditions-index" class="main">
    <h2>{{ __('ddss.conditions_index__title') }}</h2>
    <nav>
        <a href="{{ route('conditions.create') }}">{{ __('ddss.conditions_index__nav_create') }}</a>
    </nav>
    <table>
        <thead>
            <tr>
                <th>{{ __('ddss.conditions_index__thead_condition') }}</th>
                <th>{{ __('ddss.conditions_index__thead_view') }}</th>
                <th>{{ __('ddss.conditions_index__thead_edit') }}</th>
            </tr>
        </thead>
        <tbody>
                @forelse ($conditions as $condition)
                    <tr>
                        <td>{{ $condition->name }}</td>
                        <td><a href="{{ route('conditions.show', [$condition->id]) }}">{{ __('ddss.conditions_index__row_view') }}</a></td>
                        <td><a href="{{ route('conditions.edit', [$condition->id]) }}">{{ __('ddss.conditions_index__row_edit') }}</a></td>
                    </tr>
                @empty
                    <tr><td colspan="3">{{ __('ddss.conditions_index__table_empty') }}</td></tr>
                @endforelse
        </tbody>
    </table>
</section>

@include('footer')