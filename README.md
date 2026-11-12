# EBiM-Lite 2026 Website

Static bilingual website (English / 繁體中文) for **EBiM-Lite 2026**, the Embodied Bimanual Manipulation Competition (dual SO-101 adaptation).

Live: https://casear.github.io/ebim-lite-2026/ (繁中: `/zh-tw/`)

## How to edit

**Edit only the files in `src/`, then run the build.** The `*.html` files in the root and in `zh-tw/` are generated, so do not edit them directly.

```bash
python3 build.py          # regenerates ./*.html (EN) and ./zh-tw/*.html (繁中)
python3 -m http.server    # preview at http://localhost:8000
```

Syntax in `src/*.html`:

| Syntax | Meaning |
|---|---|
| `[[English::中文]]` | Bilingual text. The English output gets the left side, the zh-tw output gets the right side. |
| `{{root}}` | Path to the site root (`''` or `../`). Use it for images: `{{root}}img/x.jpg` |
| `{{icon:name}}` | Inline SVG icon. See `ICONS` in `build.py` |

The navbar (with dropdowns), footer, `<head>` and page titles are defined in `build.py` (`NAV`, `FOOTER`, `PAGES`).
After changing `css/style.css` or `js/main.js`, bump `ASSET_VERSION` in `build.py` so browsers drop the cached copy.

## Pages

| Page | Status |
|---|---|
| `index.html` | Home: overview, ways to engage, key themes, tracks, platform, dates |
| `competition.html` | Content follows the PDF. Code, submission, eligibility and prize details are TBA |
| `resources.html` | DLI courses and compute per phase |
| `faq.html` | FAQ |
| `workshop.html`, `results.html`, `register.html`, `partners.html`, `openday.html`, `contact.html` | Placeholders, to be filled in later |

## TODO (waiting for information)

- Registration form link and contact email
- Organizers, academic host, sponsors (we are still seeking sponsors), prizes
- GitHub repo for code and submission format, rulebook (eligibility, process and safety metrics)
- Workshop program, Open Day details, validation site venues
- Community channels (Discord, chat group, etc.)
