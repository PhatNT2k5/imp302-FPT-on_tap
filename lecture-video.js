import {lectures} from './lecture-data.js?v=1';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const time=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
const SPEED_KEY='lecture-speed';
const readSpeed=()=>{try{return Number(localStorage.getItem(SPEED_KEY))||1}catch{return 1}};
const saveSpeed=v=>{try{localStorage.setItem(SPEED_KEY,String(v))}catch{}};

export const hasLecture=chapter=>Boolean(lectures[chapter]);
export function lectureLabel(chapter){const l=lectures[chapter];return l?`▶ Video bài giảng · ${time(l.duration)}`:'';}

export function renderLecture(chapter){
 const l=lectures[chapter];
 if(!l)return '';
 const speed=readSpeed();
 return `<section class="lecture" aria-label="Video bài giảng chương ${chapter}">
<div class="lecture-player"><video id="lecture-video" controls playsinline preload="metadata" poster="${esc(l.poster)}"><source src="${esc(l.src)}" type="video/mp4"><track kind="captions" src="${esc(l.track)}" srclang="vi" label="Tiếng Việt" default><p><a href="${esc(l.src)}">Mở video bài giảng</a></p></video></div>
<div class="lecture-tools"><span class="lecture-now" aria-live="polite">Giảng bằng tiếng Việt · ${time(l.duration)} · ${l.outline.length} phần</span><label>Tốc độ <select id="lecture-speed" aria-label="Tốc độ phát">${[.75,1,1.25,1.5,1.75,2].map(v=>`<option value="${v}" ${v===speed?'selected':''}>${v}×</option>`).join('')}</select></label><button class="text-button" id="lecture-cc" type="button" aria-pressed="true">CC Phụ đề</button></div>
<ol class="lecture-outline">${l.outline.map((p,i)=>`<li><button type="button" data-lecture-seek="${p.start}" data-lecture-part="${i}"><span>${time(p.start)}</span><strong>${esc(p.title)}</strong></button></li>`).join('')}</ol>
</section>`;
}

export function bindLecture(root,onFinish){
 const video=root.querySelector('#lecture-video');
 if(!video)return;
 const parts=[...root.querySelectorAll('[data-lecture-part]')];
 const now=root.querySelector('.lecture-now');
 const speed=root.querySelector('#lecture-speed');
 const cc=root.querySelector('#lecture-cc');
 const starts=parts.map(b=>Number(b.dataset.lectureSeek));
 let finished=false;
 video.playbackRate=readSpeed();
 video.addEventListener('loadedmetadata',()=>{video.playbackRate=readSpeed();});
 speed.onchange=()=>{const v=Number(speed.value);video.playbackRate=v;saveSpeed(v);};
 cc.onclick=()=>{const track=video.textTracks[0];if(!track)return;const on=track.mode!=='showing';track.mode=on?'showing':'hidden';cc.setAttribute('aria-pressed',String(on));};
 parts.forEach(b=>b.onclick=()=>{video.currentTime=Number(b.dataset.lectureSeek)+.05;video.play().catch(()=>{});video.scrollIntoView({block:'nearest',behavior:'smooth'});});
 video.addEventListener('timeupdate',()=>{
  let i=starts.length-1;while(i>0&&video.currentTime<starts[i])i--;
  parts.forEach((b,j)=>b.classList.toggle('active',j===i));
  if(parts[i])now.textContent=`Phần ${i+1}/${parts.length} · ${parts[i].querySelector('strong').textContent}`;
  if(!finished&&video.duration&&video.currentTime/video.duration>.9){finished=true;onFinish?.();}
 });
}
