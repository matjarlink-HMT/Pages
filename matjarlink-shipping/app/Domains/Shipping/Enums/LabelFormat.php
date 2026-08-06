<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Enums;

enum LabelFormat: string
{
    case PdfA4    = 'pdf_a4';
    case Pdf10x15 = 'pdf_10x15';
    case Zpl      = 'zpl';

    public function extension(): string
    {
        return $this === self::Zpl ? 'zpl' : 'pdf';
    }

    public function mimeType(): string
    {
        return $this === self::Zpl ? 'application/vnd.zebra.zpl' : 'application/pdf';
    }

    public function view(): string
    {
        return match ($this) {
            self::Pdf10x15 => 'shipping.labels.thermal',
            default        => 'shipping.labels.a4',
        };
    }
}
