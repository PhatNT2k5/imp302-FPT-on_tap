export function begin(ids, section, size) {
  return {section,size,ids:[...ids],queue:[...ids],position:0,retry:[],mastered:[],errors:0,round:1,feedback:null,selected:[],done:false};
}
export function sameSet(a,b) {return a.length===b.length&&new Set(a).size===a.length&&a.every(x=>b.includes(x));}
export function grade(state, selected, correct) {
  if(state.done||state.feedback) return state;
  const s=structuredClone(state), id=s.queue[s.position];
  s.selected=[...selected];
  const ok=sameSet(selected,correct);
  s.feedback=ok?'correct':'wrong';
  if(ok) {if(!s.mastered.includes(id)) s.mastered.push(id);}
  else {s.errors++;if(!s.retry.includes(id))s.retry.push(id);}
  return s;
}
export function advance(state) {
  if(!state.feedback||state.done)return state;
  const s=structuredClone(state);s.feedback=null;s.selected=[];s.position++;
  if(s.position>=s.queue.length) {
    if(s.retry.length){s.queue=[...s.retry];s.retry=[];s.position=0;s.round++;}
    else s.done=true;
  }
  return s;
}
