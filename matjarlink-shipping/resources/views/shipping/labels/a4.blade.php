<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{{ $shipment->reference }}</title>
    <style>
        @page { size: A4; margin: 12mm; }
        body { font-family: "DejaVu Sans", Tahoma, sans-serif; color: #111; font-size: 12px; }
        .box { border: 1.5px solid #111; border-radius: 6px; padding: 10px; margin-bottom: 10px; }
        .row { display: flex; justify-content: space-between; gap: 12px; }
        h1 { font-size: 18px; margin: 0 0 4px; }
        .ref { font-size: 20px; font-weight: 800; letter-spacing: 1px; direction: ltr; }
        .label { color: #555; font-size: 10px; }
        .big { font-size: 15px; font-weight: 700; }
        .cod { border: 2px solid #111; padding: 8px; text-align: center; font-size: 16px; font-weight: 800; }
        table { width: 100%; border-collapse: collapse; font-size: 11px; }
        th, td { border-bottom: 1px solid #ddd; padding: 4px 6px; text-align: start; }
    </style>
</head>
<body>
    <div class="box row">
        <div>
            <h1>{{ $shipment->carrier?->name() }}</h1>
            <div class="label">{{ $shipment->service_name ?? $shipment->service_code }}</div>
        </div>
        <div>
            <div class="ref">{{ $shipment->tracking_number ?? $shipment->reference }}</div>
            <div class="label">{{ $shipment->reference }} · {{ $shipment->created_at?->format('Y-m-d') }}</div>
        </div>
    </div>

    <div class="box">
        <div class="label">المرسل إليه</div>
        <div class="big">{{ $shipment->receiver?->name }}</div>
        <div style="direction:ltr; text-align:start">{{ $shipment->receiver?->phone }}</div>
        <div>{{ $shipment->receiver?->oneLine() }}</div>
        @if ($shipment->receiver?->landmark)
            <div class="label">معلم بارز: {{ $shipment->receiver->landmark }}</div>
        @endif
    </div>

    <div class="box">
        <div class="label">المرسل</div>
        <div>{{ $shipment->sender?->name }} · <span style="direction:ltr">{{ $shipment->sender?->phone }}</span></div>
        <div>{{ $shipment->sender?->oneLine() }}</div>
    </div>

    <div class="box row">
        <div>
            <div class="label">الوزن المحتسب</div>
            <div class="big">{{ (float) $shipment->billable_weight_kg }} كجم</div>
        </div>
        <div>
            <div class="label">عدد القطع</div>
            <div class="big">{{ $shipment->pieces_count }}</div>
        </div>
        @if ($shipment->is_cod)
            <div class="cod">تحصيل عند الاستلام<br>{{ number_format((float) $shipment->cod_amount, 3) }} ر.ع</div>
        @endif
    </div>

    @if ($shipment->items->isNotEmpty())
        <div class="box">
            <table>
                <tr><th>الصنف</th><th>الكمية</th></tr>
                @foreach ($shipment->items as $item)
                    <tr><td>{{ $item->name }}</td><td>{{ $item->quantity }}</td></tr>
                @endforeach
            </table>
        </div>
    @endif

    @if ($shipment->notes)
        <div class="box"><div class="label">ملاحظات</div><div>{{ $shipment->notes }}</div></div>
    @endif
</body>
</html>
