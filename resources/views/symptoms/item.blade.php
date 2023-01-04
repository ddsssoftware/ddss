<div class="symptom_item">
    <span id="symptom_item_name_{{ $result->symptom_id }}"
          class="symptom_item_name">{{ $result->symptom_name }}</span>
    <div id="symptom_item_details_{{ $result->symptom_id }}" 
        class="symptom_item_details"
        style="display: none;">
        <a href="{{ route('factsheet.symptom', [$result->symptom_id])}}" target="_blank">Factsheet</a>
    </div>
</div>