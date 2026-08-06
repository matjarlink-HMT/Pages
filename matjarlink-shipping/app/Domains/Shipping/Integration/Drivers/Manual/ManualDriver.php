<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Drivers\Manual;

use App\Domains\Shipping\DTOs\CancellationResult;
use App\Domains\Shipping\DTOs\CarrierCapabilities;
use App\Domains\Shipping\DTOs\CarrierShipmentResult;
use App\Domains\Shipping\DTOs\ConnectionResult;
use App\Domains\Shipping\DTOs\RateRequest;
use App\Domains\Shipping\DTOs\ShipmentRequest;
use App\Domains\Shipping\Integration\Drivers\AbstractCarrierDriver;
use App\Domains\Shipping\Services\RateCardEngine;
use Illuminate\Support\Str;

/**
 * شركات التوصيل بلا API: المندوبون والشركات الصغيرة.
 *
 * ليس حالة استثنائية بل Driver كامل يحقق نفس العقد — لذلك يظهر في
 * المقارنة والتقارير ولوحة التحكم مثل غيره تماماً. وجوده يعني أن الوحدة
 * تعمل بالكامل من اليوم الأول دون انتظار بيانات اعتماد أي شركة.
 */
final class ManualDriver extends AbstractCarrierDriver
{
    public function __construct(private readonly RateCardEngine $rateCards) {}

    public function capabilities(): CarrierCapabilities
    {
        return new CarrierCapabilities(
            rating: true,          // من بطاقة الأسعار المحلية لا من API
            label: true,           // بوليصة داخلية بباركود
            tracking: false,       // التحديث يدوي أو باستيراد ملف
            webhook: false,
            cancellation: true,
            pickup: false,
            cod: true,
            returns: true,
            multiPiece: true,
            insurance: false,
            volumetricDivisor: (int) config('shipping.weight.volumetric_divisor', 5000),
            labelFormats: ['pdf_a4', 'pdf_10x15'],
            coverageScope: 'domestic',
        );
    }

    public static function credentialSchema(): array
    {
        /* لا مفاتيح — بيانات تشغيلية فقط تُطبع على البوليصة. */
        return [
            'driver_name' => [
                'type' => 'text', 'label' => 'اسم المندوب / الشركة', 'required' => false,
            ],
            'driver_phone' => [
                'type' => 'tel', 'label' => 'هاتف المندوب', 'required' => false,
            ],
        ];
    }

    public function testConnection(): ConnectionResult
    {
        $hasRateCard = $this->rateCards->hasActiveCard($this->account);

        return $hasRateCard
            ? ConnectionResult::ok(__('shipping.manual.ready'))
            : ConnectionResult::failed(__('shipping.manual.no_rate_card'));
    }

    public function getRates(RateRequest $request): array
    {
        return $this->rateCards->quote($this->account, $request);
    }

    public function createShipment(ShipmentRequest $request): CarrierShipmentResult
    {
        $quotes = $this->getRates($request->toRateRequest());

        if ($quotes === []) {
            return CarrierShipmentResult::failure(__('shipping.errors.no_rate_for_destination'));
        }

        $quote = $quotes[0];

        foreach ($quotes as $candidate) {
            if ($request->serviceCode !== null && $candidate->serviceCode === $request->serviceCode) {
                $quote = $candidate;
                break;
            }
        }

        /* رقم تتبع داخلي: مقروء، فريد، وقابل للطباعة كباركود Code128. */
        $tracking = 'MJL'.strtoupper(Str::padLeft((string) random_int(1, 99_999_999), 8, '0'));

        return new CarrierShipmentResult(
            success: true,
            trackingNumber: $tracking,
            carrierShipmentId: $tracking,
            cost: $quote->price,
            costBreakdown: $quote->breakdown,
            etaMaxDays: $quote->etaMaxDays,
        );
    }

    public function cancelShipment(string $carrierShipmentId): CancellationResult
    {
        /* لا نظام خارجي يُخطَر — الإلغاء محلي والرسوم لم تُحمّل بعد. */
        return CancellationResult::ok(feeRefunded: true);
    }

    public function statusMap(): array
    {
        return [];
    }
}
