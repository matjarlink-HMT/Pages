@props(['shipment'])

@php
    $stages = [
        __('shipping.status.created'),
        __('shipping.status.picked_up'),
        __('shipping.status.in_transit'),
        __('shipping.status.out_for_delivery'),
        __('shipping.status.delivered'),
    ];
    $current = $shipment->status->stage();
    $isBad = $shipment->status->needsAttention()
        || in_array($shipment->status->value, ['returning', 'returned', 'cancelled'], true);
@endphp

<ol class="ship-stages" aria-label="{{ __('shipping.ui.timeline') }}">
    @foreach ($stages as $index => $stage)
        @php $step = $index + 1; @endphp
        <li class="ship-stage
            @if($step < $current) is-done @elseif($step === $current) {{ $isBad ? 'is-bad' : 'is-current' }} @endif">
            <span class="ship-stage__dot">{{ $step < $current ? '✓' : $step }}</span>
            <span class="ship-stage__label">{{ $stage }}</span>
        </li>
    @endforeach
</ol>
