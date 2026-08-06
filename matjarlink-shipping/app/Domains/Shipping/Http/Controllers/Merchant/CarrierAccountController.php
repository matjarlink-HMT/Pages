<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Controllers\Merchant;

use App\Domains\Shipping\Actions\TestCarrierConnectionAction;
use App\Domains\Shipping\Enums\ConnectionStatus;
use App\Domains\Shipping\Http\Requests\StoreCarrierAccountRequest;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\ShippingCarrier;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Contracts\View\View;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;

final class CarrierAccountController extends Controller
{
    public function __construct(private readonly CarrierRegistry $registry) {}

    public function index(): View
    {
        $this->authorize('viewAny', StoreCarrierAccount::class);

        $accounts = StoreCarrierAccount::query()
            ->with('carrier')
            ->withCount('shipments')
            ->get()
            ->keyBy('carrier_id');

        return view('shipping.carriers.index', [
            'carriers' => ShippingCarrier::query()->active()->orderBy('sort_order')->get(),
            'accounts' => $accounts,
            /* النموذج يُبنى من مخطط الـ Driver — لا نموذج مكتوب لكل شركة. */
            'schemas' => collect($this->registry->codes())
                ->mapWithKeys(fn (string $code): array => [$code => $this->registry->credentialSchema($code)])
                ->all(),
        ]);
    }

    public function store(StoreCarrierAccountRequest $request, TestCarrierConnectionAction $test): RedirectResponse
    {
        $account = StoreCarrierAccount::query()->create($request->validated() + [
            'connection_status' => ConnectionStatus::Unknown,
            'is_active' => false,
            'created_by' => $request->user()->getAuthIdentifier(),
        ]);

        /* اختبار فوري بعد الحفظ: لا يُفعَّل حساب لم يُثبت أنه يعمل. */
        $result = $test->execute($account->load('carrier'));

        if ($result->success) {
            $account->forceFill(['is_active' => true])->save();
        }

        return redirect()
            ->route('shipping.carrier-accounts.index')
            ->with('status', $result->success
                ? __('shipping.flash.carrier_connected')
                : __('shipping.flash.carrier_failed', ['reason' => $result->message]));
    }

    public function update(StoreCarrierAccountRequest $request, StoreCarrierAccount $account): RedirectResponse
    {
        $this->authorize('update', $account);

        $data = $request->validated();

        /* المفاتيح تُستبدل ولا تُقرأ: حقل فارغ يعني «اتركها كما هي». */
        if (empty($data['credentials'])) {
            unset($data['credentials']);
        } elseif (! $request->user()->can('manageCredentials', StoreCarrierAccount::class)) {
            unset($data['credentials']);
        }

        $account->update($data);

        return back()->with('status', __('shipping.flash.carrier_updated'));
    }

    public function destroy(StoreCarrierAccount $account): RedirectResponse
    {
        $this->authorize('delete', $account);

        $account->delete();

        return back()->with('status', __('shipping.flash.carrier_removed'));
    }

    public function test(StoreCarrierAccount $account, TestCarrierConnectionAction $action): RedirectResponse
    {
        $this->authorize('update', $account);

        $result = $action->execute($account->load('carrier'));

        return back()->with('status', $result->success
            ? __('shipping.flash.connection_ok')
            : __('shipping.flash.connection_failed', ['reason' => $result->message]));
    }

    public function setDefault(Request $request, StoreCarrierAccount $account): RedirectResponse
    {
        $this->authorize('update', $account);

        StoreCarrierAccount::query()->where('is_default', true)->update(['is_default' => false]);
        $account->forceFill(['is_default' => true])->save();

        return back()->with('status', __('shipping.flash.default_set'));
    }
}
