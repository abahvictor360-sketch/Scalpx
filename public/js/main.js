(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
const store={get(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch(e){return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};

/* ---- demo auth (client-side only; swap for a real backend before launch) ---- */
async function hash(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode('scalpx:'+s));return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')}
const Auth={
 user(){return store.get('scalpx_session',null)},
 async register(name,email,pw){const u=store.get('scalpx_users',{});email=email.toLowerCase();if(u[email])throw Error('An account with this email already exists.');u[email]={name,email,h:await hash(pw)};store.set('scalpx_users',u);store.set('scalpx_session',{name,email})},
 async login(email,pw){const u=store.get('scalpx_users',{})[email.toLowerCase()];if(!u||u.h!==await hash(pw))throw Error('Email or password is incorrect.');store.set('scalpx_session',{name:u.name,email:u.email})},
 logout(){try{localStorage.removeItem('scalpx_session')}catch(e){}}
};
window.Scalpx={Auth,store};

function toast(msg){let t=$('.toast');if(!t){t=document.createElement('div');t.className='toast glass-dark';document.body.appendChild(t)}t.textContent=msg;requestAnimationFrame(()=>t.classList.add('show'));clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('show'),3200)}
window.Scalpx.toast=toast;

/* ---- nav state ---- */
const u=Auth.user();
$$('[data-auth]').forEach(el=>{const m=el.dataset.auth;
 if(m==='out')el.style.display=u?'none':'';
 if(m==='in')el.style.display=u?'':'none'});
$$('[data-initial]').forEach(el=>el.textContent=u?u.name.trim()[0].toUpperCase():'');
$$('[data-name]').forEach(el=>el.textContent=u?u.name.split(' ')[0]:'');
const burger=$('.burger'),menu=$('.menu');
if(burger)burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.classList.toggle('x',o);burger.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''});
$$('.menu a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');burger.classList.remove('x');document.body.style.overflow=''}));
let ly=0;const nav=$('.nav');addEventListener('scroll',()=>{const y=scrollY;if(nav){nav.classList.toggle('hide',y>ly&&y>300&&!menu.classList.contains('open'));}ly=y},{passive:true});

/* ---- page transitions ---- */
document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a||a.target||e.metaKey||e.ctrlKey)return;const h=a.getAttribute('href');if(!h||h[0]==='#'||/^(https?:|mailto:|tel:)/.test(h))return;e.preventDefault();document.body.classList.add('leaving');setTimeout(()=>location.href=h,260)});
addEventListener('pageshow',e=>{if(e.persisted)document.body.classList.remove('leaving')});

/* ---- reveal + counters + bars ---- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const t=e.target;t.classList.add('in');io.unobserve(t);
 if(t.dataset.count)count(t);if(t.classList.contains('bar'))t.classList.add('on')}),{threshold:.15,rootMargin:'0px 0px -6% 0px'});
$$('.rv,.rvx,[data-count],.bar').forEach(el=>io.observe(el));
function count(el){const to=+el.dataset.count,d=1600,t0=performance.now();const dec=el.dataset.dec|0;(function f(t){const p=Math.min(1,(t-t0)/d),e=1-Math.pow(1-p,4);el.firstChild.textContent=(to*e).toFixed(dec);if(p<1)requestAnimationFrame(f)})(t0)}

/* ---- glass sheen follows pointer + tilt ---- */
$$('.glass,.glass-dark,.card,.tcard,.step').forEach(el=>el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect();el.style.setProperty('--mx',(e.clientX-r.left)+'px');el.style.setProperty('--my',(e.clientY-r.top)+'px')}));
if(!reduce&&matchMedia('(hover:hover)').matches){
 $$('.tilt').forEach(el=>{el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.animation='none';el.style.transform=`perspective(700px) rotateY(${x*14}deg) rotateX(${-y*14}deg) translateZ(6px)`});el.addEventListener('pointerleave',()=>{el.style.transform='';el.style.animation=''})});
 const g=document.createElement('div');g.className='glow-cur';document.body.appendChild(g);let gx=0,gy=0,tx=0,ty=0;addEventListener('pointermove',e=>{tx=e.clientX;ty=e.clientY});(function l(){gx+=(tx-gx)*.12;gy+=(ty-gy)*.12;g.style.left=gx+'px';g.style.top=gy+'px';requestAnimationFrame(l)})();
}

/* ---- hero parallax ---- */
const fig=$('.hero-figure'),word=$('.hero-word'),hero=$('.hero');
if(hero){
 const setH=()=>hero.style.setProperty('--wordh',word.getBoundingClientRect().height+'px');setH();addEventListener('resize',setH);document.fonts&&document.fonts.ready.then(setH);
 if(!reduce){addEventListener('scroll',()=>{const y=Math.min(scrollY,900);fig.style.translate=`0 ${y*.12}px`;word.style.translate=`0 ${-y*.05}px`;const fc=$('.float-card');if(fc)fc.style.translate=`0 ${y*.22}px`},{passive:true});
  hero.addEventListener('pointermove',e=>{const x=(e.clientX/innerWidth-.5),y=(e.clientY/innerHeight-.5);fig.style.setProperty('rotate',(x*1.5)+'deg');$$('.trail',fig).forEach((t,i)=>t.style.marginLeft=(x*-30*(i+1))+'px')})}
}

/* ---- parallax images ---- */
if(!reduce)addEventListener('scroll',()=>{$$('[data-par]').forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;const p=(r.top+r.height/2-innerHeight/2)*(+el.dataset.par);el.style.transform=`translateY(${p}px)`})},{passive:true});

