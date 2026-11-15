import {lectures} from './lecture-data.js?v=5';
import {legacyLectures} from './lecture-legacy-data.js?v=1';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const time=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
const SPEED_KEY='lecture-speed',WATCHED_KEY='lecture-watched-v1',TAB_KEY='lecture-tab';
const KIND={intro:'Mở đầu',method:'Phương pháp',extra:'Mở rộng',summary:'Tổng kết'};
const readSpeed=()=>{try{return Number(localStorage.getItem(SPEED_KEY))||1}catch{return 1}};
const saveSpeed=v=>{try{localStorage.setItem(SPEED_KEY,String(v))}catch{}};
const readWatched=()=>{try{return JSON.parse(localStorage.getItem(WATCHED_KEY)||'{}')||{}}catch{return {}}};
const saveWatched=w=>{try{localStorage.setItem(WATCHED_KEY,JSON.stringify(w))}catch{}};
const readTab=()=>{try{return localStorage.getItem(TAB_KEY)==='old'?'old':'new'}catch{return 'new'}};
const saveTab=t=>{try{localStorage.setItem(TAB_KEY,t)}catch{}};
const speedSelect=speed=>`<label>Tốc độ <select class="lecture-speed" aria-label="Tốc độ phát">${[.75,1,1.25,1.5,1.75,2].map(v=>`<option value="${v}" ${v===speed?'selected':''}>${v}×</option>`).join('')}</select></label><button class="text-button lecture-cc" type="button" aria-pressed="true">CC Phụ đề</button>`;
const videoInner=v=>`<source src="${esc(v.src)}" type="video/mp4"><track kind="captions" src="${esc(v.track)}" srclang="vi" label="Tiếng Việt" default>${v.chapters?`<track kind="chapters" src="${esc(v.chapters)}" srclang="vi" label="Mục lục">`:''}<p><a href="${esc(v.src)}">Mở video bài giảng</a></p>`;
const outlineItems=v=>v.outline.map((p,i)=>`<li><button type="button" data-lecture-seek="${p.start}" data-lecture-part="${i}" data-title="${esc(p.beat?`${p.beat}: ${p.title}`:p.title)}"><span>${time(p.start)}</span><strong>${p.beat?`<em>${esc(p.beat)}</em>`:''}${esc(p.title)}</strong></button></li>`).join('');

export const hasLecture=chapter=>Boolean(lectures[chapter]||legacyLectures[chapter]);
export function lectureLabel(chapter){
 const l=lectures[chapter];
 if(!l)return legacyLectures[chapter]?`▶ Video bài giảng · ${time(legacyLectures[chapter].duration)}`:'';
 return l.stories?`▶ ${l.stories.length} video kể chuyện · ${time(l.duration)}`:`▶ Video bài giảng · ${time(l.duration)}`;
}

export function renderLecture(chapter){
 const l=lectures[chapter],old=legacyLectures[chapter];
 if(!l&&!old)return '';
 const main=l?(l.stories?renderStories(chapter,l):renderSingle(chapter,l)):'';
 if(!l||!old||!l.stories)return main||renderSingle(chapter,old);
 const tab=readTab();
 return `<div class="lecture-tabs" role="tablist" aria-label="Chọn loại video">
<button type="button" role="tab" data-lecture-tab="new" aria-selected="${tab==='new'}">Video kể chuyện <small>${l.stories.length} video · ${time(l.duration)}</small></button>
<button type="button" role="tab" data-lecture-tab="old" aria-selected="${tab==='old'}">Bài giảng cũ <small>cả chương · ${time(old.duration)}</small></button>
</div>
<div role="tabpanel" data-lecture-panel="new" ${tab==='new'?'':'hidden'}>${main}</div>
<div role="tabpanel" data-lecture-panel="old" ${tab==='old'?'':'hidden'}>${renderSingle(chapter,old)}</div>`;
}

function renderSingle(chapter,l){
 return `<section class="lecture" aria-label="Video bài giảng chương ${chapter}">
<div class="lecture-player"><video class="lecture-video" controls playsinline preload="metadata" poster="${esc(l.poster)}">${videoInner(l)}</video></div>
<div class="lecture-tools"><span class="lecture-now" aria-live="polite">Giảng bằng tiếng Việt · ${time(l.duration)} · ${l.outline.length} phần</span>${speedSelect(readSpeed())}</div>
<ol class="lecture-outline">${outlineItems(l)}</ol>
</section>`;
}

function renderStories(chapter,l){
 const watched=new Set(readWatched()[chapter]||[]);
 const first=l.stories[Math.max(0,l.stories.findIndex(s=>!watched.has(s.id)))];
 return `<section class="lecture" data-lecture-chapter="${chapter}" aria-label="Video kể chuyện chương ${chapter}">
<div class="lecture-player"><video class="lecture-video" controls playsinline preload="metadata" poster="${esc(first.poster)}">${videoInner(first)}</video></div>
<div class="lecture-tools"><span class="lecture-now" aria-live="polite"></span>${speedSelect(readSpeed())}</div>
<div class="lecture-next" hidden><span>Xong video này.</span><button class="primary lecture-next-button" type="button"></button></div>
<div class="story-list"><div class="story-list-head"><h2>${l.stories.length} video · ${time(l.duration)}</h2><span class="story-progress"></span></div>
<ol>${l.stories.map((s,i)=>`<li><button type="button" data-story="${i}"><span class="story-num">${String(i).padStart(2,'0')}</span><span class="story-text"><strong>${esc(s.title)}</strong><small>${KIND[s.kind]||''} · ${time(s.duration)}</small></span><span class="story-tick" aria-label="Đã xem">✓</span></button></li>`).join('')}</ol></div>
<details class="story-beats" open><summary>Các nhịp của video đang xem · nhấn để tua</summary><ol class="lecture-outline"></ol></details>
</section>`;
}

