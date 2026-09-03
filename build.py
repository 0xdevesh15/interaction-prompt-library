import json, html, os

DIST = '/tmp/insp-site/dist'
recs = json.load(open('/tmp/insp-site/interactions.json'))
E = html.escape

STYLE = """
:root{--bg:#0a0a0b;--panel:#131315;--line:#26262a;--txt:#ececee;--mut:#8b8b93;--acc:#7c8cff;--mono:ui-monospace,'SF Mono',Menlo,monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:15px/1.6 -apple-system,'Inter',Segoe UI,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
header.top{padding:56px 0 28px;border-bottom:1px solid var(--line)}
h1{font-size:34px;letter-spacing:-.02em}
.sub{color:var(--mut);margin-top:8px;max-width:640px}
.stats{display:flex;gap:24px;margin-top:20px;color:var(--mut);font-size:13px}
.stats b{color:var(--txt);font-family:var(--mono)}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding:20px 0;position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);z-index:5}
#q{background:var(--panel);border:1px solid var(--line);color:var(--txt);border-radius:10px;padding:9px 14px;width:280px;font-size:14px;outline:none}
#q:focus{border-color:var(--acc)}
.chip{background:var(--panel);border:1px solid var(--line);color:var(--mut);border-radius:999px;padding:5px 13px;font-size:12.5px;cursor:pointer;user-select:none}
.chip.on{color:#0a0a0b;background:var(--txt);border-color:var(--txt)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;padding:28px 0 80px}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;color:var(--txt)}
.card:hover{border-color:#3a3a40;text-decoration:none;transform:translateY(-2px);transition:transform .15s}
.card img{width:100%;aspect-ratio:1.2;object-fit:cover;display:block;background:#000}
.card .b{padding:12px 14px}
.card h3{font-size:14px;font-weight:600;letter-spacing:-.01em}
.card .m{color:var(--mut);font-size:12px;margin-top:4px;display:flex;justify-content:space-between}
.cat{font-family:var(--mono);font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--acc)}
/* detail */
.dhead{padding:44px 0 24px;border-bottom:1px solid var(--line)}
.back{font-size:13px;color:var(--mut)}
.dhead h1{margin-top:14px}
.meta{display:flex;flex-wrap:wrap;gap:18px;margin-top:14px;color:var(--mut);font-size:13px}
.meta b{color:var(--txt);font-weight:600}
section{padding:30px 0;border-bottom:1px solid var(--line)}
h2{font-size:13px;font-family:var(--mono);text-transform:uppercase;letter-spacing:.08em;color:var(--mut);margin-bottom:16px}
.lede{font-size:16.5px;max-width:760px}
video.dmedia,img.dmedia{max-width:520px;width:100%;border-radius:12px;border:1px solid var(--line);background:#000;display:block}
.mrow{display:flex;gap:16px;flex-wrap:wrap}
.phases{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.phase{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px}
.phase .p{font-family:var(--mono);font-size:11px;color:var(--acc);margin-bottom:6px}
.phase .d{font-size:13.5px;color:#c9c9cf}
.mech{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.mech .k{font-family:var(--mono);font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.mech .v{font-size:14px}
pre.prompt{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;font-family:var(--mono);font-size:13px;line-height:1.65;white-space:pre-wrap;color:#d8d8de;position:relative}
.copy{position:absolute;top:10px;right:10px;background:#26262a;border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:4px 10px;font-size:12px;cursor:pointer}
.copy:hover{background:#333}
.montage{width:100%;border-radius:12px;border:1px solid var(--line)}
footer{padding:40px 0 60px;color:var(--mut);font-size:13px}
@media(max-width:640px){#q{width:100%}}
"""
open(f'{DIST}/assets-style.css','w').write(STYLE)

APPJS = """
const R = window.__DATA__;
const grid = document.getElementById('grid');
const q = document.getElementById('q');
let cat = null;
const cats = [...new Set(R.map(r=>r.category))];
const cwrap = document.getElementById('cats');
cats.forEach(c=>{
  const el=document.createElement('span');el.className='chip';el.textContent=c;
  el.onclick=()=>{cat=(cat===c?null:c);document.querySelectorAll('#cats .chip').forEach(x=>x.classList.toggle('on',x.textContent===cat));render();};
  cwrap.appendChild(el);
});
function render(){
  const s=(q.value||'').toLowerCase();
  grid.innerHTML='';
  let n=0;
  for(const r of R){
    if(cat&&r.category!==cat)continue;
    if(s&&!(r.title+' '+r.desc+' '+r.summary+' '+r.prompt).toLowerCase().includes(s))continue;
    n++;
    const thumb=r.media[0]?(r.media[0].poster||r.media[0].montage||r.media[0].src):'';
    const a=document.createElement('a');a.className='card';a.href='i/'+r.slug+'.html';
    a.innerHTML=`<img loading="lazy" src="${thumb}" alt=""><div class="b"><div class="cat">${r.category}</div><h3></h3><div class="m"><span>${r.author||''}</span><span>${r.media.length} media</span></div></div>`;
    a.querySelector('h3').textContent=r.title;
    grid.appendChild(a);
  }
  document.getElementById('count').textContent=n;
}
q.addEventListener('input',render);render();
"""

