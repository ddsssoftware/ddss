<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Staudenmeir\EloquentHasManyDeep\HasManyDeep;
use Staudenmeir\EloquentHasManyDeep\HasRelationships;

class Test extends Model
{
    use HasRelationships;

    public function symptoms(): BelongsToMany
    {
        return $this->belongsToMany(Symptom::class);
    }

    public function conditions(): HasManyDeep
    {
        return $this->hasManyDeep(Condition::class, ['symptom_test', Symptom::class, 'condition_symptom']);
    }
}
