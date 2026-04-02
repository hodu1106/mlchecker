from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>메이플랜드 경험치 측정기</title>
  <style>
    :root{--bg:#0b1020;--bg2:#121933;--card:rgba(18,25,51,.72);--line:rgba(255,255,255,.10);--text:#eef2ff;--muted:#a7b0d1;--accent:#7c9cff;--accent2:#4de2c5;--danger:#ff7f9f;--warning:#ffcf66;--shadow:0 18px 40px rgba(0,0,0,.35);--radius:22px;}
    *{box-sizing:border-box} html,body{margin:0;padding:0;background:radial-gradient(circle at top left, rgba(124,156,255,.16), transparent 28%),radial-gradient(circle at top right, rgba(77,226,197,.12), transparent 22%),linear-gradient(180deg, #0b1020 0%, #11182e 100%);color:var(--text);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
    .wrap{max-width:1240px;margin:0 auto;padding:28px 18px 80px} a{color:inherit}
    .hero{display:flex;justify-content:space-between;gap:24px;align-items:flex-start;flex-wrap:wrap;padding:26px;border:1px solid var(--line);border-radius:28px;background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));box-shadow:var(--shadow);backdrop-filter: blur(18px);}
    .brand h1{margin:0 0 10px;font-size:clamp(28px,5vw,44px);letter-spacing:-.03em}.brand p{margin:0;color:var(--muted);line-height:1.6;max-width:720px}
    .kbd{display:inline-flex;align-items:center;justify-content:center;min-width:30px;padding:0 10px;height:30px;border-radius:10px;border:1px solid var(--line);background:rgba(255,255,255,.05);color:#fff;font-size:13px;margin-left:6px}
    .hero-side{display:grid;gap:10px;min-width:260px}
    .mini-note{border:1px solid var(--line);border-radius:18px;padding:14px 16px;background:rgba(255,255,255,.04);color:var(--muted);font-size:14px;line-height:1.55;}
    .controls{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:22px}
    .btn{appearance:none;border:none;cursor:pointer;color:#fff;font-weight:700;letter-spacing:-.02em;background:linear-gradient(180deg, rgba(124,156,255,.88), rgba(86,109,214,.92));padding:15px 16px;border-radius:18px;box-shadow:0 14px 28px rgba(80,109,214,.35);transition:transform .14s ease, filter .14s ease, opacity .14s ease;}
    .btn:hover{transform:translateY(-1px);filter:brightness(1.04)} .btn:disabled{opacity:.45;cursor:not-allowed;transform:none}
    .btn.secondary{background:linear-gradient(180deg, rgba(255,255,255,.11), rgba(255,255,255,.07));border:1px solid var(--line);box-shadow:none}
    .btn.success{background:linear-gradient(180deg, rgba(77,226,197,.95), rgba(21,174,148,.95));box-shadow:0 14px 28px rgba(21,174,148,.28)}
    .btn.warn{background:linear-gradient(180deg, rgba(255,207,102,.95), rgba(208,146,18,.95));box-shadow:0 14px 28px rgba(208,146,18,.24)}
    .grid{display:grid;grid-template-columns:1.15fr .85fr;gap:18px;margin-top:18px}
    .card{border:1px solid var(--line);border-radius:26px;background:var(--card);backdrop-filter: blur(16px);box-shadow:var(--shadow);overflow:hidden}
    .card-head{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:18px 20px;border-bottom:1px solid var(--line)}
    .card-head h2,.card-head h3{margin:0;font-size:18px;letter-spacing:-.02em}.sub{color:var(--muted);font-size:13px}.body{padding:18px 20px}
    .capture-area{display:grid;gap:14px}.viewer-wrap{position:relative;aspect-ratio:16/9;background:#050814;border-radius:20px;overflow:hidden;border:1px solid var(--line)}
    video{width:100%;height:100%;object-fit:contain;background:#050814;display:block} #overlay{position:absolute;inset:0;cursor:crosshair}
    .hint{display:flex;flex-wrap:wrap;gap:10px;color:var(--muted);font-size:13px}.chip{display:inline-flex;align-items:center;gap:8px;padding:10px 12px;border-radius:999px;background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--muted);font-size:13px}
    .stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.stat{padding:18px;border-radius:20px;border:1px solid var(--line);background:rgba(255,255,255,.04)}
    .label{font-size:13px;color:var(--muted);margin-bottom:10px}.value{font-size:clamp(24px,4vw,38px);font-weight:800;letter-spacing:-.04em}.value.small{font-size:clamp(18px,3vw,28px)}.value .pct{font-size:.46em;color:var(--muted);font-weight:700}
    .pill{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.05);color:var(--muted);font-size:13px}
    .settings{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.field{display:grid;gap:8px}.field label{font-size:13px;color:var(--muted)}
    .field input,.field select,textarea{width:100%;background:rgba(255,255,255,.05);color:#fff;border:1px solid var(--line);border-radius:14px;padding:13px 14px;outline:none}
    .field input::placeholder,textarea::placeholder{color:#93a0cc}
    .graph-wrap{display:grid;gap:12px} canvas{width:100%;height:260px;background:linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));border:1px solid var(--line);border-radius:18px}
    .mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}.log{border-radius:18px;border:1px solid var(--line);background:rgba(255,255,255,.04);padding:14px;min-height:110px;color:#cbd4f6;white-space:pre-wrap;line-height:1.5;}
    .footer-note{margin-top:18px;color:var(--muted);font-size:13px;line-height:1.65}.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .badge-live{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;font-size:12px;background:rgba(77,226,197,.12);color:#bcfff3;border:1px solid rgba(77,226,197,.26)} .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
    @media (max-width:980px){.controls{grid-template-columns:repeat(2,minmax(0,1fr))}.grid{grid-template-columns:1fr}.settings,.two,.stats{grid-template-columns:1fr}}
    @media (max-width:620px){.wrap{padding:16px 12px 56px}.hero{padding:18px}.card-head,.body{padding:16px}.controls{grid-template-columns:1fr}}
  </style>
</head>
<body>
<div class="wrap">
  <section class="hero">
    <div class="brand">
      <h1>메이플랜드 경험치 측정기</h1>
      <p>화면 공유로 게임 창을 캡처하고, 선택한 영역의 경험치 숫자를 OCR로 읽어 실시간 페이스를 계산합니다. <strong>게임 메모리 접근이나 입력 자동화 없이</strong> 브라우저 화면 공유만 사용합니다.</p>
    </div>
    <div class="hero-side">
      <div class="mini-note">권장 브라우저: <strong>Chrome / Edge</strong><br>단축키: 시작/중지 <span class="kbd">Space</span> 초기화 <span class="kbd">R</span> PiP <span class="kbd">P</span></div>
      <div class="mini-note">OCR 특성상 글꼴, 해상도, UI 배율에 따라 오차가 있을 수 있습니다. 첫 사용 때는 경험치 숫자 부분만 정확히 박스로 지정해 주세요.</div>
    </div>
  </section>

  <div class="controls">
    <button class="btn" id="shareBtn">화면 공유 시작</button>
    <button class="btn success" id="measureBtn" disabled>측정 시작</button>
    <button class="btn secondary" id="stopBtn" disabled>측정 중지</button>
    <button class="btn warn" id="resetBtn">초기화</button>
    <button class="btn secondary" id="pipBtn">PiP 열기</button>
    <button class="btn secondary" id="copyTextBtn">결과 텍스트 복사</button>
  </div>

  <div class="grid">
    <section class="card">
      <div class="card-head">
        <div><h2>캡처 화면</h2><div class="sub">드래그해서 경험치 숫자 영역을 지정하세요.</div></div>
        <div id="liveBadge" class="badge-live" style="display:none"><span class="dot"></span>측정 중</div>
      </div>
      <div class="body capture-area">
        <div class="viewer-wrap" id="viewerWrap">
          <video id="video" playsinline autoplay muted></video>
          <canvas id="overlay"></canvas>
        </div>
        <div class="hint">
          <div class="chip">1) 화면 공유 시작</div>
          <div class="chip">2) 경험치 숫자 박스 지정</div>
          <div class="chip">3) 측정 시작</div>
          <div class="chip">4) OCR이 튀면 숫자 영역을 더 좁게</div>
        </div>
        <div class="two">
          <div class="field">
            <label>직접 초기 기준값 입력 (선택)</label>
            <input id="manualBaseInput" type="text" placeholder="예: 123456 또는 123,456">
          </div>
          <div class="field">
            <label>OCR 전처리 모드</label>
            <select id="preprocessSelect">
              <option value="threshold">흑백 강조</option>
              <option value="grayscale">그레이스케일</option>
              <option value="invert">반전 + 흑백</option>
            </select>
          </div>
        </div>
      </div>
    </section>

    <aside class="card">
      <div class="card-head">
        <div><h2>측정 정보</h2><div class="sub">1초 주기 · 숫자 인식 기반</div></div>
        <span class="pill" id="ocrStatus">OCR 대기 중</span>
      </div>
      <div class="body">
        <div class="stats">
          <div class="stat"><div class="label">경과된 시간</div><div class="value mono" id="elapsed">00:00:00</div></div>
          <div class="stat"><div class="label">다음 시간 되는 시각</div><div class="value small mono" id="nextHour">-</div></div>
          <div class="stat"><div class="label">현재까지 획득한 경험치</div><div class="value" id="gained">0 <span class="pct">[0.00%]</span></div></div>
          <div class="stat"><div class="label">페이스 (60분 기준)</div><div class="value" id="pace">0 <span class="pct">[0.00%]</span></div></div>
        </div>
        <div style="height:14px"></div>
        <div class="settings">
          <div class="field"><label>레벨업까지 필요 경험치 (선택)</label><input id="expToLevel" type="number" min="0" step="1" placeholder="예: 428280"></div>
          <div class="field"><label>측정 간격 (초)</label><input id="intervalSec" type="number" min="1" max="5" step="1" value="1"></div>
        </div>
        <div class="footer-note">퍼센트 계산은 <strong>레벨업까지 필요 경험치</strong>를 입력했을 때만 표시됩니다. 입력하지 않아도 숫자 기준 측정은 동작합니다.</div>
      </div>
    </aside>
  </div>

  <section class="card" style="margin-top:18px">
    <div class="card-head">
      <div><h3>전체 페이스 (60분 기준)</h3><div class="sub">최근 30초 누적 그래프</div></div>
      <button class="btn secondary" id="copyImageBtn" style="padding:10px 14px;border-radius:14px">결과 이미지 복사</button>
    </div>
    <div class="body graph-wrap">
      <canvas id="graph" width="1200" height="320"></canvas>
      <div class="log mono" id="logBox">데이터 없음</div>
    </div>
  </section>
</div>

<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const els = {shareBtn:$('shareBtn'),measureBtn:$('measureBtn'),stopBtn:$('stopBtn'),resetBtn:$('resetBtn'),pipBtn:$('pipBtn'),copyTextBtn:$('copyTextBtn'),copyImageBtn:$('copyImageBtn'),video:$('video'),overlay:$('overlay'),viewerWrap:$('viewerWrap'),elapsed:$('elapsed'),nextHour:$('nextHour'),gained:$('gained'),pace:$('pace'),ocrStatus:$('ocrStatus'),expToLevel:$('expToLevel'),intervalSec:$('intervalSec'),preprocessSelect:$('preprocessSelect'),manualBaseInput:$('manualBaseInput'),graph:$('graph'),logBox:$('logBox'),liveBadge:$('liveBadge')};
  const state = {stream:null,running:false,timer:null,ocrBusy:false,startAt:null,selection:null,displaySelection:null,baseExp:null,lastExp:null,history:[],lastRecognizedText:'',lastOCRAt:null,pipWindow:null};
  const key='ml-exp-tracker-settings';

  function loadSettings(){try{const s=JSON.parse(localStorage.getItem(key)||'{}'); if(s.expToLevel) els.expToLevel.value=s.expToLevel; if(s.intervalSec) els.intervalSec.value=s.intervalSec; if(s.preprocess) els.preprocessSelect.value=s.preprocess; if(s.manualBase) els.manualBaseInput.value=s.manualBase;}catch{}}
  function saveSettings(){localStorage.setItem(key, JSON.stringify({expToLevel:els.expToLevel.value, intervalSec:els.intervalSec.value, preprocess:els.preprocessSelect.value, manualBase:els.manualBaseInput.value}));}
  const formatNumber=(n)=>Number.isFinite(n)?Math.round(n).toLocaleString('ko-KR'):'0';
  const formatPct=(v)=>Number.isFinite(v)?v.toFixed(2):'0.00';
  function formatDuration(ms){const sec=Math.max(0,Math.floor(ms/1000));const h=String(Math.floor(sec/3600)).padStart(2,'0');const m=String(Math.floor((sec%3600)/60)).padStart(2,'0');const s=String(sec%60).padStart(2,'0');return `${h}:${m}:${s}`;}
  function calcPct(exp,total){if(!Number.isFinite(exp)||!Number.isFinite(total)||total<=0)return 0; return exp/total*100;}
  function setOCRStatus(t){els.ocrStatus.textContent=t;}
  function updateStats(){
    const now=Date.now(); const elapsedMs=state.startAt?(now-state.startAt):0; const gained=(state.baseExp!=null&&state.lastExp!=null)?Math.max(0,state.lastExp-state.baseExp):0;
    const total=Number(els.expToLevel.value||0)||0; const gainedPct=total?calcPct(gained,total):0; const pace=elapsedMs>0?(gained/elapsedMs)*3600000:0; const pacePct=total?calcPct(pace,total):0;
    els.elapsed.textContent=formatDuration(elapsedMs);
    if(state.startAt){const nextHourAt=new Date(state.startAt+3600000); els.nextHour.textContent=`${String(nextHourAt.getHours()).padStart(2,'0')}:${String(nextHourAt.getMinutes()).padStart(2,'0')}:${String(nextHourAt.getSeconds()).padStart(2,'0')}`;} else els.nextHour.textContent='-';
    els.gained.innerHTML=`${formatNumber(gained)} <span class="pct">[${formatPct(gainedPct)}%]</span>`;
    els.pace.innerHTML=`${formatNumber(pace)} <span class="pct">[${formatPct(pacePct)}%]</span>`;
    els.logBox.textContent=[
      `마지막 OCR: ${state.lastOCRAt ? new Date(state.lastOCRAt).toLocaleTimeString('ko-KR') : '-'}`,
      `마지막 인식 텍스트: ${state.lastRecognizedText || '-'}`,
      `현재 인식 경험치: ${state.lastExp != null ? formatNumber(state.lastExp) : '-'}`,
      `초기 기준 경험치: ${state.baseExp != null ? formatNumber(state.baseExp) : '-'}`,
      `최근 포인트 수: ${state.history.length}`
    ].join('\n');
    drawGraph();
    syncPiPStats();
  }
  function getVideoMetrics(){
    const rect=els.video.getBoundingClientRect(); if(!els.video.videoWidth||!els.video.videoHeight) return null;
    const aspectVideo=els.video.videoWidth/els.video.videoHeight; const aspectBox=rect.width/rect.height; let renderWidth,renderHeight,offsetX,offsetY;
    if(aspectVideo>aspectBox){renderWidth=rect.width; renderHeight=rect.width/aspectVideo; offsetX=0; offsetY=(rect.height-renderHeight)/2;}
    else {renderHeight=rect.height; renderWidth=rect.height*aspectVideo; offsetY=0; offsetX=(rect.width-renderWidth)/2;}
    return {rect,renderWidth,renderHeight,offsetX,offsetY};
  }
  function resizeOverlay(){const rect=els.viewerWrap.getBoundingClientRect(); els.overlay.width=rect.width*devicePixelRatio; els.overlay.height=rect.height*devicePixelRatio; els.overlay.style.width=rect.width+'px'; els.overlay.style.height=rect.height+'px'; const ctx=els.overlay.getContext('2d'); ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0); drawOverlay();}
  function drawOverlay(dragRect=null){
    const ctx=els.overlay.getContext('2d'); const rect=els.viewerWrap.getBoundingClientRect(); ctx.clearRect(0,0,rect.width,rect.height);
    ctx.fillStyle='rgba(0,0,0,.18)'; ctx.fillRect(0,0,rect.width,rect.height);
    const metrics=getVideoMetrics(); if(metrics){ctx.clearRect(metrics.offsetX,metrics.offsetY,metrics.renderWidth,metrics.renderHeight);}
    const drawRect=dragRect||state.displaySelection;
    if(drawRect){ctx.save(); ctx.strokeStyle='#7c9cff'; ctx.lineWidth=2; ctx.setLineDash([8,6]); ctx.strokeRect(drawRect.x,drawRect.y,drawRect.w,drawRect.h); ctx.fillStyle='rgba(124,156,255,.16)'; ctx.fillRect(drawRect.x,drawRect.y,drawRect.w,drawRect.h); ctx.restore();}
    else if(metrics){ctx.save(); ctx.fillStyle='rgba(255,255,255,.82)'; ctx.font='600 14px Inter, sans-serif'; ctx.fillText('여기를 드래그해서 경험치 숫자 영역을 선택', metrics.offsetX+16, metrics.offsetY+28); ctx.restore();}
  }
  function clampSelection(sel){const m=getVideoMetrics(); if(!m) return null; const x=Math.max(m.offsetX, Math.min(sel.x, m.offsetX+m.renderWidth)); const y=Math.max(m.offsetY, Math.min(sel.y, m.offsetY+m.renderHeight)); const maxW=m.offsetX+m.renderWidth-x; const maxH=m.offsetY+m.renderHeight-y; const w=Math.max(8, Math.min(sel.w,maxW)); const h=Math.max(8, Math.min(sel.h,maxH)); return {x,y,w,h};}
  function displayToVideoCrop(r){const m=getVideoMetrics(); if(!m) return null; return {x:Math.max(0,(r.x-m.offsetX)/m.renderWidth)*els.video.videoWidth, y:Math.max(0,(r.y-m.offsetY)/m.renderHeight)*els.video.videoHeight, w:Math.min(1,r.w/m.renderWidth)*els.video.videoWidth, h:Math.min(1,r.h/m.renderHeight)*els.video.videoHeight};}
  function setupSelection(){
    let dragging=false,start=null;
    function pointFromEvent(e){const rect=els.overlay.getBoundingClientRect(); const clientX=e.clientX??(e.touches&&e.touches[0]?.clientX)??0; const clientY=e.clientY??(e.touches&&e.touches[0]?.clientY)??0; return {x:clientX-rect.left,y:clientY-rect.top};}
    function down(e){if(!state.stream) return; dragging=true; start=pointFromEvent(e); drawOverlay(); e.preventDefault();}
    function move(e){if(!dragging) return; const p=pointFromEvent(e); drawOverlay({x:Math.min(start.x,p.x), y:Math.min(start.y,p.y), w:Math.abs(start.x-p.x), h:Math.abs(start.y-p.y)}); e.preventDefault();}
    function up(e){if(!dragging) return; dragging=false; const p=pointFromEvent(e); let rect={x:Math.min(start.x,p.x), y:Math.min(start.y,p.y), w:Math.abs(start.x-p.x), h:Math.abs(start.y-p.y)}; rect=clampSelection(rect); if(rect&&rect.w>=8&&rect.h>=8){state.displaySelection=rect; state.selection=displayToVideoCrop(rect);} drawOverlay(); e.preventDefault();}
    els.overlay.addEventListener('mousedown', down); window.addEventListener('mousemove', move); window.addEventListener('mouseup', up);
    els.overlay.addEventListener('touchstart', down, {passive:false}); window.addEventListener('touchmove', move, {passive:false}); window.addEventListener('touchend', up, {passive:false});
  }
  async function startShare(){
    saveSettings();
    try{
      const stream=await navigator.mediaDevices.getDisplayMedia({video:{displaySurface:"browser", frameRate:{ideal:10,max:15}}, audio:false});
      state.stream=stream; els.video.srcObject=stream; await els.video.play(); resizeOverlay(); els.measureBtn.disabled=false; els.stopBtn.disabled=true; syncPiPStats();
      stream.getVideoTracks()[0].addEventListener('ended', ()=>{stopMeasure(false); if(state.stream) state.stream.getTracks().forEach(t=>t.stop()); state.stream=null; els.video.srcObject=null; state.selection=null; state.displaySelection=null; drawOverlay(); setOCRStatus('화면 공유 종료'); els.measureBtn.disabled=true; els.stopBtn.disabled=true; syncPiPStats();});
      setOCRStatus('영역 지정 후 측정 시작');
    }catch(err){setOCRStatus('화면 공유 취소됨'); alert('화면 공유를 시작하지 못했습니다.');}
  }
  function parseOCRText(text){
    if(!text) return null; const normalized=text.replace(/\s+/g,' ').trim(); state.lastRecognizedText=normalized;
    const withoutPct=normalized.replace(/\[?\s*\d+(?:[.,]\d{1,2})?\s*%?\s*\]?/g,' ');
    let raw=(withoutPct.match(/\d[\d,.]{1,}/)||[])[0]; if(!raw){const fallback=normalized.match(/\d+/); raw=fallback?fallback[0]:null;} if(!raw) return null;
    const exp=Number(raw.replace(/[^\d]/g,'')); if(!Number.isFinite(exp)) return null; return {exp};
  }
  function preprocessCropToCanvas(crop){
    const c=document.createElement('canvas'); const scale=2; c.width=Math.max(1,Math.floor(crop.w*scale)); c.height=Math.max(1,Math.floor(crop.h*scale));
    const ctx=c.getContext('2d',{willReadFrequently:true}); ctx.drawImage(els.video,crop.x,crop.y,crop.w,crop.h,0,0,c.width,c.height);
    const img=ctx.getImageData(0,0,c.width,c.height), d=img.data, mode=els.preprocessSelect.value;
    for(let i=0;i<d.length;i+=4){const gray=.299*d[i]+.587*d[i+1]+.114*d[i+2]; let v=gray; if(mode==='grayscale'){v=gray;} else if(mode==='invert'){v=255-gray; v=v>140?255:0;} else {v=gray>150?255:0;} d[i]=d[i+1]=d[i+2]=v; d[i+3]=255;}
    ctx.putImageData(img,0,0); return c;
  }
  async function readOCR(){
    if(!state.running||state.ocrBusy||!state.selection||!state.stream) return; state.ocrBusy=true; setOCRStatus('OCR 분석 중');
    try{
      const cropCanvas=preprocessCropToCanvas(state.selection);
      const result=await Tesseract.recognize(cropCanvas,'eng',{logger:()=>{}, tessedit_char_whitelist:'0123456789,.[ ]%'});
      const parsed=parseOCRText(result.data.text||''); state.lastOCRAt=Date.now();
      if(parsed){
        if(state.baseExp==null){const manualBase=Number(String(els.manualBaseInput.value||'').replace(/[^\d]/g,'')); state.baseExp=Number.isFinite(manualBase)&&manualBase>0?manualBase:parsed.exp;}
        if(state.lastExp==null || parsed.exp>=state.lastExp) state.lastExp=parsed.exp;
        const elapsedMs=state.startAt?Date.now()-state.startAt:0; const gained=(state.baseExp!=null&&state.lastExp!=null)?Math.max(0,state.lastExp-state.baseExp):0; const pace=elapsedMs>0?(gained/elapsedMs)*3600000:0;
        state.history.push({ts:Date.now(), pace}); state.history=state.history.filter(p=>Date.now()-p.ts<=30000); setOCRStatus('OCR 정상');
      } else setOCRStatus('숫자 인식 실패');
    }catch(err){console.error(err); setOCRStatus('OCR 오류');}
    finally{state.ocrBusy=false; updateStats();}
  }
  function startMeasure(){if(!state.stream) return alert('먼저 화면 공유를 시작해 주세요.'); if(!state.selection) return alert('경험치 숫자 영역을 먼저 드래그해서 지정해 주세요.');
    saveSettings(); state.running=true; state.startAt=Date.now(); state.baseExp=null; state.lastExp=null; state.history=[]; els.liveBadge.style.display='inline-flex'; setOCRStatus('측정 시작'); els.measureBtn.disabled=true; els.stopBtn.disabled=false; updateStats();
    const interval=Math.max(1, Number(els.intervalSec.value||1))*1000; state.timer=setInterval(()=>{readOCR(); updateStats();}, interval); readOCR();
  }
  function stopMeasure(resetRunning=true){if(state.timer) clearInterval(state.timer); state.timer=null; if(resetRunning) state.running=false; els.liveBadge.style.display='none'; els.measureBtn.disabled=!state.stream||state.running; els.stopBtn.disabled=!state.stream||!state.running; updateStats();}
  function resetAll(){stopMeasure(); state.running=false; state.startAt=null; state.baseExp=null; state.lastExp=null; state.history=[]; state.lastRecognizedText=''; state.lastOCRAt=null; setOCRStatus('초기화됨'); els.measureBtn.disabled=!state.stream; els.stopBtn.disabled=true; updateStats();}
  function drawGraph(){
    const canvas=els.graph, ctx=canvas.getContext('2d'); const cssWidth=canvas.clientWidth||1200, cssHeight=canvas.clientHeight||320;
    canvas.width=cssWidth*devicePixelRatio; canvas.height=cssHeight*devicePixelRatio; ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0); ctx.clearRect(0,0,cssWidth,cssHeight);
    const w=cssWidth,h=cssHeight,pad={l:52,r:18,t:18,b:34}; const grad=ctx.createLinearGradient(0,0,0,h); grad.addColorStop(0,'rgba(124,156,255,.14)'); grad.addColorStop(1,'rgba(124,156,255,.02)'); ctx.fillStyle=grad; ctx.fillRect(0,0,w,h);
    const points=[...state.history], plotW=w-pad.l-pad.r, plotH=h-pad.t-pad.b; ctx.strokeStyle='rgba(255,255,255,.08)'; ctx.lineWidth=1;
    for(let i=0;i<5;i++){const y=pad.t+(plotH/4)*i; ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(w-pad.r,y); ctx.stroke();}
    if(!points.length){ctx.fillStyle='rgba(255,255,255,.72)'; ctx.font='600 16px Inter, sans-serif'; ctx.fillText('데이터 없음', pad.l, pad.t+24); return;}
    const maxPace=Math.max(...points.map(p=>p.pace),1), minTs=points[0].ts, maxTs=points[points.length-1].ts, tsSpan=Math.max(1,maxTs-minTs);
    ctx.strokeStyle='#7c9cff'; ctx.lineWidth=3; ctx.beginPath();
    points.forEach((p,idx)=>{const x=pad.l+((p.ts-minTs)/tsSpan)*plotW; const y=pad.t+plotH-(p.pace/maxPace)*plotH; if(idx===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);}); ctx.stroke();
    const areaGrad=ctx.createLinearGradient(0,pad.t,0,pad.t+plotH); areaGrad.addColorStop(0,'rgba(77,226,197,.28)'); areaGrad.addColorStop(1,'rgba(77,226,197,0)'); ctx.fillStyle=areaGrad; ctx.beginPath();
    points.forEach((p,idx)=>{const x=pad.l+((p.ts-minTs)/tsSpan)*plotW; const y=pad.t+plotH-(p.pace/maxPace)*plotH; if(idx===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);});
    ctx.lineTo(pad.l+plotW,pad.t+plotH); ctx.lineTo(pad.l,pad.t+plotH); ctx.closePath(); ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.75)'; ctx.font='12px Inter, sans-serif'; ctx.fillText('0s', pad.l, h-10); ctx.fillText('30s', w-pad.r-20, h-10); ctx.fillText(formatNumber(maxPace)+'/h', 8, pad.t+10);
  }
  async function copyResultText(){
    const now=new Date().toLocaleString('ko-KR'); const elapsedMs=state.startAt?Date.now()-state.startAt:0; const gained=(state.baseExp!=null&&state.lastExp!=null)?Math.max(0,state.lastExp-state.baseExp):0; const pace=elapsedMs>0?(gained/elapsedMs)*3600000:0; const total=Number(els.expToLevel.value||0)||0;
    const text=[`[메랜 경험치 측정 결과]`,`시간: ${now}`,`경과: ${formatDuration(elapsedMs)}`,`획득 경험치: ${formatNumber(gained)}${total?` (${formatPct(calcPct(gained,total))}%)`:''}`,`60분 페이스: ${formatNumber(pace)}${total?` (${formatPct(calcPct(pace,total))}%)`:''}`,`마지막 OCR: ${state.lastRecognizedText||'-'}`].join('\n');
    await navigator.clipboard.writeText(text); alert('결과 텍스트를 복사했습니다.');
  }
  function roundRect(ctx,x,y,w,h,r){ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath();}
  async function copyResultImage(){
    const c=document.createElement('canvas'); c.width=1400; c.height=900; const ctx=c.getContext('2d'); const grad=ctx.createLinearGradient(0,0,0,c.height); grad.addColorStop(0,'#0d1429'); grad.addColorStop(1,'#131d3c'); ctx.fillStyle=grad; ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle='#eef2ff'; ctx.font='800 52px Inter, sans-serif'; ctx.fillText('메이플랜드 경험치 측정 결과', 80, 110);
    const elapsedMs=state.startAt?Date.now()-state.startAt:0; const gained=(state.baseExp!=null&&state.lastExp!=null)?Math.max(0,state.lastExp-state.baseExp):0; const pace=elapsedMs>0?(gained/elapsedMs)*3600000:0; const total=Number(els.expToLevel.value||0)||0;
    function card(x,y,w,h,title,value,sub){ctx.fillStyle='rgba(255,255,255,.06)'; roundRect(ctx,x,y,w,h,28); ctx.fill(); ctx.strokeStyle='rgba(255,255,255,.10)'; ctx.stroke(); ctx.fillStyle='#a7b0d1'; ctx.font='500 24px Inter, sans-serif'; ctx.fillText(title,x+28,y+46); ctx.fillStyle='#ffffff'; ctx.font='800 48px Inter, sans-serif'; ctx.fillText(value,x+28,y+110); ctx.fillStyle='#9eb0ff'; ctx.font='600 22px Inter, sans-serif'; ctx.fillText(sub||'',x+28,y+150);}
    card(80,170,590,190,'경과된 시간', formatDuration(elapsedMs), '실시간 OCR 측정'); card(730,170,590,190,'획득 경험치', formatNumber(gained), total?`${formatPct(calcPct(gained,total))}%`:''); card(80,390,590,190,'60분 페이스', formatNumber(pace), total?`${formatPct(calcPct(pace,total))}%`:''); card(730,390,590,190,'마지막 OCR', (state.lastRecognizedText||'-').slice(0,24), '인식 원문');
    ctx.drawImage(els.graph,80,620,1240,210); ctx.fillStyle='#7d88b5'; ctx.font='500 20px Inter, sans-serif'; ctx.fillText('browser screen share · OCR only · no game memory access',80,860);
    const blob=await new Promise(res=>c.toBlob(res,'image/png')); await navigator.clipboard.write([new ClipboardItem({'image/png':blob})]); alert('결과 이미지를 클립보드에 복사했습니다.');
  }
  function syncPiPStats(){
    if(!state.pipWindow || state.pipWindow.closed) return;
    const doc = state.pipWindow.document;
    const elapsedMs=state.startAt?Date.now()-state.startAt:0;
    const gained=(state.baseExp!=null&&state.lastExp!=null)?Math.max(0,state.lastExp-state.baseExp):0;
    const pace=elapsedMs>0?(gained/elapsedMs)*3600000:0;
    const setText=(id,val)=>{ const el=doc.getElementById(id); if(el) el.textContent=val; };
    setText('pipElapsed', formatDuration(elapsedMs));
    setText('pipGained', formatNumber(gained));
    setText('pipPace', formatNumber(pace));
    setText('pipStatus', state.running ? '측정 중' : '대기 중');
    const startBtn = doc.getElementById('pipStartBtn');
    const stopBtn = doc.getElementById('pipStopBtn');
    if(startBtn) startBtn.disabled = !state.stream || state.running;
    if(stopBtn) stopBtn.disabled = !state.stream || !state.running;
  }

  async function openPiP(){
    if(!('documentPictureInPicture' in window)) return alert('이 브라우저에서는 Document Picture-in-Picture를 지원하지 않습니다. 최신 Chrome/Edge에서 시도해 주세요.');
    if(state.pipWindow && !state.pipWindow.closed){ state.pipWindow.focus(); return; }
    const pipWindow=await window.documentPictureInPicture.requestWindow({width:300,height:220});
    state.pipWindow=pipWindow;
    pipWindow.document.body.innerHTML=`<style>
      :root{color-scheme:dark}
      body{margin:0;padding:10px;background:#0d1429;color:#eef2ff;font-family:Inter,system-ui,sans-serif}
      .wrap{display:grid;gap:8px}
      .top{display:grid;grid-template-columns:1.2fr .8fr;gap:8px}
      .row{display:grid;grid-template-columns:1fr 1fr;gap:8px}
      .card{padding:10px 12px;border-radius:14px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.10)}
      .label{color:#a7b0d1;font-size:11px;margin-bottom:4px}
      .value{font-size:24px;font-weight:800;letter-spacing:-.04em;line-height:1.1}
      .value.small{font-size:17px}
      .status{display:inline-flex;align-items:center;justify-content:center;height:100%;min-height:58px;border-radius:14px;background:rgba(77,226,197,.12);border:1px solid rgba(77,226,197,.26);font-size:12px;font-weight:700;color:#bcfff3}
      .actions{display:grid;grid-template-columns:1fr 1fr;gap:7px}
      button{appearance:none;border:none;cursor:pointer;border-radius:12px;padding:10px 8px;font-size:12px;font-weight:800;color:#fff;background:linear-gradient(180deg, rgba(124,156,255,.88), rgba(86,109,214,.92))}
      button.secondary{background:linear-gradient(180deg, rgba(255,255,255,.11), rgba(255,255,255,.07));border:1px solid rgba(255,255,255,.10)}
      button.warn{background:linear-gradient(180deg, rgba(255,207,102,.95), rgba(208,146,18,.95))}
      button:disabled{opacity:.45;cursor:not-allowed}
    </style>
    <div class='wrap'>
      <div class='top'>
        <div class='card'><div class='label'>획득 경험치</div><div class='value' id='pipGained'>0</div></div>
        <div class='status' id='pipStatus'>대기 중</div>
      </div>
      <div class='row'>
        <div class='card'><div class='label'>경과</div><div class='value small' id='pipElapsed'>00:00:00</div></div>
        <div class='card'><div class='label'>60분 페이스</div><div class='value small' id='pipPace'>0</div></div>
      </div>
      <div class='actions'>
        <button id='pipStartBtn'>측정 시작</button>
        <button id='pipStopBtn' class='secondary'>측정 정지</button>
        <button id='pipResetBtn' class='warn'>초기화</button>
        <button id='pipCopyBtn' class='secondary'>결과 복사</button>
      </div>
    </div>`;
    pipWindow.document.getElementById('pipStartBtn').onclick = () => startMeasure();
    pipWindow.document.getElementById('pipStopBtn').onclick = () => { state.running=false; stopMeasure(); setOCRStatus('측정 중지'); };
    pipWindow.document.getElementById('pipResetBtn').onclick = () => resetAll();
    pipWindow.document.getElementById('pipCopyBtn').onclick = () => copyResultText();
    pipWindow.addEventListener('pagehide', () => { state.pipWindow = null; });
    syncPiPStats();
  }

  function bindEvents(){
    window.addEventListener('resize', resizeOverlay); els.video.addEventListener('loadedmetadata', resizeOverlay); els.shareBtn.addEventListener('click', startShare); els.measureBtn.addEventListener('click', startMeasure); els.stopBtn.addEventListener('click', ()=>{state.running=false; stopMeasure(); setOCRStatus('측정 중지');}); els.resetBtn.addEventListener('click', resetAll); els.copyTextBtn.addEventListener('click', copyResultText); els.copyImageBtn.addEventListener('click', copyResultImage); els.pipBtn.addEventListener('click', openPiP);
    [els.expToLevel, els.intervalSec, els.preprocessSelect, els.manualBaseInput].forEach(el=>{el.addEventListener('change', saveSettings); el.addEventListener('input', saveSettings);});
    window.addEventListener('keydown',(e)=>{if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName)) return; if(e.code==='Space'){e.preventDefault(); if(state.running){state.running=false; stopMeasure(); setOCRStatus('측정 중지');} else startMeasure();} else if(e.key?.toLowerCase()==='r'){e.preventDefault(); resetAll();} else if(e.key?.toLowerCase()==='p'){e.preventDefault(); openPiP();}});
  }

  loadSettings(); setupSelection(); bindEvents(); resizeOverlay(); updateStats();
})();
</script>
</body>
</html>'''
@app.route('/')
def index():
    return render_template_string(HTML)
if __name__ == '__main__':
    app.run(debug=True)
