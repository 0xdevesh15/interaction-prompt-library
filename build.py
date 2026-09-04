import json, html, os

DIST = '/tmp/insp-site/dist'
recs = json.load(open('/tmp/insp-site/interactions.json'))
E = html.escape

STYLE = r"""
:root{
  --bg:#ffffff; --well:#fafafa; --fill:#f4f4f4; --hover:#f5f5f5;
  --line:rgba(0,0,0,.08); --line-strong:rgba(0,0,0,.14);
  --txt:#09090b; --sec:#52525b; --mut:#a1a1aa;
  --link:#0099ff;
  --mono:ui-monospace,'SF Mono','Cascadia Mono',Menlo,monospace;
  --sans:'InterVariable','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  --radius:12px; --pill:999px;
  --ease:cubic-bezier(.22,.68,.26,1);
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--txt);font:16px/1.65 var(--sans);-webkit-font-smoothing:antialiased;font-feature-settings:'cv02','cv03','cv04','cv11','ss01','ss03';letter-spacing:.001em;isolation:isolate}
@media(min-width:640px){body{font-size:14px}}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline;text-underline-offset:3px}
::selection{background:#09090b;color:#fff}
.wrap{max-width:1200px;margin:0 auto;padding:0 32px}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
header.top{padding:88px 0 40px;animation:rise .5s var(--ease) both}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin-bottom:18px}
h1{font-size:44px;font-weight:600;letter-spacing:-.03em;text-wrap:balance}
.sub{color:var(--sec);margin-top:16px;max-width:58ch;font-size:15px;text-wrap:pretty}
.stats{display:flex;gap:28px;margin-top:28px;color:var(--mut);font-size:13px;font-variant-numeric:tabular-nums}
.stats b{color:var(--txt);font-family:var(--mono);font-weight:500}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:14px 0;position:sticky;top:0;background:rgba(255,255,255,.8);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line);z-index:10}
#q{background:var(--bg);border:1px solid var(--line-strong);color:var(--txt);border-radius:var(--pill);padding:9px 18px;width:300px;font:13px var(--sans);outline:none;transition:border-color .18s var(--ease),box-shadow .18s var(--ease)}
#q::placeholder{color:var(--mut)}
#q:focus{border-color:#09090b;box-shadow:0 0 0 3px rgba(0,0,0,.06)}
.chip{background:var(--bg);border:1px solid var(--line-strong);color:var(--sec);border-radius:var(--pill);padding:6px 14px;font-size:12.5px;cursor:pointer;user-select:none;transition:transform .18s var(--ease),background-color .18s var(--ease),color .18s var(--ease),border-color .18s var(--ease)}
.chip:hover{border-color:#09090b;color:var(--txt)}
.chip.on{color:#fff;background:#09090b;border-color:#09090b}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;padding:36px 0 96px}
.card{display:block;background:var(--bg);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;color:var(--txt);transition:transform .25s var(--ease),box-shadow .25s var(--ease);animation:rise .45s var(--ease) both}
.card:hover{box-shadow:0 0 0 1px rgba(0,0,0,.05),0 2px 8px rgba(0,0,0,.04),0 12px 32px rgba(0,0,0,.06);transform:translateY(-3px);text-decoration:none}
.card:hover img{transform:scale(1.035)}
.card .imgwrap{overflow:hidden;background:var(--fill);aspect-ratio:1.25}
.card img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s var(--ease)}
.card .b{padding:14px 16px 16px}
.card h3{font-size:14px;font-weight:600;letter-spacing:-.01em}
.card .m{color:var(--mut);font-size:12px;margin-top:5px;display:flex;justify-content:space-between}
.cat{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--sec)}
/* detail */
.dhead{padding:64px 0 32px;animation:rise .5s var(--ease) both}
.back{font-size:13px;color:var(--sec)}
.dhead h1{margin-top:20px}
.meta{display:flex;flex-wrap:wrap;gap:10px 20px;margin-top:18px;color:var(--sec);font-size:13px;align-items:center}
.meta b{color:var(--txt);font-weight:600}
.meta .sep{color:var(--line-strong)}
section{padding:36px 0;border-top:1px solid var(--line)}
h2{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.14em;color:var(--mut);margin-bottom:20px;font-weight:500}
.lede{font-size:17px;line-height:1.7;max-width:65ch;letter-spacing:-.005em;text-wrap:pretty}
.duo{display:block}
@media(min-width:1024px){
  .duo{display:flex;gap:48px;align-items:flex-start}
  .duo .main{flex:1;min-width:0}
  .duo .rail{width:400px;flex-shrink:0;position:sticky;top:76px}
}
.duo section{border-top:none;padding:0 0 36px}
.duo section:first-child{padding-top:36px;border-top:1px solid var(--line)}
.rail section:first-child{padding-top:36px}
video.dmedia,img.dmedia{max-width:100%;width:100%;border-radius:var(--radius);background:var(--fill);display:block;outline:1px solid rgba(0,0,0,.05);outline-offset:-1px}
.mrow{display:flex;gap:18px;flex-wrap:wrap}
.phases{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.phase{background:var(--well);border:1px solid var(--line);border-radius:var(--radius);padding:16px}
.phase .p{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;color:var(--link);margin-bottom:8px;text-transform:uppercase}
.phase .d{font-size:13.5px;color:var(--sec);line-height:1.6}
.mech{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px 24px}
.mech .k{font-family:var(--mono);font-size:10.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.12em;margin-bottom:6px}
.mech .v{font-size:14px;line-height:1.55}
.promptwrap{position:relative}
pre.prompt{background:var(--well);border:1px solid var(--line);border-radius:var(--radius);padding:22px 24px;font-family:var(--mono);font-size:13px;line-height:1.7;white-space:pre-wrap;color:#3f3f46;max-height:70vh;overflow:auto}
.copy{position:absolute;top:12px;right:12px;background:#09090b;border:none;color:#fff;border-radius:var(--pill);padding:6px 14px;font:11.5px var(--sans);letter-spacing:.04em;cursor:pointer}
.copy:hover{opacity:.85}
.montage{width:100%;border-radius:var(--radius);outline:1px solid rgba(0,0,0,.05);outline-offset:-1px}
footer{padding:48px 0 72px;color:var(--mut);font-size:13px;border-top:1px solid var(--line)}
@media(max-width:640px){#q{width:100%}h1{font-size:32px}.wrap{padding:0 20px}}
"""
open(f'{DIST}/assets-style.css','w').write(STYLE)

