@extends('shipping.layouts.shipping')

@section('shipping')
    {{--
        عند القدوم من طلب داخل متجرلينك تُعبّأ كل الحقول مسبقاً من OrderSnapshot،
        فلا يُدخل الموظف البيانات مرتين — وهذا جوهر وعد الوحدة.
    --}}
    @if ($order)
        <p class="ship-alert ship-alert--info">
            {{ __('الشحنة مسبقة التعبئة من الطلب :order — راجع الوزن فقط.', ['order' => $order->orderNumber]) }}
        </p>
    @endif

    <form method="POST" action="{{ route('shipping.shipments.store') }}" class="ship-form" id="shipmentForm">
        @csrf
        <input type="hidden" name="order_id" value="{{ $order?->orderId }}">

        <div class="ship-grid ship-grid--2">
            <section class="ship-card">
                <h2 class="ship-card__title">{{ __('بيانات المستلم') }}</h2>

                <label class="ship-field">
                    <span>{{ __('الاسم') }} *</span>
                    <input name="receiver[name]" class="ship-input" required
                           value="{{ old('receiver.name', $order?->receiver->name) }}">
                </label>

                <label class="ship-field">
                    <span>{{ __('الهاتف') }} *</span>
                    <input name="receiver[phone]" class="ship-input" dir="ltr" required
                           value="{{ old('receiver.phone', $order?->receiver->phone) }}">
                </label>

                <div class="ship-grid ship-grid--2">
                    <label class="ship-field">
                        <span>{{ __('المحافظة') }} *</span>
                        <select name="receiver[governorate]" class="ship-input" id="governorate" required>
                            @foreach (array_keys($geo) as $governorate)
                                <option value="{{ $governorate }}"
                                    @selected(old('receiver.governorate', $order?->receiver->governorate) === $governorate)>
                                    {{ $governorate }}
                                </option>
                            @endforeach
                        </select>
                    </label>

                    <label class="ship-field">
                        <span>{{ __('الولاية') }} *</span>
                        <select name="receiver[wilayat]" class="ship-input" id="wilayat" required></select>
                    </label>
                </div>

                <label class="ship-field">
                    <span>{{ __('العنوان') }}</span>
                    <input name="receiver[street]" class="ship-input"
                           value="{{ old('receiver.street', $order?->receiver->street) }}">
                </label>

                <label class="ship-field">
                    <span>{{ __('معلم بارز') }}</span>
                    <input name="receiver[landmark]" class="ship-input"
                           value="{{ old('receiver.landmark', $order?->receiver->landmark) }}"
                           placeholder="{{ __('خلف مسجد النور') }}">
                </label>
            </section>

            <section class="ship-card">
                <h2 class="ship-card__title">{{ __('بيانات الطرد') }}</h2>

                <div class="ship-grid ship-grid--2">
                    <label class="ship-field">
                        <span>{{ __('الوزن الفعلي (كجم)') }} *</span>
                        <input type="number" step="0.01" min="0.01" name="packages[0][weight_kg]"
                               class="ship-input" id="weight" required value="{{ old('packages.0.weight_kg', 1) }}">
                    </label>

                    <label class="ship-field">
                        <span>{{ __('عدد القطع') }}</span>
                        <input type="number" min="1" name="packages[0][quantity]" class="ship-input"
                               value="{{ old('packages.0.quantity', 1) }}">
                    </label>
                </div>

                <fieldset class="ship-field">
                    <legend>{{ __('الأبعاد (سم)') }}</legend>
                    <div class="ship-row">
                        <input type="number" step="0.1" name="packages[0][length_cm]" id="len" class="ship-input" placeholder="{{ __('طول') }}">
                        <input type="number" step="0.1" name="packages[0][width_cm]" id="wid" class="ship-input" placeholder="{{ __('عرض') }}">
                        <input type="number" step="0.1" name="packages[0][height_cm]" id="hei" class="ship-input" placeholder="{{ __('ارتفاع') }}">
                    </div>
                </fieldset>

                {{-- الوزن المحتسب يُعرض أثناء الإدخال: يمنع مفاجأة فاتورة الشركة. --}}
                <p class="ship-alert ship-alert--info" id="billableHint">{{ __('shipping.ui.volumetric_hint') }}</p>

                <label class="ship-field">
                    <span>{{ __('قيمة الطرد') }}</span>
                    <input type="number" step="0.001" min="0" name="declared_value" class="ship-input"
                           value="{{ old('declared_value', $order?->total ?? 0) }}">
                </label>

                <label class="ship-check">
                    <input type="checkbox" name="is_cod" value="1" @checked(old('is_cod', $order?->isCod))>
                    <span>{{ __('shipping.payment.cod') }}</span>
                </label>

                <label class="ship-field">
                    <span>{{ __('مبلغ التحصيل') }}</span>
                    <input type="number" step="0.001" min="0" name="cod_amount" class="ship-input"
                           value="{{ old('cod_amount', $order?->codAmount ?? 0) }}">
                </label>
            </section>
        </div>

        <section class="ship-card">
            <h2 class="ship-card__title">{{ __('shipping.carriers') }}</h2>

            @forelse ($accounts as $account)
                <label class="ship-rate">
                    <input type="radio" name="store_carrier_account_id" value="{{ $account->id }}"
                           @checked($account->is_default) required>
                    <span class="ship-rate__name">{{ $account->displayName() }}</span>
                    <span class="ship-rate__meta">{{ $account->carrier->capabilities()->coverageScope }}</span>
                </label>
            @empty
                <p class="ship-empty">
                    {{ __('لا توجد شركة شحن مربوطة بعد.') }}
                    <a href="{{ route('shipping.carrier-accounts.index') }}" class="ship-btn ship-btn--primary">
                        {{ __('ربط أول شركة') }}
                    </a>
                </p>
            @endforelse

            <p class="ship-muted">{{ __('تُجلب الأسعار الحيّة عند اختيار الوجهة والوزن عبر نقطة النهاية shipping/rates.') }}</p>
        </section>

        <label class="ship-field">
            <span>{{ __('ملاحظات للمندوب') }}</span>
            <input name="notes" class="ship-input" value="{{ old('notes') }}">
        </label>

        {{-- الزر يُقفل فور الضغط، وIdempotency-Key يمنع الازدواج عند إعادة الإرسال. --}}
        <button type="submit" class="ship-btn ship-btn--primary" id="submitBtn" @disabled($accounts->isEmpty())>
            {{ __('تأكيد وإنشاء بوليصة الشحن') }}
        </button>
    </form>

    @push('scripts')
        <script>
            const GEO = @json($geo);
            const DIVISOR = {{ (int) config('shipping.weight.volumetric_divisor', 5000) }};
            const gov = document.getElementById('governorate');
            const wilayat = document.getElementById('wilayat');
            const selected = @json(old('receiver.wilayat', $order?->receiver->wilayat));

            const fillWilayats = () => {
                wilayat.innerHTML = (GEO[gov.value] || [])
                    .map((w) => `<option ${w === selected ? 'selected' : ''}>${w}</option>`).join('');
            };
            gov.addEventListener('change', fillWilayats);
            fillWilayats();

            const hint = document.getElementById('billableHint');
            const recalc = () => {
                const [l, w, h] = ['len', 'wid', 'hei'].map((id) => parseFloat(document.getElementById(id).value) || 0);
                const actual = parseFloat(document.getElementById('weight').value) || 0;
                const volumetric = (l * w * h) / DIVISOR;
                const billable = Math.max(actual, volumetric);
                hint.textContent = volumetric > 0
                    ? `{{ __('shipping.ui.billable_weight') }}: ${billable.toFixed(2)} {{ __('كجم') }}`
                    : @json(__('shipping.ui.volumetric_hint'));
            };
            ['weight', 'len', 'wid', 'hei'].forEach((id) => document.getElementById(id).addEventListener('input', recalc));
            recalc();

            document.getElementById('shipmentForm').addEventListener('submit', (e) => {
                document.getElementById('submitBtn').disabled = true;
            });
        </script>
    @endpush
@endsection
