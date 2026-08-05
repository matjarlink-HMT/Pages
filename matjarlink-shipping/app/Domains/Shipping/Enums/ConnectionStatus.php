<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Enums;

enum ConnectionStatus: string
{
    case Unknown   = 'unknown';
    case Connected = 'connected';
    case Failed    = 'failed';

    public function label(): string
    {
        return __('shipping.connection.'.$this->value);
    }

    public function color(): string
    {
        return match ($this) {
            self::Connected => 'green',
            self::Failed    => 'red',
            self::Unknown   => 'gray',
        };
    }
}
