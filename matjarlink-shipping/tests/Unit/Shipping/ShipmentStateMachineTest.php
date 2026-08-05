<?php

declare(strict_types=1);

namespace Tests\Unit\Shipping;

use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\StateMachine\ShipmentStateMachine;
use PHPUnit\Framework\TestCase;

final class ShipmentStateMachineTest extends TestCase
{
    private ShipmentStateMachine $machine;

    protected function setUp(): void
    {
        $this->machine = new ShipmentStateMachine();
    }

    public function test_allows_forward_transitions(): void
    {
        self::assertTrue($this->machine->canTransition(ShipmentStatus::Created, ShipmentStatus::PickedUp));
        self::assertTrue($this->machine->canTransition(ShipmentStatus::OutForDelivery, ShipmentStatus::Delivered));
    }

    /** حدث متأخر من الشركة بعد التسليم يُسجَّل ولا ينقض النتيجة النهائية. */
    public function test_terminal_states_are_never_reverted(): void
    {
        foreach ([ShipmentStatus::InTransit, ShipmentStatus::OutForDelivery, ShipmentStatus::Returned] as $late) {
            self::assertFalse($this->machine->canTransition(ShipmentStatus::Delivered, $late));
        }

        self::assertSame(
            ShipmentStatus::Delivered,
            $this->machine->resolve(ShipmentStatus::Delivered, ShipmentStatus::InTransit, incomingIsNewer: true),
        );
    }

    /** أحداث الـ Webhook تصل خارج ترتيبها: الأقدم لا يغيّر الحالة. */
    public function test_older_event_does_not_change_status(): void
    {
        self::assertSame(
            ShipmentStatus::OutForDelivery,
            $this->machine->resolve(ShipmentStatus::OutForDelivery, ShipmentStatus::PickedUp, incomingIsNewer: false),
        );
    }

    public function test_failed_attempt_can_retry_or_return(): void
    {
        self::assertTrue($this->machine->canTransition(ShipmentStatus::FailedAttempt, ShipmentStatus::OutForDelivery));
        self::assertTrue($this->machine->canTransition(ShipmentStatus::FailedAttempt, ShipmentStatus::Returning));
    }

    public function test_same_status_is_not_a_transition(): void
    {
        self::assertFalse($this->machine->canTransition(ShipmentStatus::InTransit, ShipmentStatus::InTransit));
    }
}
