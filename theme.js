/* Run before CSS to avoid a white flash when opening a saved dark theme. */
(()=>{
  const key='imp-theme';
  const system=window.matchMedia('(prefers-color-scheme: dark)');
  let saved=null;
  try{saved=localStorage.getItem(key);}catch{}
  let explicit=saved==='dark'||saved==='light';
  function apply(value){
    document.documentElement.dataset.theme=value;
    document.documentElement.style.colorScheme=value;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content',value==='dark'?'#111c18':'#f7f8f2');
    window.dispatchEvent(new Event('nhip-theme-change'));
  }
  apply(explicit?saved:system.matches?'dark':'light');
  window.nhipTheme={set(value){if(!['dark','light'].includes(value))return;explicit=true;apply(value);try{localStorage.setItem(key,value);}catch{}}};
  system.addEventListener?.('change',e=>{if(!explicit)apply(e.matches?'dark':'light');});
  window.addEventListener('storage',e=>{if(e.key!==key)return;explicit=e.newValue==='dark'||e.newValue==='light';apply(explicit?e.newValue:system.matches?'dark':'light');});
})();
