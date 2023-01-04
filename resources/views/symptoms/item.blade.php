<div class="symptom_item">
    <span class="symptom_item_name">{{ $result->symptom_name }}</span>
    <div class="symptom_item_details">
        <a href="{{ route('factsheet.symptom', [$result->symptom_id])}}" target="_blank">Factsheet</a>
    </div>
</div>