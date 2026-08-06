<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\DTOs\LabelFile;
use App\Domains\Shipping\Enums\LabelFormat;
use App\Domains\Shipping\Events\LabelGenerated;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\ShipmentLabel;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\View;

/**
 * البوليصة: من الشركة إن أصدرتها، وإلا قالب داخلي بباركود.
 * تُخزَّن على قرص خاص ولا تُنشر — تحمل بيانات عميل كاملة.
 */
final class LabelService
{
    public function __construct(private readonly CarrierRegistry $registry) {}

    public function generate(Shipment $shipment, ?LabelFormat $format = null): ShipmentLabel
    {
        $format ??= LabelFormat::PdfA4;

        $file = $this->fetchFromCarrier($shipment, $format) ?? $this->renderInternal($shipment, $format);

        $disk = (string) config('shipping.storage.disk', 'local');
        $version = (int) $shipment->labels()->max('version') + 1;
        $path = sprintf(
            '%s/%d/%s-v%d.%s',
            trim((string) config('shipping.storage.labels_path', 'shipping/labels'), '/'),
            $shipment->store_id,
            $shipment->reference,
            $version,
            $format->extension(),
        );

        Storage::disk($disk)->put($path, $file->contents, ['visibility' => 'private']);

        $label = $shipment->labels()->create([
            'format' => $format,
            'disk' => $disk,
            'path' => $path,
            'version' => $version,
            'print_count' => 0,
        ]);

        event(new LabelGenerated($shipment, $label));

        return $label;
    }

    public function latest(Shipment $shipment, ?LabelFormat $format = null): ?ShipmentLabel
    {
        return $shipment->labels()
            ->when($format !== null, static fn ($q) => $q->where('format', $format->value))
            ->orderByDesc('version')
            ->first();
    }

    public function markPrinted(ShipmentLabel $label): void
    {
        $label->forceFill([
            'printed_at' => now(),
            'printed_by' => auth()->id(),
            'print_count' => $label->print_count + 1,
        ])->save();
    }

    private function fetchFromCarrier(Shipment $shipment, LabelFormat $format): ?LabelFile
    {
        if ($shipment->carrier_shipment_id === null || $shipment->account === null) {
            return null;
        }

        if (! $shipment->carrier->capabilities()->label) {
            return null;
        }

        return $this->registry->for($shipment->account)
            ->fetchLabel($shipment->carrier_shipment_id, $format);
    }

    /**
     * القالب الداخلي: يخدم الشركات اليدوية ويكون بديلاً حين يتعذّر جلب البوليصة.
     * يُحوَّل إلى PDF عبر Dompdf إن كان مثبّتاً في المنصة، وإلا يُحفظ HTML
     * قابلاً للطباعة من المتصفح — فلا تتعطّل الطباعة بانتظار حزمة.
     */
    private function renderInternal(Shipment $shipment, LabelFormat $format): LabelFile
    {
        $html = View::make($format->view(), [
            'shipment' => $shipment->loadMissing(['sender', 'receiver', 'packages', 'items', 'carrier']),
        ])->render();

        if (class_exists(\Barryvdh\DomPDF\Facade\Pdf::class)) {
            $paper = $format === LabelFormat::Pdf10x15 ? [0, 0, 283.5, 425.2] : 'a4';

            return new LabelFile(
                \Barryvdh\DomPDF\Facade\Pdf::loadHTML($html)->setPaper($paper)->output(),
                $format,
            );
        }

        return new LabelFile($html, $format);
    }
}
