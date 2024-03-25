<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Symptom extends Model
{
    const NAME_SIZE_MAX = 256;

    public $timestamps = false;

    protected $fillable = ['name', 'desc', 'delay', 'urgency'];

    public function aka(): HasMany
    {
        return $this->hasMany(SymptomAka::class);
    }

    public function conditions(): BelongsToMany
    {
        return $this->belongsToMany(Condition::class);
    }

    public function tests(): BelongsToMany
    {
        return $this->belongsToMany(Test::class);
    }
}
