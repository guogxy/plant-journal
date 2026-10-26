#!/usr/bin/env python3
"""Publication checks: every locale, local URL, anchor, metadata and required notice."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://guogxy.github.io/plant-journal/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.links, self.ids, self.tags = path, [], set(), []
        self.feed(path.read_text())

    def handle_starttag(self, tag, values):
        attrs = dict(values)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"{self.path}: duplicate id {attrs['id']}"
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


errors = []
def require(ok, message):
    if not ok:
        errors.append(message)


subprocess.run([sys.executable, str(ROOT / "tools/build.py"), "--check"], check=True)
pages = {p.resolve(): Page(p) for p in ROOT.rglob("*.html")}
for path, page in pages.items():
    rel = path.relative_to(ROOT)
    for href in page.links:
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc:
            require(parsed.scheme in ("https", "mailto"), f"{rel}: nonsecure/unexpected URL {href}")
            continue
        if parsed.path.startswith("/"):
            require(parsed.path.startswith("/plant-journal/"), f"{rel}: root-relative URL loses repo path {href}")
            target = ROOT / unquote(parsed.path.removeprefix("/plant-journal/"))
        else:
            target = path.parent / unquote(parsed.path)
        if not parsed.path:
            target = path
        if target.is_dir():
            target /= "index.html"
        target = target.resolve()
        require(target.is_relative_to(ROOT), f"{rel}: URL escapes site {href}")
        require(target.exists(), f"{rel}: broken local URL {href}")
        if parsed.fragment and target in pages:
            require(unquote(parsed.fragment) in pages[target].ids, f"{rel}: missing fragment {href}")
    imgs = [a for t, a in page.tags if t == "img"]
    for attrs in imgs:
        require("alt" in attrs, f"{rel}: image has no alt text")
        require("width" in attrs and "height" in attrs, f"{rel}: image has no intrinsic dimensions")
    require(not [1 for t, a in page.tags if t in ("form", "iframe", "script")], f"{rel}: unexpected script/embed/form")
    require(len([1 for t, a in page.tags if t == "h1"]) == 1, f"{rel}: expected one h1")
    require(len([1 for t, a in page.tags if t == "main"]) == 1, f"{rel}: expected one main")
    if rel.parts[0] in ("en", "zh"):
        locale = rel.parts[0]
        suffix = "/".join(rel.parts[:-1]) + "/"
        expected = BASE + suffix
        canonical = [a.get("href") for t, a in page.tags if t == "link" and a.get("rel") == "canonical"]
        require(canonical == [expected], f"{rel}: wrong canonical")
        alternate = {a.get("hreflang"): a.get("href") for t, a in page.tags if t == "link" and a.get("rel") == "alternate"}
        require(set(alternate) == {"en", "zh-Hans", "x-default"}, f"{rel}: incomplete language alternatives")
        require(alternate.get("en") == BASE + "en/" + "/".join(rel.parts[1:-1]) + ("/" if len(rel.parts) > 2 else ""), f"{rel}: wrong English alternative")
        language = [a.get("lang") for t, a in page.tags if t == "html"]
        require(language == ["en" if locale == "en" else "zh-Hans"], f"{rel}: wrong document language")
        require(any(t == "a" and a.get("class") == "language" for t, a in page.tags), f"{rel}: missing language switch")
        require(any(t == "meta" and a.get("name") == "description" and a.get("content") for t, a in page.tags), f"{rel}: no description")
    source = path.read_text()
    for forbidden in ("apps.apple.com/", "APP_STORE_ID", "example.com", "Lorem ipsum", "永不离开设备", "无需账号，原片保存在设备上", "google-analytics", "gtag("):
        require(forbidden not in source, f"{rel}: unexpected placeholder or unverified claim {forbidden}")

expected_pages = {ROOT / locale / page / "index.html" for locale in ("en", "zh") for page in ("", "privacy", "terms", "support", "licenses")}
require(expected_pages.issubset(pages), "Missing required bilingual page")
require((ROOT / ".nojekyll").exists(), "Missing .nojekyll")
sitemap = ET.parse(ROOT / "sitemap.xml")
locations = [node.text for node in sitemap.findall(".//{*}loc")]
require(len(locations) == 11 and all(u.startswith(BASE) for u in locations), "Sitemap does not contain 11 correct URLs")
for locale in ("en", "zh"):
    privacy = (ROOT / locale / "privacy/index.html").read_text()
    require("EXIF" in privacy and "CloudKit" in privacy and "GitHub" in privacy, f"{locale}: incomplete privacy data flows")
    license_page = (ROOT / locale / "licenses/index.html").read_text()
    require("Copyright (c) 2021 hzwer" in license_page and "Unsplash" in license_page, f"{locale}: missing material attribution")

if errors:
    sys.exit("\n".join(errors))
print(f"PASS: {len(pages)} HTML files; internal URLs, fragments, bilingual metadata, notices and deployment path verified.")
