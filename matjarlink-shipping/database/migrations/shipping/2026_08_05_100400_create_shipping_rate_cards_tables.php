<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('shipping_rate_cards', function (Blueprint $table): void {
            $table->id();
            $table->unsignedBigInteger('store_id')->index();
            $table->foreignId('store_carrier_account_id')->constrained('store_carrier_accounts')->cascadeOnDelete();
            $table->string('name', 120);
            $table->char('currency', 3)->default('OMR');
            $table->date('effective_from')->nullable();
            $table->date('effective_to')->nullable();
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });

        Schema::create('shipping_rate_rules', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('rate_card_id')->constrained('shipping_rate_cards')->cascadeOnDelete();
            $table->foreignId('zone_id')->constrained('shipping_zones')->cascadeOnDelete();
            $table->string('service_code', 50);
            $table->string('service_name', 120)->nullable();
            $table->decimal('min_weight_kg', 8, 3)->default(0);
            $table->decimal('max_weight_kg', 8, 3)->nullable();
            /* الريال العُماني ثلاث خانات عشرية — والعائم يفسد المحاسبة. */
            $table->decimal('base_price', 10, 3);
            $table->decimal('price_per_extra_kg', 10, 3)->default(0);
            $table->decimal('cod_fee_fixed', 10, 3)->default(0);
            $table->decimal('cod_fee_percent', 5, 2)->default(0);
            $table->decimal('remote_area_surcharge', 10, 3)->default(0);
            $table->decimal('insurance_percent', 5, 2)->default(0);
            $table->decimal('fuel_surcharge_percent', 5, 2)->default(0);
            $table->decimal('vat_percent', 5, 2)->default(0);
            $table->tinyInteger('eta_min_days')->default(1);
            $table->tinyInteger('eta_max_days')->default(3);
            $table->smallInteger('priority')->default(0);
            $table->timestamps();

            $table->index(['rate_card_id', 'zone_id', 'service_code'], 'idx_rate_rule_lookup');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipping_rate_rules');
        Schema::dropIfExists('shipping_rate_cards');
    }
};
