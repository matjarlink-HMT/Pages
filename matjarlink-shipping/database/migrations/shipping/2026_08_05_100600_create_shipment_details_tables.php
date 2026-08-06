<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        /*
        | لقطة العنوان لا مرجع لجدول عناوين: تعديل العميل لعنوانه بعد شهر
        | يجب ألا يغيّر ما طُبع على بوليصة سابقة.
        */
        Schema::create('shipment_addresses', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('shipment_id')->constrained('shipments')->cascadeOnDelete();
            $table->enum('type', ['sender', 'receiver', 'return']);
            $table->string('name', 150);
            $table->string('phone', 30);
            $table->string('alt_phone', 30)->nullable();
            $table->string('email', 150)->nullable();
            $table->char('country_code', 2)->default('OM');
            $table->string('governorate', 100);
            $table->string('wilayat', 100);
            $table->string('area', 100)->nullable();
            $table->string('street')->nullable();
            $table->string('building', 100)->nullable();
            /* معلم بارز — ضروري في العناوين العُمانية أكثر من الترميز البريدي. */
            $table->string('landmark')->nullable();
            $table->string('postal_code', 20)->nullable();
            $table->decimal('latitude', 10, 7)->nullable();
            $table->decimal('longitude', 10, 7)->nullable();
            $table->string('notes')->nullable();
            $table->timestamps();

            $table->index(['shipment_id', 'type']);
            $table->index('phone');
        });

        Schema::create('shipment_packages', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('shipment_id')->constrained('shipments')->cascadeOnDelete();
            $table->smallInteger('piece_no')->default(1);
            $table->decimal('weight_kg', 8, 3);
            $table->decimal('length_cm', 8, 2)->nullable();
            $table->decimal('width_cm', 8, 2)->nullable();
            $table->decimal('height_cm', 8, 2)->nullable();
            $table->decimal('volumetric_weight_kg', 8, 3)->default(0);
            $table->string('barcode', 100)->nullable();
            $table->string('carrier_piece_id', 100)->nullable();
            $table->string('description')->nullable();
            $table->timestamps();

            $table->index('shipment_id');
        });

        Schema::create('shipment_items', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('shipment_id')->constrained('shipments')->cascadeOnDelete();
            $table->unsignedBigInteger('order_item_id')->nullable();
            $table->string('sku', 100)->nullable();
            $table->string('name');
            $table->integer('quantity')->default(1);
            $table->decimal('unit_value', 12, 3)->default(0);
            $table->decimal('weight_kg', 8, 3)->nullable();
            $table->string('hs_code', 20)->nullable();
            $table->char('country_of_origin', 2)->nullable();
            $table->timestamps();

            $table->index('shipment_id');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipment_items');
        Schema::dropIfExists('shipment_packages');
        Schema::dropIfExists('shipment_addresses');
    }
};
