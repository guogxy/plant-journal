# Plant Journal / 植物记录 — official website

Complete, buildless Chinese and English static website. Generated HTML is checked in and can be deployed directly from this folder to GitHub Pages. No Node packages, cookies, analytics, external fonts, hosted form, or server are needed. Python tools run locally during authoring only.

Canonical deployment: **https://guogxy.github.io/plant-journal/**

## Author and verify

```sh
python3 Website/tools/build.py
python3 Website/tools/check.py
python3 Website/tools/serve.py --port 8767
```

Preview `http://127.0.0.1:8767/plant-journal/`. Stop the owned preview process after review. Copy for pages lives in `tools/content.py`; layout/metadata in `tools/build.py`; styling in `assets/site.css`. All generated URLs work under the repository subpath. Each language is a complete document with its own canonical URL, language switching, and hreflang.

Publish **this folder’s contents**, not the parent native app repository. The deployment root must include `.nojekyll`, `index.html`, `assets/`, `en/`, and `zh/`. No build command is necessary in GitHub Pages after upload. `tools/` and this README are authoring resources and can be excluded from a deployed artifact. Keep license text assets in the deployment.

## Native app URLs

| Page | English | 简体中文 |
| --- | --- | --- |
| Home | `/plant-journal/en/` | `/plant-journal/zh/` |
| Privacy | `/plant-journal/en/privacy/` | `/plant-journal/zh/privacy/` |
| Terms | `/plant-journal/en/terms/` | `/plant-journal/zh/terms/` |
| Support | `/plant-journal/en/support/` | `/plant-journal/zh/support/` |
| Licenses | `/plant-journal/en/licenses/` | `/plant-journal/zh/licenses/` |

## Release and icon status

Website copy truthfully states that the app is in preparation. No App Store ID, purchase offer, price, review, customer result, or release date is assumed. Add the real download URL only after it is supplied and verified.

The user-approved simple production icon is installed at **`assets/app-icon.png`** and is used by each localized page header, favicon, and Apple touch icon. It is an exact copy of `design/icon-review/plant-journal-simple-v1.png`, with SHA-256 `4dc20207acaa8f5a7eb5148633f206278be1003aa5451ca9c3f157e75d4193fd`. The builder includes these icon references when the file exists. Use only the approved production asset for subsequent updates.

The English page currently displays the actual Chinese development screenshot, explicitly labeled. When an equivalent real English screenshot is available, copy it to **`assets/reference-screen-en.png`** and regenerate; the builder selects it for the English page and updates the caption. The current screenshot dimensions are 1206 × 2622; update the dimensions in the generator if the replacement differs. Neither the screenshot nor bundled sample imagery is described as a user’s genuine growth result.

## Content verification, 2026-10-26

App-specific data flows were checked against `README.md`, `PrivacyInfo.xcprivacy`, local photo storage, `CloudBackupService.swift`, `MODEL-PROVENANCE.md`, `RIFE-LICENSE.txt`, and `Resources/SOURCES.md`. The public support mailbox `gggxxxyyyy@gmail.com` is reused from the owner’s existing AeroWisp website. No company name, postal address, or App Store identity was invented.

Key disclosures: original files retain possible EXIF metadata; local processing; explicitly chosen export destinations; optional/default-off private CloudKit backup with foreground execution, user iCloud quota, non-merge recovery, snapshot retention and old-media cleanup limits; disabling versus deleting backups; independent Calendar/Reminders copies; support email; GitHub hosting logs. The website does not make an unverified App Store “Data Not Collected” questionnaire determination.

Primary references checked while preparing original app-specific policies:

- [Apple App Review Guidelines, privacy 5.1.1](https://developer.apple.com/app-store/review/guidelines/#privacy)
- [Apple App privacy details](https://developer.apple.com/app-store/app-privacy-details/)
- [Apple Standard EULA](https://www.apple.com/legal/internet-services/itunes/dev/stdeula/)
- [Apple Privacy Policy](https://www.apple.com/legal/privacy/)
- [GitHub General Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)
- [Unsplash License](https://unsplash.com/license)

Keep these policies and the App Store privacy answers accurate when shipping behavior changes. The product policies are editable source, not a substitute for the developer’s App Store submission review.
