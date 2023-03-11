<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('panel_logs', function (Blueprint $table) {
            $table->foreignId('idPanel');
            $table->dateTime('date', 3);
            $table->string('type')->nullable();
            $table->integer('sensor1');
            $table->integer('sensor2');
            $table->integer('sensor3');
            $table->integer('sensor4');
            $table->integer('motor1');
            $table->integer('motor2');
            $table->string('battery');
            $table->integer('potency');
            $table->string('image');
            $table->string('ocvOutput');

            $table->foreign('idPanel')->references('id')->on('panel')->onDelete('cascade');

            $table->primary(['idPanel', 'date']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('panel_logs');
    }
};
