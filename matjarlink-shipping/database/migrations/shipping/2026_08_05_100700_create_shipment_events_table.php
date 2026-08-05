<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('shipment_events', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('shipment_id')->constrained('shipments')->cascadeOnDelete();
            $table->string('status', 30);
            $table->string('carrier_status_code', 50)->nullable();
            $table->string('carrier_status_text')->nullable();
            $table->string('description_ar')->nullable();
            $table->string('description_en')->nullable();
            $table->string('location', 150)->nullable();

            /* زمن الحدث لدى الشركة لا زمن استقبالنا له. */
            $table->timestamp('occurred_at');

            $table->enum('source', ['webhook', 'polling', 'manual', 'system', 'import'])->default('polling');
            $table->unsignedBigInteger('actor_id')->nullable();

            /* القيد الفريد على البصمة يمنع تكرار أحداث الـ Webhook في القاعدة. */
            $table->char('hash', 40);
            $table->json('raw_payload')->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->unique(['shipment_id', 'hash']);
            $table->index(['shipment_id', 'occurred_at']);
        });

        Schema::create('carrier_status_maps', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('carrier_id')->constrained('shipping_carriers')->cascadeOnDelete();
            $table->string('carrier_status_code', 50);
            $table->string('carrier_status_text')->nullable();
            $table->string('internal_status', 30);
            $table->boolean('is_terminal')->default(false);
            $table->string('notes')->nullable();
            $table->timestamps();

            $table->unique(['carrier_id', 'carrier_status_code']);
        });

        Schema::create('shipment_labels', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('shipment_id')->constrained('shipments')->cascadeOnDelete();
            $table->enum('format', ['pdf_a4', 'pdf_10x15', 'zpl'])->default('pdf_a4');
            $table->string('disk', 50)->default('local');
            $table->string('path');
            $table->unsignedInteger('version')->default(1);
            $table->timestamp('printed_at')->nullable();
            $table->unsignedBigInteger('printed_by')->nullable();
            $table->unsignedInteger('print_count')->default(0);
            $table->timestamps();

            $table->index(['shipment_id', 'version']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipment_labels');
        Schema::dropIfExists('carrier_status_maps');
        Schema::dropIfExists('shipment_events');
    }
};
