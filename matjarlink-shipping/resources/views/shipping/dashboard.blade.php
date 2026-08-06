@extends('shipping.layouts.shipping')

@section('shipping')
    @php
        $money = fn (float $v): string => number_format($v, 3).' '.__('ر.ع');
        $trend = function (float $now, float $before): string {
            if ($before <= 0) { return ''; }
            $pct = round((($now - $before) / $before) * 100);
            $dir = $pct > 0 ? 'up' : ($pct < 0 ? 'down' : 'flat');
            $arrow = $pct > 0 ? '▲' : ($pct < 0 ? '▼' : '—');
            return '<span class="ship-trend ship-trend--'.$dir.'">'.$arrow.' '.abs($pct).'٪</span>';
        };
    @endphp

    <div class="ship-toolbar">
        <div class="ship-range" role="group" aria-label="{{ __('shipping.dashboard') }}">
            @foreach ([7, 30, 90] as $days)
                <a href="{{ route('shipping.dashboard', ['range' => $days]) }}"
                   class="ship-chip @if($range === $days) is-active @endif">{{ $days }}</a>
            @endforeach
        </div>
        <a href="{{ route('shipping.shipments.create') }}" class="ship-btn ship-btn--primary">
            {{ __('shipping.create_shipment') }}
        </a>
    </div>

    {{-- يُخفى الصف كاملاً حين لا شيء يحتاج تدخلاً: الصفوف الفارغة ضجيج. --}}
    @php
        /* كل بطاقة رابط إلى قائمة مفلترة مسبقاً — الأرقام قابلة للنقر لا للعرض فقط. */
        $attentionLinks = [
            'delayed' => ['is_delayed' => 1],
            'stale' => ['is_stale' => 1],
            'failed_attempt' => ['status' => ['failed_attempt']],
            'carrier_error' => ['status' => ['carrier_error']],
        ];
    @endphp

    @if (array_sum($attention) > 0)
        <section class="ship-attention" aria-label="{{ __('shipping.ui.attention') }}">
            @foreach ($attention as $key => $count)
                @continue($count === 0)
                <a class="ship-attention__card"
                   href="{{ route('shipping.shipments.index', $attentionLinks[$key] ?? []) }}">
                    <span class="ship-attention__count">{{ $count }}</span>
                    <span class="ship-attention__label">{{ __('shipping.attention.'.$key) }}</span>
                </a>
            @endforeach
        </section>
    @endif

    <section class="ship-grid ship-grid--4">
        <x-shipping.stat-tile :label="__('shipping.ui.total_shipments')"
            :value="number_format($stats['shipments'])"
            :sub="$trend($stats['shipments'], $previous['shipments'])" />

        @foreach (['created', 'picked_up', 'in_transit', 'out_for_delivery', 'delivered', 'returned'] as $status)
            <x-shipping.stat-tile
                :label="__('shipping.status.'.$status)"
                :value="number_format($stats['by_status'][$status] ?? 0)"
                :tone="$status === 'delivered' ? 'good' : ($status === 'returned' ? 'bad' : null)" />
        @endforeach
    </section>

    <section class="ship-grid ship-grid--4">
        <x-shipping.stat-tile :label="__('shipping.ui.total_cost')"
            :value="$money($stats['cost'])" :sub="$trend($stats['cost'], $previous['cost'])" />

        <x-shipping.stat-tile :label="__('shipping.ui.avg_cost')"
            :value="$money($stats['shipments'] > 0 ? $stats['cost'] / $stats['shipments'] : 0)" />

        <x-shipping.stat-tile :label="__('shipping.ui.avg_delivery')"
            :value="$stats['avg_delivery_hours'] !== null ? round($stats['avg_delivery_hours'] / 24, 1).' '.__('يوم') : '—'"
            :sub="$stats['delivered'].' '.__('shipping.status.delivered')" />

        <x-shipping.stat-tile :label="__('shipping.ui.on_time_rate')"
            :value="$stats['on_time_rate'] !== null ? $stats['on_time_rate'].'٪' : '—'" tone="good" />

        <x-shipping.stat-tile :label="__('shipping.ui.cod_pending')" :value="$money($stats['cod_total'])" tone="warn" />

        {{-- فروقات الفوترة: ما دفعناه فعلاً مقابل ما سُعِّر لنا. --}}
        <x-shipping.stat-tile :label="__('shipping.ui.invoice_variance')"
            :value="$money($invoiceVariance['variance'])"
            :sub="$invoiceVariance['overbilled_count'].' '.__('شحنة فُوترت أعلى من المُسعّر')"
            :tone="$invoiceVariance['variance'] > 0 ? 'warn' : null" />
    </section>

    <section class="ship-card">
        <h2 class="ship-card__title">{{ __('shipping.ui.top_wilayats') }}</h2>
        @php $max = max(1, ...array_values($topWilayats ?: [1])); @endphp
        <ul class="ship-bars">
            @forelse ($topWilayats as $wilayat => $count)
                <li class="ship-bars__row">
                    <span class="ship-bars__label">{{ $wilayat }}</span>
                    <span class="ship-bars__track">
                        <i style="inline-size: {{ max(3, (int) round($count / $max * 100)) }}%"></i>
                    </span>
                    <span class="ship-bars__value">{{ $count }}</span>
                </li>
            @empty
                <li class="ship-muted">{{ __('shipping.ui.no_shipments') }}</li>
            @endforelse
        </ul>
    </section>
@endsection
