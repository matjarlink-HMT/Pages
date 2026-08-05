<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Enums;

enum ShipmentEventSource: string
{
    case Webhook = 'webhook';
    case Polling = 'polling';
    case Manual  = 'manual';
    case System  = 'system';
    case Import  = 'import';

    public function label(): string
    {
        return __('shipping.source.'.$this->value);
    }
}
