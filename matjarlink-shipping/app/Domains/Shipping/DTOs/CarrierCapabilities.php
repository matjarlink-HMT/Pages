<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

/**
 * الواجهة تُبنى من القدرات: إن كانت الشركة لا تدعم جدولة الاستلام
 * لا يظهر الزر أصلاً — لا رسالة خطأ بعد الضغط.
 */
final readonly class CarrierCapabilities
{
    public function __construct(
        public bool $rating = false,
        public bool $label = false,
        public bool $tracking = false,
        public bool $webhook = false,
        public bool $cancellation = false,
        public bool $pickup = false,
        public bool $cod = false,
        public bool $returns = false,
        public bool $multiPiece = false,
        public bool $insurance = false,
        public int $volumetricDivisor = 5000,
        /** @var list<string> */
        public array $labelFormats = ['pdf_a4'],
        public string $coverageScope = 'domestic',
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            rating: (bool) ($data['rating'] ?? false),
            label: (bool) ($data['label'] ?? false),
            tracking: (bool) ($data['tracking'] ?? false),
            webhook: (bool) ($data['webhook'] ?? false),
            cancellation: (bool) ($data['cancellation'] ?? false),
            pickup: (bool) ($data['pickup'] ?? false),
            cod: (bool) ($data['cod'] ?? false),
            returns: (bool) ($data['returns'] ?? false),
            multiPiece: (bool) ($data['multi_piece'] ?? false),
            insurance: (bool) ($data['insurance'] ?? false),
            volumetricDivisor: (int) ($data['volumetric_divisor'] ?? 5000),
            labelFormats: (array) ($data['label_formats'] ?? ['pdf_a4']),
            coverageScope: (string) ($data['coverage_scope'] ?? 'domestic'),
        );
    }

    public function toArray(): array
    {
        return [
            'rating' => $this->rating, 'label' => $this->label, 'tracking' => $this->tracking,
            'webhook' => $this->webhook, 'cancellation' => $this->cancellation,
            'pickup' => $this->pickup, 'cod' => $this->cod, 'returns' => $this->returns,
            'multi_piece' => $this->multiPiece, 'insurance' => $this->insurance,
            'volumetric_divisor' => $this->volumetricDivisor,
            'label_formats' => $this->labelFormats, 'coverage_scope' => $this->coverageScope,
        ];
    }
}
