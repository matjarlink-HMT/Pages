<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Enums;

enum PaymentType: string
{
    case Prepaid        = 'prepaid';
    case Cod            = 'cod';
    case CarrierAccount = 'carrier_account';

    public function label(): string
    {
        return __('shipping.payment.'.$this->value);
    }
}
