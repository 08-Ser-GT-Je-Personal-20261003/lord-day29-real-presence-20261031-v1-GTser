(()=>{'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const saved={get:k=>{try{return localStorage.getItem('gtser29-'+k)}catch{return null}},set:(k,v)=>{try{localStorage.setItem('gtser29-'+k,v)}catch{}}};
if(saved.get('theme')==='dark')document.documentElement.dataset.theme='dark';
if(saved.get('big')==='1')document.body.classList.add('big');
const theme=$('#theme');function themeLabel(){if(theme)theme.innerHTML=document.documentElement.dataset.theme==='dark'?'◐ <span>日读</span>':'◐ <span>夜读</span>'}themeLabel();
theme?.addEventListener('click',()=>{const dark=document.documentElement.dataset.theme!=='dark';document.documentElement.dataset.theme=dark?'dark':'light';saved.set('theme',dark?'dark':'light');themeLabel()});
$('#font-size')?.addEventListener('click',()=>{document.body.classList.toggle('big');saved.set('big',document.body.classList.contains('big')?'1':'0')});
$('#print')?.addEventListener('click',()=>window.print());
const toc=$('#toc'),toggle=$('#toc-toggle');function setToc(open){toc?.classList.toggle('open',open);toggle?.setAttribute('aria-expanded',String(open))}
toggle?.addEventListener('click',()=>setToc(!toc.classList.contains('open')));$('#toc-close')?.addEventListener('click',()=>{setToc(false);toggle?.focus()});
$$('#toc a').forEach(a=>a.addEventListener('click',()=>setToc(false)));
document.addEventListener('keydown',e=>{if(e.key==='Escape'){setToc(false);stopStory()}});
document.addEventListener('click',e=>{if(toc?.classList.contains('open')&&!toc.contains(e.target)&&!toggle.contains(e.target))setToc(false)});
let queued=false;function progress(){queued=false;const max=document.documentElement.scrollHeight-innerHeight;$('#progress').style.transform=`scaleX(${max>0?Math.min(1,scrollY/max):0})`}
addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(progress)}},{passive:true});addEventListener('resize',progress);progress();
if('IntersectionObserver'in window){const observer=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){$$('#toc a').forEach(a=>a.classList.toggle('current',a.hash==='#'+e.target.id))}})},{rootMargin:'-15% 0px -65% 0px'});$$('section[data-title]').forEach(s=>observer.observe(s))}
$('#answers-all')?.addEventListener('click',()=>$$('details.answer').forEach(d=>d.open=true));$('#answers-hide')?.addEventListener('click',()=>$$('details.answer').forEach(d=>d.open=false));
const story=window.STUDY.story;
let storyIndex=0,storyTimer=null;function renderStory(i){storyIndex=i;$('#story-label').textContent=story[i][0];$('#story-text').textContent=story[i][1];$$('[data-story]').forEach(b=>{b.classList.toggle('active',Number(b.dataset.story)===i);b.setAttribute('aria-pressed',String(Number(b.dataset.story)===i))})}
function stopStory(){if(storyTimer)clearInterval(storyTimer);storyTimer=null;if($('#story-play'))$('#story-play').textContent='▶ 播放救赎脉络'}
$$('[data-story]').forEach(b=>b.addEventListener('click',()=>{stopStory();renderStory(Number(b.dataset.story))}));
$('#story-play')?.addEventListener('click',()=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches){renderStory((storyIndex+1)%story.length);return}if(storyTimer){stopStory();return}renderStory(0);$('#story-play').textContent='Ⅱ 暂停';storyTimer=setInterval(()=>{if(storyIndex===5){stopStory();return}renderStory(storyIndex+1)},4500)});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopStory()});
if($('#story-flow'))renderStory(0);
const quiz=window.STUDY.quiz;
let qi=0,answered=false,score=0;
function renderQuiz(){if(!$('#quiz'))return;answered=false;$('#quiz-question').textContent=`${qi+1} / ${quiz.length} · ${quiz[qi].q}`;$('#quiz-feedback').textContent='';$('#quiz-options').replaceChildren(...quiz[qi].o.map((s,i)=>{const b=document.createElement('button');b.textContent=s;b.addEventListener('click',()=>{if(answered)return;answered=true;const good=i===quiz[qi].a;if(good)score++;$$('#quiz-options button').forEach((x,j)=>{x.disabled=true;if(j===quiz[qi].a)x.classList.add('correct')});if(!good)b.classList.add('wrong');$('#quiz-feedback').textContent=(good?'✓ 正确。':'请再想一想。')+quiz[qi].e;$('#quiz-score').textContent=`本轮答对 ${score} 题`});return b}));$('#quiz-next').textContent=qi===quiz.length-1?'重新一轮 ↻':'下一题 →'}
$('#quiz-next')?.addEventListener('click',()=>{qi=(qi+1)%quiz.length;if(qi===0){score=0;$('#quiz-score').textContent=''}renderQuiz()});renderQuiz();
$$('[data-review]').forEach(c=>{c.checked=saved.get(c.dataset.review)==='1';c.addEventListener('change',()=>saved.set(c.dataset.review,c.checked?'1':'0'))});
const creed=$('#creed-text'),mask=$('#mask-toggle');let masked=false;
const paragraphs=creed?[...creed.querySelectorAll('p')]:[];
mask?.addEventListener('click',()=>{masked=!masked;creed.classList.toggle('masked',masked);mask.setAttribute('aria-pressed',String(masked));mask.textContent=masked?'关闭背诵遮盖':'开启背诵遮盖';paragraphs.forEach((p,i)=>{p.classList.remove('revealed');if(masked){p.tabIndex=0;p.setAttribute('role','button');p.setAttribute('aria-label',`第${i+1}段，按回车揭示`);p.setAttribute('aria-pressed','false')}else{p.removeAttribute('tabindex');p.removeAttribute('role');p.removeAttribute('aria-label');p.removeAttribute('aria-pressed')}})});
paragraphs.forEach((p,i)=>{function reveal(){if(!masked)return;p.classList.toggle('revealed');const visible=p.classList.contains('revealed');p.setAttribute('aria-pressed',String(visible));p.setAttribute('aria-label',visible?`第${i+1}段已揭示，按回车遮盖`:`第${i+1}段，按回车揭示`)}p.addEventListener('click',reveal);p.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();reveal()}})});
$('#speak')?.addEventListener('click',()=>{const status=$('#speech-status');if(!('speechSynthesis'in window)){status.textContent='此终端不支持本机朗读，请使用设备的辅助阅读功能。';return}speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(creed.innerText);u.lang='zh-CN';u.rate=.86;const voice=speechSynthesis.getVoices().find(v=>v.lang.startsWith('zh'));if(voice)u.voice=voice;u.onstart=()=>status.textContent='正在朗读；可随时停止。';u.onend=()=>status.textContent='朗读结束。';u.onerror=()=>status.textContent='本机语音暂不可用，请检查终端语音支持。';status.textContent='正在请求本机语音…';speechSynthesis.speak(u)});
$('#speak-stop')?.addEventListener('click',()=>{if('speechSynthesis'in window)speechSynthesis.cancel();$('#speech-status').textContent='已停止朗读。'});
addEventListener('pagehide',()=>{stopStory();if('speechSynthesis'in window)speechSynthesis.cancel()});

