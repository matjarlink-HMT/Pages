<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('shipments', function (Blueprint $table): void {
            $table->id();
            $table->uuid('uuid')->unique();
            $table->unsignedBigInteger('store_id');
            $table->string('reference', 30)->unique();
            $table->unsignedInteger('store_sequence')->default(0);
            $table->unsignedBigInteger('order_id')->nullable();

            $table->foreignId('carrier_id')->constrained('shipping_carriers');
            $table->foreignId('store_carrier_account_id')->constrained('store_carrier_accounts');
            $table->string('service_code', 50)->nullable();
            $table->string('service_name', 120)->nullable();

            $table->string('status', 30)->default('draft');
            $table->timestamp('status_updated_at')->nullable();
            $table->string('tracking_number', 100)->nullable();
            $table->string('carrier_shipment_id', 100)->nullable();
            $table->text('carrier_error')->nullable();

            /* الحماية من ازدواج البوالص والرسوم — أهم قيد في الجدول. */
            $table->char('idempotency_key', 64)->unique();

            $table->smallInteger('pieces_count')->default(1);
            $table->decimal('total_weight_kg', 8, 3)->default(0);
            $table->decimal('billable_weight_kg', 8, 3)->default(0);
            $table->decimal('declared_value', 12, 3)->default(0);
            $table->char('currency', 3)->default('OMR');

            $table->boolean('is_cod')->default(false);
            $table->decimal('cod_amount', 12, 3)->default(0);
            $table->timestamp('cod_collected_at')->nullable();
            $table->unsignedBigInteger('cod_settlement_id')->nullable();

            /* المُسعّر مقابل الفعلي = أساس تقرير مطابقة فواتير الشحن. */
            $table->decimal('quoted_cost', 10, 3)->default(0);
            $table->decimal('actual_cost', 10, 3)->default(0);
            $table->decimal('extra_fees', 10, 3)->default(0);
            $table->decimal('total_cost', 10, 3)->default(0);
            $table->json('cost_breakdown')->nullable();
            $table->enum('payment_type', ['prepaid', 'cod', 'carrier_account'])->default('prepaid');

            $table->timestamp('promised_delivery_at')->nullable();
            $table->timestamp('picked_up_at')->nullable();
            $table->timestamp('delivered_at')->nullable();
            $table->timestamp('returned_at')->nullable();
            $table->timestamp('cancelled_at')->nullable();
            $table->tinyInteger('delivery_attempts')->default(0);

            /* علامتان مشتقتان لكن مخزّنتان ومفهرستان: لوحة التحكم تقرأ فهرساً. */
            $table->boolean('is_delayed')->default(false);
            $table->boolean('is_stale')->default(false);

            $table->timestamp('last_synced_at')->nullable();
            $table->timestamp('next_sync_at')->nullable();
            $table->tinyInteger('sync_failures')->default(0);

            $table->text('notes')->nullable();
            $table->text('internal_notes')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('cancelled_by')->nullable();
            $table->timestamps();
            $table->softDeletes();

            $table->index(['store_id', 'status', 'created_at'], 'idx_shipments_store_status');
            $table->index(['store_id', 'created_at'], 'idx_shipments_store_created');
            $table->index(['store_id', 'order_id'], 'idx_shipments_store_order');
            $table->index(['store_id', 'carrier_id', 'delivered_at'], 'idx_shipments_carrier_perf');
            $table->index(['store_id', 'is_delayed', 'status'], 'idx_shipments_attention');
            $table->index(['next_sync_at', 'status'], 'idx_shipments_sync_queue');
            $table->index('tracking_number');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipments');
    }
};
