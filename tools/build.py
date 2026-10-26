#!/usr/bin/env python3
"""Build complete static HTML. No network, package manager, or server required."""
from html import escape
from pathlib import Path
import argparse
import sys

from content import CONTACT, HOME, PAGES, UI, UPDATED

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://guogxy.github.io/plant-journal/"
PAGES_KEYS = ("privacy", "terms", "support", "licenses")
ICON = ROOT / "assets/app-icon.png"  # Add only the user-approved production icon here.


def url(locale, page=""):
    return BASE + locale + "/" + (page + "/" if page else "")


def root_path(page):
    return "../../" if page else "../"


def link(locale, page="", current_page=""):
    return root_path(current_page) + locale + "/" + (page + "/" if page else "")


def header(locale, page):
    t = UI[locale]
    home = link(locale, current_page=page)
    other = "zh" if locale == "en" else "en"
    icon = f'<img class="brand-icon" src="{root_path(page)}assets/app-icon.png" width="34" height="34" alt="">' if ICON.exists() else ""
    nav = "".join(f'<a href="{home}#{key}">{escape(label)}</a>' for key, label in t["nav"])
    active = ' aria-current="page"' if page == "support" else ""
    return f'''<a class="skip-link" href="#main">{t['skip']}</a>
<header class="site-header"><div class="wrap nav-inner">
<a class="wordmark" href="{home}" aria-label="{escape(t['name'])}">{icon}{t['name']}</a>
<nav class="nav-links" aria-label="{'Main navigation' if locale == 'en' else '主导航'}">{nav}<a href="{link(locale, 'support', page)}"{active}>{t['support']}</a></nav>
<a class="language" href="{link(other, page, page)}" hreflang="{UI[other]['lang']}" lang="{UI[other]['lang']}" aria-label="{'切换到简体中文' if locale == 'en' else 'Switch to English'}">{t['other']}</a>
</div></header>'''


def footer(locale, page):
    t = UI[locale]
    nav = "".join(f'<a href="{link(locale, key, page)}"' + (' aria-current="page"' if key == page else '') + f'>{t[key]}</a>' for key in PAGES_KEYS)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="footer-top"><div><a class="wordmark" href="{link(locale, current_page=page)}">{t['name']}</a><p style="font-size:12px;color:var(--muted);margin-top:8px">{t['footer']}</p></div><nav class="footer-links" aria-label="{'Information' if locale == 'en' else '网站信息'}">{nav}</nav></div>
<div class="footer-bottom"><p>© 2026 {t['copyright']}</p><p>{t['site_note']}</p></div>
</div></footer>'''


def document(locale, page, title, description, body):
    title = escape(title)
    desc = escape(description, quote=True)
    icon = f'<link rel="icon" type="image/png" href="{root_path(page)}assets/app-icon.png">\n<link rel="apple-touch-icon" href="{root_path(page)}assets/app-icon.png">' if ICON.exists() else ""
    return f'''<!doctype html>
<html lang="{UI[locale]['lang']}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#f7f8f1"><meta name="color-scheme" content="light">
<link rel="canonical" href="{url(locale, page)}">
<link rel="alternate" hreflang="en" href="{url('en', page)}">
<link rel="alternate" hreflang="zh-Hans" href="{url('zh', page)}">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{url(locale, page)}">
<meta property="og:locale" content="{'en_US' if locale == 'en' else 'zh_CN'}">
<meta property="og:site_name" content="{UI[locale]['name']}">
<meta name="twitter:card" content="summary"><link rel="stylesheet" href="{root_path(page)}assets/site.css">
{icon}
</head>
<body>{header(locale, page)}
{body}
{footer(locale, page)}
</body></html>
'''


def home(locale):
    c, t = HOME[locale], UI[locale]
    screenshot_file = "reference-screen-en.png" if locale == "en" and (ROOT / "assets/reference-screen-en.png").exists() else "reference-screen.png"
    screenshot_caption = c['screenshot_caption']
    if screenshot_file == "reference-screen-en.png":
        screenshot_caption = screenshot_caption.replace("Development screenshot in Chinese,", "Development screenshot,")
    bands = "".join(f'<div class="intro-item"><b>{escape(a)}</b><span>{escape(b)}</span></div>' for a, b in c['bands'])
    steps = "".join(f'<article class="step"><span class="number">0{i}</span><h3>{escape(a)}</h3><p>{escape(b)}</p></article>' for i, (a, b) in enumerate(c['steps'], 1))
    features = "".join(f'<li><b>{escape(a)}</b><span>{escape(b)}</span></li>' for a, b in c['alignment_features'])
    cards = ""
    for card in c['edit_cards']:
        options = "".join(f'<li><span>{escape(a)}</span><span class="control-tag">{escape(b)}</span></li>' for a, b in card['options'])
        cards += f'<article class="edit-card"><span class="small-label">{card["label"]}</span><h3>{card["title"]}</h3><p>{card["body"]}</p><ul class="settings-list">{options}</ul></article>'
    notes = "".join(f'<li><h3>{escape(a)}</h3><p>{escape(b)}</p></li>' for a, b in c['data_notes'])
    body = f'''<main id="main">
