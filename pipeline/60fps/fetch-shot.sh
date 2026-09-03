#!/bin/bash
UA="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
slug="$1"; out="/tmp/60fps/shots/$slug"; mkdir -p "$out"
[ -s "$out/meta.json" ] || curl -s "https://60fps.design/shots/$slug" -H "$UA" > "$out/page.html"
python3 - "$slug" << 'PYEOF'
import re, sys, json, html as H
slug=sys.argv[1]
h=open(f'/tmp/60fps/shots/{slug}/page.html').read()
def og(p):
    m=re.search(rf'<meta property="og:{p}" content="([^"]*)"', h)
    return H.unescape(m.group(1)) if m else None
vids=re.findall(r'<source src="(https://video\.gumlet\.io/[a-z0-9]+/[a-z0-9]+/main\.mp4)"', h)
hero=vids[0] if vids else None
poster=None
m=re.search(r'<video[^>]*poster="([^"]+)"', h)
if m: poster=m.group(1)
meta={'slug':slug,'title':(og('title') or '').replace(' - 60fps UI/UX animation',''),'desc':og('description'),'url':f'https://60fps.design/shots/{slug}','video':hero,'poster':poster}
json.dump(meta, open(f'/tmp/60fps/shots/{slug}/meta.json','w'), indent=1)
print(slug, 'hero:', (hero or 'NONE')[-40:])
PYEOF
[ -s "$out/main.mp4" ] || curl -s "$(python3 -c "import json;print(json.load(open('$out/meta.json'))['video'] or '')")" -o "$out/main.mp4"
n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$out/main.mp4" 2>/dev/null)
[ -z "$n" -o "$n" -lt 9 ] && n=24
step=$(( n / 9 )); [ $step -lt 1 ] && step=1
ffmpeg -y -v error -i "$out/main.mp4" -vf "select='not(mod(n\,$step))',scale=320:-1,tile=3x3" -frames:v 1 "$out/montage.jpg"
echo "$slug montage: $(identify -format '%wx%h' "$out/montage.jpg" 2>/dev/null)"