APPJS = """
const R = window.__DATA__;
const grid = document.getElementById('grid');
const q = document.getElementById('q');
let cat = null;
const cats = [...new Set(R.map(r=>r.category))];
const cwrap = document.getElementById('cats');
let src_filter=null;
const swrap=document.getElementById('srcs');
const sources=[...new Set(R.map(r=>r.source))];
sources.forEach(c=>{
  const el=document.createElement('span');el.className='chip';el.textContent=c;
  el.onclick=()=>{src_filter=(src_filter===c?null:c);document.querySelectorAll('#srcs .chip').forEach(x=>x.classList.toggle('on',x.textContent===src_filter));render();};
  swrap.appendChild(el);
});
cats.forEach(c=>{
  const el=document.createElement('span');el.className='chip';el.textContent=c;
  el.onclick=()=>{cat=(cat===c?null:c);document.querySelectorAll('#cats .chip').forEach(x=>x.classList.toggle('on',x.textContent===cat));render();};
  cwrap.appendChild(el);
});
function render(){
  const s=(q.value||'').toLowerCase();
  grid.innerHTML='';
  let n=0, i=0;
  for(const r of R){
    if(cat&&r.category!==cat)continue;
    if(src_filter&&r.source!==src_filter)continue;
    if(s&&!(r.title+' '+r.desc+' '+r.summary+' '+r.prompt).toLowerCase().includes(s))continue;
    n++; i++;
    const thumb=r.media[0]?(r.media[0].poster||r.media[0].montage||r.media[0].src):'';
    const a=document.createElement('a');a.className='card';a.href='i/'+r.slug+'.html';
    a.style.animationDelay=Math.min(i*28,400)+'ms';
    a.innerHTML=`<div class="imgwrap"><img loading="lazy" src="${thumb}" alt=""></div><div class="b"><div class="cat">${r.category}</div><h3></h3><div class="m"><span>${r.author||''}</span><span>${r.media.length} media</span></div></div>`;
    a.querySelector('h3').textContent=r.title;
    grid.appendChild(a);
  }
  document.getElementById('count').textContent=n;
}
q.addEventListener('input',render);render();
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600&display=swap" rel="stylesheet">'

lite = [{k:r[k] for k in ('slug','title','category','desc','author','summary','prompt','source')} | {'media':[{'poster':m.get('poster'),'src':m.get('src'),'montage':m.get('montage')} for m in r['media']]} for r in recs]
index_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>16ms - 2,113 frame-by-frame UI interaction teardowns</title>
<meta name="description" content="A curated library of 2,113 mobile and web interactions, reverse-engineered frame-by-frame into build-ready prompts. Sources: inspora.design and 60fps.design.">
<link rel="canonical" href="https://16ms.vercel.app/">
<link rel="icon" type="image/png" href="icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="16ms">
<meta property="og:title" content="16ms - 2,113 frame-by-frame UI interaction teardowns">
<meta property="og:description" content="A curated library of 2,113 mobile and web interactions, reverse-engineered frame-by-frame into build-ready prompts.">
<meta property="og:url" content="https://16ms.vercel.app/">
<meta property="og:image" content="https://16ms.vercel.app/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="16ms - frame-by-frame interaction teardowns">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="16ms - 2,113 frame-by-frame UI interaction teardowns">
<meta name="twitter:description" content="A curated library of 2,113 mobile and web interactions, reverse-engineered frame-by-frame into build-ready prompts.">
<meta name="twitter:image" content="https://16ms.vercel.app/og-image.png">
{FONTS}<link rel="stylesheet" href="assets-style.css"></head><body>
<div class="wrap"><header class="top">
<div class="eyebrow">16ms &middot; {len(recs)} interactions &middot; inspora.design + 60fps.design</div>
<h1>16<span style="color:#f97316">ms</span></h1>
<p class="sub">Frame-by-frame teardowns of the best interactions on the web, reverse-engineered into build-ready prompts. Sources: <a href="https://www.inspora.design/">inspora.design</a> (80) and <a href="https://60fps.design/">60fps.design</a> (2,033 shots, full teardown). Query it from your AI tool via the <a href="mcp/">MCP server</a>.</p>
<div class="stats"><span><b>{len(recs)}</b> interactions</span><span><b>{sum(len(r['media']) for r in recs)}</b> media teardowns</span><span><b>{len(set(r['category'] for r in recs))}</b> categories</span><span><b>{len(set(r['source'] for r in recs))}</b> sources</span><span><b id="count">{len(recs)}</b> shown</span></div>
</header>
<div class="controls"><input id="q" placeholder="Search interactions, mechanics, prompts..." ><div id="srcs" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px"></div><div id="cats" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px"></div></div>
<div class="grid" id="grid"></div>
<footer>Built from full teardowns of inspora.design (80 posts, Sep 2026 snapshot) and 60fps.design (2,033 shots, full teardown, Sep 2026). Every record: summary, montage, mechanics, and a build prompt.</footer>
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
            media_html += f'<img class="dmedia" src="{E(m.get("src") or m.get("poster",""))}" alt="">'
    montages = ''.join(f'<img class="montage" src="../{E(m["montage"])}" alt="">' for m in r['media'] if m.get('montage'))
    pub = (r.get('published') or '')[:10]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(r['title'])} - 16ms</title>
<meta name="description" content="{E(r.get('desc') or r.get('summary') or '')}">
<link rel="canonical" href="https://16ms.vercel.app/i/{E(r['slug'])}.html">
<link rel="icon" type="image/png" href="../icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="16ms">
<meta property="og:title" content="{E(r['title'])} - 16ms">
<meta property="og:description" content="{E(r.get('desc') or r.get('summary') or '')}">
<meta property="og:url" content="https://16ms.vercel.app/i/{E(r['slug'])}.html">
<meta property="og:image" content="https://16ms.vercel.app/{E(r['media'][0].get('montage') or '')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(r['title'])} - 16ms">
<meta name="twitter:description" content="{E(r.get('desc') or r.get('summary') or '')}">
<meta name="twitter:image" content="https://16ms.vercel.app/{E(r['media'][0].get('montage') or '')}">
{FONTS}<link rel="stylesheet" href="../assets-style.css"></head><body>
<div class="wrap">
<div class="dhead"><a class="back" href="../index.html">&larr; All interactions</a>
<h1>{E(r['title'])}</h1>
<div class="meta"><span class="cat">{E(r['category'] or '')}</span><span class="sep">&middot;</span><span>by <a href="{E(r.get('authorUrl') or '#')}"><b>{E(r.get('author') or 'unknown')}</b></a></span><span class="sep">&middot;</span><span>{pub}</span><span class="sep">&middot;</span><span><a href="{E(r['pageUrl'])}">{E(r['source'])} page</a></span><span class="sep">&middot;</span><span><a href="{E(r.get('originalUrl') or '#')}">original post</a></span></div>
</div>
<section><h2>What it is</h2><p class="lede">{E(r.get('summary') or '')}</p></section>
<div class="duo">
<div class="main">
<section><h2>Media</h2><div class="mrow">{media_html}</div></section>
<section><h2>Frame-by-frame</h2><div class="mrow" style="margin-bottom:20px">{montages}</div><div class="phases">{phases}</div></section>
</div>
<div class="rail">
<section><h2>Build prompt</h2><div class="promptwrap"><pre class="prompt"><button class="copy" onclick="navigator.clipboard.writeText(this.parentElement.dataset.p);this.textContent='Copied'">Copy</button>{E(r.get('prompt') or '')}</pre></div></section>
<section><h2>Mechanics</h2><div class="mech">{mech_html}</div></section>
</div>
</div>
<footer>Source: {E(r['source'])}.design - <a href="{E(r['pageUrl'])}">original interaction</a> by {E(r.get('author') or '')}. Teardown snapshot Sep 2026.</footer>
</div>
<script>document.querySelector('.prompt').dataset.p={json.dumps(r.get('prompt') or '')}</script>
</body></html>"""
    open(f'{DIST}/i/{r["slug"]}.html','w').write(page)

