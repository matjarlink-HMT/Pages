<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

use App\Domains\Shipping\Enums\LabelFormat;

final readonly class LabelFile
{
    public function __construct(
        public string $contents,
        public LabelFormat $format = LabelFormat::PdfA4,
    ) {}

    public function size(): int
    {
        return strlen($this->contents);
    }
}
