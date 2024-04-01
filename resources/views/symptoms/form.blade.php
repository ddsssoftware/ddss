<x-forms.input :obj="$symptom ?? null" fld="name" :label="__('ddss.symptoms_form__name')" />
<x-forms.textarea :obj="$symptom ?? null" fld="desc" :label="__('ddss.symptoms_form__desc')" />
<x-forms.input :obj="$symptom ?? null" fld="delay" :label="__('ddss.symptoms_form__delay')" />
<x-forms.input :obj="$symptom ?? null" fld="urgency" :label="__('ddss.symptoms_form__urgency')" />