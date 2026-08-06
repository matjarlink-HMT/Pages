<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Drivers;

use App\Domains\Shipping\DTOs\CancellationResult;
use App\Domains\Shipping\DTOs\LabelFile;
use App\Domains\Shipping\DTOs\RateRequest;
use App\Domains\Shipping\Enums\LabelFormat;
use App\Domains\Shipping\Integration\Contracts\CarrierDriver;
use App\Domains\Shipping\Models\CarrierApiLog;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use App\Domains\Shipping\Support\CredentialMasker;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Str;
use Throwable;

/**
 * السلوك المشترك لكل الـ Drivers: المهلات، تسجيل النداءات منقّحة من
 * الأسرار، وقاطع الدائرة. الـ Driver الجديد يرث كل هذا ويكتب منطقه فقط.
 */
abstract class AbstractCarrierDriver implements CarrierDriver
{
    protected StoreCarrierAccount $account;

    public function forAccount(StoreCarrierAccount $account): static
    {
        $clone = clone $this;
        $clone->account = $account;

        return $clone;
    }

    public function fetchLabel(string $carrierShipmentId, LabelFormat $format): ?LabelFile
    {
        return null;
    }

    public function track(string $trackingNumber): array
    {
        return [];
    }

    public function cancelShipment(string $carrierShipmentId): CancellationResult
    {
        return CancellationResult::failed(__('shipping.errors.cancellation_unsupported'));
    }

    public function statusMap(): array
    {
        return [];
    }

    public function getRates(RateRequest $request): array
    {
        return [];
    }

    /* ----------------------------------------------------------------- */

    protected function credential(string $key, mixed $default = null): mixed
    {
        return data_get($this->account->credentials, $key, $default);
    }

    protected function http(string $operation): PendingRequest
    {
        $timeout = (int) config("shipping.timeouts.{$operation}", 10);

        return Http::timeout($timeout)
            ->connectTimeout(min($timeout, 5))
            ->acceptJson()
            ->withHeaders(['X-Correlation-Id' => (string) Str::ulid()]);
    }

    /**
     * تغليف موحّد لأي نداء خارجي: يقيس الزمن، يسجّل الطلب والرد منقّحين،
     * ويحدّث عدّاد قاطع الدائرة. لا نداء خارج هذا الغلاف.
     */
    protected function call(string $operation, callable $callback, array $context = []): mixed
    {
        $startedAt = microtime(true);
        $correlationId = (string) Str::ulid();

        try {
            $result = $callback();
            $this->recordSuccess();
            $this->log($operation, $context, ['ok' => true], 200, $startedAt, true, null, $correlationId);

            return $result;
        } catch (Throwable $e) {
            $this->recordFailure();
            $this->log($operation, $context, ['error' => $e->getMessage()], 0, $startedAt, false, $e->getMessage(), $correlationId);

            throw $e;
        }
    }

    protected function log(
        string $operation,
        array $request,
        array $response,
        int $status,
        float $startedAt,
        bool $success,
        ?string $error,
        string $correlationId,
    ): void {
        CarrierApiLog::query()->create([
            'store_id' => $this->account->store_id,
            'store_carrier_account_id' => $this->account->id,
            'operation' => $operation,
            'correlation_id' => $correlationId,
            'request_payload' => CredentialMasker::redact($request),
            'response_payload' => CredentialMasker::redact($response),
            'http_status' => $status,
            'duration_ms' => (int) round((microtime(true) - $startedAt) * 1000),
            'success' => $success,
            'error_message' => $error,
        ]);
    }

    /* ---------------- قاطع الدائرة ---------------- */

    public function isCircuitOpen(): bool
    {
        return $this->account->circuit_opened_until !== null
            && $this->account->circuit_opened_until->isFuture();
    }

    protected function recordSuccess(): void
    {
        Cache::forget($this->circuitKey());

        if ($this->account->circuit_opened_until !== null) {
            $this->account->forceFill(['circuit_opened_until' => null])->save();
        }
    }

    protected function recordFailure(): void
    {
        $threshold = (int) config('shipping.circuit_breaker.failure_threshold', 5);
        $failures = (int) Cache::increment($this->circuitKey());

        if ($failures === 1) {
            Cache::put($this->circuitKey(), 1, now()->addMinutes(10));
        }

        if ($failures >= $threshold) {
            $this->account->forceFill([
                'circuit_opened_until' => now()->addSeconds((int) config('shipping.circuit_breaker.open_seconds', 300)),
            ])->save();

            Cache::forget($this->circuitKey());
        }
    }

    private function circuitKey(): string
    {
        return "shipping:circuit:{$this->account->id}";
    }
}