export function bindLecture(root,onFinish){
 const sections=[...root.querySelectorAll('section.lecture')];
 sections.forEach(section=>bindSection(section,onFinish));
 const tabs=[...root.querySelectorAll('[data-lecture-tab]')];
 tabs.forEach(tab=>tab.onclick=()=>{
  const name=tab.dataset.lectureTab;saveTab(name);
  tabs.forEach(t=>t.setAttribute('aria-selected',String(t===tab)));
  root.querySelectorAll('[data-lecture-panel]').forEach(p=>p.hidden=p.dataset.lecturePanel!==name);
  sections.forEach(s=>s.querySelector('video')?.pause());
 });
}

function bindSection(section,onFinish){
 const video=section.querySelector('.lecture-video');
 if(!video)return;
 const chapter=section.dataset.lectureChapter;
 const now=section.querySelector('.lecture-now'),speed=section.querySelector('.lecture-speed'),cc=section.querySelector('.lecture-cc');
 let ccOn=true,parts=[],starts=[],label='';
 const applyCc=()=>{const track=video.textTracks[0];if(track)track.mode=ccOn?'showing':'hidden';cc.setAttribute('aria-pressed',String(ccOn));};
 video.playbackRate=readSpeed();
 video.addEventListener('loadedmetadata',()=>{video.playbackRate=readSpeed();applyCc();});
 speed.onchange=()=>{const v=Number(speed.value);video.playbackRate=v;saveSpeed(v);};
 cc.onclick=()=>{ccOn=!ccOn;applyCc();};
 const bindOutline=()=>{
  parts=[...section.querySelectorAll('[data-lecture-part]')];starts=parts.map(b=>Number(b.dataset.lectureSeek));
  parts.forEach(b=>b.onclick=()=>{video.currentTime=Number(b.dataset.lectureSeek)+.05;video.play().catch(()=>{});video.scrollIntoView({block:'nearest',behavior:'smooth'});});
 };
 const showPart=()=>{
  let i=starts.length-1;while(i>0&&video.currentTime<starts[i])i--;
  parts.forEach((b,j)=>b.classList.toggle('active',j===i));
  if(parts[i])now.textContent=`${label}Phần ${i+1}/${parts.length} · ${parts[i].dataset.title}`;
 };
 if(!chapter){
  let finished=false;bindOutline();
  video.addEventListener('timeupdate',()=>{showPart();if(!finished&&video.duration&&video.currentTime/video.duration>.9){finished=true;onFinish?.();}});
  return;
 }
 const stories=lectures[chapter].stories,buttons=[...section.querySelectorAll('[data-story]')];
 const outline=section.querySelector('.story-beats ol'),next=section.querySelector('.lecture-next'),nextButton=section.querySelector('.lecture-next-button'),progress=section.querySelector('.story-progress');
 const watched=new Set(readWatched()[chapter]||[]);
 let current=-1,counted=false;
 const paint=()=>{
  buttons.forEach((b,i)=>{b.classList.toggle('active',i===current);b.classList.toggle('watched',watched.has(stories[i].id));if(i===current)b.setAttribute('aria-current','true');else b.removeAttribute('aria-current');});
  progress.textContent=`Đã xem ${stories.filter(s=>watched.has(s.id)).length}/${stories.length}`;
 };
 const markWatched=()=>{
  if(counted)return;counted=true;watched.add(stories[current].id);
  const all=readWatched();all[chapter]=[...watched];saveWatched(all);paint();
  if(stories.every(s=>watched.has(s.id)))onFinish?.();
 };
 const load=(i,play)=>{
  current=i;counted=false;const s=stories[i];
  label=`Video ${String(i).padStart(2,'0')} · `;
  video.poster=s.poster;video.innerHTML=videoInner(s);video.load();
  outline.innerHTML=outlineItems(s);bindOutline();
  now.textContent=`${label}${s.title} · ${time(s.duration)}`;
  next.hidden=true;paint();
  if(play)video.play().catch(()=>{});
 };
 buttons.forEach((b,i)=>b.onclick=()=>{load(i,true);video.scrollIntoView({block:'nearest',behavior:'smooth'});});
 video.addEventListener('timeupdate',()=>{showPart();if(video.duration&&video.currentTime/video.duration>.9)markWatched();});
 video.addEventListener('ended',()=>{
  markWatched();
  if(current+1<stories.length){nextButton.textContent=`Tiếp: ${stories[current+1].title} →`;next.hidden=false;nextButton.onclick=()=>load(current+1,true);}
 });
 load(Math.max(0,stories.findIndex(s=>!watched.has(s.id))),false);
}
