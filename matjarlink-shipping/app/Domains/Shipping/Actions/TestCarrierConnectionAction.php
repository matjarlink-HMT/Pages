<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Actions;

use App\Domains\Shipping\DTOs\ConnectionResult;
use App\Domains\Shipping\Enums\ConnectionStatus;
use App\Domains\Shipping\Events\CarrierConnectionFailed;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use Throwable;

/** زر «اختبار الاتصال» — ونفس المسار يستخدمه الفحص الدوري كل ٦ ساعات. */
final readonly class TestCarrierConnectionAction
{
    public function __construct(private CarrierRegistry $registry) {}

    public function execute(StoreCarrierAccount $account): ConnectionResult
    {
        $startedAt = microtime(true);

        try {
            $result = $this->registry->for($account)->testConnection();
        } catch (Throwable $e) {
            $result = ConnectionResult::failed($e->getMessage(), (int) ((microtime(true) - $startedAt) * 1000));
        }

        $account->forceFill([
            'connection_status' => $result->success ? ConnectionStatus::Connected : ConnectionStatus::Failed,
            'last_checked_at' => now(),
            'last_error' => $result->success ? null : $result->message,
            'circuit_opened_until' => $result->success ? null : $account->circuit_opened_until,
        ])->save();

        if (! $result->success) {
            event(new CarrierConnectionFailed($account, $result->message));
        }

        return $result;
    }
}
