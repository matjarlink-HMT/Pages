<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Controllers\Merchant;

use App\Domains\Shipping\Contracts\TenantResolver;
use App\Domains\Shipping\DTOs\UnavailableCarrier;
use App\Domains\Shipping\Http\Requests\RateQuoteRequest;
use App\Domains\Shipping\Models\ShippingSettings;
use App\Domains\Shipping\Services\RateComparisonService;
use Illuminate\Http\JsonResponse;
use Illuminate\Routing\Controller;

final class RateController extends Controller
{
    public function __construct(
        private readonly RateComparisonService $rates,
        private readonly TenantResolver $tenant,
    ) {}

    public function quote(RateQuoteRequest $request): JsonResponse
    {
        $storeId = (int) $this->tenant->currentStoreId();
        $defaults = (array) (ShippingSettings::query()->find($storeId)?->sender_defaults ?? []);

        $quotes = $this->rates->compare($storeId, $request->toDto($defaults));

        return response()->json([
            'data' => array_map(static fn ($q): array => $q->toArray(), $quotes),
            'meta' => [
                /* الشركات غير المتاحة تُعرض مع أسبابها لا تُخفى. */
                'unavailable' => array_map(
                    static fn (UnavailableCarrier $u): array => $u->toArray(),
                    $this->rates->unavailable(),
                ),
                'currency' => config('shipping.currency'),
            ],
        ]);
    }
}