$$('[data-view]').forEach(b=>b.addEventListener('click',()=>{const k=b.dataset.view;const v=window.STUDY.views[k];$('.presence-diagram').dataset.focus=k;$('#presence-title').textContent=v[0];$('#presence-text').textContent=v[1];$$('[data-view]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))}));
let speechEpoch=0;
$('#sermon-speak')?.addEventListener('click',()=>{const status=$('#sermon-status');if(!('speechSynthesis' in window)){status.textContent='此设备暂不支持本机朗读。';return}const epoch=++speechEpoch;speechSynthesis.cancel();const items=$$('.sermon-body p,.sermon-body h3,.sermon-body blockquote');let i=0;function next(){if(epoch!==speechEpoch)return;if(i===items.length){status.textContent='朗读完成。';return}const u=new SpeechSynthesisUtterance(items[i].textContent);u.lang='zh-CN';u.rate=.88;const v=speechSynthesis.getVoices().find(x=>x.lang.startsWith('zh'));if(v)u.voice=v;u.onend=next;u.onerror=()=>{if(epoch===speechEpoch)status.textContent='语音暂不可用，请检查设备中文语音支持。'};status.textContent=`正在请求朗读 ${++i}/${items.length} 段…`;speechSynthesis.speak(u)}next()});
$('#sermon-stop')?.addEventListener('click',()=>{speechEpoch++;if('speechSynthesis'in window)speechSynthesis.cancel();$('#sermon-status').textContent='已停止。'});
let printStates=[];addEventListener('beforeprint',()=>{printStates=$$('details.answer').map(d=>[d,d.open]);printStates.forEach(([d])=>d.open=true)});addEventListener('afterprint',()=>printStates.forEach(([d,open])=>d.open=open));

})();
