<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Requests;

use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

final class StoreCarrierAccountRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('manage', StoreCarrierAccount::class) ?? false;
    }

    public function rules(): array
    {
        return [
            'carrier_id' => ['required', 'integer', 'exists:shipping_carriers,id'],
            'label' => ['nullable', 'string', 'max:100'],
            'environment' => ['required', Rule::in(['sandbox', 'live'])],
            'credentials' => ['nullable', 'array'],
            'credentials.*' => ['nullable', 'string', 'max:500'],
            'default_service_code' => ['nullable', 'string', 'max:50'],
            'cod_enabled' => ['boolean'],
            'cod_fee_fixed' => ['nullable', 'numeric', 'min:0'],
            'cod_fee_percent' => ['nullable', 'numeric', 'between:0,100'],
            'markup_type' => ['nullable', Rule::in(['none', 'fixed', 'percent'])],
            'markup_value' => ['nullable', 'numeric', 'min:0'],
            'priority' => ['nullable', 'integer', 'min:0', 'max:999'],
        ];
    }

    /**
     * store_id لا يُقبل من المدخلات أبداً — يُملأ من سياق الجلسة في
     * BelongsToStore. تمريره في الطلب لا أثر له.
     */
    public function validated($key = null, $default = null): array
    {
        $data = parent::validated();
        unset($data['store_id']);

        return $data;
    }
}
