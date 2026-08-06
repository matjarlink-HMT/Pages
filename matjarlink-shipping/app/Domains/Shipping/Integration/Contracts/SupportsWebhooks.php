<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Contracts;

use Illuminate\Http\Request;

/** واجهة اختيارية — لا تُثقَل بها الشركات التي لا تدفع أحداثاً. */
interface SupportsWebhooks
{
    public function verifyWebhook(Request $request): bool;

    /** @return list<\App\Domains\Shipping\DTOs\TrackingEventData> */
    public function parseWebhook(array $payload): array;

    public function webhookTrackingNumber(array $payload): ?string;
}
