<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        /* العروض المحفوظة تثبت لماذا اختير هذا السعر وقتها (تدقيق). */
        Schema::create('rate_quotes', function (Blueprint $table): void {
            $table->id();
            $table->unsignedBigInteger('store_id')->index();
            $table->uuid('quote_group_uuid')->index();
            $table->unsignedBigInteger('order_id')->nullable();
            $table->unsignedBigInteger('shipment_id')->nullable();
            $table->foreignId('carrier_id')->constrained('shipping_carriers')->cascadeOnDelete();
            $table->foreignId('store_carrier_account_id')->constrained('store_carrier_accounts')->cascadeOnDelete();
            $table->string('service_code', 50);
            $table->string('service_name', 120)->nullable();
            $table->decimal('price', 10, 3);
            $table->char('currency', 3)->default('OMR');
            $table->tinyInteger('eta_min_days')->default(1);
            $table->tinyInteger('eta_max_days')->default(3);
            $table->json('features')->nullable();
            $table->decimal('score', 5, 2)->default(0);
            $table->boolean('is_selected')->default(false);
            $table->enum('source', ['api', 'rate_card'])->default('api');
            $table->timestamp('expires_at')->nullable();
            $table->json('raw')->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['store_id', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('rate_quotes');
    }
};