<div class="wrap"><section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><p class="eyebrow">{c['eyebrow']}</p><h1 id="hero-title">{c['headline']}</h1><p>{c['intro']}</p>
<div class="actions"><a class="button" href="#workflow">{c['cta']}</a><a class="button secondary" href="support/">{c['secondary']}</a></div><span class="status">{t['status']} · iPhone & iPad</span></div>
<figure class="hero-visual"><div class="photo-stage"><img src="../assets/reference-plant.jpg" width="900" height="676" alt="{c['photo_alt']}" fetchpriority="high"><div class="viewfinder" aria-hidden="true"></div><div class="frame-label" aria-hidden="true"><div><strong>{c['frame_title']}</strong><span>{c['frame_sub']}</span></div><i class="crosshair"></i></div></div><figcaption class="visual-caption">{c['photo_caption']}</figcaption></figure>
</section><div class="intro-band">{bands}</div>
<section class="workflow" id="workflow" aria-labelledby="workflow-title"><div class="section-heading"><div><p class="eyebrow">{c['workflow_label']}</p><h2 id="workflow-title">{c['workflow_title']}</h2></div><p>{c['workflow_intro']}</p></div><div class="workflow-grid">{steps}</div></section></div>
<section class="dark-section" aria-labelledby="alignment-title"><div class="wrap detail-grid"><div class="detail-copy"><p class="eyebrow">{c['alignment_label']}</p><h2 id="alignment-title">{c['alignment_title']}</h2><p>{c['alignment_intro']}</p><ul class="feature-list">{features}</ul></div>
<figure class="screenshot-figure"><div class="phone-frame"><img src="../assets/{screenshot_file}" width="1206" height="2622" loading="lazy" alt="{c['screenshot_alt']}"></div><figcaption>{screenshot_caption}</figcaption></figure></div></section>
<div class="wrap"><section class="editing" id="editing" aria-labelledby="editing-title"><div class="section-heading"><div><p class="eyebrow">{c['edit_label']}</p><h2 id="editing-title">{c['edit_title']}</h2></div><p>{c['edit_intro']}</p></div><div class="edit-grid">{cards}</div><p class="visual-caption" style="max-width:850px;margin-top:22px">{c['ai_note']}</p></section>
<section class="data-section" id="data" aria-labelledby="data-title"><div class="data-grid"><div><p class="eyebrow">{c['data_label']}</p><h2 id="data-title">{c['data_title']}</h2><p>{c['data_intro']}</p><a class="text-link" href="privacy/">{c['data_link']} ↗</a></div><ul class="data-notes">{notes}</ul></div></section>
<section class="closing" aria-labelledby="closing-title"><div><p class="eyebrow">{c['closing_label']}</p><h2 id="closing-title">{c['closing_title']}</h2><p>{c['closing_body']}</p></div><a class="button" href="support/#contact">{c['closing_cta']}</a></section></div>
</main>'''
    return document(locale, "", c['title'], c['description'], body)


def policy(locale, page):
    c, t = PAGES[locale][page], UI[locale]
    toc = "".join(f'<li><a href="#{key}">{escape(title)}</a></li>' for key, title, _ in c['sections'])
    parts = []
    for key, title, body in c['sections']:
        if body == "__MIT__":
            body = '<pre class="license-text">' + escape((ROOT / "assets/RIFE-LICENSE.txt").read_text()) + '</pre>'
            body += '<p><a href="../../assets/RIFE-LICENSE.txt">' + ('Download the license text' if locale == 'en' else '下载许可文本') + '</a></p>'
        parts.append(f'<section id="{key}"><h2>{escape(title)}</h2>{body}</section>')
    related = ('See also: ' if locale == 'en' else '另见：') + ' · '.join(f'<a href="{link(locale, key, page)}">{t[key]}</a>' for key in PAGES_KEYS if key != page)
    body = f'''<main id="main"><div class="wrap">
