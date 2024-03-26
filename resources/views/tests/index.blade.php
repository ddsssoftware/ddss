@include('header')


<section id="tests-index" class="main">
    <h2>{{ __('ddss.tests_index__title') }}</h2>
    <nav>
        <a href="{{ route('tests.create') }}">{{ __('ddss.tests_index__nav_create') }}</a>
    </nav>
    <table>
        <thead>
            <tr>
                <th>{{ __('ddss.tests_index__thead_symptom') }}</th>
                <th>{{ __('ddss.tests_index__thead_view') }}</th>
                <th>{{ __('ddss.tests_index__thead_edit') }}</th>
            </tr>
        </thead>
        <tbody>
                @forelse ($tests as $test)
                    <tr>
                        <td>{{ $test->name }}</td>
                        <td><a href="{{ route('tests.show', [$test->id]) }}">{{ __('ddss.tests_index__row_view') }}</a></td>
                        <td><a href="{{ route('tests.edit', [$test->id]) }}">{{ __('ddss.tests_index__row_edit') }}</a></td>
                    </tr>
                @empty
                    <tr><td colspan="3">{{ __('ddss.tests_index__table_empty') }}</td></tr>
                @endforelse
        </tbody>
    </table>
</section>

@include('footer')