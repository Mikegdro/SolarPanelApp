<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Panel extends Model
{
    use HasFactory;

    protected $table = 'panel';
    public $timestamps = false;

    protected $fillable = ['token'];

    public function logs() {
        return $this->hasMany('App\Models\PanelLog', 'idPanel');
    }
}
