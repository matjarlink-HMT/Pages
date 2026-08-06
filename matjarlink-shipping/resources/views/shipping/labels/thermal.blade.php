<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{{ $shipment->reference }}</title>
    <style>
        @page { size: 100mm 150mm; margin: 4mm; }
        body { font-family: "DejaVu Sans", Tahoma, sans-serif; font-size: 11px; color: #000; }
        .ref { font-size: 16px; font-weight: 800; direction: ltr; text-align: center; letter-spacing: 1px; }
        .sep { border-top: 1px dashed #000; margin: 6px 0; }
        .big { font-size: 13px; font-weight: 700; }
        .cod { border: 2px solid #000; padding: 5px; text-align: center; font-weight: 800; margin-top: 6px; }
    </style>
</head>
<body>
    <div class="ref">{{ $shipment->tracking_number ?? $shipment->reference }}</div>
    <div style="text-align:center">{{ $shipment->carrier?->name() }}</div>
    <div class="sep"></div>

    <div class="big">{{ $shipment->receiver?->name }}</div>
    <div style="direction:ltr">{{ $shipment->receiver?->phone }}</div>
    <div>{{ $shipment->receiver?->oneLine() }}</div>
    @if ($shipment->receiver?->landmark)<div>{{ $shipment->receiver->landmark }}</div>@endif

    <div class="sep"></div>
    <div>{{ (float) $shipment->billable_weight_kg }} كجم · {{ $shipment->pieces_count }} قطعة</div>

    @if ($shipment->is_cod)
        <div class="cod">تحصيل {{ number_format((float) $shipment->cod_amount, 3) }} ر.ع</div>
    @endif
</body>
</html>