os.makedirs(f'{DIST}/mcp', exist_ok=True)
mcp_page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCP server - 16ms</title>
<meta name="description" content="Query the 16ms interaction library from Cursor, Claude Code, or Claude Desktop via the MCP server.">
<link rel="canonical" href="https://16ms.vercel.app/mcp/">
<link rel="icon" type="image/png" href="../icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="16ms">
<meta property="og:title" content="MCP server - 16ms">
<meta property="og:description" content="Query the 16ms interaction library from your AI tool.">
<meta property="og:url" content="https://16ms.vercel.app/mcp/">
<meta property="og:image" content="https://16ms.vercel.app/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://16ms.vercel.app/og-image.png">
{FONTS}<link rel="stylesheet" href="../assets-style.css"></head><body>
<div class="wrap"><header class="top">
<div class="eyebrow">16ms &middot; MCP server</div>
<h1>Query the library from your AI tool.</h1>
<p class="sub">The 16ms MCP server exposes all {len(recs)} interaction teardowns - search, browse, and pull full build prompts - directly inside Cursor, Claude Code, or Claude Desktop. It runs locally over stdio: Node 18+, zero dependencies, one file.</p>
</header>
<section><h2>1. Get the code</h2>
<div class="promptwrap"><pre class="prompt">git clone https://github.com/0xdevesh15/interaction-prompt-library.git</pre></div>
<p class="sub" style="margin-top:14px">The server is <b>mcp/server.js</b>. It reads the bundled dataset (<b>dist/interactions.json</b>) - nothing to install, no API keys.</p></section>
<section><h2>2. Connect your tool</h2>
<p class="sub" style="margin-bottom:18px">Replace <b>/ABS/PATH/TO</b> with where you cloned the repo.</p>
<p class="lede" style="margin-bottom:10px"><b>Cursor</b> - add to <b>~/.cursor/mcp.json</b>:</p>
<div class="promptwrap"><pre class="prompt">{{
  "mcpServers": {{
    "interaction-prompt-library": {{
      "command": "node",
      "args": ["/ABS/PATH/TO/interaction-prompt-library/mcp/server.js"]
    }}
  }}
}}</pre></div>
<p class="lede" style="margin:22px 0 10px"><b>Claude Code</b> - one command:</p>
<div class="promptwrap"><pre class="prompt">claude mcp add interaction-prompt-library -- node /ABS/PATH/TO/interaction-prompt-library/mcp/server.js</pre></div>
<p class="lede" style="margin:22px 0 10px"><b>Claude Desktop</b> - add to <b>claude_desktop_config.json</b> (same JSON as Cursor), then restart the app.</p></section>
<section><h2>3. Tools you get</h2>
<div class="phases">
<div class="phase"><div class="p">search_interactions</div><div class="d">Full-text search over titles, summaries, mechanics, and prompts. "show me toggle switches", "scroll stack", "glass refraction".</div></div>
<div class="phase"><div class="p">get_interaction_prompt</div><div class="d">The full teardown for one interaction: summary, frame-by-frame phases, mechanics (trigger, timing, easing), and the build-ready prompt.</div></div>
<div class="phase"><div class="p">list_interactions</div><div class="d">Browse everything, optionally filtered by category (Motion, Product, Web...) or source (inspora, 60fps).</div></div>
</div></section>
<section><h2>Try it</h2>
<p class="lede">Ask your tool: <i>"search the interaction library for a pull to refresh animation and give me the build prompt"</i> - it calls the MCP tools and hands you a prompt you can build from.</p></section>
<footer>The dataset ships with the repo, so the server works fully offline. Set IPL_DATA=/path/to/interactions.json to point at another copy.</footer>
</div>
</body></html>"""
open(f'{DIST}/mcp/index.html','w').write(mcp_page)

print('built', len(recs), 'pages')
