@props(['status', 'delayed' => false, 'stale' => false])

{{-- الحالة نص ولون معاً لا لوناً وحده — إتاحة لمن لا يميّز الألوان. --}}
<span class="ship-badge ship-badge--{{ $status->color() }}">{{ $status->label() }}</span>

@if ($delayed)
    <span class="ship-badge ship-badge--red">{{ __('shipping.ui.delayed') }}</span>
@endif

@if ($stale)
    <span class="ship-badge ship-badge--amber">{{ __('shipping.ui.stale') }}</span>
@endif
