import json, struct, urllib.request, concurrent.futures, os

recs = json.load(open('interactions.json'))
urls = sorted({m.get('poster') or m.get('src') for r in recs for m in r['media'] if (m.get('poster') or m.get('src'))})
cache = {}
if os.path.exists('poster-dims.json'):
    cache = json.load(open('poster-dims.json'))
todo = [u for u in urls if u not in cache]
print('total', len(urls), 'cached', len(cache), 'todo', len(todo))

def webp_dims(b):
    if len(b) < 30 or b[:4] != b'RIFF' or b[8:12] != b'WEBP': return None
    kind = b[12:16]
    if kind == b'VP8X':
        w = 1 + int.from_bytes(b[24:27], 'little'); h = 1 + int.from_bytes(b[27:30], 'little'); return (w, h)
    if kind == b'VP8 ':
        w = int.from_bytes(b[26:28], 'little') & 0x3FFF; h = int.from_bytes(b[28:30], 'little') & 0x3FFF; return (w, h)
    if kind == b'VP8L' and b[20] == 0x2f:
        b0, b1, b2, b3 = b[21], b[22], b[23], b[24]
        w = 1 + (((b1 & 0x3F) << 8) | b0); h = 1 + (((b3 & 0xF) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6)); return (w, h)
    return None

def png_dims(b):
    if len(b) >= 24 and b[:8] == b'\x89PNG\r\n\x1a\n':
        w, h = struct.unpack('>II', b[16:24]); return (w, h)

def jpg_dims(b):
    if len(b) < 4 or b[:2] != b'\xff\xd8': return None
    i = 2
    while i + 9 < len(b):
        if b[i] != 0xFF: i += 1; continue
        m = b[i+1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack('>HH', b[i+5:i+9]); return (w, h)
        ln = struct.unpack('>H', b[i+2:i+4])[0]; i += 2 + ln
    return None

def fetch(u):
    try:
        req = urllib.request.Request(u, headers={'Range': 'bytes=0-2047', 'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            b = r.read(2048)
        d = webp_dims(b) or png_dims(b) or jpg_dims(b)
        return u, d
    except Exception:
        return u, None

done = 0
with concurrent.futures.ThreadPoolExecutor(32) as ex:
    for u, d in ex.map(fetch, todo):
        if d: cache[u] = d
        done += 1
        if done % 200 == 0: print('fetched', done, '/', len(todo))
json.dump(cache, open('poster-dims.json', 'w'))
print('dims known:', len(cache))
