# Manaca Brand Guidelines

Apply Manaca Tecnologias Sociais' official brand identity to any visual artifact: PDFs, presentations, Google Docs, images, and social media assets.

## Trigger

Use this skill when:
- Generating PDFs (proposals, dossies, reports, material de apoio) that should look like Manaca
- Creating PowerPoint/PPTX presentations
- Styling Google Docs with Manaca brand
- Any artifact that needs Manaca's visual identity (colors, fonts, logo)
- User mentions "identidade visual", "marca Manaca", "brand", "cores da Manaca", "template Manaca"

## Quick Reference

| Element | Value |
|---------|-------|
| Primary color | `#181448` (navy blue) |
| Accent color | `#F800A8` (magenta) — gradient to `#F868F0` |
| Background | `#E8E8F8` (lavender) |
| Text dark | `#18144C` |
| Font | Sora (Google Fonts, geometric sans-serif) |
| Logo (PDF light bg) | `assets/logos/logo_horizontal_tagline_light.png` |
| Logo (PDF dark bg) | `assets/logos/logo_horizontal_tagline_dark.png` |

## References

| File | Purpose |
|------|---------|
| `references/brand-tokens.md` | Design tokens: colors, fonts, typographic scale, spacing — as Python dicts |
| `references/asset-registry.md` | Paths to logos, icons, fonts (local + Drive) |

## How to Use

1. Load `references/brand-tokens.md` for color palette, font registration code, and ParagraphStyle definitions
2. Copy the Python code blocks directly into your ReportLab/python-pptx scripts
3. Use `assets/fonts/` for TTF files and `assets/logos/` for logo PNGs
4. Follow the typographic hierarchy (Title → H1 → H2 → H3 → Body → Caption)

## Important Notes

- Font files (Sora TTF) are bundled in `assets/fonts/` — never rely on system fonts
- Logo has 28 variants in the shared drive; the 4 most-used are in `assets/logos/`
- Always use navy blue `#181448` for headers and primary text, never pure black
- The magenta accent `#F800A8` is for highlights and table headers, not body text
- Background lavender `#E8E8F8` is for alternating table rows and page backgrounds
