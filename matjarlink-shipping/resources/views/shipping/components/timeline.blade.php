@props(['events'])

{{-- مصدر كل حدث معروض: تحديث تلقائي أم مزامنة أم تسجيل يدوي ومن سجّله. --}}
<ol class="ship-timeline">
    @forelse ($events as $event)
        <li class="ship-timeline__item ship-timeline__item--{{ $event->status->color() }}">
            <p class="ship-timeline__title">{{ $event->description() }}</p>
            <p class="ship-timeline__meta">
                <time datetime="{{ $event->occurred_at?->toIso8601String() }}">
                    {{ $event->occurred_at?->translatedFormat('Y-m-d · H:i') }}
                </time>
                @if ($event->location) · {{ $event->location }} @endif
                <span class="ship-chip">{{ $event->source->label() }}</span>
            </p>
        </li>
    @empty
        <li class="ship-muted">{{ __('shipping.ui.no_results') }}</li>
    @endforelse
</ol>
