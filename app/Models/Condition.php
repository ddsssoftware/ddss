<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Condition extends Model
{
    use \Staudenmeir\EloquentHasManyDeep\HasRelationships;

    const NAME_SIZE_MAX = 256;

    public $timestamps = false;

    protected $fillable = ['name', 'desc', 'urgency'];

    public function aka(): HasMany
    {
        return $this->hasMany(ConditionAka::class);
    }

    public function symptoms(): BelongsToMany
    {
        return $this->belongsToMany(Symptom::class);
    }

    public function tests()
    {
        return $this->hasManyDeep(Test::class, ['condition_symptom', Symptom::class, 'symptom_test']);
    }
}
