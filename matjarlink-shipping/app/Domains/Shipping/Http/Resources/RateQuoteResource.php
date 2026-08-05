<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Resources;

use App\Domains\Shipping\DTOs\RateQuoteData;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/** @mixin RateQuoteData */
final class RateQuoteResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return $this->resource->toArray();
    }
}
