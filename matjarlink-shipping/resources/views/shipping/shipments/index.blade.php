@extends('shipping.layouts.shipping')

@section('shipping')
    <form method="GET" class="ship-card ship-filters">
        <input type="search" name="q" value="{{ $filters['q'] ?? '' }}" class="ship-input ship-input--grow"
               placeholder="{{ __('بحث برقم الطلب أو التتبع أو اسم العميل أو الهاتف') }}" aria-label="{{ __('بحث') }}">

        <select name="status[]" class="ship-input" aria-label="{{ __('shipping.status.created') }}">
            <option value="">{{ __('كل الحالات') }}</option>
            @foreach ($statuses as $status)
                <option value="{{ $status->value }}"
                    @selected(in_array($status->value, (array) ($filters['status'] ?? []), true))>
                    {{ $status->label() }}
                </option>
            @endforeach
        </select>

        <select name="carrier_id[]" class="ship-input" aria-label="{{ __('shipping.carriers') }}">
            <option value="">{{ __('كل الشركات') }}</option>
            @foreach ($carriers as $carrier)
                <option value="{{ $carrier->id }}"
                    @selected(in_array((string) $carrier->id, (array) ($filters['carrier_id'] ?? []), true))>
                    {{ $carrier->name() }}
                </option>
            @endforeach
        </select>

        <select name="governorate[]" class="ship-input" aria-label="{{ __('المحافظة') }}">
            <option value="">{{ __('كل المحافظات') }}</option>
            @foreach ($governorates as $governorate)
                <option value="{{ $governorate }}"
                    @selected(in_array($governorate, (array) ($filters['governorate'] ?? []), true))>
                    {{ $governorate }}
                </option>
            @endforeach
        </select>

        <button type="submit" class="ship-btn ship-btn--primary">{{ __('تطبيق') }}</button>
        <a href="{{ route('shipping.shipments.index') }}" class="ship-btn">{{ __('shipping.ui.clear_filters') }}</a>
    </form>

    <div class="ship-card ship-card--flush">
        <div class="ship-tablewrap">
            <table class="ship-table">
                <thead>
                    <tr>
                        <th scope="col">{{ __('المرجع') }}</th>
                        <th scope="col">{{ __('رقم التتبع') }}</th>
                        <th scope="col">{{ __('shipping.carriers') }}</th>
                        <th scope="col">{{ __('العميل') }}</th>
                        <th scope="col">{{ __('الولاية') }}</th>
                        <th scope="col">{{ __('الإنشاء') }}</th>
                        <th scope="col">{{ __('الحالة') }}</th>
                        @can('viewCosts', \App\Domains\Shipping\Models\Shipment::class)
                            <th scope="col">{{ __('التكلفة') }}</th>
                        @endcan
                    </tr>
                </thead>
                <tbody>
                    @forelse ($shipments as $shipment)
                        <tr>
                            <td data-label="{{ __('المرجع') }}">
                                <a href="{{ route('shipping.shipments.show', $shipment) }}">{{ $shipment->reference }}</a>
                            </td>
                            <td data-label="{{ __('رقم التتبع') }}" class="ship-num">{{ $shipment->tracking_number ?? '—' }}</td>
                            <td data-label="{{ __('shipping.carriers') }}">{{ $shipment->carrier?->name() }}</td>
                            <td data-label="{{ __('العميل') }}">{{ $shipment->receiver?->name }}</td>
                            <td data-label="{{ __('الولاية') }}">
                                {{ $shipment->receiver?->wilayat }}
                                <small class="ship-muted">{{ $shipment->receiver?->governorate }}</small>
                            </td>
                            <td data-label="{{ __('الإنشاء') }}" class="ship-num">{{ $shipment->created_at?->format('Y-m-d') }}</td>
                            <td data-label="{{ __('الحالة') }}">
                                <x-shipping.status-badge :status="$shipment->status"
                                    :delayed="(bool) $shipment->is_delayed" :stale="(bool) $shipment->is_stale" />
                            </td>
                            @can('viewCosts', \App\Domains\Shipping\Models\Shipment::class)
                                <td data-label="{{ __('التكلفة') }}" class="ship-num">
                                    {{ number_format((float) $shipment->total_cost, 3) }}
                                </td>
                            @endcan
                        </tr>
                    @empty
                        <tr>
                            <td colspan="8" class="ship-empty">
                                {{ __('shipping.ui.no_shipments') }}
                                <a href="{{ route('shipping.shipments.create') }}" class="ship-btn ship-btn--primary">
                                    {{ __('shipping.create_shipment') }}
                                </a>
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </div>

    {{-- ترقيم بالمؤشر: أداء ثابت مهما عمقت الصفحة. --}}
    <div class="ship-pagination">{{ $shipments->links() }}</div>
@endsection
