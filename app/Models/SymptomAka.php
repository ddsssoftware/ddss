<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class SymptomAka extends Model
{
    public $timestamps = false;

    public function symptom(): BelongsTo
    {
        return $this->belongsTo(Symptom::class);
    }
}
