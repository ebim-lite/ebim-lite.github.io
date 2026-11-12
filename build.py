#!/usr/bin/env python3
"""Build the bilingual static site.

Source pages live in src/*.html and contain only the <main> content.
Bilingual text is written inline as [[English::中文]]; {{root}} expands to the
path from the output page to the site root ('' for EN, '../' for zh-tw).

    python3 build.py      # writes ./*.html (English) and ./zh-tw/*.html (繁中)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = 'https://ebim-lite.github.io/'
ASSET_VERSION = '6'

LANGS = {
    'en': {'dir': '', 'root': '', 'html_lang': 'en', 'idx': 0},
    'zh': {'dir': 'zh-tw', 'root': '../', 'html_lang': 'zh-Hant-TW', 'idx': 1},
}

# page key -> (file, title, description)
PAGES = {
    'home': ('index.html',
             '[[EBiM-Lite 2026 · Embodied Bimanual Manipulation Competition::EBiM-Lite 2026 · 具身雙臂操作競賽]]',
             '[[EBiM-Lite 2026: a low-cost embodied bimanual manipulation competition on dual SO-101 arms. Isaac Sim pre-selection, real-robot final at GTC Taipei.'
             '::EBiM-Lite 2026：以雙 SO-101 手臂打造的低成本具身雙臂操作競賽。Isaac Sim 模擬初選，GTC Taipei 實機決賽。]]'),
    'competition': ('competition.html', '[[Competition::競賽內容]] · EBiM-Lite 2026',
                    '[[EBiM-Lite 2026 tracks, scoring rules, robot platform, arena, submission and awards.::EBiM-Lite 2026 賽道、計分規則、機器人平台、場地、提交方式與獎項。]]'),
    'results': ('results.html', '[[Final Results::決賽結果]] · EBiM-Lite 2026',
                '[[Final results of EBiM-Lite 2026.::EBiM-Lite 2026 決賽結果。]]'),
    'workshop': ('workshop.html', '[[Workshop::工作坊]] · EBiM-Lite 2026',
                 '[[The EBiM-Lite workshop at GTC Taipei: talks, panel, posters and awards.::GTC Taipei 的 EBiM-Lite 工作坊：演講、座談、海報與頒獎。]]'),
    'resources': ('resources.html', '[[Learning & Compute::學習與算力]] · EBiM-Lite 2026',
                  '[[Training courses and computing resources for EBiM-Lite 2026 teams.::EBiM-Lite 2026 隊伍可使用的訓練課程與算力資源。]]'),
    'register': ('register.html', '[[Register::報名]] · EBiM-Lite 2026',
                 '[[How to register a team for EBiM-Lite 2026.::EBiM-Lite 2026 隊伍報名方式。]]'),
    'partners': ('partners.html', '[[Partners::合作夥伴]] · EBiM-Lite 2026',
                 '[[Partners and supporters of EBiM-Lite 2026.::EBiM-Lite 2026 的合作夥伴與支持單位。]]'),
    'openday': ('openday.html', '[[Open Day::開放參觀日]] · EBiM-Lite 2026',
                '[[EBiM-Lite 2026 Open Day.::EBiM-Lite 2026 開放參觀日。]]'),
    'faq': ('faq.html', '[[FAQ::常見問題]] · EBiM-Lite 2026',
            '[[Frequently asked questions about EBiM-Lite 2026.::EBiM-Lite 2026 常見問題。]]'),
    'contact': ('contact.html', '[[Contact::聯絡我們]] · EBiM-Lite 2026',
                '[[Contact the EBiM-Lite 2026 organizers.::聯絡 EBiM-Lite 2026 主辦單位。]]'),
}

# Navbar: (label, href, page key, [dropdown items (label, href)])
NAV = [
    ('[[Home::首頁]]', 'index.html', 'home', [
        ('[[Overview::競賽概覽]]', 'index.html#overview'),
        ('[[Two Ways to Engage::兩種參與方式]]', 'index.html#engage'),
        ('[[Key Themes::核心主題]]', 'index.html#themes'),
        ('[[Platform::競賽平台]]', 'index.html#platform'),
        ('[[Important Dates::重要日期]]', 'index.html#dates'),
        ('[[Organizers::主辦團隊]]', 'index.html#organizers'),
    ]),
    ('[[Competition::競賽]]', 'competition.html', 'competition', [
        ('[[Why This Benchmark::為什麼辦這個競賽]]', 'competition.html#why'),
        ('[[EBiM vs EBiM-Lite::EBiM 與 Lite 比較]]', 'competition.html#compare'),
        ('[[Three-Stage Mechanism::三階段機制]]', 'competition.html#mechanism'),
        ('[[The Benchmark::Benchmark 設計]]', 'competition.html#benchmark'),
        ('[[Tasks::賽道任務]]', 'competition.html#tracks'),
        ('[[Platform::競賽平台]]', 'competition.html#platform'),
        ('[[Arena::競賽場地]]', 'competition.html#arena'),
        ('[[Validation Sites::驗證站]]', 'competition.html#sites'),
        ('[[Architecture::競賽架構]]', 'competition.html#architecture'),
        ('[[Call for Participation::參賽辦法]]', 'competition.html#participation'),
        ('[[Get the Code::取得程式碼]]', 'competition.html#code'),
        ('[[Submission::提交方式]]', 'competition.html#submission'),
        ('[[Awards & Prizes::獎項]]', 'competition.html#awards'),
        ('[[Final Results::決賽結果]]', 'results.html'),
    ]),
    ('[[Workshop::工作坊]]', 'workshop.html', 'workshop', [
        ('[[Overview::概覽]]', 'workshop.html#overview'),
        ('[[Schedule::議程]]', 'workshop.html#schedule'),
        ('[[Invited Talks::邀請演講]]', 'workshop.html#talks'),
        ('[[Panel::座談]]', 'workshop.html#panel'),
        ('[[Posters & Demos::海報與展示]]', 'workshop.html#posters'),
        ('[[Important Dates::重要日期]]', 'workshop.html#dates'),
    ]),
    ('[[Resources::學習資源]]', 'resources.html', 'resources', []),
    ('[[Open Day::開放日]]', 'openday.html', 'openday', []),
    ('[[Partners::合作夥伴]]', 'partners.html', 'partners', []),
    ('[[FAQ::常見問題]]', 'faq.html', 'faq', []),
    ('[[Contact::聯絡]]', 'contact.html', 'contact', []),
]

GLOBE = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/>'
         '<path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>')


def nav_html(page, lang, file):
    items = []
    for label, href, key, sub in NAV:
        cls = ' class="active"' if key == page else ''
        if sub:
            subs = ''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in sub)
            items.append(
                f'<li class="has-drop"><a href="{href}"{cls}>{label}</a>'
                f'<button class="drop-btn" aria-label="[[Open submenu::展開子選單]]" aria-expanded="false">▾</button>'
                f'<ul class="drop">{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    reg_cls = ' active' if page == 'register' else ''
    items.append(f'<li><a class="nav-cta{reg_cls}" href="register.html">[[Register::報名]]</a></li>')
    en_href = ('../' if lang == 'zh' else '') + file
    zh_href = ('' if lang == 'zh' else 'zh-tw/') + file
    en_cur = ' class="cur" aria-current="true"' if lang == 'en' else ''
    zh_cur = ' class="cur" aria-current="true"' if lang == 'zh' else ''
    return f'''<nav class="nav" id="site-nav">
    <div class="container">
      <a class="nav-logo" href="index.html">EBiM<span>-Lite</span> 2026</a>
      <ul class="nav-links">{''.join(items)}</ul>
      <div class="lang-switch" role="group" aria-label="Language / 語言">{GLOBE}<a href="{en_href}" hreflang="en" lang="en"{en_cur}>EN</a><a href="{zh_href}" hreflang="zh-Hant" lang="zh-Hant"{zh_cur}>中文</a></div>
      <button class="nav-toggle" aria-label="[[Menu::選單]]" aria-expanded="false">☰</button>
    </div>
  </nav>'''


FOOTER = '''<footer>
    <div class="container">
      <div class="cols">
        <div>
          <a class="nav-logo" href="index.html">EBiM<span>-Lite</span> 2026</a>
          <p style="margin-top:12px">[[Embodied Bimanual Manipulation Competition — Dual SO-101 adaptation. Simulation → Cross-Site Validation → Real-World Evaluation.::具身雙臂操作競賽：雙 SO-101 版本。模擬 → 跨站驗證 → 實機評測。]]</p>
        </div>
        <div>
          <h4>[[Pages::頁面]]</h4>
          <ul>
            <li><a href="index.html">[[Home::首頁]]</a></li>
            <li><a href="competition.html">[[Competition::競賽]]</a></li>
            <li><a href="workshop.html">[[Workshop::工作坊]]</a></li>
            <li><a href="resources.html">[[Learning & Compute::學習與算力]]</a></li>
            <li><a href="results.html">[[Final Results::決賽結果]]</a></li>
            <li><a href="openday.html">[[Open Day::開放參觀日]]</a></li>
          </ul>
        </div>
        <div>
          <h4>[[People::團隊]]</h4>
          <ul>
            <li><a href="index.html#organizers">[[Organizers::主辦團隊]]</a></li>
            <li><a href="partners.html">[[Partners::合作夥伴]]</a></li>
          </ul>
        </div>
        <div>
          <h4>[[Participate::參加]]</h4>
          <ul>
            <li><a href="register.html">[[Register::報名]]</a></li>
            <li><a href="competition.html#participation">[[Compete::參賽辦法]]</a></li>
            <li><a href="workshop.html#posters">[[Submit a Poster::投稿海報]]</a></li>
            <li><a href="faq.html">[[FAQ::常見問題]]</a></li>
            <li><a href="contact.html">[[Contact Us::聯絡我們]]</a></li>
          </ul>
        </div>
      </div>
      <div class="bottom">
        <span>© 2026 [[The EBiM-Lite Organizing Committee::EBiM-Lite 籌備委員會]]</span>
        <span>[[Final at GTC Taipei · May 2027::決賽 · GTC Taipei · 2027 年 5 月]]</span>
      </div>
    </div>
  </footer>'''

FONTS = {
    'en': 'family=Inter:wght@400;500;600;700;800',
    'zh': 'family=Inter:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900',
}

def _svg(*parts):
    return ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ''.join(parts) + '</svg>')


def _p(d):
    return f'<path d="{d}"/>'


ICONS = {
    'monitor': _svg('<rect x="2" y="3" width="20" height="14" rx="2"/>', _p('M8 21h8'), _p('M12 17v4')),
    'pin': _svg(_p('M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0'), '<circle cx="12" cy="10" r="3"/>'),
    'trophy': _svg(_p('M6 9H4.5a2.5 2.5 0 0 1 0-5H6'), _p('M18 9h1.5a2.5 2.5 0 0 0 0-5H18'), _p('M4 22h16'),
                   _p('M10 14.7V17c0 .6-.5 1-1 1.2C7.9 18.8 7 20.2 7 22'), _p('M14 14.7V17c0 .6.5 1 1 1.2 1.1.6 2 2 2 3.8'), _p('M18 2H6v7a6 6 0 0 0 12 0V2Z')),
    'bot': _svg(_p('M12 8V4H8'), '<rect x="4" y="8" width="16" height="12" rx="2"/>', _p('M2 14h2'), _p('M20 14h2'), _p('M15 13v2'), _p('M9 13v2')),
    'flag': _svg(_p('M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z'), _p('M4 22v-7')),
    'repeat': _svg(_p('m17 2 4 4-4 4'), _p('M3 11v-1a4 4 0 0 1 4-4h14'), _p('m7 22-4-4 4-4'), _p('M21 13v1a4 4 0 0 1-4 4H3')),
    'table': _svg(_p('M2 9h20'), _p('M4 9l2-4h12l2 4'), _p('M5 9v11'), _p('M19 9v11')),
    'arrows': _svg(_p('m18 8 4 4-4 4'), _p('M2 12h20'), _p('m6 8-4 4 4 4')),
    'flask': _svg(_p('M10 2v7.5a2 2 0 0 1-.2.9L4.7 20.6a1 1 0 0 0 .9 1.4h12.8a1 1 0 0 0 .9-1.4l-5.1-10.2a2 2 0 0 1-.2-.9V2'), _p('M8.5 2h7'), _p('M7 16h10')),
    'cpu': _svg('<rect x="4" y="4" width="16" height="16" rx="2"/>', '<rect x="9" y="9" width="6" height="6"/>',
                _p('M9 2v2'), _p('M15 2v2'), _p('M9 20v2'), _p('M15 20v2'), _p('M2 9h2'), _p('M2 15h2'), _p('M20 9h2'), _p('M20 15h2')),
    'arm': _svg(_p('M4 21h10'), _p('M9 21v-4'), '<circle cx="9" cy="14.5" r="2.5"/>', _p('M10.8 12.7 15.5 7'), '<circle cx="16.5" cy="5.5" r="2"/>', _p('M18.3 4.6 21 3'), _p('M18.3 6.6 21 8.5')),
    'compass': _svg('<circle cx="12" cy="12" r="10"/>', _p('m16.2 7.8-2.1 6.3-6.3 2.1 2.1-6.3z')),
    'book': _svg(_p('M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20')),
    'chart': _svg(_p('M3 3v18h18'), _p('M7 16l4-5 3 3 5-7')),
    'shield': _svg(_p('M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z')),
    'database': _svg('<ellipse cx="12" cy="5" rx="9" ry="3"/>', _p('M3 5v14a9 3 0 0 0 18 0V5'), _p('M3 12a9 3 0 0 0 18 0')),
    'layers': _svg(_p('m12 2 10 5-10 5L2 7z'), _p('m2 17 10 5 10-5'), _p('m2 12 10 5 10-5')),
    'users': _svg(_p('M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'), '<circle cx="9" cy="7" r="4"/>', _p('M22 21v-2a4 4 0 0 0-3-3.9'), _p('M16 3.1a4 4 0 0 1 0 7.8')),
    'code': _svg(_p('m16 18 6-6-6-6'), _p('m8 6-6 6 6 6')),
    'send': _svg(_p('M22 2 11 13'), _p('M22 2 15 22l-4-9-9-4z')),
    'mic': _svg('<rect x="9" y="2" width="6" height="12" rx="3"/>', _p('M19 10v2a7 7 0 0 1-14 0v-2'), _p('M12 19v3')),
    'message': _svg(_p('M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z')),
    'image': _svg('<rect x="3" y="3" width="18" height="18" rx="2"/>', '<circle cx="9" cy="9" r="2"/>', _p('m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21')),
    'calendar': _svg('<rect x="3" y="4" width="18" height="18" rx="2"/>', _p('M16 2v4'), _p('M8 2v4'), _p('M3 10h18')),
    'mail': _svg('<rect x="2" y="4" width="20" height="16" rx="2"/>', _p('m22 7-10 6L2 7')),
    'github': _svg(_p('M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.1-1.3-.3-2.5-1-3.5.3-1.2.3-2.4 0-3.5 0 0-1 0-3 1.5-2.6-.5-5.4-.5-8 0C6 2 5 2 5 2c-.3 1.1-.3 2.3 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.4.5-.7 1-.8 1.6-.2.6-.3 1.2-.2 1.9v4'), _p('M9 18c-4.5 2-5-2-7-2')),
    'video': _svg(_p('m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 11'), '<rect x="2" y="6" width="14" height="12" rx="2"/>'),
    'door': _svg(_p('M13 4h3a2 2 0 0 1 2 2v14'), _p('M2 20h3'), _p('M13 20h9'), _p('M10 12v.01'), _p('M13 4.6v16.2a1 1 0 0 1-1.2 1L5 20V5.6a2 2 0 0 1 1.5-1.9l4-1A2 2 0 0 1 13 4.6Z')),
    'handshake': _svg(_p('m11 17 2 2a1 1 0 1 0 3-3'), _p('m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.9-3.9a3 3 0 0 0-4.2 0l-.9.9a1 1 0 1 1-3-3l2.8-2.8a5.8 5.8 0 0 1 7.1-.9l.5.3a2 2 0 0 0 1.4.3L21 4'), _p('m21 3 1 11h-2'), _p('M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3'), _p('M3 4h8')),
    'target': _svg('<circle cx="12" cy="12" r="10"/>', '<circle cx="12" cy="12" r="6"/>', '<circle cx="12" cy="12" r="2"/>'),
    'clock': _svg('<circle cx="12" cy="12" r="10"/>', _p('M12 6v6l4 2')),
    'check': _svg('<circle cx="12" cy="12" r="10"/>', _p('m9 12 2 2 4-4')),
}

ICON = re.compile(r'\{\{icon:([a-z]+)\}\}')

MARK = re.compile(r'\[\[(.*?)::(.*?)\]\]', re.S)


def localize(text, lang):
    idx = LANGS[lang]['idx']
    out = MARK.sub(lambda m: m.group(1 + idx), text)
    out = ICON.sub(lambda m: ICONS[m.group(1)], out)
    if lang == 'zh':  # a line break between CJK characters renders as a stray space
        out = re.sub(r'(?<=[\u3000-\u9fff\uff00-\uffef])[ \t]*\n[ \t]*(?=[\u3000-\u9fff\uff00-\uffef])', '', out)
    return out.replace('{{root}}', LANGS[lang]['root'])


def render(page, lang):
    file, title, desc = PAGES[page]
    with open(os.path.join(HERE, 'src', file), encoding='utf-8') as f:
        body = f.read()
    root = LANGS[lang]['root']
    en_url = SITE_URL + ('' if file == 'index.html' else file)
    zh_url = SITE_URL + 'zh-tw/' + ('' if file == 'index.html' else file)
    html = f'''<!doctype html>
<html lang="{LANGS[lang]['html_lang']}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="icon" href="{root}img/favicon.svg" type="image/svg+xml" />
  <link rel="alternate" hreflang="en" href="{en_url}" />
  <link rel="alternate" hreflang="zh-Hant" href="{zh_url}" />
  <link rel="alternate" hreflang="x-default" href="{en_url}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?{FONTS[lang]}&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{root}css/style.css?v={ASSET_VERSION}" />
  <script src="{root}js/main.js?v={ASSET_VERSION}" defer></script>
</head>
<body data-page="{page}">
  <!-- Generated by build.py from src/{file}. Do not edit directly. -->
  {nav_html(page, lang, file)}

{body.rstrip()}

  {FOOTER}
</body>
</html>
'''
    html = localize(html, lang)
    if '[[' in html or ']]' in html or '{{' in html:
        line = next(l for l in html.splitlines() if '[[' in l or ']]' in l or '{{' in l)
        sys.exit(f'Unresolved marker in {lang}/{file}: {line.strip()[:120]}')
    return html


def main():
    for lang, cfg in LANGS.items():
        out_dir = os.path.join(HERE, cfg['dir'])
        os.makedirs(out_dir, exist_ok=True)
        for page, (file, _, _) in PAGES.items():
            with open(os.path.join(out_dir, file), 'w', encoding='utf-8') as f:
                f.write(render(page, lang))
    print(f'Built {len(PAGES)} pages x {len(LANGS)} languages')


if __name__ == '__main__':
    main()
