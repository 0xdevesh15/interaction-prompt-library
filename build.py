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
const R=window.__DATA__;
const wall=document.getElementById('wall');
const q=document.getElementById('q');
let cat=null,srcf=null;
const counts={};R.forEach(r=>counts[r.category]=(counts[r.category]||0)+1);
const cats=Object.keys(counts).filter(c=>counts[c]>=5).sort((a,b)=>counts[b]-counts[a]);
const sources=[...new Set(R.map(r=>r.source))];
const cwrap=document.getElementById('btabs');
function addTab(label){
  const b=document.createElement('button');b.className='btab'+(label===null?' on':'');b.textContent=label||'All';
  b.onclick=()=>{cat=(label===null||cat===label)?null:label;
    cwrap.querySelectorAll('.btab').forEach(x=>x.classList.toggle('on',x.textContent===(cat||'All')));render();};
  cwrap.appendChild(b);
}
addTab(null);cats.forEach(addTab);
const swrap=document.getElementById('stabs');
function addSrc(label){
  const b=document.createElement('button');b.className='stab'+(label===null?' on':'');b.textContent=label||'All sources';
  b.onclick=()=>{srcf=(label===null||srcf===label)?null:label;
    swrap.querySelectorAll('.stab').forEach(x=>x.classList.toggle('on',x.textContent===(srcf||'All sources')));render();};
  swrap.appendChild(b);
}
addSrc(null);sources.forEach(addSrc);
const LAYERS='<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 8l10 6 10-6-10-6z"/><path d="m2 14 10 6 10-6"/></svg>';
function render(){
  const s=(q.value||'').toLowerCase();
  wall.innerHTML='';let n=0;
  const frag=document.createDocumentFragment();
  for(const r of R){
    if(cat&&r.category!==cat)continue;
    if(srcf&&r.source!==srcf)continue;
    if(s&&!(r.title+' '+r.desc+' '+r.summary+' '+r.prompt).toLowerCase().includes(s))continue;
    n++;
    const m=r.media[0]||{};
    const thumb=m.poster||m.src||m.montage||'';
    const a=document.createElement('a');a.className='mcard';a.href='i/'+r.slug+'.html';
    const dim=r.dims;
    const dimAttr=(dim&&dim[0]&&dim[1])?` width="${dim[0]}" height="${dim[1]}"`:'';
    a.innerHTML=`<img loading="lazy" src="${thumb}"${dimAttr} alt="">`+
      (r.media.length>1?`<span class="mcount">${LAYERS}${r.media.length}</span>`:'')+
      `<span class="mover"><span class="mt"></span><span class="mm">${r.category} &middot; ${r.author||r.source}</span></span>`;
    a.querySelector('.mt').textContent=r.title;
    frag.appendChild(a);
  }
  wall.appendChild(frag);
  document.getElementById('count').textContent=n.toLocaleString();
}
q.addEventListener('input',render);
function onScroll(){document.body.classList.toggle('scrolled',window.scrollY>240)}
addEventListener('scroll',onScroll,{passive:true});onScroll();
q.readOnly=true;
q.style.cursor='pointer';
q.addEventListener('focus',()=>{q.blur();window.__cmdk&&window.__cmdk.open();});
q.addEventListener('click',()=>{window.__cmdk&&window.__cmdk.open();});
document.addEventListener('keydown',e=>{
  if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();window.__cmdk&&window.__cmdk.toggle();}
  else if(e.key==='/'&&document.activeElement!==q){e.preventDefault();window.__cmdk&&window.__cmdk.open();}
});
render();
"""



FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600&display=swap" rel="stylesheet">'

DIMS = json.load(open('/tmp/insp-site/poster-dims.json')) if os.path.exists('/tmp/insp-site/poster-dims.json') else {}

PALETTE_CSS = r"""
<style>
.ck-overlay{position:fixed;inset:0;z-index:100;background:rgba(9,9,11,.3);backdrop-filter:blur(10px) saturate(1.1);-webkit-backdrop-filter:blur(10px) saturate(1.1);display:flex;justify-content:center;align-items:flex-start;padding:14vh 16px 16px;opacity:0;transition:opacity .18s var(--ease)}
.ck-overlay.on{opacity:1}
.ck-modal{width:100%;max-width:580px;background:#fff;border-radius:16px;box-shadow:0 24px 70px rgba(0,0,0,.22),0 4px 16px rgba(0,0,0,.08),0 0 0 1px rgba(0,0,0,.06);overflow:hidden;transform:translateY(10px) scale(.985);transition:transform .2s var(--ease)}
.ck-overlay.on .ck-modal{transform:none}
.ck-inputrow{display:flex;align-items:center;gap:11px;padding:15px 18px;border-bottom:1px solid rgba(0,0,0,.07)}
.ck-inputrow svg{flex:none;color:var(--mut)}
.ck-input{flex:1;min-width:0;border:0;outline:none;background:none;font:15px var(--sans);color:var(--txt);letter-spacing:.001em}
.ck-input::placeholder{color:var(--mut)}
.ck-esc{flex:none;font:500 11px var(--mono);color:var(--mut);background:var(--fill);border:1px solid var(--line);border-radius:6px;padding:3px 7px}
.ck-list{max-height:min(400px,52vh);overflow-y:auto;padding:8px;overscroll-behavior:contain}
.ck-group{font:500 10.5px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:8px 12px 5px}
.ck-row{display:flex;align-items:center;gap:12px;padding:9px 12px;border-radius:10px;cursor:pointer}
.ck-row.sel{background:var(--fill)}
.ck-rt{flex:1;min-width:0;font-size:14px;font-weight:500;letter-spacing:-.005em;color:var(--txt);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ck-rm{flex:none;font:11.5px var(--mono);color:var(--mut)}
.ck-row.sel .ck-rm{color:var(--sec)}
.ck-empty{padding:34px 20px;text-align:center;font-size:13.5px;color:var(--mut)}
.ck-empty b{color:var(--sec);font-weight:500}
.ck-foot{display:flex;align-items:center;gap:18px;padding:10px 18px;border-top:1px solid rgba(0,0,0,.07);background:var(--well)}
.ck-hint{display:flex;align-items:center;gap:6px;font-size:11.5px;color:var(--mut)}
.ck-hint kbd{font:500 10.5px var(--mono);color:var(--sec);background:#fff;border:1px solid var(--line-strong);border-bottom-width:2px;border-radius:5px;padding:2px 5px;min-width:19px;text-align:center}
.ck-total{margin-left:auto;font:11px var(--mono);color:var(--mut);font-variant-numeric:tabular-nums}
@media(max-width:640px){.ck-overlay{padding:10vh 10px 10px}.ck-input{font-size:16px}.ck-hint{display:none}.ck-hint:first-child{display:flex}}
</style>
"""

PALETTE_JS = r"""
(function(){
  var PREFIX = window.__CMDK_PREFIX__ || '';
  var overlay=null, input=null, list=null, totalEl=null;
  var DATA=null, results=[], sel=0, isOpen=false;

  function loadData(cb){
    if(DATA){cb();return}
    if(window.__DATA__){
      DATA=window.__DATA__.map(function(r){return{slug:r.slug,title:r.title,category:r.category,source:r.source,author:r.author}});
      cb();return;
    }
    fetch(PREFIX+'search-index.json').then(function(r){return r.json()}).then(function(d){DATA=d;cb()}).catch(function(){DATA=[];cb()});
  }

  function fuzz(q,t){
    q=q.toLowerCase().replace(/\s+/g,'');t=t.toLowerCase();
    var qi=0,score=0,last=-2;
    for(var i=0;i<t.length&&qi<q.length;i++){
      if(t[i]===q[qi]){
        score+=(last===i-1?4:1)+((i===0||/[\s\-_\u00b7]/.test(t[i-1]))?3:0);
        last=i;qi++;
      }
    }
    if(qi<q.length)return -1;
    return score-Math.min(t.length,200)*0.01;
  }

  function search(q){
    if(!DATA)return [];
    if(!q){
      return DATA.slice(0,8);
    }
    var scored=[];
    for(var i=0;i<DATA.length;i++){
      var r=DATA[i];
      var s=fuzz(q,r.title);
      if(s<0){var s2=fuzz(q,r.title+' '+(r.category||'')+' '+(r.author||'')+' '+(r.source||''));if(s2>=0)s=s2*0.5;}
      if(s>=0)scored.push([s,r]);
    }
    scored.sort(function(a,b){return b[0]-a[0]});
    return scored.slice(0,50).map(function(x){return x[1]});
  }

  function render(){
    var q=input.value.trim();
    results=search(q);
    if(sel>=results.length)sel=0;
    var h='';
    if(results.length){
      h+='<div class="ck-group">'+(q?'Results':'Suggestions')+'</div>';
      for(var i=0;i<results.length;i++){
        var r=results[i];
        h+='<div class="ck-row'+(i===sel?' sel':'')+'" data-i="'+i+'" role="option" aria-selected="'+(i===sel)+'">'
          +'<span class="ck-rt"></span>'
          +'<span class="ck-rm"></span></div>';
      }
    } else {
      h='<div class="ck-empty">No results for <b></b></div>';
    }
    list.innerHTML=h;
    var rows=list.querySelectorAll('.ck-row');
    for(var i=0;i<rows.length;i++){
      (function(row,i){
        row.querySelector('.ck-rt').textContent=results[i].title;
        row.querySelector('.ck-rm').textContent=(results[i].category||'')+(results[i].source?' \u00b7 '+results[i].source:'');
        row.addEventListener('mouseenter',function(){sel=i;paint()});
        row.addEventListener('click',function(){openSel()});
      })(rows[i],i);
    }
    if(!results.length){
      var b=list.querySelector('.ck-empty b');if(b)b.textContent='"'+q+'"';
    }
    totalEl.textContent=(q?results.length+' of ':'')+DATA.length.toLocaleString()+' interactions';
  }

  function paint(){
    var rows=list.querySelectorAll('.ck-row');
    for(var i=0;i<rows.length;i++){
      rows[i].classList.toggle('sel',i===sel);
      rows[i].setAttribute('aria-selected',i===sel?'true':'false');
    }
    var s=list.querySelector('.ck-row.sel');
    if(s)s.scrollIntoView({block:'nearest'});
  }

  function openSel(){
    var r=results[sel];
    if(r)location.href=PREFIX+'i/'+r.slug+'.html';
  }

  function build(){
    overlay=document.createElement('div');
    overlay.className='ck-overlay';
    overlay.innerHTML='<div class="ck-modal" role="dialog" aria-modal="true" aria-label="Search interactions">'
      +'<div class="ck-inputrow">'
      +'<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="4.75" stroke="currentColor" stroke-width="1.5"/><path d="m10.75 10.75 3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
      +'<input class="ck-input" type="text" placeholder="Search interactions\u2026" aria-label="Search interactions" autocomplete="off" spellcheck="false">'
      +'<kbd class="ck-esc">esc</kbd></div>'
      +'<div class="ck-list" role="listbox"></div>'
      +'<div class="ck-foot">'
      +'<span class="ck-hint"><kbd>\u2191</kbd><kbd>\u2193</kbd>Navigate</span>'
      +'<span class="ck-hint"><kbd>\u21b5</kbd>Open</span>'
      +'<span class="ck-hint"><kbd>esc</kbd>Close</span>'
      +'<span class="ck-total"></span>'
      +'</div></div>';
    document.body.appendChild(overlay);
    input=overlay.querySelector('.ck-input');
    list=overlay.querySelector('.ck-list');
    totalEl=overlay.querySelector('.ck-total');
    overlay.addEventListener('mousedown',function(e){if(e.target===overlay)close()});
    input.addEventListener('input',function(){sel=0;render()});
    input.addEventListener('keydown',function(e){
      if(e.key==='ArrowDown'){e.preventDefault();sel=Math.min(sel+1,results.length-1);paint()}
      else if(e.key==='ArrowUp'){e.preventDefault();sel=Math.max(sel-1,0);paint()}
      else if(e.key==='Enter'){e.preventDefault();openSel()}
      else if(e.key==='Escape'){e.preventDefault();close()}
    });
  }

  function open(){
    if(isOpen)return;
    if(!overlay)build();
    isOpen=true;
    document.body.style.overflow='hidden';
    overlay.style.display='flex';
    requestAnimationFrame(function(){overlay.classList.add('on')});
    input.value='';sel=0;
    loadData(render);
    input.focus();
  }
  function close(){
    if(!isOpen)return;
    isOpen=false;
    overlay.classList.remove('on');
    document.body.style.overflow='';
    setTimeout(function(){if(!isOpen)overlay.style.display='none'},200);
  }
  function toggle(){isOpen?close():open()}

  document.addEventListener('keydown',function(e){
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();toggle()}
    else if(e.key==='Escape'&&isOpen){close()}
  });

  window.__cmdk={open:open,close:close,toggle:toggle};
})();
"""

def cmdk_tags(prefix):
    return PALETTE_CSS + f'<script>window.__CMDK_PREFIX__={json.dumps(prefix)}</script><script>{PALETTE_JS}</script>'

lite = []
for r in recs:
    m0 = r['media'][0] if r['media'] else {}
    d = DIMS.get(m0.get('poster') or m0.get('src') or '')
    lite.append({k:r[k] for k in ('slug','title','category','desc','author','summary','prompt','source')} | {'media':[{'poster':m.get('poster'),'src':m.get('src'),'montage':m.get('montage')} for m in r['media']], 'dims': d})
json.dump([{k:r[k] for k in ('slug','title','category','source','author')} for r in recs], open(f'{DIST}/search-index.json','w'), separators=(',',':'))
BENTO_STYLE = """
<style>
.bbar{position:fixed;top:0;left:0;right:0;z-index:20;background:rgba(255,255,255,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line);transform:translateY(-110%);transition:transform .38s var(--ease)}
body.scrolled .bbar{transform:translateY(0)}
.bin{max-width:1400px;margin:0 auto;padding:10px 24px;display:flex;align-items:center;gap:24px}
.bword{font-weight:700;font-size:16.5px;letter-spacing:-.02em;color:var(--txt);text-decoration:none;flex:none}
.bword:hover{text-decoration:none}
.bword span{color:#f97316}
.btabs{display:flex;gap:2px;flex:1;justify-content:center;overflow:auto;scrollbar-width:none}
.btabs::-webkit-scrollbar{display:none}
.btab{padding:6px 13px;border-radius:var(--pill);background:none;border:0;color:var(--sec);font:500 13px var(--sans);cursor:pointer;white-space:nowrap;transition:background-color .18s var(--ease),color .18s var(--ease)}
.btab:hover{color:var(--txt)}
.btab.on{background:#09090b;color:#fff}
#q{flex:none;width:210px;background:var(--bg);border:1px solid var(--line-strong);color:var(--txt);border-radius:var(--pill);padding:7px 15px;font:13px var(--sans);outline:none;transition:border-color .18s var(--ease)}
#q::placeholder{color:var(--mut)}
#q:focus{border-color:#09090b}
.bwrap{max-width:1400px;margin:0 auto;padding:0 24px}
.bhero{padding:48px 0 4px;animation:rise .5s var(--ease) both}
.bsub{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 0 0;flex-wrap:wrap}
.stabs{display:flex;gap:16px}
.stab{font:500 13px var(--sans);color:var(--mut);background:none;border:0;cursor:pointer;padding:5px 1px;border-bottom:2px solid transparent;transition:color .18s var(--ease)}
.stab:hover{color:var(--txt)}
.stab.on{color:var(--txt);border-color:var(--txt)}
.shown{font:12px var(--mono);color:var(--mut)}
.shown b{color:var(--sec);font-weight:500}
.masonry{columns:4 250px;column-gap:16px;padding:20px 0 96px}
.mcard{position:relative;display:block;margin:0 0 16px;border-radius:14px;overflow:hidden;break-inside:avoid;background:var(--fill);animation:rise .45s var(--ease) both}
.mcard:hover{text-decoration:none}
.mcard img{width:100%;height:auto;display:block;transition:transform .5s var(--ease)}
.mcard:hover img{transform:scale(1.03)}
.mcount{position:absolute;top:10px;right:10px;display:flex;align-items:center;gap:5px;background:rgba(0,0,0,.55);backdrop-filter:blur(6px);color:#fff;font:500 11px var(--mono);padding:4px 9px;border-radius:var(--pill)}
.mover{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:14px;background:linear-gradient(to top,rgba(0,0,0,.6),rgba(0,0,0,0) 42%);opacity:0;transition:opacity .22s var(--ease)}
.mcard:hover .mover{opacity:1}
.mt{display:block;color:#fff;font-size:13.5px;font-weight:600;letter-spacing:-.01em;line-height:1.35}
.mm{display:block;color:rgba(255,255,255,.75);font-size:11.5px;margin-top:3px}
@media(max-width:680px){.bin{gap:12px;padding:10px 16px}.bwrap{padding:0 16px}#q{width:130px}.masonry{columns:2;column-gap:10px}.mcard{margin-bottom:10px;border-radius:12px}}
</style>
"""

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
{FONTS}<link rel="stylesheet" href="assets-style.css">{BENTO_STYLE}</head><body>
<div class="bbar"><div class="bin">
<a class="bword" href="./">16<span>ms</span></a>
<div class="btabs" id="btabs"></div>
<input id="q" placeholder="Search  &#8984;K">
</div></div>
<div class="bwrap">
<header class="top" style="padding-bottom:32px">
<div class="eyebrow">16ms &middot; {len(recs)} interactions &middot; inspora.design + 60fps.design</div>
<h1>16<span style="color:#f97316">ms</span></h1>
<p class="sub">Frame-by-frame teardowns of the best interactions on the web, reverse-engineered into build-ready prompts. Sources: <a href="https://www.inspora.design/">inspora.design</a> (80) and <a href="https://60fps.design/">60fps.design</a> (2,033 shots, full teardown). Query it from your AI tool via the <a href="mcp/">MCP server</a>.</p>
<div class="stats"><span><b>{len(recs)}</b> interactions</span><span><b>{sum(len(r['media']) for r in recs)}</b> media</span><span><b>{len(set(r['category'] for r in recs))}</b> categories</span><span><b>{len(set(r['source'] for r in recs))}</b> sources</span></div>
</header>
<div class="bsub"><div class="stabs" id="stabs"></div><span class="shown"><b id="count">{len(recs)}</b> shown</span></div>
<div class="masonry" id="wall"></div>
<footer>Built from full teardowns of inspora.design (80 posts, Sep 2026 snapshot) and 60fps.design (2,033 shots, full teardown, Sep 2026). Every record: summary, montage, mechanics, and a build prompt.</footer>
</div>
<script>window.__DATA__={json.dumps(lite)}</script><script>{APPJS}</script>{cmdk_tags('')}
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
    refs = []
    for m in r['media']:
        if m.get('montage'):
            refs.append('https://16ms.vercel.app/' + m['montage'])
        if m.get('poster'):
            refs.append(m['poster'])
    copy_text = (r.get('prompt') or '').rstrip() + "\n\n---\n\nFrame references (image URLs - fetch them for visual frame-by-frame context):\n" + "\n".join('- ' + u for u in refs)
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
<script>document.querySelector('.prompt').dataset.p={json.dumps(copy_text)}</script>{cmdk_tags('../')}
</body></html>"""
    open(f'{DIST}/i/{r["slug"]}.html','w').write(page)

os.makedirs(f'{DIST}/mcp', exist_ok=True)
import base64, urllib.parse
MCP_URL = 'https://16ms.vercel.app/api/mcp'
_cursor_cfg = base64.b64encode(json.dumps({"url": MCP_URL}).encode()).decode()
CURSOR_LINK = 'cursor://anysphere.cursor-deeplink/mcp/install?name=interaction-prompt-library&config=' + _cursor_cfg
VS_LINK = 'vscode:mcp/install?' + urllib.parse.quote(json.dumps({"name": "interaction-prompt-library", "type": "http", "url": MCP_URL}))
TRY_PROMPT = 'Search the 16ms interaction library for a pull-to-refresh animation and give me the full build prompt.'
SETUP_PROMPT = 'Add an MCP server called "interaction-prompt-library" at ' + MCP_URL + ' (streamable HTTP transport, no auth). Then list its tools and search it for a toggle switch interaction.'

def _code(t):
    return '<div class="mcopy"><code>' + E(t) + '</code><button class="mcbtn" data-copy="' + E(t) + '" aria-label="Copy"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg></button></div>'

def _step(num, title, desc, action_html):
    return ('<div class="mstep"><div class="mleft"><div class="mnum">' + num + '</div>'
            '<h3>' + title + '</h3><p>' + desc + '</p></div>'
            '<div class="mright">' + action_html + '</div></div>')

def _try_step():
    return _step('02', 'Try it', 'With the server connected, ask your tool:', _code(TRY_PROMPT))

ICONS = {'Claude': '<svg viewBox="0 0 24 24" class="cico" fill="currentColor" ><path d="m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z"></path></svg>', 'ChatGPT': '<svg viewBox="0 0 24 24" class="cico" fill="currentColor" ><path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"></path></svg>', 'Codex': '<svg viewBox="0 0 24 24" class="cico" fill="currentColor" ><path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"></path></svg>', 'Claude Code': '<svg viewBox="0 0 16 16" class="cico" fill="currentColor" ><path d="m3.127 10.604 3.135-1.76.053-.153-.053-.085H6.11l-.525-.032-1.791-.048-1.554-.065-1.505-.08-.38-.081L0 7.832l.036-.234.32-.214.455.04 1.009.069 1.513.105 1.097.064 1.626.17h.259l.036-.105-.089-.065-.068-.064-1.566-1.062-1.695-1.121-.887-.646-.48-.327-.243-.306-.104-.67.435-.48.585.04.15.04.593.456 1.267.981 1.654 1.218.242.202.097-.068.012-.049-.109-.181-.9-1.626-.96-1.655-.428-.686-.113-.411a2 2 0 0 1-.068-.484l.496-.674L4.446 0l.662.089.279.242.411.94.666 1.48 1.033 2.014.302.597.162.553.06.17h.105v-.097l.085-1.134.157-1.392.154-1.792.052-.504.25-.605.497-.327.387.186.319.456-.045.294-.19 1.23-.37 1.93-.243 1.29h.142l.161-.16.654-.868 1.097-1.372.484-.545.565-.601.363-.287h.686l.505.751-.226.775-.707.895-.585.759-.839 1.13-.524.904.048.072.125-.012 1.897-.403 1.024-.186 1.223-.21.553.258.06.263-.218.536-1.307.323-1.533.307-2.284.54-.028.02.032.04 1.029.098.44.024h1.077l2.005.15.525.346.315.424-.053.323-.807.411-3.631-.863-.872-.218h-.12v.073l.726.71 1.331 1.202 1.667 1.55.084.383-.214.302-.226-.032-1.464-1.101-.565-.497-1.28-1.077h-.084v.113l.295.432 1.557 2.34.08.718-.112.234-.404.141-.444-.08-.911-1.28-.94-1.44-.759-1.291-.093.053-.448 4.821-.21.246-.484.186-.403-.307-.214-.496.214-.98.258-1.28.21-1.016.19-1.263.112-.42-.008-.028-.092.012-.953 1.307-1.448 1.957-1.146 1.227-.274.109-.477-.247.045-.44.266-.39 1.586-2.018.956-1.25.617-.723-.004-.105h-.036l-4.212 2.736-.75.096-.324-.302.04-.496.154-.162 1.267-.871z"></path></svg>', 'Cursor': '<svg viewBox="0 0 466.73 532.09" class="cico" fill="currentColor" ><path d="M457.43,125.94L244.42,2.96c-6.84-3.95-15.28-3.95-22.12,0L9.3,125.94c-5.75,3.32-9.3,9.46-9.3,16.11v247.99c0,6.65,3.55,12.79,9.3,16.11l213.01,122.98c6.84,3.95,15.28,3.95,22.12,0l213.01-122.98c5.75-3.32,9.3-9.46,9.3-16.11v-247.99c0-6.65-3.55-12.79-9.3-16.11h-.01ZM444.05,151.99l-205.63,356.16c-1.39,2.4-5.06,1.42-5.06-1.36v-233.21c0-4.66-2.49-8.97-6.53-11.31L24.87,145.67c-2.4-1.39-1.42-5.06,1.36-5.06h411.26c5.84,0,9.49,6.33,6.57,11.39h-.01Z"></path></svg>', 'VS Code': '<svg viewBox="0 0 96 96" class="cico" fill="currentColor" ><path fill-rule="evenodd" clip-rule="evenodd" d="M95.6877 67.9677C92.2446 73.9488 72.2522 88.0617 48 88.0617C23.7478 88.0617 3.75535 73.9488 0.312312 67.9677C0.0605215 67.5303 -0.0207525 67.031 -0.0207525 66.5263L-0.0207524 55.8787C-0.0207524 55.4373 0.0473833 54.9986 0.210699 54.5885C1.69959 50.8499 5.59895 45.4192 10.6313 43.9621C11.2985 42.2494 12.2867 39.7456 13.2087 37.8974C13.0543 36.4833 13 35.0248 13 33.5512C13 28.2274 14.1285 23.5576 17.5288 20.0801C19.117 18.4559 21.0876 17.21 23.4246 16.2735C29.0217 11.7264 36.992 7.90112 47.9136 7.90112C58.8352 7.90112 66.9783 11.7264 72.5754 16.2735C74.9124 17.21 76.883 18.4559 78.4712 20.0801C81.8715 23.5576 83 28.2274 83 33.5512C83 35.0248 82.9457 36.4833 82.7913 37.8974C83.7133 39.7456 84.7015 42.2494 85.3687 43.9621C90.401 45.4192 94.3004 50.8499 95.7893 54.5885C95.9526 54.9986 96.0208 55.4373 96.0208 55.8787L96.0208 66.5263C96.0208 67.031 95.9395 67.5303 95.6877 67.9677ZM51.253 32.2606C51.0828 30.9345 51.0018 29.747 50.9995 28.686L50.9995 28.6021C51.0048 25.5242 51.6776 23.5215 52.7524 22.2914C54.1172 20.7295 56.9379 19.5328 62.8829 20.1762C68.9059 20.828 72.2725 22.3229 74.1812 24.2749C76.0291 26.1648 76.9999 28.9922 76.9999 33.5512C76.9999 38.3951 76.3018 41.2568 74.767 42.9977C73.3075 44.6531 70.4335 46 64.1386 46C59.2994 46 56.5326 44.4261 54.7637 42.2493C52.8644 39.912 51.7955 36.4878 51.253 32.2606ZM44.747 32.2606C44.9172 30.9344 44.9982 29.747 45.0005 28.686L45.0005 28.6021C44.9952 25.5242 44.3224 23.5214 43.2476 22.2914C41.8828 20.7295 39.0621 19.5328 33.1171 20.1762C27.0941 20.828 23.7275 22.3229 21.8188 24.2749C19.9709 26.1647 19.0001 28.9922 19.0001 33.5512C19.0001 38.3951 19.6982 41.2568 21.233 42.9977C22.6925 44.6531 25.5665 46 31.8614 46C36.7006 46 39.4674 44.4261 41.2363 42.2493C43.1356 39.9119 44.2045 36.4878 44.747 32.2606ZM48.6889 43.9983C48.4592 43.9995 48.9185 43.9983 48.6889 43.9983C48.4594 43.9983 47.5408 43.9995 47.3111 43.9983C46.8877 44.7075 46.4168 45.3882 45.8926 46.0332C42.8139 49.8219 38.2182 52 31.8613 52C24.9615 52 19.9049 50.564 16.7324 46.9657C16.552 46.7611 16.3906 46.5469 16.3906 46.5469L16 46.9657L16 73.3023C21.7392 76.4213 34.0576 82.0184 48 82.0184C61.9424 82.0184 74.2608 76.4213 80 73.3023L80 46.9657L79.6094 46.5469C79.6094 46.5469 79.4772 46.728 79.2676 46.9657C76.0951 50.564 71.0385 52 64.1387 52C57.7818 52 53.1861 49.8219 50.1074 46.0332C49.5832 45.3882 49.1123 44.7075 48.6889 43.9983Z"></path><path d="M58 57C60.2091 57 62 58.7909 62 61L62 69C62 71.2092 60.2091 73 58 73C55.7909 73 54 71.2092 54 69L54 61C54 58.7909 55.7909 57 58 57Z"></path><path d="M38 57C40.2091 57 42 58.7909 42 61L42 69C42 71.2092 40.2091 73 38 73C35.7909 73 34 71.2092 34 69L34 61C34 58.7909 35.7909 57 38 57Z"></path></svg>'}

CLIENTS = [
    ('claude', 'Claude',
     _step('01', 'Add the connector', 'Claude &rarr; Settings &rarr; Connectors &rarr; Add custom connector. Custom connectors need a paid Claude plan.', _code(MCP_URL)) + _try_step()),
    ('chatgpt', 'ChatGPT',
     _step('01', 'Add a developer connector', 'ChatGPT &rarr; Settings &rarr; Connectors &rarr; Advanced &rarr; Developer mode (Pro), then create a connector with this URL.', _code(MCP_URL)) + _try_step()),
    ('codex', 'Codex',
     _step('01', 'Add it from the CLI', 'One command:', _code('codex mcp add interaction-prompt-library --url ' + MCP_URL)) + _try_step()),
    ('claude-code', 'Claude Code',
     _step('01', 'Add it from the CLI', 'One command:', _code('claude mcp add --transport http interaction-prompt-library ' + MCP_URL)) + _try_step()),
    ('cursor', 'Cursor',
     _step('01', 'Add it in one click', 'Installs the server into your Cursor MCP config.',
           '<a class="mbtn" href="' + CURSOR_LINK + '">Add to Cursor&nbsp;&nearr;</a>'
           '<p class="mor">Or add it by hand in <b>~/.cursor/mcp.json</b>:</p>'
           + _code('{\n  "mcpServers": {\n    "interaction-prompt-library": {\n      "url": "' + MCP_URL + '"\n    }\n  }\n}')) + _try_step()),
    ('vscode', 'VS Code',
     _step('01', 'Add it in one click', 'Installs the server into your VS Code MCP config.',
           '<a class="mbtn" href="' + VS_LINK + '">Add to VS Code&nbsp;&nearr;</a>'
           '<p class="mor">Or add it by hand in <b>.vscode/mcp.json</b>:</p>'
           + _code('{\n  "servers": {\n    "interaction-prompt-library": {\n      "type": "http",\n      "url": "' + MCP_URL + '"\n    }\n  }\n}')) + _try_step()),
]

_tab_btns = ''.join('<button class="ctab' + (' on' if i == 0 else '') + '" data-c="' + cid + '"><span class="cic">' + ICONS[label] + '</span>' + label + '</button>' for i, (cid, label, _) in enumerate(CLIENTS))
_panes = ''.join('<div class="cpane" id="cp-' + cid + '"' + ('' if i == 0 else ' hidden') + '>' + html + '</div>' for i, (cid, _, html) in enumerate(CLIENTS))

MCP_STYLE = """
<style>
body.mcpd{background:#fff;color:#09090b}
.mwrap{max-width:860px;margin:0 auto;padding:72px 24px 110px}
.mhome{font:500 12px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;color:#a1a1aa;text-decoration:none}
.mhome:hover{color:#52525b}
.mwrap h1{font-size:52px;font-weight:600;letter-spacing:-.03em;line-height:1.05;margin:64px 0 0;color:#09090b}
.mwrap h1 .cli{color:#a1a1aa}
.msub{color:#52525b;font-size:17px;line-height:1.6;margin:18px 0 0;max-width:560px}
.mcard{margin-top:48px;background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:20px;overflow:hidden}
.mtabs{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px;border-bottom:1px solid rgba(0,0,0,.08)}
.ctabset{display:flex;gap:2px;flex-wrap:nowrap;overflow:auto;scrollbar-width:none;min-width:0}
.ctabset::-webkit-scrollbar{display:none}
.ctab{flex:none;display:inline-flex;align-items:center;gap:8px;padding:5px 14px 5px 5px;border-radius:999px;background:none;border:0;color:#52525b;font:500 13.5px InterVariable,Inter,sans-serif;cursor:pointer;transition:background-color .18s,color .18s}
.ctab:hover{color:#09090b}
.ctab.on{background:#09090b;color:#fff}
.cic{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:999px;background:#f4f4f4;color:#3f3f46;flex:none}
.ctab.on .cic{background:rgba(255,255,255,.16);color:#fff}
.cico{width:12px;height:12px}
.mtoggle{display:flex;background:#f4f4f4;border-radius:999px;padding:3px;flex:none}
.mtg{padding:5px 13px;border-radius:999px;background:none;border:0;color:#71717a;font:600 11px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.1em;cursor:pointer}
.mtg.on{background:#09090b;color:#fff}
.mstep{display:flex;gap:36px;padding:28px 32px;border-top:1px solid rgba(0,0,0,.06)}
.mstep:first-child{border-top:0}
.mleft{width:250px;flex:none}
.mnum{font:500 12px ui-monospace,SFMono-Regular,Menlo,monospace;color:#a1a1aa;margin-bottom:8px}
.mleft h3{font-size:17px;font-weight:600;letter-spacing:-.01em;margin:0 0 6px;color:#09090b}
.mleft p{font-size:13.5px;line-height:1.55;color:#52525b;margin:0}
.mright{flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center}
.mbtn{display:inline-block;align-self:flex-start;background:#09090b;color:#fff;font:600 14px InterVariable,Inter,sans-serif;padding:11px 20px;border-radius:999px;text-decoration:none}
.mbtn:hover{background:#27272a;text-decoration:none}
.mor{font-size:13px;color:#71717a;margin:18px 0 0}
.mor b{color:#52525b;font-weight:500}
.mcopy{display:flex;align-items:flex-start;gap:10px;background:#fafafa;border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:13px 14px 13px 16px;margin-top:14px}
.mright > .mcopy:first-child{margin-top:0}
.mcopy code{flex:1;font:13px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;color:#3f3f46;white-space:pre-wrap;word-break:break-all}
.mcbtn{flex:none;background:none;border:0;color:#a1a1aa;cursor:pointer;padding:2px;margin-top:1px}
.mcbtn:hover{color:#09090b}
.mcbtn.ok{color:#16a34a}
.mtools{margin-top:64px}
.mtools h2{font-size:26px;font-weight:600;letter-spacing:-.02em;margin:0 0 20px;color:#09090b}
.mgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.mtool{background:#fafafa;border:1px solid rgba(0,0,0,.08);border-radius:14px;padding:18px}
.mtool .t{font:600 13px ui-monospace,SFMono-Regular,Menlo,monospace;color:#09090b;margin-bottom:8px}
.mtool .d{font-size:13px;line-height:1.55;color:#52525b}
.mfoot{margin-top:56px;text-align:center;font-size:13px;line-height:1.7;color:#71717a}
.mfoot a{color:#52525b}
@media(max-width:680px){.mstep{flex-direction:column;gap:14px;padding:24px 20px}.mleft{width:auto}.mgrid{grid-template-columns:1fr}.mwrap h1{font-size:38px}}
</style>
"""

MCP_JS = """
<script>
var tabs=document.querySelectorAll('.ctab'),panes=document.querySelectorAll('.cpane'),
    mtgM=document.getElementById('mtg-mcp'),mtgP=document.getElementById('mtg-prompt'),
    promptPane=document.getElementById('cp-prompt'),stepsWrap=document.getElementById('mcp-panes');
tabs.forEach(function(t){t.onclick=function(){
  tabs.forEach(function(x){x.classList.toggle('on',x===t)});
  panes.forEach(function(p){p.hidden=p.id!=='cp-'+t.dataset.c});
  mtgM.classList.add('on');mtgP.classList.remove('on');
}});
mtgM.onclick=function(){mtgM.classList.add('on');mtgP.classList.remove('on');promptPane.hidden=true;
  panes.forEach(function(p){if(p.id!=='cp-prompt')p.hidden=p.id!=='cp-'+document.querySelector('.ctab.on').dataset.c})};
mtgP.onclick=function(){mtgP.classList.add('on');mtgM.classList.remove('on');
  panes.forEach(function(p){p.hidden=p.id!=='cp-prompt'})};
document.querySelectorAll('.mcbtn').forEach(function(b){b.onclick=function(){
  navigator.clipboard.writeText(b.dataset.copy);b.classList.add('ok');setTimeout(function(){b.classList.remove('ok')},1200)}});
var clis=['Claude','ChatGPT','Codex','Claude Code','Cursor','VS Code'],ci=0,cn=document.getElementById('cli');
setInterval(function(){ci=(ci+1)%clis.length;cn.textContent=clis[ci]},1800);
</script>
"""

mcp_page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCP server - 16ms</title>
<meta name="description" content="Query all {len(recs)} 16ms interaction teardowns from Claude, ChatGPT, Codex, Claude Code, Cursor, or VS Code via one hosted MCP server.">
<link rel="canonical" href="https://16ms.vercel.app/mcp/">
<link rel="icon" type="image/png" href="../icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="16ms">
<meta property="og:title" content="MCP server - 16ms">
<meta property="og:description" content="Query the 16ms interaction library from your AI tool. One hosted MCP server, no API key.">
<meta property="og:url" content="https://16ms.vercel.app/mcp/">
<meta property="og:image" content="https://16ms.vercel.app/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://16ms.vercel.app/og-image.png">
{FONTS}<link rel="stylesheet" href="../assets-style.css">{MCP_STYLE}</head><body class="mcpd">
<div class="mwrap">
<a class="mhome" href="../">&larr; 16ms</a>
<h1>Query {len(recs):,} interaction teardowns<br>from <span class="cli" id="cli">Claude</span>.</h1>
<p class="msub">One hosted MCP server over every frame-by-frame teardown in the library - search, browse, and pull build-ready prompts straight into your AI tool. Read-only, no API key.</p>
<div class="mcard">
<div class="mtabs">
<div class="ctabset">{_tab_btns}</div>
<div class="mtoggle"><button class="mtg on" id="mtg-mcp">MCP</button><button class="mtg" id="mtg-prompt">PROMPT</button></div>
</div>
<div id="mcp-panes">{_panes}
<div class="cpane" id="cp-prompt" hidden>
<div class="mstep"><div class="mleft"><div class="mnum">01</div><h3>Set up in one prompt</h3><p>Paste this into your tool. It adds the server and runs a first search.</p></div>
<div class="mright">{_code(SETUP_PROMPT)}</div></div>
</div>
</div>
</div>
<div class="mtools">
<h2>Tools you get</h2>
<div class="mgrid">
<div class="mtool"><div class="t">search_interactions</div><div class="d">Full-text search over titles, summaries, mechanics, and prompts. "toggle switch", "scroll stack", "glass refraction".</div></div>
<div class="mtool"><div class="t">get_interaction_prompt</div><div class="d">The full teardown for one interaction: summary, frame-by-frame phases, mechanics, and the build-ready prompt.</div></div>
<div class="mtool"><div class="t">list_interactions</div><div class="d">Browse everything, filtered by category (Motion, Product, Web...) or source (inspora, 60fps).</div></div>
</div>
</div>
<p class="mfoot">Hosted on Vercel, streamable HTTP, read-only. Prefer running it locally over stdio? <a href="https://github.com/0xdevesh15/interaction-prompt-library#run-the-mcp-server">One file, zero dependencies</a>.</p>
</div>
{MCP_JS}{cmdk_tags('../')}
</body></html>"""
open(f'{DIST}/mcp/index.html','w').write(mcp_page)


print('built', len(recs), 'pages')