/* ---- blog filter + modal ---- */
const posts=$$('.post');
$$('.chip[data-f]').forEach(c=>c.addEventListener('click',()=>{$$('.chip[data-f]').forEach(x=>x.classList.remove('on'));c.classList.add('on');posts.forEach(p=>p.classList.toggle('hide',c.dataset.f!=='all'&&p.dataset.cat!==c.dataset.f))}));
const modal=$('.modal');
if(modal){posts.forEach(p=>p.addEventListener('click',()=>{$('.modal img').src=p.dataset.img;$('.modal small').textContent=p.dataset.cat;$('.modal h3').textContent=$('h3',p).textContent;$('.modal .body').innerHTML=p.querySelector('template').innerHTML;modal.classList.add('open')}));
 modal.addEventListener('click',e=>{if(e.target===modal||e.target.closest('.x-btn'))modal.classList.remove('open')});addEventListener('keydown',e=>e.key==='Escape'&&modal.classList.remove('open'))}

/* ---- forms ---- */
function bad(f,msg){f.classList.add('bad');$('.err',f).textContent=msg;return false}
function clear(f){f.classList.remove('bad')}
const emailOk=v=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
const af=$('#authform');
if(af){
 let mode=location.hash==='#register'?'reg':'in';const tabs=$('.tabs');
 const set=m=>{mode=m;tabs.classList.toggle('reg',m==='reg');$$('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));$$('[data-only]').forEach(el=>el.style.display=el.dataset.only===m?'':'none');$('#atitle').textContent=m==='reg'?'Create your account':'Welcome back';$('#asub').textContent=m==='reg'?'Start your personalised scalp journey with Scalpx.':'Sign in to manage consultations and your scalp plan.';$('#submit span').textContent=m==='reg'?'Create account':'Sign in';$('#amsg').className='formmsg'};
 $$('.tabs button').forEach(b=>b.addEventListener('click',()=>set(b.dataset.m)));set(mode);
 $$('.pw button').forEach(b=>b.addEventListener('click',()=>{const i=$('input',b.parentElement);i.type=i.type==='password'?'text':'password';b.textContent=i.type==='password'?'Show':'Hide'}));
 $('#forgot').addEventListener('click',e=>{e.preventDefault();toast('Password reset needs a backend, demo mode only')});
 af.addEventListener('submit',async e=>{e.preventDefault();const g=n=>af.elements[n],msg=$('#amsg');let ok=true;$$('.field',af).forEach(clear);
  if(mode==='reg'&&g('name').value.trim().length<2)ok=bad(g('name').closest('.field'),'Please enter your name.');
  if(!emailOk(g('email').value))ok=bad(g('email').closest('.field'),'Enter a valid email address.');
  if(g('password').value.length<8)ok=bad(g('password').closest('.field'),'Use at least 8 characters.');
  if(!ok)return;
  try{if(mode==='reg')await Auth.register(g('name').value.trim(),g('email').value,g('password').value);else await Auth.login(g('email').value,g('password').value);
   msg.className='formmsg ok show';msg.textContent=mode==='reg'?'Account created, taking you to your dashboard…':'Signed in, loading your dashboard…';setTimeout(()=>location.href='dashboard.html',800)}
  catch(err){msg.className='formmsg bad show';msg.textContent=err.message}})
}
const dash=$('#dash');
if(dash){if(!u){location.replace('login.html')}
 else{$$('[data-email]').forEach(e=>e.textContent=u.email);
  $('#signout').addEventListener('click',()=>{Auth.logout();location.href='index.html'});
  const key='scalpx_routine_'+u.email,saved=store.get(key,{});$$('.chk input').forEach(i=>{i.checked=!!saved[i.name];i.addEventListener('change',()=>{saved[i.name]=i.checked;store.set(key,saved);const n=$$('.chk input:checked').length;$('#prog').textContent=n+' / '+$$('.chk input').length+' done';})});$('#prog').textContent=$$('.chk input:checked').length+' / '+$$('.chk input').length+' done';
  const bk=store.get('scalpx_bookings',[]).filter(b=>b.email===u.email);const list=$('#bookings');
  list.innerHTML=bk.length?bk.map(b=>`<div class="bk"><div><b>${b.concern}</b><br><small>${b.date} · ${b.time}</small></div><small>Requested</small></div>`).join(''):'<p class="empty">No consultations yet. Book your first scalp analysis below.</p>'}}
const bf=$('#bookform');
if(bf){const dt=bf.elements.date;const d=new Date();d.setDate(d.getDate()+1);dt.min=d.toISOString().slice(0,10);
 if(u){bf.elements.name.value=u.name;bf.elements.email.value=u.email}
 bf.addEventListener('submit',e=>{e.preventDefault();let ok=true;$$('.field',bf).forEach(clear);const g=n=>bf.elements[n];
  if(g('name').value.trim().length<2)ok=bad(g('name').closest('.field'),'Please enter your name.');
  if(!emailOk(g('email').value))ok=bad(g('email').closest('.field'),'Enter a valid email address.');
  if(!g('date').value)ok=bad(g('date').closest('.field'),'Choose a preferred date.');
  if(!ok)return;
  const b=store.get('scalpx_bookings',[]);b.push({name:g('name').value,email:g('email').value,concern:g('concern').value,date:g('date').value,time:g('time').value});store.set('scalpx_bookings',b);
  $('#bookwrap').style.display='none';$('#booked').style.display='block';$('#bookedmsg').textContent=`Thanks ${g('name').value.split(' ')[0]}, we’ve noted ${g('concern').value.toLowerCase()} on ${g('date').value} (${g('time').value}). (Demo: stored in this browser only.)`;scrollTo({top:0,behavior:'smooth'})})}
const nf=$('#newsform');if(nf)nf.addEventListener('submit',e=>{e.preventDefault();if(!emailOk(nf.elements.email.value))return toast('Enter a valid email');nf.reset();toast('You’re on the list, welcome to Scalpx')});
})();
