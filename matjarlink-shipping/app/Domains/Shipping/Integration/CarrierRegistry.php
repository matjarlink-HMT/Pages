<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration;

use App\Domains\Shipping\Integration\Contracts\CarrierDriver;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Contracts\Container\Container;
use InvalidArgumentException;

/**
 * سجل الـ Drivers: يحوّل صف حساب في قاعدة البيانات إلى نسخة Driver جاهزة.
 * تسجيل شركة جديدة سطر واحد في config/shipping.php أو عبر register().
 */
final class CarrierRegistry
{
    /** @var array<string, class-string<CarrierDriver>> */
    private array $drivers = [];

    public function __construct(private readonly Container $container)
    {
        foreach ((array) config('shipping.drivers', []) as $code => $class) {
            $this->register((string) $code, $class);
        }
    }

    /** @param class-string<CarrierDriver> $class */
    public function register(string $code, string $class): void
    {
        if (! is_subclass_of($class, CarrierDriver::class)) {
            throw new InvalidArgumentException("{$class} must implement CarrierDriver.");
        }

        $this->drivers[$code] = $class;
    }

    public function has(string $code): bool
    {
        return isset($this->drivers[$code]);
    }

    /** @return list<string> */
    public function codes(): array
    {
        return array_keys($this->drivers);
    }

    public function driverClass(string $code): string
    {
        if (! $this->has($code)) {
            throw new InvalidArgumentException("No shipping driver registered for [{$code}].");
        }

        return $this->drivers[$code];
    }

    public function for(StoreCarrierAccount $account): CarrierDriver
    {
        $code = $account->carrier->code;

        /** @var CarrierDriver $driver */
        $driver = $this->container->make($this->driverClass($code));

        return $driver->forAccount($account);
    }

    public function credentialSchema(string $code): array
    {
        $class = $this->driverClass($code);

        return $class::credentialSchema();
    }
}
