# 60fps.design full-teardown slice manifest (batch 2+)

1976 remaining shots, 7 disjoint slices of ~283 slugs (sitemap order; all 27 visible
featured shots already landed in batch 1 - the full featured list is PRO-gated).

Each worker agent takes ONE slice file (slice-00 .. slice-06) and:

1. For every slug: run `pipeline/60fps/fetch-shot.sh <slug>` (idempotent; downloads
   page HTML, hero mp4 = FIRST gumlet main.mp4 in DOM order, builds montage.jpg).
   NOTE: og:image is 60fps's brand gif - never use it as the shot media.
2. Watch the montage + page meta, then write a v3 prompt to `prompts/<slug>.md`
   (format: Goal paragraph / ## Integration one-liner / ## Scene / ## Motion spec /
   ## Calibration / ## Reduced motion / ## Don't miss; exact values, no adjectives;
   see any existing file in pipeline/60fps/prompts/ for the reference shape).
3. Produce ONE records JSON for the slice using `gen-records.py`-compatible schema:
   id "60fps:<slug>", source "60fps", slug, title, category (Interaction if
   -interaction suffix else Animation), desc, author (app name), authorUrl, published,
   originalUrl, pageUrl (https://60fps.design/shots/<slug>), media
   [{poster, src, type: video, montage}], summary (first prompt paragraph),
   frames [], mechanics {Pattern, Content type, Source}, prompt (full md).
4. Return the records JSON + montages to the coordinator. Do NOT merge into
   interactions.json, do NOT push to the repo, do NOT deploy - the coordinator
   (main 60fps task agent) is the sole merger/rebuilder/deployer.
