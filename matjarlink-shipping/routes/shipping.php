<?php

declare(strict_types=1);

use App\Domains\Shipping\Http\Controllers\Merchant\CarrierAccountController;
use App\Domains\Shipping\Http\Controllers\Merchant\DashboardController;
use App\Domains\Shipping\Http\Controllers\Merchant\RateController;
use App\Domains\Shipping\Http\Controllers\Merchant\ShipmentController;
use Illuminate\Support\Facades\Route;

/*
| مسارات لوحة التاجر. البادئة والوسائط من config/shipping.php ليتوافق
| التركيب مع تنظيم المسارات القائم في متجرلينك دون تعديل هذا الملف.
*/

Route::name('shipping.')->group(function (): void {

    Route::get('/', DashboardController::class)->name('dashboard');

    Route::prefix('shipments')->name('shipments.')->group(function (): void {
        Route::get('/', [ShipmentController::class, 'index'])->name('index');
        Route::get('/create', [ShipmentController::class, 'create'])->name('create');
        Route::post('/', [ShipmentController::class, 'store'])->name('store');
        Route::get('/export', [ShipmentController::class, 'export'])->name('export');
        Route::get('/{shipment}', [ShipmentController::class, 'show'])->name('show');
        Route::delete('/{shipment}', [ShipmentController::class, 'cancel'])->name('cancel');
        Route::post('/{shipment}/sync', [ShipmentController::class, 'sync'])->name('sync');
        Route::post('/{shipment}/events', [ShipmentController::class, 'storeEvent'])->name('events.store');
        Route::get('/{shipment}/label', [ShipmentController::class, 'label'])->name('label');
    });

    Route::post('rates', [RateController::class, 'quote'])->name('rates.quote');

    Route::prefix('carrier-accounts')->name('carrier-accounts.')->group(function (): void {
        Route::get('/', [CarrierAccountController::class, 'index'])->name('index');
        Route::post('/', [CarrierAccountController::class, 'store'])->name('store');
        Route::patch('/{account}', [CarrierAccountController::class, 'update'])->name('update');
        Route::delete('/{account}', [CarrierAccountController::class, 'destroy'])->name('destroy');
        Route::post('/{account}/test', [CarrierAccountController::class, 'test'])->name('test');
        Route::post('/{account}/default', [CarrierAccountController::class, 'setDefault'])->name('default');
    });
});
