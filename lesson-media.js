import {lessonMedia} from './lesson-media-data.js?v=8';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const time=s=>`${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
export function mediaCount(chapter){const rows=lessonMedia[chapter]||[];return `${rows.filter(r=>r.kind==='image').length} hình · ${rows.filter(r=>r.kind==='video').length} video`;}
function renderMedia(r){
 if(r.kind==='video'){
  const detail=r.detailed;
  return `<figure class="lesson-media video-figure ${detail?'detailed-video':''}" ${detail?`id="video-${esc(r.id)}"`:''}>
<div class="media-heading"><span class="media-kind">▶ ${detail?'VIDEO TỪNG BƯỚC':'XEM NHANH'} · ${time(r.duration)}${detail?' · 5 BƯỚC':''}</span><h3>${esc(r.title)}</h3>${detail?`<p class="video-goal">${esc(r.goal)}</p>`:''}</div>
<video controls playsinline preload="none" poster="${esc(r.poster)}" aria-label="${esc(r.title)}" ${detail?`data-video-id="${esc(r.id)}"`:''}><source src="${esc(r.src)}" type="video/mp4"><track kind="captions" src="${esc(r.track)}" srclang="vi" label="Tiếng Việt"><p><a href="${esc(r.src)}">Mở video mô phỏng</a></p></video>
${detail?`<div class="video-tools"><span class="video-step-status" aria-label="Bước hiện tại">Sẵn sàng · 5 bước</span><label>Tốc độ <select class="video-speed" aria-label="Tốc độ: ${esc(r.title)}">${[.5,.75,1,1.25,1.5,2].map(v=>`<option value="${v}" ${v===1?'selected':''}>${v}×</option>`).join('')}</select></label><button class="text-button video-restart" type="button">↺ Xem từ đầu</button></div><details class="video-walkthrough"><summary>5 bước giải thích · Nhấn mốc thời gian để xem lại</summary><ol>${r.steps.map((s,i)=>`<li data-step-row="${i}"><button class="video-seek" data-seek="${s.start}" data-step-index="${i}" type="button" aria-label="Xem bước ${i+1} lúc ${time(s.start)}: ${esc(s.title)}"><span>${time(s.start)}</span><strong>${i+1}. ${esc(s.title)}</strong><span aria-hidden="true">▶</span></button><p>${esc(s.text)}</p><div class="step-formula">${esc(s.formula)}</div></li>`).join('')}</ol></details>`:''}
<figcaption><strong>${detail?'Điều cần nhớ':'Chú ý khi xem'}</strong> ${esc(r.caption)}<span class="media-source">Ví dụ và sơ đồ minh họa · Chú thích tiếng Việt trong video · Không có lời thoại.</span>${detail?`<a class="media-source" href="${esc(r.source)}" target="_blank" rel="noopener">Đối chiếu slide · trang PDF ${Number(r.source.split('#page=')[1])} ↗</a>`:''}</figcaption></figure>`;
 }
 return `<figure class="lesson-media"><div class="media-heading"><span class="media-kind">${r.derived?'SƠ ĐỒ MINH HỌA · THEO SLIDE':'HÌNH TỪ SLIDE · TRANG PDF '+r.page}</span><h3>${esc(r.title)}</h3></div><button class="slide-zoom" type="button" data-zoom-src="${esc(r.src)}" data-zoom-title="${esc(r.title)}" data-zoom-alt="${esc(r.alt)}" aria-label="Phóng to: ${esc(r.title)}"><img src="${esc(r.src)}" alt="${esc(r.alt)}" width="${r.width}" height="${r.height}" loading="lazy" decoding="async"><span>⤢ Nhấn để phóng to</span></button><figcaption><strong>Nhìn để nhớ</strong> ${esc(r.caption)}<a class="media-source" href="${esc(r.source)}" target="_blank" rel="noopener">Mở trang slide gốc ↗</a></figcaption></figure>`;
}
export function renderLessonBody(lesson){
 const media=lessonMedia[lesson.chapter]||[],blocks=[];let block={heading:'',sections:[]};
 for(const s of lesson.sections){if(s.kind==='heading'){blocks.push(block);block={heading:s.text,sections:[]};}else block.sections.push(s);}
 blocks.push(block);
 const ids=new Map(blocks.filter(b=>b.heading).map((b,i)=>[b,`lesson-topic-${i}`]));
 const used=new Set();
 const body=blocks.map(b=>{const visuals=media.filter(r=>b.heading.startsWith(r.anchor)&&/^(?:\s|$)/.test(b.heading.slice(r.anchor.length)));visuals.forEach(r=>used.add(r));return `<section class="lesson-topic"${b.heading?` id="${ids.get(b)}"`:''}>${b.heading?`<h2>${esc(b.heading)}</h2>`:''}${b.sections.map(s=>`<p class="${s.kind==='bullet'?'bullet':''}">${esc(s.text)}</p>`).join('')}${visuals.map(renderMedia).join('')}</section>`;}).join('');
 if(used.size!==media.length)throw Error('Unmatched lesson media anchor: '+lesson.chapter);
 const detailed=media.filter(r=>r.detailed);
 return `<div class="lesson-visual-intro"><span class="media-kind">HỌC BẰNG HÌNH ẢNH</span><p>${mediaCount(lesson.chapter)} ngay trong bài. Mỗi video từng bước có ví dụ, công thức và 5 mốc để dừng hoặc tua lại.</p><div class="chapter-video-library"><h2>Video chương ${lesson.chapter}</h2><p class="library-hint">Chọn một kỹ thuật để xem · ${detailed.length} video từng bước · ${time(detailed.reduce((a,r)=>a+r.duration,0))} nội dung</p><div class="chapter-video-links">${detailed.map((r,i)=>`<a href="#video-${esc(r.id)}"><span class="video-number">${String(i+1).padStart(2,'0')}</span><span><strong>${esc(r.title)}</strong><small>5 bước · ${time(r.duration)}</small></span><span aria-hidden="true">↗</span></a>`).join('')}</div></div><details class="lesson-toc"><summary>Đi nhanh đến chủ đề</summary><nav aria-label="Mục lục chương">${blocks.filter(b=>b.heading).map(b=>`<a href="#${ids.get(b)}">${esc(b.heading)}</a>`).join('')}</nav></details></div>${body}`;
}
export function bindLessonMedia(root){
 root.querySelectorAll('[data-zoom-src]').forEach(b=>b.addEventListener('click',()=>{
  const d=document.createElement('dialog');d.className='media-lightbox';d.setAttribute('aria-label',b.dataset.zoomTitle);
  d.innerHTML=`<div class="lightbox-bar"><strong>${esc(b.dataset.zoomTitle)}</strong><button class="secondary" type="button" autofocus>Đóng ✕</button></div><div class="lightbox-scroll"><img src="${esc(b.dataset.zoomSrc)}" alt="${esc(b.dataset.zoomAlt)}"></div><p>Cuộn ngang hoặc dọc để xem chi tiết · Esc để đóng</p>`;
  document.body.append(d);d.querySelector('button').onclick=()=>d.close();d.addEventListener('click',e=>{if(e.target===d)d.close();});d.addEventListener('close',()=>{d.remove();b.focus();},{once:true});d.showModal();
 }));
 root.querySelectorAll('.video-figure').forEach(card=>{
  const video=card.querySelector('video');
  // Keep one explanation playing at a time when moving through a long chapter.
  video.addEventListener('play',()=>root.querySelectorAll('video').forEach(other=>{if(other!==video)other.pause();}));
  if(!card.classList.contains('detailed-video'))return;
  const row=[...card.querySelectorAll('[data-step-row]')],seekButtons=[...card.querySelectorAll('[data-seek]')],status=card.querySelector('.video-step-status');
  function update(){const index=Math.min(4,Math.floor(video.currentTime/8));status.textContent=`Bước ${index+1} / 5 · ${time(video.currentTime)} / 0:40`;row.forEach((el,i)=>el.classList.toggle('is-current-step',i===index));seekButtons.forEach((b,i)=>{if(i===index)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});}
  function seekTo(seconds){video.currentTime=seconds;update();video.scrollIntoView({block:'center',behavior:'smooth'});video.play().catch(()=>{status.textContent='Nhấn ▶ trên video để phát.';});}
  seekButtons.forEach(b=>b.addEventListener('click',()=>seekTo(Number(b.dataset.seek))));
  card.querySelector('.video-restart').onclick=()=>seekTo(0);
  card.querySelector('.video-speed').onchange=e=>{video.playbackRate=Number(e.target.value);};
  video.addEventListener('timeupdate',update);video.addEventListener('loadedmetadata',update);
  video.addEventListener('error',()=>{status.textContent='Chưa tải được video. Thử tải lại trang.';});
 });
}
