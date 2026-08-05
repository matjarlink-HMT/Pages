<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('shipping_settings', function (Blueprint $table): void {
            $table->unsignedBigInteger('store_id')->primary();
            $table->unsignedBigInteger('default_carrier_account_id')->nullable();
            $table->enum('auto_create_shipment_on', ['never', 'order_paid', 'order_confirmed'])->default('never');
            $table->boolean('auto_select_carrier')->default(false);
            $table->string('default_service_code', 50)->nullable();
            $table->enum('label_format', ['pdf_a4', 'pdf_10x15', 'zpl'])->default('pdf_a4');
            $table->tinyInteger('sla_default_days')->default(3);
            $table->smallInteger('stale_threshold_hours')->default(72);
            $table->json('sender_defaults')->nullable();
            $table->json('notification_settings')->nullable();
            $table->json('cod_settings')->nullable();
            $table->json('scoring_weights')->nullable();
            $table->boolean('public_tracking_enabled')->default(true);
            $table->string('timezone', 60)->default('Asia/Muscat');
            $table->timestamps();
        });

        Schema::create('shipping_address_book', function (Blueprint $table): void {
            $table->id();
            $table->unsignedBigInteger('store_id')->index();
            $table->enum('type', ['origin', 'return', 'customer'])->default('customer');
            $table->string('label', 120)->nullable();
            $table->unsignedBigInteger('customer_id')->nullable();
            $table->string('name', 150);
            $table->string('phone', 30);
            $table->string('email', 150)->nullable();
            $table->char('country_code', 2)->default('OM');
            $table->string('governorate', 100);
            $table->string('wilayat', 100);
            $table->string('area', 100)->nullable();
            $table->string('street')->nullable();
            $table->string('building', 100)->nullable();
            $table->string('landmark')->nullable();
            $table->decimal('latitude', 10, 7)->nullable();
            $table->decimal('longitude', 10, 7)->nullable();
            $table->boolean('is_default')->default(false);
            $table->unsignedInteger('usage_count')->default(0);
            $table->timestamp('last_used_at')->nullable();
            $table->timestamps();

            $table->index(['store_id', 'type']);
            $table->index(['store_id', 'phone']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipping_address_book');
        Schema::dropIfExists('shipping_settings');
    }
};
