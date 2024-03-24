<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Symptom extends Model
{
    public function conditions(): BelongsToMany
    {
        return $this->belongsToMany(Condition::class);
    }

    public function tests(): BelongsToMany
    {
        return $this->belongsToMany(Test::class);
    }
}