# embed compact data for client-side search
lite = [{k:r[k] for k in ('slug','title','category','desc','author','summary','prompt')} | {'media':[{'poster':m.get('poster'),'src':m.get('src'),'montage':m.get('montage')} for m in r['media']]} for r in recs]
index_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Interaction Prompt Library</title><link rel="stylesheet" href="assets-style.css"></head><body>
<div class="wrap"><header class="top">
<h1>Interaction Prompt Library</h1>
<p class="sub">Frame-by-frame teardowns of the best interactions on the web, reverse-engineered into build-ready prompts. Source #1: <a href="https://www.inspora.design/">inspora.design</a>. Query it from your AI tool via the MCP server.</p>
<div class="stats"><span><b>{len(recs)}</b> interactions</span><span><b>{sum(len(r['media']) for r in recs)}</b> media teardowns</span><span><b>{len(set(r['category'] for r in recs))}</b> categories</span><span><b id="count">{len(recs)}</b> shown</span></div>
</header>
<div class="controls"><input id="q" placeholder="Search interactions, mechanics, prompts..." ><div id="cats" style="display:flex;gap:8px;flex-wrap:wrap"></div></div>
<div class="grid" id="grid"></div>
<footer>Built from a full teardown of inspora.design (80 posts, Sep 2026 snapshot). 60fps.design teardown coming as source #2. Every record: summary, frame-by-frame phases, mechanics, and a build prompt.</footer>
</div>
<script>window.__DATA__={json.dumps(lite)}</script><script>{APPJS}</script>
</body></html>"""
open(f'{DIST}/index.html','w').write(index_html)

os.makedirs(f'{DIST}/i', exist_ok=True)
for r in recs:
    mech = r.get('mechanics') or {}
    mech_html = ''.join(f'<div><div class="k">{E(str(k))}</div><div class="v">{E(", ".join(v) if isinstance(v,list) else str(v))}</div></div>' for k,v in mech.items() if v)
    phases = ''.join(f'<div class="phase"><div class="p">{E(f.get("phase",""))}</div><div class="d">{E(f.get("desc",""))}</div></div>' for f in (r.get('frames') or []))
    media_html = ''
    for m in r['media']:
        if m.get('type') == 'video':
            media_html += f'<video class="dmedia" src="{E(m["src"])}" poster="{E(m.get("poster",""))}" autoplay loop muted playsinline controls></video>'
        else:
            media_html += f'<img class="dmedia" src="{E(m.get("src") or m.get("poster",""))}">'
    montages = ''.join(f'<img class="montage" src="../{E(m["montage"])}">' for m in r['media'] if m.get('montage'))
    pub = (r.get('published') or '')[:10]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(r['title'])} - Interaction Prompt Library</title><link rel="stylesheet" href="../assets-style.css"></head><body>
<div class="wrap">
<div class="dhead"><a class="back" href="../index.html">&larr; all interactions</a>
<h1>{E(r['title'])}</h1>
<div class="meta"><span class="cat">{E(r['category'] or '')}</span><span>by <a href="{E(r.get('authorUrl') or '#')}"><b>{E(r.get('author') or 'unknown')}</b></a></span><span>{pub}</span><span><a href="{E(r['pageUrl'])}">inspora page</a></span><span><a href="{E(r.get('originalUrl') or '#')}">original post</a></span></div>
</div>
<section><h2>What it is</h2><p class="lede">{E(r.get('summary') or '')}</p></section>
<section><h2>Media</h2><div class="mrow">{media_html}</div></section>
<section><h2>Frame-by-frame</h2><div class="mrow" style="margin-bottom:16px">{montages}</div><div class="phases">{phases}</div></section>
<section><h2>Mechanics</h2><div class="mech">{mech_html}</div></section>
<section><h2>Build prompt</h2><pre class="prompt"><button class="copy" onclick="navigator.clipboard.writeText(this.parentElement.dataset.p);this.textContent='copied'">copy</button>{E(r.get('prompt') or '')}</pre></section>
<footer>Source: inspora.design - <a href="{E(r['pageUrl'])}">original interaction</a> by {E(r.get('author') or '')}. Teardown snapshot Sep 2026.</footer>
</div>
<script>document.querySelector('.prompt').dataset.p={json.dumps(r.get('prompt') or '')}</script>
</body></html>"""
    open(f'{DIST}/i/{r["slug"]}.html','w').write(page)
print('built', len(recs), 'pages')
