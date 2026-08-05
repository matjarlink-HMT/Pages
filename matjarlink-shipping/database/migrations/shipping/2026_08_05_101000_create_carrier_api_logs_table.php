<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        /* الحمولات تُخزَّن منقّحة من الأسرار عبر CredentialMasker::redact(). */
        Schema::create('carrier_api_logs', function (Blueprint $table): void {
            $table->id();
            $table->unsignedBigInteger('store_id')->index();
            $table->unsignedBigInteger('store_carrier_account_id')->index();
            $table->enum('operation', ['rate', 'create', 'label', 'track', 'cancel', 'pickup', 'test']);
            $table->char('correlation_id', 26)->nullable()->index();
            $table->json('request_payload')->nullable();
            $table->json('response_payload')->nullable();
            $table->unsignedSmallInteger('http_status')->default(0);
            $table->unsignedInteger('duration_ms')->default(0);
            $table->boolean('success')->default(false);
            $table->text('error_message')->nullable();
            $table->unsignedBigInteger('shipment_id')->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['store_id', 'operation', 'created_at'], 'idx_api_logs_lookup');
            $table->index(['success', 'created_at'], 'idx_api_logs_prune');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('carrier_api_logs');
    }
};
