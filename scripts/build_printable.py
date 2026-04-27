#!/usr/bin/env python3
"""
PDF builder for KGB cache printables.
Creates a ready-to-print PDF with QR code, letterhead, and instructions.
"""

import argparse
import json
import sys
from pathlib import Path
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from PIL import Image
except ImportError as e:
    print(f"ERROR: Missing dependency. Install with: pip install reportlab pillow", file=sys.stderr)
    print(f"Details: {e}", file=sys.stderr)
    sys.exit(1)


def load_cache_spec(guid: str) -> dict:
    """Load cache specification from specs/{guid}.json"""
    spec_path = Path("specs") / f"{guid}.json"
    with open(spec_path, "r") as f:
        return json.load(f)


def load_kgb_config() -> dict:
    """Load KGB configuration from src/_data/kgb.json"""
    config_path = Path("src") / "_data" / "kgb.json"
    with open(config_path, "r") as f:
        return json.load(f)


def build_printable(guid: str, output_path: str = None) -> str:
    """
    Build a printable PDF with QR code and KGB letterhead.

    Args:
        guid: Cache GUID
        output_path: Optional output path. If not provided, uses printables/{guid}.pdf

    Returns:
        Path to the generated PDF file
    """
    if output_path is None:
        output_path = Path("printables") / f"{guid}.pdf"
    else:
        output_path = Path(output_path)

    # Load cache spec and KGB config
    spec = load_cache_spec(guid)
    config = load_kgb_config()

    cache_number = spec["cache_number"]
    title = spec["title"]
    base_url = config["base_url"]
    bureau_name = config["bureau_name"]
    colors = config["colors"]

    # Construct the cache URL
    cache_url = f"{base_url}/c/{guid}/"

    # Create PDF
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=letter)

    # Page dimensions
    width, height = letter
    margin = 0.5 * inch
    content_width = width - (2 * margin)

    # Colors
    ink_color = HexColor(colors["ink"])
    paper_color = HexColor(colors["paper"])
    stamp_red = HexColor(colors["stamp_red"])
    muted_color = HexColor(colors["muted"])

    # Set background
    c.setFillColor(paper_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # ===== LETTERHEAD =====
    y_pos = height - margin

    # KGB Logo/Header
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(stamp_red)
    c.drawString(margin, y_pos - 0.3 * inch, "KHAN GEOCACHING BUREAU")

    # Subheader
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(ink_color)
    c.drawString(margin, y_pos - 0.5 * inch, "CLASSIFIED FIELD OPERATIONS")

    # Divider line
    y_pos -= 0.65 * inch
    c.setLineWidth(1.5)
    c.setStrokeColor(stamp_red)
    c.line(margin, y_pos, width - margin, y_pos)

    # ===== CACHE INFO =====
    y_pos -= 0.3 * inch
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(ink_color)
    c.drawString(margin, y_pos, f"CACHE: {cache_number}")

    y_pos -= 0.25 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y_pos, title)

    # ===== QR CODE =====
    qr_path = Path("printables") / f"{guid}-qr.png"
    if qr_path.exists():
        y_pos -= 0.5 * inch
        qr_size = 3 * inch

        # Center QR code horizontally
        qr_x = (width - qr_size) / 2
        qr_y = y_pos - qr_size

        # Draw QR code border
        c.setLineWidth(2)
        c.setStrokeColor(stamp_red)
        c.rect(qr_x - 0.1 * inch, qr_y - 0.1 * inch, qr_size + 0.2 * inch, qr_size + 0.2 * inch, fill=0)

        # Draw QR code
        c.drawImage(str(qr_path), qr_x, qr_y, width=qr_size, height=qr_size)

        y_pos = qr_y - 0.3 * inch
    else:
        c.setFont("Helvetica", 10)
        c.setFillColor(stamp_red)
        c.drawString(margin, y_pos, f"[QR CODE NOT FOUND: {qr_path}]")
        y_pos -= 0.3 * inch

    # ===== URL FALLBACK =====
    y_pos -= 0.2 * inch
    c.setFont("Helvetica", 8)
    c.setFillColor(ink_color)
    c.drawString(margin, y_pos, f"Fallback URL: {cache_url}")

    # ===== INSTRUCTIONS =====
    y_pos -= 0.4 * inch
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(stamp_red)
    c.drawString(margin, y_pos, "Scan to receive your orders, Agent.")

    # ===== CUT LINES =====
    margin_cut = 0.25 * inch

    # Draw dashed cut lines around perimeter
    c.setLineWidth(0.5)
    c.setStrokeColor(muted_color)

    # Create dashed lines using dash pattern (on, off)
    c.setDash(3, 3)

    # Top cut line
    y_cut = height - margin_cut
    c.line(margin_cut, y_cut, width - margin_cut, y_cut)

    # Left cut line
    cut_top = height - margin_cut
    cut_bottom = margin_cut
    c.line(margin_cut, cut_top, margin_cut, cut_bottom)

    # Right cut line
    c.line(width - margin_cut, cut_top, width - margin_cut, cut_bottom)

    # Bottom cut line
    c.line(margin_cut, margin_cut, width - margin_cut, margin_cut)

    # Reset dash pattern for solid lines
    c.setDash(1, 0)

    # ===== FOOTER =====
    y_pos = margin_cut * 0.7
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(ink_color)
    footer_text = "Property of KGB. Return to its hiding place after finding."
    text_width = c.stringWidth(footer_text, "Helvetica-Oblique", 8)
    footer_x = (width - text_width) / 2
    c.drawString(footer_x, y_pos, footer_text)

    # Save the PDF
    c.save()

    return str(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build printable PDF for KGB cache")
    parser.add_argument("--guid", required=True, help="Cache GUID")
    parser.add_argument("--output", help="Output path (optional, defaults to printables/{guid}.pdf)")

    args = parser.parse_args()

    try:
        output_file = build_printable(args.guid, args.output)
        print(output_file)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
