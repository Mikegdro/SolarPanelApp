<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class PanelLog extends Model
{
    use HasFactory;

    protected $table = 'panel_logs';
    public $timestamps = false;

    protected $fillable = ['idPanel', 'date', 'type', 'sensor1', 'sensor2', 'sensor3', 'sensor4', 'motor1', 'motor2', 'battery', 'potency', 'image', 'ocvOutput'];

    public function panel() {
        return $this->belongsTo('App\Models\Panel', 'idPanel');
    }
}
