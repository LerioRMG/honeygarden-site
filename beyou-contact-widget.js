(()=>{
'use strict';
function init(){
 if(document.getElementById('be-contact'))return;
 const style=document.createElement('style');
 style.textContent=`
#be-contact{position:fixed;right:max(24px,env(safe-area-inset-right));bottom:calc(24px + env(safe-area-inset-bottom));z-index:9000;font-family:'DM Sans',Arial,sans-serif;color:#faf3e8}
#be-contact[hidden],#be-contact [hidden]{display:none!important}
#be-contact *{box-sizing:border-box}
#be-contact button,#be-contact a{-webkit-tap-highlight-color:transparent}
#be-contact .bc-toggle{width:60px;height:60px;padding:0;display:flex;align-items:center;justify-content:center;border:1px solid #e9b85f;border-radius:50%;background:#e9b85f;color:#15100d;cursor:pointer;box-shadow:0 6px 25px #0005;transition:transform .2s,background .2s}
#be-contact .bc-toggle:hover{transform:translateY(-2px);background:#f6d18d}
#be-contact svg{display:block;width:26px;height:26px}
#be-contact .bc-close{width:21px;height:21px}
#be-contact .bc-options{position:absolute;right:0;bottom:76px;display:flex;flex-direction:column;gap:12px;align-items:flex-end;min-width:0;animation:bc-enter .2s ease-out}
#be-contact .bc-link{display:flex;align-items:center;gap:12px;text-decoration:none;color:#faf3e8;font-size:13px;font-weight:500;white-space:nowrap}
#be-contact .bc-icon{display:flex;align-items:center;justify-content:center;width:50px;height:50px;border:1px solid #e9b85f;border-radius:50%;background:#15100d;color:#e9b85f;box-shadow:0 4px 16px #0004;transition:background .2s,transform .2s}
#be-contact .bc-link:hover .bc-icon{background:#2d261a;transform:translateY(-2px)}
#be-contact .bc-icon.bc-telegram{background:#fff;border-color:#fff;color:#26a5e4}
#be-contact .bc-telegram svg{width:50px;height:50px;fill:currentColor}
#be-contact .bc-icon.bc-whatsapp{background:#25d366;border-color:#25d366;color:#fff}
#be-contact .bc-whatsapp svg{width:29px;height:29px;fill:currentColor}
#be-contact .bc-link:hover .bc-telegram{background:#fff}
#be-contact .bc-link:hover .bc-whatsapp{background:#25d366}
#be-contact :focus-visible{outline:3px solid #faf3e8;outline-offset:5px}
@keyframes bc-enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:600px){#be-contact{right:max(16px,env(safe-area-inset-right));bottom:calc(16px + env(safe-area-inset-bottom))}#be-contact .bc-toggle{width:56px;height:56px}#be-contact .bc-options{bottom:72px}}
@media(prefers-reduced-motion:reduce){#be-contact *,#be-contact .bc-options{animation:none!important;transition:none!important}}
@media print{#be-contact{display:none!important}}
`;
 document.head.appendChild(style);
 const root=document.createElement('div');root.id='be-contact';root.setAttribute('aria-label','Contatta Honey Garden');
 const chat='<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 4.5h14a1.5 1.5 0 0 1 1.5 1.5v10a1.5 1.5 0 0 1-1.5 1.5h-8l-5 3v-3H5A1.5 1.5 0 0 1 3.5 16V6A1.5 1.5 0 0 1 5 4.5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="8" cy="11" r="1" fill="currentColor"/><circle cx="12" cy="11" r="1" fill="currentColor"/><circle cx="16" cy="11" r="1" fill="currentColor"/></svg>';
 const cross='<svg class="bc-close" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
 const whatsapp='<svg aria-hidden="true" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';
 root.innerHTML='<div class="bc-options" id="be-contact-options" hidden><a class="bc-link" href="https://wa.me/393520180705" target="_blank" rel="noopener noreferrer" aria-label="Scrivi a Honey Garden su WhatsApp, si apre in una nuova scheda"><span class="bc-icon bc-whatsapp">'+whatsapp+'</span></a></div><button class="bc-toggle" type="button" aria-label="Contatta Honey Garden" aria-expanded="false" aria-controls="be-contact-options">'+chat+'</button>';
 document.body.appendChild(root);
 const button=root.querySelector('button'),options=root.querySelector('.bc-options');
 function setOpen(open,focus){options.hidden=!open;button.setAttribute('aria-expanded',String(open));button.setAttribute('aria-label',open?'Chiudi contatti':'Contatta Honey Garden');button.innerHTML=open?cross:chat;if(focus)button.focus();}
 button.addEventListener('click',e=>{e.stopPropagation();setOpen(options.hidden,false)});
 document.addEventListener('click',e=>{if(!e.composedPath().includes(root)&&!options.hidden)setOpen(false,false)});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!options.hidden)setOpen(false,root.contains(document.activeElement))});
 function privacyState(){const notice=document.getElementById('beyou-privacy-notice');const blocked=Boolean(notice&&!notice.hidden);root.hidden=blocked;if(blocked&&!options.hidden)setOpen(false,false);}
 const observer=new MutationObserver(records=>{if(records.some(r=>r.type==='childList'||r.target.id==='beyou-privacy-notice'))privacyState()});
 observer.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']});privacyState();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
