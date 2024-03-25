@include('header')


<section id="symptoms-index" class="main">
    <h2>{{ __('ddss.symptoms_index__title') }}</h2>
    <nav>
        <a href="{{ route('symptoms.create') }}">{{ __('ddss.symptoms_index__nav_create') }}</a>
    </nav>
    <table>
        <thead>
            <tr>
                <th>{{ __('ddss.symptoms_index__thead_symptom') }}</th>
                <th>{{ __('ddss.symptoms_index__thead_view') }}</th>
                <th>{{ __('ddss.symptoms_index__thead_edit') }}</th>
            </tr>
        </thead>
        <tbody>
                @forelse ($symptoms as $symptom)
                    <tr>
                        <td>{{ $symptom->name }}</td>
                        <td><a href="{{ route('symptoms.show', [$symptom->id]) }}">{{ __('ddss.symptoms_index__row_view') }}</a></td>
                        <td><a href="{{ route('symptoms.edit', [$symptom->id]) }}">{{ __('ddss.symptoms_index__row_edit') }}</a></td>
                    </tr>
                @empty
                    <tr><td colspan="3">{{ __('ddss.symptoms_index__table_empty') }}</td></tr>
                @endforelse
        </tbody>
    </table>
</section>

@include('footer')