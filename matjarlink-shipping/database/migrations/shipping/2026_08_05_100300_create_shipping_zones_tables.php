<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('shipping_zones', function (Blueprint $table): void {
            $table->id();
            $table->unsignedBigInteger('store_id')->index();
            $table->string('name', 120);
            $table->string('description')->nullable();
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });

        Schema::create('shipping_zone_regions', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('zone_id')->constrained('shipping_zones')->cascadeOnDelete();
            $table->char('country_code', 2)->default('OM');
            $table->string('governorate', 100);
            /* NULL = كل ولايات المحافظة. */
            $table->string('wilayat', 100)->nullable();
            $table->string('area', 100)->nullable();
            $table->boolean('is_remote')->default(false);
            $table->timestamps();

            $table->index(['country_code', 'governorate', 'wilayat'], 'idx_zone_region_lookup');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipping_zone_regions');
        Schema::dropIfExists('shipping_zones');
    }
};
