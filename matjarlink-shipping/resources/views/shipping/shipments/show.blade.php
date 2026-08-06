@extends('shipping.layouts.shipping')

@section('shipping')
    <header class="ship-detail__head">
        <div>
            <h1 class="ship-detail__ref">{{ $shipment->reference }}</h1>
            <x-shipping.status-badge :status="$shipment->status"
                :delayed="(bool) $shipment->is_delayed" :stale="(bool) $shipment->is_stale" />
            @if ($shipment->tracking_number)
                <p class="ship-num">{{ $shipment->tracking_number }}</p>
            @endif
        </div>

        <div class="ship-actions">
            <form method="POST" action="{{ route('shipping.shipments.sync', $shipment) }}">
                @csrf
                <button class="ship-btn">{{ __('تحديث الآن') }}</button>
            </form>

            @can('printLabel', $shipment)
                <a href="{{ route('shipping.shipments.label', $shipment) }}" class="ship-btn">{{ __('بوليصة الشحن') }}</a>
            @endcan

            @can('cancel', $shipment)
                <form method="POST" action="{{ route('shipping.shipments.cancel', $shipment) }}"
                      onsubmit="return confirm('{{ __('إلغاء الشحنة؟ سيُطلب الإلغاء من شركة الشحن أيضاً.') }}')">
                    @csrf
                    @method('DELETE')
                    <button class="ship-btn ship-btn--danger">{{ __('إلغاء الشحنة') }}</button>
                </form>
            @endcan
        </div>
    </header>

    <x-shipping.stages :shipment="$shipment" />

    <div class="ship-grid ship-grid--2">
        <section class="ship-card">
            <h2 class="ship-card__title">{{ __('shipping.ui.timeline') }}</h2>
            <x-shipping.timeline :events="$shipment->events" />

            @can('recordEvent', $shipment)
                <form method="POST" action="{{ route('shipping.shipments.events.store', $shipment) }}" class="ship-inline-form">
                    @csrf
                    <select name="status" class="ship-input" required aria-label="{{ __('الحالة') }}">
                        @foreach (\App\Domains\Shipping\Enums\ShipmentStatus::cases() as $status)
                            <option value="{{ $status->value }}">{{ $status->label() }}</option>
                        @endforeach
                    </select>
                    <input type="text" name="description" class="ship-input ship-input--grow" required
                           placeholder="{{ __('وصف الحدث — مثال: اتصلت بالشركة وأكدت الاستلام') }}">
                    <input type="text" name="location" class="ship-input" placeholder="{{ __('الموقع') }}">
                    <button class="ship-btn">{{ __('تسجيل حدث يدوي') }}</button>
                </form>
            @endcan
        </section>

        <div class="ship-stack">
            <section class="ship-card">
                <h2 class="ship-card__title">{{ __('بيانات المستلم') }}</h2>
                <dl class="ship-dl">
                    <dt>{{ __('الاسم') }}</dt><dd>{{ $shipment->receiver?->name }}</dd>
                    <dt>{{ __('الهاتف') }}</dt><dd class="ship-num">{{ $shipment->receiver?->phone }}</dd>
                    <dt>{{ __('الوجهة') }}</dt><dd>{{ $shipment->receiver?->wilayat }} — {{ $shipment->receiver?->governorate }}</dd>
                    <dt>{{ __('العنوان') }}</dt><dd>{{ $shipment->receiver?->oneLine() }}</dd>
                    @if ($shipment->receiver?->landmark)
                        <dt>{{ __('معلم بارز') }}</dt><dd>{{ $shipment->receiver->landmark }}</dd>
                    @endif
                </dl>
            </section>

            <section class="ship-card">
                <h2 class="ship-card__title">{{ __('shipping.carriers') }}</h2>
                <dl class="ship-dl">
                    <dt>{{ __('الشركة') }}</dt><dd>{{ $shipment->carrier?->name() }}</dd>
                    <dt>{{ __('الخدمة') }}</dt><dd>{{ $shipment->service_name ?? $shipment->service_code }}</dd>
                    <dt>{{ __('shipping.ui.billable_weight') }}</dt>
                    <dd>{{ (float) $shipment->billable_weight_kg }} {{ __('كجم') }} · {{ $shipment->pieces_count }} {{ __('قطعة') }}</dd>
                    <dt>{{ __('الوعد بالتسليم') }}</dt><dd>{{ $shipment->promised_delivery_at?->format('Y-m-d') ?? '—' }}</dd>
                </dl>
            </section>

            @can('viewCosts', $shipment)
                <section class="ship-card">
                    <h2 class="ship-card__title">{{ __('التكلفة') }}</h2>
                    <dl class="ship-dl">
                        <dt>{{ __('المُسعّر') }}</dt><dd>{{ number_format((float) $shipment->quoted_cost, 3) }}</dd>
                        <dt>{{ __('الفعلي') }}</dt><dd>{{ number_format((float) $shipment->actual_cost, 3) }}</dd>
                        <dt>{{ __('الفرق') }}</dt>
                        <dd class="@if($shipment->isOverbilled()) ship-text--danger @endif">
                            {{ number_format($shipment->costVariance(), 3) }}
                        </dd>
                        <dt>{{ __('الدفع') }}</dt>
                        <dd>{{ $shipment->payment_type->label() }}
                            @if($shipment->is_cod) — {{ number_format((float) $shipment->cod_amount, 3) }} @endif
                        </dd>
                    </dl>

                    @if ($shipment->isOverbilled())
                        <p class="ship-alert ship-alert--warn">
                            {{ __('التكلفة الفعلية تجاوزت المُسعّر — يظهر هذا الفرق في تقرير مطابقة الفواتير.') }}
                        </p>
                    @endif
                </section>
            @endcan
        </div>
    </div>
@endsection
