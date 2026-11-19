(()=>{'use strict';
const canvas=document.querySelector('.beyou-snow');if(!canvas)return;
const ctx=canvas.getContext('2d');if(!ctx)return;
const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
try{localStorage.removeItem('beyou_snow_enabled_v1')}catch(e){}
let w=0,h=0,flakes=[],raf=0,last=0;
function resize(){w=innerWidth;h=innerHeight;const d=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(w*d);canvas.height=Math.round(h*d);ctx.setTransform(d,0,0,d,0,0);const count=Math.min(70,Math.max(22,Math.floor(w*h/20000)));flakes=Array.from({length:count},()=>({x:Math.random()*w,y:Math.random()*h,r:.8+Math.random()*2.7,v:13+Math.random()*28,drift:Math.random()*Math.PI*2,alpha:.28+Math.random()*.55}))}
function frame(t){if(document.hidden||motion.matches){raf=0;last=0;return}const dt=Math.min((t-(last||t))/1000,.05);last=t;ctx.clearRect(0,0,w,h);for(const f of flakes){f.y+=f.v*dt;f.drift+=dt*.5;f.x+=Math.sin(f.drift)*8*dt;if(f.y>h+5){f.y=-5;f.x=Math.random()*w}if(f.x<-5)f.x=w+5;if(f.x>w+5)f.x=-5;ctx.beginPath();ctx.fillStyle='rgba(255,255,255,'+f.alpha+')';ctx.arc(f.x,f.y,f.r,0,Math.PI*2);ctx.fill()}raf=requestAnimationFrame(frame)}
function sync(){if(motion.matches||document.hidden){if(raf)cancelAnimationFrame(raf);raf=0;last=0;ctx.clearRect(0,0,w,h)}else if(!raf){resize();raf=requestAnimationFrame(frame)}}
window.addEventListener('resize',()=>{if(!motion.matches)resize()},{passive:true});document.addEventListener('visibilitychange',sync);
if(motion.addEventListener)motion.addEventListener('change',sync);else if(motion.addListener)motion.addListener(sync);sync();
})();