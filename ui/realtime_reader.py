"""
==========================================================
ReadingAI - Real-Time Reader Component
Embeds the reading coach as a self-contained HTML widget.
Results are returned via a hidden Streamlit text_input that
the JS sets via dispatchEvent/input simulation.
==========================================================
"""

from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components


def realtime_reader(article_words: list):
    """
    Renders the Real-Time Reading Coach.

    The HTML widget runs entirely in the browser using the Web Speech API.
    After the user finishes, a 'results' JSON string is stored in
    st.session_state['_rt_result_raw'] via a hidden Streamlit text_input.

    Args:
        article_words : list of str — words from the article
    """
    words_json = json.dumps(article_words, ensure_ascii=False)

    html = f"""
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:#0f172a;color:#e2e8f0;height:100vh;display:flex;
  flex-direction:column;overflow:hidden;padding:12px;gap:7px;}}
.srow{{display:flex;gap:8px;flex-shrink:0;}}
.sc{{flex:1;background:#1e293b;border:1px solid #334155;border-radius:10px;padding:7px 10px;text-align:center;}}
.sv{{font-size:1.2rem;font-weight:800;color:#38bdf8;line-height:1.2;}}
.sl{{font-size:.6rem;color:#64748b;text-transform:uppercase;letter-spacing:.05em;}}
.pt{{width:100%;height:5px;background:#1e293b;border-radius:3px;overflow:hidden;flex-shrink:0;}}
.pf{{height:100%;background:linear-gradient(90deg,#6366f1,#38bdf8);border-radius:3px;width:0%;transition:width .4s ease;}}
.hr{{background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:5px 14px;font-size:.82rem;
  color:#475569;display:flex;align-items:center;gap:6px;flex-shrink:0;min-height:32px;}}
.hw{{color:#38bdf8;font-weight:600;}}
.aw{{position:relative;flex:1;min-height:0;}}
.ab{{width:100%;height:100%;background:#1e293b;border:1px solid #334155;border-radius:12px;
  padding:16px 20px;overflow-y:auto;line-height:2.4;font-size:1.1rem;}}
.w{{display:inline;padding:1px 3px;border-radius:4px;transition:all .2s ease;}}
.w.wait{{color:#94a3b8;}}
.w.active{{background:rgba(251,191,36,.18);color:#fbbf24;font-weight:700;
  border-bottom:2.5px solid #fbbf24;animation:wb .85s ease-in-out infinite;}}
.w.ok{{color:#4ade80;background:rgba(74,222,128,.1);}}
.w.bad{{color:#f87171;background:rgba(248,113,113,.12);animation:sk .35s ease;}}
.w.skip{{color:#fb923c;background:rgba(251,146,60,.1);text-decoration:underline dotted #fb923c;}}
@keyframes wb{{0%,100%{{box-shadow:0 2px 0 0 #fbbf24;}}
  50%{{box-shadow:0 2px 0 0 rgba(251,191,36,0),0 0 12px 4px rgba(251,191,36,.3);}}}}
@keyframes sk{{0%,100%{{transform:translateX(0);}}20%{{transform:translateX(-5px);}}60%{{transform:translateX(5px);}}}}
.ov{{display:none;position:absolute;inset:0;background:rgba(15,23,42,.96);border-radius:12px;
  flex-direction:column;align-items:center;justify-content:center;padding:24px;text-align:center;z-index:10;}}
.ov.show{{display:flex;}}
.rp{{font-size:3.8rem;font-weight:900;background:linear-gradient(135deg,#4ade80,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;margin-bottom:6px;}}
.rg2{{font-size:1.1rem;color:#94a3b8;margin-bottom:14px;}}
.rgrid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%;max-width:280px;margin-bottom:14px;}}
.ri{{background:#1e293b;border-radius:10px;padding:10px;}}
.rv{{font-size:1.3rem;font-weight:800;}}
.rl{{font-size:.62rem;color:#64748b;text-transform:uppercase;margin-top:2px;}}
.bdone{{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;padding:10px 28px;
  border:none;border-radius:10px;font-size:.9rem;font-weight:700;cursor:pointer;transition:all .2s;}}
.bdone:hover{{transform:translateY(-2px);box-shadow:0 8px 20px rgba(34,197,94,.4);}}
.bdone:disabled{{opacity:.5;cursor:not-allowed;transform:none;}}
.eb{{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);border-radius:8px;
  padding:6px 14px;font-size:.8rem;color:#f87171;text-align:center;min-height:32px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:opacity .3s;}}
.eb.hidden{{opacity:0;pointer-events:none;}}
.cr{{display:flex;gap:8px;align-items:center;flex-shrink:0;}}
.md{{width:40px;height:40px;border-radius:50%;background:#1e293b;border:2px solid #334155;
  display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;transition:all .3s;}}
.md.on{{background:rgba(239,68,68,.15);border-color:#ef4444;animation:mr 1.5s ease-in-out infinite;}}
@keyframes mr{{0%,100%{{box-shadow:0 0 0 0 rgba(239,68,68,.3);}}50%{{box-shadow:0 0 0 9px rgba(239,68,68,0);}}}}
.btn{{padding:9px 0;border:none;border-radius:8px;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .2s;flex:1;}}
.btn:disabled{{opacity:.35;cursor:not-allowed;transform:none!important;}}
.bs{{background:linear-gradient(135deg,#6366f1,#4f46e5);color:#fff;}}
.bs:not(:disabled):hover{{transform:translateY(-1px);box-shadow:0 5px 14px rgba(99,102,241,.4);}}
.bk{{background:linear-gradient(135deg,#f97316,#ea580c);color:#fff;}}
.bk:not(:disabled):hover{{transform:translateY(-1px);}}
.bt{{background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;}}
.bt:not(:disabled):hover{{transform:translateY(-1px);}}
.ab::-webkit-scrollbar{{width:5px;}}
.ab::-webkit-scrollbar-track{{background:#0f172a;}}
.ab::-webkit-scrollbar-thumb{{background:#334155;border-radius:3px;}}
</style></head><body>

<div class="srow">
  <div class="sc"><div class="sv" id="sa">—</div><div class="sl">Accuracy</div></div>
  <div class="sc"><div class="sv" id="so" style="color:#4ade80">0</div><div class="sl">✅ Correct</div></div>
  <div class="sc"><div class="sv" id="se" style="color:#f87171">0</div><div class="sl">❌ Errors</div></div>
  <div class="sc"><div class="sv" id="sw">—</div><div class="sl">WPM</div></div>
</div>

<div class="pt"><div class="pf" id="pg"></div></div>
<div class="hr">🎙️&nbsp;<span id="hd" class="hw">Click "Start Reading" to begin...</span></div>

<div class="aw">
  <div class="ab" id="ab"></div>
  <div class="ov" id="ov">
    <div class="rp" id="rp">—%</div>
    <div class="rg2" id="rg2"></div>
    <div class="rgrid">
      <div class="ri"><div class="rv" id="ro" style="color:#4ade80">0</div><div class="rl">Correct</div></div>
      <div class="ri"><div class="rv" id="re" style="color:#f87171">0</div><div class="rl">Errors</div></div>
      <div class="ri"><div class="rv" id="rs" style="color:#fb923c">0</div><div class="rl">Skipped</div></div>
      <div class="ri"><div class="rv" id="rw" style="color:#38bdf8">0</div><div class="rl">WPM</div></div>
    </div>
    <p id="rb" style="color:#64748b;font-size:.78rem;margin-bottom:12px;"></p>
    <button class="bdone" id="bdone" onclick="submitResult()">📊 Submit to Dashboard →</button>
  </div>
</div>

<div class="eb hidden" id="eb">&nbsp;</div>
<div class="cr">
  <div class="md" id="md">🎙️</div>
  <button class="btn bs" id="bs" onclick="startR()">🎙 Start Reading</button>
  <button class="btn bk" id="bk" onclick="skipW()" disabled>⏭ Skip</button>
  <button class="btn bt" id="bt" onclick="stopR()" disabled>⏹ Stop</button>
</div>

<script>
const WDS={words_json};
let el=[],st2=[],cur=0,nOk=0,nErr=0,nSk=0,t0=null,recog=null,listen=false;
let ws=0,eT=null,wR=[],fd=null;

function lev(a,b){{if(!a.length)return b.length;if(!b.length)return a.length;
  const d=Array.from({{length:b.length+1}},(_,i)=>i);
  for(let j=0;j<a.length;j++){{let p=d[0];d[0]=j+1;
    for(let i=1;i<=b.length;i++){{const t=d[i];d[i]=a[j]===b[i-1]?p:1+Math.min(p,d[i],d[i-1]);p=t;}}}}return d[b.length];}}
function sim(a,b){{
  a=a.toLowerCase().replace(/[^a-z']/g,'');b=b.toLowerCase().replace(/[^a-z']/g,'');
  if(!a||!b)return 0;if(a===b)return 100;
  if(a+'s'===b || b+'s'===a) return 95;
  if(a+'d'===b || b+'d'===a) return 95;
  if(a+'ed'===b || b+'ed'===a) return 95;
  if(a+'ing'===b || b+'ing'===a) return 90;
  return Math.round((1-lev(a,b)/Math.max(a.length,b.length))*100);}}

(function init(){{
  st2=new Array(WDS.length).fill('wait');wR=[];cur=nOk=nErr=nSk=ws=0;fd=null;
  const box=document.getElementById('ab');box.innerHTML='';el=[];
  WDS.forEach((w,i)=>{{
    const sp=document.createElement('span');sp.className='w wait';sp.id='wd'+i;sp.textContent=w;
    box.appendChild(sp);box.appendChild(document.createTextNode(' '));el.push(sp);}});
  act(0);}})();

function act(i){{if(i>=0&&i<el.length){{el[i].className='w active';st2[i]='active';
  el[i].scrollIntoView({{block:'nearest',behavior:'smooth'}});}}}}
function setW(i,c){{if(i<0||i>=el.length)return;st2[i]=c;el[i].className='w '+c;}}

function startR(){{
  if(!WDS.length){{showE('No article loaded.');return;}}
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){{showE('Please use Chrome or Edge for speech recognition.');return;}}
  
  // Initialize AudioContext inside click handler to bypass browser autoplay restrictions!
  try{{
    const AC=window.AudioContext||window.webkitAudioContext;
    if(AC && !window._aCtx) window._aCtx=new AC();
    if(window._aCtx && window._aCtx.state==='suspended') window._aCtx.resume();
  }}catch(e){{}}

  listen=true;t0=Date.now();ws=0;
  document.getElementById('bs').disabled=true;
  document.getElementById('bk').disabled=false;
  document.getElementById('bt').disabled=false;
  document.getElementById('md').classList.add('on');
  setHd('Listening... Read the highlighted word');
  recog=new SR();recog.continuous=true;recog.interimResults=true;
  recog.lang='en-US';recog.maxAlternatives=3;
  recog.onresult=onSp;
  let netRetries=0;
  recog.onerror=(e)=>{{
    if(e.error==='not-allowed'){{
      showE('🔒 Microphone access denied. Click the lock icon in the address bar to allow.');
      listen=false;rCtrl();
    }} else if(e.error==='network'){{
      // Network blip — silently retry instead of showing error
      netRetries++;
      if(netRetries<=5){{
        setHd('🔄 Reconnecting... ('+ netRetries +'/5)');
        setTimeout(()=>{{
          if(listen){{try{{recog.stop();}}catch(_){{}}}}
        }},800);
      }} else {{
        showE('❌ Network error — please check your internet and click Start Reading again.');
        listen=false;rCtrl();
      }}
    }} else if(e.error!=='no-speech'&&e.error!=='aborted'){{
      showE('⚠️ Speech error: '+e.error+' — retrying...');
    }}
  }};
  recog.onend=()=>{{
    if(listen){{
      try{{recog.start();netRetries=0;}}catch(_){{}}
    }}
  }};
  recog.start();}}

const bzSnd = new Audio('data:audio/wav;base64,UklGRmQGAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YUAGAAAAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPYAACNJztLjWe7ef9/u3mNZztLjScAAHPYxbRzmEWGAYBFhnOYxbRz2AAAjSc7S41nu3n/f7t5jWc7S40nAABz2MW0c5hFhgGARYZzmMW0c9gAAI0nO0uNZ7t5/3+7eY1nO0uNJwAAc9jFtHOYRYYBgEWGc5jFtHPY');
function playBuzz(){{
  try{{
    bzSnd.currentTime = 0;
    bzSnd.play().catch(e=>{{}});
  }}catch(e){{}}
}}

function onSp(ev){{
  if(cur>=WDS.length)return;
  
  // Combine unfinalized and final transcripts for a complete picture
  let tr = '';
  for(let i=ev.resultIndex; i<ev.results.length; i++) {{
     tr += ev.results[i][0].transcript + ' ';
  }}
  tr = tr.trim();
  if(tr) setHd('🎙️ "'+tr+'"');
  
  const arr=tr.toLowerCase().split(/\s+/).filter(Boolean);
  const isFinal = ev.results[ev.results.length-1].isFinal;
  
  let matchedAny = false;
  
  for(let i=0; i<arr.length; i++){{
    const sw = arr[i];
    if(cur>=WDS.length) break;
    if(st2[cur]==='ok') continue;
    
    // Lookahead window: check current word and next 2 words to handle fast reading or skips
    let bestMatchIdx = -1;
    let bestMatchScore = 0;
    
    for(let j=0; j<=2; j++){{
      if(cur+j >= WDS.length) break;
      const exp = WDS[cur+j];
      const s = sim(sw, exp);
      if(s >= 70 && s > bestMatchScore){{
        bestMatchScore = s;
        bestMatchIdx = cur+j;
      }}
    }}
    
    if(bestMatchIdx !== -1){{
      // If we matched a future word, mark intermediate words as skipped
      while(cur < bestMatchIdx){{
         setW(cur, 'skip');
         wR.push({{index:cur, expected:WDS[cur], spoken:'', status:'skipped', similarity:0}});
         nSk++;
         cur++;
      }}
      doOk(cur, sw, WDS[cur], bestMatchScore);
      matchedAny = true;
    }}
  }}
  
  // If no words matched and the speech segment is final, flag an error
  if(!matchedAny && isFinal && arr.length > 0){{
     const lastWord = arr[arr.length-1];
     doBad(cur, lastWord, WDS[cur], sim(lastWord, WDS[cur]));
  }}
}}

function doOk(i,sp,exp,s){{
  setW(i,'ok');nOk++;ws=0;clrE();
  wR=wR.filter(r=>r.index!==i);
  wR.push({{index:i,expected:exp,spoken:sp,status:'correct',similarity:s}});
  cur=Math.max(cur,i+1);if(cur<WDS.length)act(cur);
  updS();updP();if(cur>=WDS.length)fin();}}

function speakIndian(word) {{
  try {{
    const u = new SpeechSynthesisUtterance(word);
    u.lang = 'en-IN';
    u.rate = 0.8;
    const voices = window.speechSynthesis.getVoices();
    const ind = voices.find(v => v.lang.includes('en-IN') || v.name.includes('India'));
    if(ind) u.voice = ind;
    window.speechSynthesis.speak(u);
  }} catch(e) {{}}
}}

function doBad(i,sp,exp,s){{
  playBuzz(); // Play the alarm sound!
  setW(i,'bad');nErr++;ws++;
  wR=wR.filter(r=>r.index!==i);
  wR.push({{index:i,expected:exp,spoken:sp,status:'wrong',similarity:s}});
  if(ws > 6) {{
    // After 6 wrong attempts, teacher speaks the word on EVERY subsequent wrong attempt
    speakIndian(exp);
    showE('🔊 Teacher says: "'+exp+'" · You said: "'+sp+'" · Attempt #'+ws+' — Listen & repeat!');
  }} else if(ws === 6) {{
    // On the 6th mistake, warn the user that help is coming
    showE('❌ Heard: "'+sp+'"   ·   Expected: "'+exp+'"   → One more mistake and your teacher will help you!');
  }} else {{
    showE('❌ Heard: "'+sp+'"   ·   Expected: "'+exp+'"   → Say again or skip ⏭');
  }}
  updS();
}}

function skipW(){{
  if(cur>=WDS.length||!listen)return;
  const exp=WDS[cur];setW(cur,'skip');nSk++;ws=0;clrE();
  wR=wR.filter(r=>r.index!==cur);
  wR.push({{index:cur,expected:exp,spoken:'',status:'skipped',similarity:0}});
  cur++;if(cur<WDS.length)act(cur);
  updS();updP();if(cur>=WDS.length)fin();}}

function stopR(){{
  listen=false;if(recog){{try{{recog.stop();}}catch(_){{}}}}
  rCtrl();if(nOk>0||cur>0)fin();}}

function fin(){{
  listen=false;if(recog){{try{{recog.stop();}}catch(_){{}}}}
  rCtrl();
  const elapsed=t0?(Date.now()-t0)/1000:1;
  const total=WDS.length;
  const acc=Math.round((nOk/total)*100);
  const wpm=Math.round((nOk/elapsed)*60);
  for(let i=cur;i<WDS.length;i++){{
    if(st2[i]==='wait'||st2[i]==='active'){{
      setW(i,'skip');wR.push({{index:i,expected:WDS[i],spoken:'',status:'skipped',similarity:0}});nSk++;}}}}
  wR.sort((a,b)=>a.index-b.index);
  fd={{accuracy:acc,wpm,reading_time_sec:Math.round(elapsed),total_words:total,
    correct_words:nOk,error_words:nErr,skipped_words:nSk,word_results:wR,finished:true}};
  const grade=acc>=90?'🌟 Excellent!':acc>=75?'👍 Good Job!':acc>=50?'📖 Keep Practicing!':'💪 Try Again!';
  document.getElementById('rp').textContent=acc+'%';
  document.getElementById('rg2').textContent=grade;
  document.getElementById('ro').textContent=nOk;
  document.getElementById('re').textContent=nErr;
  document.getElementById('rs').textContent=nSk;
  document.getElementById('rw').textContent=wpm;
  document.getElementById('rb').textContent='Reading time: '+Math.round(elapsed)+'s · '+total+' total words';
  document.getElementById('ov').classList.add('show');}}

function submitResult(){{
  if(!fd)return;
  const payload=JSON.stringify(fd);
  // Post to parent window (Streamlit's iframe listener)
  try{{window.parent.postMessage({{isStreamlitMessage:true,type:'streamlit:setComponentValue',value:payload}},'*');}}catch(_){{}}
  // Write to the hidden textarea in the parent DOM that Streamlit watches
  try{{
    const frames=window.parent.document.querySelectorAll('iframe');
    for(const f of frames){{
      try{{
        const inputs=f.contentDocument.querySelectorAll('textarea');
        for(const inp of inputs){{
          if(inp.placeholder&&inp.placeholder.includes('finished')){{
            inp.value=payload;
            inp.dispatchEvent(new Event('input',{{bubbles:true}}));
            break;}}}}}}catch(_){{}}}}}}catch(_){{}}
  // Fallback: copy to clipboard so user can paste manually
  if(navigator.clipboard){{
    navigator.clipboard.writeText(payload).then(()=>{{
      document.getElementById('bdone').textContent='✅ Copied! Paste below ↓';
      document.getElementById('bdone').disabled=true;
    }}).catch(()=>{{
      document.getElementById('bdone').textContent='✅ Done! Scroll down ↓';
      document.getElementById('bdone').disabled=true;}});
  }}else{{
    document.getElementById('bdone').textContent='✅ Done! Scroll down ↓';
    document.getElementById('bdone').disabled=true;}}}}

function rCtrl(){{
  document.getElementById('bs').disabled=false;
  document.getElementById('bk').disabled=true;
  document.getElementById('bt').disabled=true;
  document.getElementById('md').classList.remove('on');}}
function setHd(m){{document.getElementById('hd').textContent=m;}}
function showE(m){{
  const b=document.getElementById('eb');b.textContent=m;b.classList.remove('hidden');
  clearTimeout(eT);eT=setTimeout(()=>b.classList.add('hidden'),6000);}}
function clrE(){{clearTimeout(eT);document.getElementById('eb').classList.add('hidden');}}
function updP(){{document.getElementById('pg').style.width=(WDS.length?(cur/WDS.length*100):0)+'%';}}
function updS(){{
  const done=nOk+nErr;
  document.getElementById('so').textContent=nOk;
  document.getElementById('se').textContent=nErr;
  document.getElementById('sa').textContent=done?Math.round(nOk/done*100)+'%':'—';
  if(t0&&nOk>0)document.getElementById('sw').textContent=Math.round(nOk/((Date.now()-t0)/60000));
  else document.getElementById('sw').textContent='—';}}
</script></body></html>"""

    components.html(html, height=680, scrolling=False)
