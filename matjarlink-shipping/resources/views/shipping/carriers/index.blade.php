@extends('shipping.layouts.shipping')

@section('shipping')
    <p class="ship-alert ship-alert--info">
        {{ __('الشركات ذات الـ API تُدار بمفاتيح، وشركات التوصيل بلا API تُدار بتسعيرة ومناطق — وكلاهما يظهر في المقارنة والتقارير بنفس الطريقة.') }}
    </p>

    <div class="ship-grid ship-grid--2">
        @foreach ($carriers as $carrier)
            @php $account = $accounts[$carrier->id] ?? null; @endphp

            <section class="ship-card ship-carrier @if($account && ! $account->is_active) is-dim @endif">
                <header class="ship-carrier__head">
                    <h2 class="ship-card__title">{{ $carrier->name() }}</h2>
                    @if ($account?->is_default)
                        <span class="ship-badge ship-badge--purple">{{ __('افتراضية') }}</span>
                    @endif
                    <span class="ship-badge ship-badge--{{ $account?->connection_status->color() ?? 'gray' }}">
                        {{ $account?->connection_status->label() ?? __('shipping.connection.unknown') }}
                    </span>
                </header>

                <p class="ship-muted">
                    {{ $carrier->capabilities()->tracking ? __('تكامل API') : __('إدارة يدوية (بلا API)') }}
                    · {{ $account?->shipments_count ?? 0 }} {{ __('شحنة') }}
                    @if ($account?->last_checked_at)
                        · {{ __('آخر فحص') }} {{ $account->last_checked_at->diffForHumans() }}
                    @endif
                </p>

                @if ($account?->last_error)
                    <p class="ship-alert ship-alert--danger">{{ $account->last_error }}</p>
                @endif

                @if ($account)
                    {{-- المفاتيح تُعرض مقنّعة دائماً: لا نقطة نهاية تُرجع القيمة الكاملة. --}}
                    @foreach ($account->maskedCredentials() as $key => $masked)
                        <p class="ship-muted ship-num">{{ $key }}: {{ $masked }}</p>
                    @endforeach

                    <div class="ship-actions">
                        <form method="POST" action="{{ route('shipping.carrier-accounts.test', $account) }}">
                            @csrf
                            <button class="ship-btn">{{ __('اختبار الاتصال') }}</button>
                        </form>

                        @unless ($account->is_default)
                            <form method="POST" action="{{ route('shipping.carrier-accounts.default', $account) }}">
                                @csrf
                                <button class="ship-btn">{{ __('اجعلها الافتراضية') }}</button>
                            </form>
                        @endunless
                    </div>
                @else
                    {{-- النموذج يُبنى من مخطط الـ Driver لا من نموذج مكتوب لكل شركة. --}}
                    <form method="POST" action="{{ route('shipping.carrier-accounts.store') }}">
                        @csrf
                        <input type="hidden" name="carrier_id" value="{{ $carrier->id }}">
                        <input type="hidden" name="environment" value="live">

                        @foreach ($schemas[$carrier->code] ?? [] as $field => $meta)
                            <label class="ship-field">
                                <span>{{ $meta['label'] ?? $field }}</span>
                                <input type="{{ $meta['type'] ?? 'text' }}" name="credentials[{{ $field }}]"
                                       class="ship-input" @required($meta['required'] ?? false)>
                            </label>
                        @endforeach

                        <button class="ship-btn ship-btn--primary">{{ __('ربط الشركة') }}</button>
                    </form>
                @endif
            </section>
        @endforeach
    </div>
@endsection
