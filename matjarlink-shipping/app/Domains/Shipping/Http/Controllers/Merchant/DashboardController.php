<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Controllers\Merchant;

use App\Domains\Shipping\Contracts\TenantResolver;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\ShippingAnalyticsService;
use Illuminate\Contracts\View\View;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;

final class DashboardController extends Controller
{
    public function __construct(
        private readonly ShippingAnalyticsService $analytics,
        private readonly TenantResolver $tenant,
    ) {}

    public function __invoke(Request $request): View
    {
        $this->authorize('viewAny', Shipment::class);

        $days = (int) $request->integer('range', 30);
        $days = in_array($days, [7, 30, 90], true) ? $days : 30;

        $to = now();
        $from = now()->subDays($days);
        $storeId = (int) $this->tenant->currentStoreId();

        $current = $this->analytics->dashboard($storeId, $from, $to);
        /* المقارنة بالفترة السابقة: الرقم وحده بلا سياق لا يقود قراراً. */
        $previous = $this->analytics->dashboard($storeId, $from->copy()->subDays($days), $from);

        return view('shipping.dashboard', [
            'range' => $days,
            'stats' => $current,
            'previous' => $previous,
            'attention' => $this->analytics->attention($storeId),
            'topWilayats' => $this->analytics->topWilayats($storeId, $from, $to),
            'performance' => $this->analytics->carrierPerformance($storeId),
            'invoiceVariance' => $this->analytics->invoiceVariance($storeId, $from, $to),
        ]);
    }
}
