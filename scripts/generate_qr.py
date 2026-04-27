#!/usr/bin/env python3
"""
QR code generator for KGB caches.
Generates high-error-correction QR codes suitable for outdoor use.
"""

import argparse
import sys
from pathlib import Path

try:
    import qrcode
except ImportError:
    print("ERROR: qrcode module not found. Install with: pip install qrcode[pil]", file=sys.stderr)
    sys.exit(1)


def generate_qr(guid: str, url: str, output_path: str = None) -> str:
    """
    Generate a QR code with high error correction for the given URL.

    Args:
        guid: Cache GUID
        url: Full URL to encode
        output_path: Optional output path. If not provided, uses printables/{guid}-qr.png

    Returns:
        Path to the generated QR code PNG file
    """
    if output_path is None:
        output_path = Path("printables") / f"{guid}-qr.png"
    else:
        output_path = Path(output_path)

    # Create QR code with high error correction (H = 30% redundancy)
    qr = qrcode.QRCode(
        version=None,  # Auto-determine version
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,  # Minimum 8px per module for printing
        border=2,  # Standard quiet zone
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the image
    img.save(output_path)

    return str(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QR code for KGB cache")
    parser.add_argument("--guid", required=True, help="Cache GUID")
    parser.add_argument("--url", required=True, help="URL to encode in QR code")
    parser.add_argument("--output", help="Output path (optional, defaults to printables/{guid}-qr.png)")

    args = parser.parse_args()

    try:
        output_file = generate_qr(args.guid, args.url, args.output)
        print(output_file)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
