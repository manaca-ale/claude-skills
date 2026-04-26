# Manaca Brand Tokens

Design tokens for programmatic document generation. Copy Python code blocks directly into scripts.

## Color Palette

```python
from reportlab.lib.colors import HexColor

BRAND_COLORS = {
    "primary":       HexColor("#181448"),  # Navy blue — headers, primary text, borders, table headers
    "accent":        HexColor("#F800A8"),  # Magenta — highlights, active states, accents
    "accent_light":  HexColor("#F868F0"),  # Light magenta — gradient end, hover states
    "background":    HexColor("#E8E8F8"),  # Lavender — page backgrounds, alt table rows
    "text_dark":     HexColor("#18144C"),  # Near-navy — body text (use instead of pure black)
    "text_light":    HexColor("#FFFFFF"),  # White — text on primary/dark backgrounds
    "gray":          HexColor("#555555"),  # Gray — captions, footers, secondary text
    "light_gray":    HexColor("#F5F5F5"),  # Light gray — table alt rows when lavender is too strong
    "border":        HexColor("#CCCCCC"),  # Table borders and dividers
}
```

### Color Usage Rules

| Context | Color | Token |
|---------|-------|-------|
| Page background | White or Lavender | `text_light` or `background` |
| Body text | Near-navy | `text_dark` |
| Section headings (H1) | Navy blue | `primary` |
| Subsection headings (H2, H3) | Navy blue or Near-navy | `primary` or `text_dark` |
| Table header row background | Navy blue | `primary` |
| Table header text | White | `text_light` |
| Table alt rows | Lavender | `background` |
| Table borders | Light gray | `border` |
| Accent highlights | Magenta | `accent` |
| Captions, footers | Gray | `gray` |
| Links | Magenta | `accent` |

## Font Registration (ReportLab)

```python
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
# Or use absolute path:
# FONT_DIR = "C:/Users/aleco/.claude/skills/manaca-brand-guidelines/assets/fonts"

def register_manaca_fonts(font_dir=FONT_DIR):
    """Register Sora font family with all weights for ReportLab."""
    weights = {
        "Sora-Thin":       "Sora-Thin.ttf",
        "Sora-ExtraLight": "Sora-ExtraLight.ttf",
        "Sora-Light":      "Sora-Light.ttf",
        "Sora-Regular":    "Sora-Regular.ttf",
        "Sora-Medium":     "Sora-Medium.ttf",
        "Sora-SemiBold":   "Sora-SemiBold.ttf",
        "Sora-Bold":       "Sora-Bold.ttf",
        "Sora-ExtraBold":  "Sora-ExtraBold.ttf",
    }
    for name, filename in weights.items():
        path = os.path.join(font_dir, filename)
        pdfmetrics.registerFont(TTFont(name, path))

    # Map standard 4-style family for <b> and <i> XML tags
    registerFontFamily(
        'Sora',
        normal='Sora-Regular',
        bold='Sora-Bold',
        italic='Sora-Regular',       # Sora has no italic; fallback to regular
        boldItalic='Sora-Bold'
    )
```

## Typographic Scale (Major Third ratio 1.25)

Base: 10pt body text on A4 page.

| Level | Font | Size (pt) | Leading (pt) | Space Before (pt) | Space After (pt) | Usage |
|-------|------|-----------|--------------|-------------------|-----------------|-------|
| Document Title | Sora-ExtraBold | 24 | 30 | 0 | 24 | Cover/first page title |
| H1 (Section) | Sora-Bold | 20 | 26 | 18 | 12 | Major sections |
| H2 (Subsection) | Sora-SemiBold | 16 | 22 | 14 | 8 | Subsections |
| H3 (Sub-sub) | Sora-Medium | 13 | 18 | 12 | 6 | Minor headings |
| Body | Sora-Regular | 10 | 15 | 0 | 10 | Main text (TA_JUSTIFY) |
| Table Header | Sora-SemiBold | 9 | 12 | 0 | 0 | Table column headers |
| Table Cell | Sora-Light | 9 | 12 | 0 | 0 | Table data |
| Caption | Sora-Light | 8 | 11 | 2 | 4 | Image captions, notes |
| Footer | Sora-Light | 7 | 10 | 0 | 0 | Page footer |

