@include('header')
<article id="summary">
{{ __('ddss.summary_title') }}
<br>
<br>
{{ $case[Diagnosis::DESCRIPTION] == null ||  $case[Diagnosis::DESCRIPTION] == '' ? __('ddss.summary_no-description') : $case[Diagnosis::DESCRIPTION] }}

<br>
<br>
&nbsp;-&nbsp;{{ __('ddss.summary_symptoms') }}
<br>
<br>
@forelse ($case[Diagnosis::SYMPTOMS] as $symptom)
    &nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;{{ $symptom[Diagnosis::NAME] }}
    &nbsp;&nbsp;{{ __($symptom[Diagnosis::PRESENCE] ? 'ddss.summary_symptoms_present' : 'ddss.summary_symptoms_not-present')  }}
    &nbsp;&nbsp;{{ $symptom[Diagnosis::NOTES] }}
    <br>
    @empty
    &nbsp;&nbsp;&nbsp;&nbsp;{{ __('ddss.summary_symptoms_empty') }}
    <br>
@endforelse


<br>
&nbsp;-&nbsp;{{ __('ddss.summary_tests') }}
<br>
<br>
@forelse ($case[Diagnosis::TESTS] as $test)
    &nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;{{ $test[Diagnosis::NAME] }}
    &nbsp;&nbsp;{{ $test[Diagnosis::NOTES] }}
    <br>
@empty
    &nbsp;&nbsp;&nbsp;&nbsp;{{ __('ddss.summary_tests_empty') }}
    <br>
@endforelse

<br>
&nbsp;-&nbsp;{{ __('ddss.summary_conditions') }}
<br>
<br>
@forelse ($case[Diagnosis::CONDITIONS] as $condition)
    &nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;{{ $condition[Diagnosis::NAME] }}
    &nbsp;&nbsp;{{ __($condition[Diagnosis::PRESENCE] ? 'ddss.summary_conditions_present' : 'ddss.summary_conditions_not-present')  }}
    &nbsp;&nbsp;{{ $condition[Diagnosis::NOTES] }}
    <br>
@empty
    &nbsp;&nbsp;&nbsp;&nbsp;{{ __('ddss.summary_conditions_empty') }}
    <br>
@endforelse


<br>
<br>
<br>
{{ route('case.index', ['c' => $savedCase]) }}
</article>

</body>
</html>