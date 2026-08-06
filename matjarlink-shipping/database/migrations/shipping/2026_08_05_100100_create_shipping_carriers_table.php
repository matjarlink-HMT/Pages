<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/*
| ملاحظة عامة على هجرات الوحدة:
| المفاتيح الأجنبية تُعرَّف داخل الوحدة فقط. الأعمدة المتجهة إلى جداول
| المنصة (stores / users / orders) تُخزَّن كمعرّفات مفهرسة بلا قيد أجنبي،
| لأن أسماء تلك الجداول تخص المنصة لا الوحدة — وهذا يبقي الوحدة قابلة
| للتركيب دون افتراضات عن مخطط خارجها.
*/

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('shipping_carriers', function (Blueprint $table): void {
            $table->id();
            $table->string('code', 50)->unique();
            $table->string('name_ar', 150);
            $table->string('name_en', 150)->nullable();
            $table->string('logo_path')->nullable();
            $table->json('capabilities')->nullable();
            $table->enum('coverage_scope', ['domestic', 'gcc', 'international'])->default('domestic');
            $table->string('website_url')->nullable();
            $table->string('support_phone', 30)->nullable();
            $table->boolean('is_active')->default(true);
            $table->smallInteger('sort_order')->default(0);
            $table->timestamps();

            $table->index(['is_active', 'sort_order']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('shipping_carriers');
    }
};
