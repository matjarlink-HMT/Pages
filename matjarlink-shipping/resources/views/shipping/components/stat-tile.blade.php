@props(['label', 'value', 'sub' => null, 'tone' => null, 'href' => null])

<{{ $href ? 'a' : 'div' }} @if($href) href="{{ $href }}" @endif
    class="ship-stat @if($tone) ship-stat--{{ $tone }} @endif @if($href) ship-stat--link @endif">
    <span class="ship-stat__label">{{ $label }}</span>
    <span class="ship-stat__value">{{ $value }}</span>
    @if ($sub)
        <span class="ship-stat__sub">{!! $sub !!}</span>
    @endif
</{{ $href ? 'a' : 'div' }}>
