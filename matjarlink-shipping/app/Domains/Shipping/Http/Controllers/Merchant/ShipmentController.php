<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Controllers\Merchant;

use App\Domains\Shipping\Actions\CancelShipmentAction;
use App\Domains\Shipping\Actions\CreateShipmentAction;
use App\Domains\Shipping\Actions\RecordManualEventAction;
use App\Domains\Shipping\Contracts\OrderBridge;
use App\Domains\Shipping\Contracts\TenantResolver;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Http\Filters\ShipmentFilter;
use App\Domains\Shipping\Http\Requests\CreateShipmentRequest;
use App\Domains\Shipping\Http\Resources\ShipmentDetailResource;
use App\Domains\Shipping\Http\Resources\ShipmentResource;
use App\Domains\Shipping\Jobs\SyncShipmentTrackingJob;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\ShippingCarrier;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use App\Domains\Shipping\Services\LabelService;
use App\Domains\Shipping\Support\OmanGeo;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Routing\Controller;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\HttpFoundation\StreamedResponse;

final class ShipmentController extends Controller
{
    public function __construct(
        private readonly ShipmentFilter $filter,
        private readonly LabelService $labels,
        private readonly TenantResolver $tenant,
    ) {}

    public function index(Request $request): mixed
    {
        $this->authorize('viewAny', Shipment::class);

        $query = Shipment::query()->with(['carrier', 'receiver']);

        /* من يملك view_own فقط لا يرى شحنات غيره. */
        if (! $request->user()->can('shipping.shipments.view_all')) {
            $query->where('created_by', $request->user()->getAuthIdentifier());
        }

        $shipments = $this->filter->apply($query, $request)
            ->cursorPaginate((int) min($request->integer('per_page', 25), 100))
            ->withQueryString();

        if ($request->expectsJson()) {
            return ShipmentResource::collection($shipments);
        }

        return view('shipping.shipments.index', [
            'shipments' => $shipments,
            'carriers' => ShippingCarrier::query()->active()->get(),
            'governorates' => OmanGeo::governorates(),
            'statuses' => ShipmentStatus::cases(),
            'filters' => $request->only(['q', 'status', 'carrier_id', 'governorate', 'attention', 'open', 'is_cod', 'sort']),
        ]);
    }

    public function create(Request $request, OrderBridge $orders): mixed
    {
        $this->authorize('create', Shipment::class);

        /* التعبئة المسبقة من الطلب هي جوهر وعد «لا إدخال مرتين». */
        $order = $request->filled('order_id')
            ? $orders->snapshot((int) $request->integer('order_id'))
            : null;

        return view('shipping.shipments.create', [
            'order' => $order,
            'accounts' => StoreCarrierAccount::query()->usable()->with('carrier')->get(),
            'geo' => OmanGeo::tree(),
        ]);
    }

    public function store(CreateShipmentRequest $request, CreateShipmentAction $action): RedirectResponse|JsonResponse
    {
        $shipment = $action->execute(
            (int) $this->tenant->currentStoreId(),
            $request->toDto(),
        );

        if ($request->expectsJson()) {
            return (new ShipmentDetailResource($shipment))->response()->setStatusCode(201);
        }

        return redirect()
            ->route('shipping.shipments.show', $shipment)
            ->with('status', __('shipping.flash.created', ['reference' => $shipment->reference]));
    }

    public function show(Request $request, Shipment $shipment): mixed
    {
        $this->authorize('view', $shipment);

        $shipment->load(['carrier', 'account', 'sender', 'receiver', 'packages', 'items', 'events', 'labels']);

        if ($request->expectsJson()) {
            return new ShipmentDetailResource($shipment);
        }

        return view('shipping.shipments.show', ['shipment' => $shipment]);
    }

    public function cancel(Request $request, Shipment $shipment, CancelShipmentAction $action): RedirectResponse
    {
        $this->authorize('cancel', $shipment);

        $action->execute($shipment, $request->input('reason'));

        return back()->with('status', __('shipping.flash.cancelled'));
    }

    public function sync(Shipment $shipment): RedirectResponse
    {
        $this->authorize('view', $shipment);

        SyncShipmentTrackingJob::dispatch($shipment->id);

        return back()->with('status', __('shipping.flash.sync_queued'));
    }

    public function storeEvent(Request $request, Shipment $shipment, RecordManualEventAction $action): RedirectResponse
    {
        $this->authorize('recordEvent', $shipment);

        $validated = $request->validate([
            'status' => ['required', 'string', 'in:'.implode(',', ShipmentStatus::values())],
            'description' => ['required', 'string', 'max:255'],
            'location' => ['nullable', 'string', 'max:150'],
        ]);

        $action->execute(
            $shipment,
            ShipmentStatus::from($validated['status']),
            $validated['description'],
            $validated['location'] ?? null,
        );

        return back()->with('status', __('shipping.flash.event_recorded'));
    }

    public function label(Shipment $shipment): StreamedResponse
    {
        $this->authorize('printLabel', $shipment);

        $label = $this->labels->latest($shipment) ?? $this->labels->generate($shipment);
        $this->labels->markPrinted($label);

        return Storage::disk($label->disk)->download(
            $label->path,
            "{$shipment->reference}.{$label->format->extension()}",
        );
    }

    public function export(Request $request): RedirectResponse
    {
        $this->authorize('viewAny', Shipment::class);

        /* التصدير دائماً غير متزامن: لا تجميد للشاشة على آلاف الصفوف. */
        return back()->with('status', __('shipping.flash.export_queued'));
    }
}