<header class="document-header"><p class="eyebrow">{t['name']}</p><h1>{c['title']}</h1><p>{c['intro']}</p><p class="date">{t['updated']} · {UPDATED[locale]}</p></header>
<div class="document-grid"><nav class="toc" aria-label="{t['toc']}"><p>{t['toc']}</p><ol>{toc}</ol></nav><div class="prose">{''.join(parts)}<p class="visual-caption">{related}</p></div></div>
</div></main>'''
    return document(locale, page, c['title'] + ' — ' + t['name'], c['intro'], body)


def entry_page():
    icon = '<link rel="icon" type="image/png" href="assets/app-icon.png"><link rel="apple-touch-icon" href="assets/app-icon.png">' if ICON.exists() else ''
    brand = '<img src="assets/app-icon.png" width="64" height="64" alt="" style="border-radius:16px;margin-bottom:25px">' if ICON.exists() else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Plant Journal · 植物记录</title><meta name="description" content="Plant Journal for iPhone and iPad. 植物记录，留下一段看得见的成长。"><link rel="canonical" href="{BASE}"><link rel="alternate" hreflang="en" href="{url('en')}"><link rel="alternate" hreflang="zh-Hans" href="{url('zh')}"><link rel="alternate" hreflang="x-default" href="{BASE}"><meta name="theme-color" content="#f7f8f1"><link rel="stylesheet" href="assets/site.css">{icon}</head><body><main id="main" class="wrap chooser"><div>{brand}<p class="eyebrow">Plant Journal · 植物记录</p><h1>Slow growth.<br>A story worth keeping.</h1><p lang="zh-Hans">慢慢生长，好好留下。</p><div class="actions"><a class="button" href="en/" lang="en">English</a><a class="button secondary" href="zh/" lang="zh-Hans">简体中文</a></div><p class="visual-caption">iPhone & iPad · Release in preparation / 正在准备发布</p></div></main></body></html>\n'''


def build():
    outputs = {ROOT / "index.html": entry_page()}
    for locale in UI:
        outputs[ROOT / locale / "index.html"] = home(locale)
        for page in PAGES_KEYS:
            outputs[ROOT / locale / page / "index.html"] = policy(locale, page)
    outputs[ROOT / ".nojekyll"] = ""
    outputs[ROOT / "robots.txt"] = f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n"
    urls = [BASE] + [url(locale, page) for locale in UI for page in ("", *PAGES_KEYS)]
    outputs[ROOT / "sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc><lastmod>2026-10-26</lastmod></url>\n' for u in urls) + '</urlset>\n'
    outputs[ROOT / "404.html"] = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Plant Journal</title><meta name="robots" content="noindex">''' + ('<link rel="icon" type="image/png" href="/plant-journal/assets/app-icon.png">' if ICON.exists() else '') + '''<style>body{font:18px/1.7 -apple-system,BlinkMacSystemFont,sans-serif;background:#f7f8f1;color:#17362b;max-width:650px;padding:12vh 24px;margin:auto}a{color:inherit}h1{font-weight:550;letter-spacing:-.04em}</style></head><body><main><p>Plant Journal · 植物记录</p><h1>This page hasn’t taken root.</h1><p lang="zh-Hans">没有找到这个页面。</p><p><a href="/plant-journal/en/">English home</a> · <a href="/plant-journal/zh/" lang="zh-Hans">中文首页</a></p></main></body></html>\n'''
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if checked-in generated files are stale")
    args = parser.parse_args()
    stale = []
    for path, text in build().items():
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    if stale:
        sys.exit("Stale generated files: " + ", ".join(stale))
    print("Static website is current." if args.check else "Built 11 bilingual entry/content pages, 404, sitemap and robots.txt.")