## ParagraphStyle Definitions (ReportLab)

```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

def get_manaca_styles():
    """Complete ParagraphStyle dict for Manaca brand."""
    P = BRAND_COLORS["primary"]
    T = BRAND_COLORS["text_dark"]
    G = BRAND_COLORS["gray"]
    W = BRAND_COLORS["text_light"]

    return {
        "Title": ParagraphStyle(
            name="Title", fontName="Sora-ExtraBold", fontSize=24,
            leading=30, textColor=P, alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=24,
        ),
        "H1": ParagraphStyle(
            name="H1", fontName="Sora-Bold", fontSize=20,
            leading=26, textColor=P, alignment=TA_LEFT,
            spaceBefore=18, spaceAfter=12,
        ),
        "H2": ParagraphStyle(
            name="H2", fontName="Sora-SemiBold", fontSize=16,
            leading=22, textColor=P, alignment=TA_LEFT,
            spaceBefore=14, spaceAfter=8,
        ),
        "H3": ParagraphStyle(
            name="H3", fontName="Sora-Medium", fontSize=13,
            leading=18, textColor=T, alignment=TA_LEFT,
            spaceBefore=12, spaceAfter=6,
        ),
        "Body": ParagraphStyle(
            name="Body", fontName="Sora-Regular", fontSize=10,
            leading=15, textColor=T, alignment=TA_JUSTIFY,
            spaceBefore=0, spaceAfter=10,
        ),
        "TableHeader": ParagraphStyle(
            name="TableHeader", fontName="Sora-SemiBold", fontSize=9,
            leading=12, textColor=W,
        ),
        "TableCell": ParagraphStyle(
            name="TableCell", fontName="Sora-Light", fontSize=9,
            leading=12, textColor=T,
        ),
        "Caption": ParagraphStyle(
            name="Caption", fontName="Sora-Light", fontSize=8,
            leading=11, textColor=G, alignment=TA_CENTER,
            spaceBefore=2, spaceAfter=4,
        ),
        "Footer": ParagraphStyle(
            name="Footer", fontName="Sora-Light", fontSize=7,
            leading=10, textColor=G, alignment=TA_CENTER,
        ),
    }
```

## Table Style (ReportLab)

```python
from reportlab.platypus import Table, TableStyle

MANACA_TABLE_STYLE = TableStyle([
    # Header row
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLORS["primary"]),
    ("TEXTCOLOR", (0, 0), (-1, 0), BRAND_COLORS["text_light"]),
    # Data rows — alternating
    ("BACKGROUND", (0, 1), (-1, -1), BRAND_COLORS["light_gray"]),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRAND_COLORS["text_light"], BRAND_COLORS["background"]]),
    # Borders
    ("GRID", (0, 0), (-1, -1), 0.5, BRAND_COLORS["border"]),
    # Padding
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
])
```

## Page Layout (A4)

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

MANACA_PAGE = {
    "pagesize": A4,
    "left_margin": 2 * cm,
    "right_margin": 2 * cm,
    "top_margin": 2.5 * cm,   # Extra space for header with logo
    "bottom_margin": 2 * cm,
}
```

## Logo Placement

- **Header**: Logo horizontal with tagline, aligned left, max height 1.2cm
- **Footer**: Company info text only (no logo in footer)
- **Cover page**: Logo centered, larger (max width 8cm)

```python
LOGO_PATHS = {
    "header_light_bg": "C:/Users/aleco/.claude/skills/manaca-brand-guidelines/assets/logos/logo_horizontal_tagline_light.png",
    "header_dark_bg":  "C:/Users/aleco/.claude/skills/manaca-brand-guidelines/assets/logos/logo_horizontal_tagline_dark.png",
    "symbol":          "C:/Users/aleco/.claude/skills/manaca-brand-guidelines/assets/logos/symbol_light.png",
    "logotype":        "C:/Users/aleco/.claude/skills/manaca-brand-guidelines/assets/logos/logotype_light.png",
}
```
