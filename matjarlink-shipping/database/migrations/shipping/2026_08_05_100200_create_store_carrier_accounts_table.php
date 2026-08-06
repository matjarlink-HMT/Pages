<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('store_carrier_accounts', function (Blueprint $table): void {
            $table->id();
            $table->unsignedBigInteger('store_id')->index();
            $table->foreignId('carrier_id')->constrained('shipping_carriers')->cascadeOnDelete();
            $table->string('label', 100)->nullable();

            /* مشفّرة بـ AES عبر cast الموديل — لا تُقرأ إلا داخل CarrierRegistry. */
            $table->text('credentials')->nullable();

            $table->enum('environment', ['sandbox', 'live'])->default('live');
            $table->boolean('is_active')->default(false);
            $table->boolean('is_default')->default(false);
            $table->smallInteger('priority')->default(100);
            $table->enum('connection_status', ['unknown', 'connected', 'failed'])->default('unknown');
            $table->timestamp('last_checked_at')->nullable();
            $table->text('last_error')->nullable();
            $table->json('service_codes')->nullable();
            $table->string('default_service_code', 50)->nullable();
            $table->boolean('cod_enabled')->default(true);
            $table->decimal('cod_fee_percent', 5, 2)->default(0);
            $table->decimal('cod_fee_fixed', 10, 3)->default(0);
            $table->enum('markup_type', ['none', 'fixed', 'percent'])->default('none');
            $table->decimal('markup_value', 10, 3)->default(0);
            $table->unsignedBigInteger('pickup_address_id')->nullable();
            $table->timestamp('circuit_opened_until')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->timestamps();
            $table->softDeletes();

            $table->unique(['store_id', 'carrier_id', 'label'], 'uniq_store_carrier_label');
            $table->index(['store_id', 'is_active']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('store_carrier_accounts');
    }
};
