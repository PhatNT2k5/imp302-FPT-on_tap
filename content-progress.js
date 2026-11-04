// Session rows for a mode and a filter: 'all', 'ch<N>' (chapter) or an exam id such as 'pt1'.
export function rowsFor(items,type,filter='all',stars={}){
 const rows=items.filter(r=>r.type===type);
 if(filter==='all')return rows;
 if(filter==='star')return rows.filter(r=>stars[r.id]);
 if(filter.startsWith('ch'))return rows.filter(r=>r.chapter===Number(filter.slice(2)));
 return rows.filter(r=>(r.exams||[]).includes(filter)).sort((a,b)=>Math.min(...a[filter+'Numbers'])-Math.min(...b[filter+'Numbers']));
}
// Retain prior sessions unless their membership or learned answer changed.
export function reconcileProgress(db,items,meta){
 const byId=new Map(items.map(r=>[r.id,r]));
 const legacyChanged=new Set(db.contentRevision===meta.revision?[]:(meta.relearnExistingIds||[]));
 for(const [key,s] of Object.entries(db.sessions||{})){
  const expected=rowsFor(items,s.type,s.filter,db.stars).slice(s.section*s.size,(s.section+1)*s.size).map(r=>r.id);
  const sameMembers=Array.isArray(s.ids)&&expected.length===s.ids.length&&s.ids.every(id=>expected.includes(id));
  const changed=!sameMembers||s.ids.some(id=>!byId.has(id)||(s.signatures?s.signatures[id]!==byId.get(id).contentSignature:legacyChanged.has(id)));
  if(changed){delete db.sessions[key];delete db.completed[key];}
  else s.signatures=Object.fromEntries(s.ids.map(id=>[id,byId.get(id).contentSignature]));
 }
 for(const id of legacyChanged)delete db.progress[id];
 db.contentRevision=meta.revision;
 return db;
}
