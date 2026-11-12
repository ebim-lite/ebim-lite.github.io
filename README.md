# EBiM-Lite 2026 Website

Static website for **EBiM-Lite 2026**, the Embodied Bimanual Manipulation Competition (dual SO-101 adaptation).

## Pages (English at root, Traditional Chinese in `zh-tw/`)
- `index.html`: overview, stages, tracks, platform, important dates, organizers, registration
- `competition.html`: rules, the three tracks and their scoring, platform specs, arena, validation sites, participation
- `resources.html`: NVIDIA DLI courses and computing resources
- `faq.html`: frequently asked questions

The navbar and footer are injected by `js/main.js`. All styles are in `css/style.css`.

## Local preview
```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## TODO
- Registration link, contact email, organizers and partner logos
- Keep `zh-tw/` in sync when editing English pages
