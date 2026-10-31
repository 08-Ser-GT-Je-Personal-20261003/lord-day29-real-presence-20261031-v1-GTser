// A DOM simulation, not a browser or a layout engine. No user browser is opened.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM}=require(process.env.GTSER_JSDOM||'jsdom');
const root=path.resolve(__dirname,'..'),dist=path.join(root,'dist');
const reports=[];
function create(file){
 const errors=[];const dom=new JSDOM(fs.readFileSync(path.join(dist,file),'utf8'),{url:'https://qa.invalid/'+file,runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window;w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};w.print=()=>{};
 w.addEventListener('error',e=>errors.push(String(e.error||e.message)));
 w.eval(fs.readFileSync(path.join(dist,'study-data.js'),'utf8'));w.eval(fs.readFileSync(path.join(dist,'app.js'),'utf8'));
 return {dom,w,doc:w.document,errors};
}
{
 const {dom,w,doc,errors}=create('index.html'),click=id=>doc.querySelector(id).click();
 click('#toc-toggle');assert(doc.querySelector('#toc').classList.contains('open'));assert.equal(doc.querySelector('#toc-toggle').getAttribute('aria-expanded'),'true');
 doc.querySelector('#toc a').click();assert(!doc.querySelector('#toc').classList.contains('open'));
 click('#answers-hide');assert.equal(doc.querySelectorAll('details.answer[open]').length,0);
 click('#answers-all');assert.equal(doc.querySelectorAll('details.answer[open]').length,16);
 click('#theme');assert.equal(doc.documentElement.dataset.theme,'dark');click('#font-size');assert(doc.body.classList.contains('big'));
 click('[data-view="spirit"]');assert.equal(doc.querySelector('.presence-diagram').dataset.focus,'spirit');assert(doc.querySelector('#presence-title').textContent.includes('圣灵'));
 click('[data-story="5"]');assert(doc.querySelector('#story-label').textContent.includes('终局'));
 click('#story-play');assert.equal(doc.querySelector('#story-play').textContent,'Ⅱ 暂停');click('#story-play');assert.equal(doc.querySelector('#story-play').textContent,'▶ 播放救赎脉络');
 for(let i=0;i<w.STUDY.quiz.length;i++){const q=w.STUDY.quiz[i];doc.querySelectorAll('#quiz-options button')[q.a].click();assert(doc.querySelector('#quiz-feedback').textContent.startsWith('✓'));assert(doc.querySelector('#quiz-score').textContent.includes(String(i+1)));click('#quiz-next');}
 const check=doc.querySelector('[data-review]');check.checked=true;check.dispatchEvent(new w.Event('change'));assert.equal(w.localStorage.getItem('gtser29-day0'),'1');
 click('#sermon-speak');assert(doc.querySelector('#sermon-status').textContent.includes('不支持'));click('#sermon-stop');
 assert.deepEqual(errors,[]);reports.push({page:'index.html',toc:true,all_16_answers:true,theme_and_font:true,four_perspective_explorer:true,story_nodes_and_play_pause:true,all_six_quiz_questions:true,review_storage:true,speech_fallback:true});dom.window.close();
}
for(const key of ['apostles','nicene','athanasian']){
 const {dom,w,doc,errors}=create('reader-'+key+'.html'),before=doc.querySelector('#creed-text').textContent;
 doc.querySelector('#mask-toggle').click();assert(doc.querySelector('#creed-text').classList.contains('masked'));
 const p=doc.querySelector('#creed-text p');assert.equal(p.getAttribute('role'),'button');p.click();assert(p.classList.contains('revealed'));p.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Enter',bubbles:true}));assert(!p.classList.contains('revealed'));
 doc.querySelector('#mask-toggle').click();assert.equal(before,doc.querySelector('#creed-text').textContent);assert.equal(p.getAttribute('role'),null);
 doc.querySelector('#speak').click();assert(doc.querySelector('#speech-status').textContent.includes('不支持'));assert.deepEqual(errors,[]);
 reports.push({page:'reader-'+key+'.html',mask_and_reveal:true,keyboard:true,source_text_unchanged:true,speech_fallback:true});dom.window.close();
}
{
 const {dom,doc,errors}=create('library.html');assert.equal(doc.querySelectorAll('.library-entry').length,232);assert.deepEqual(errors,[]);reports.push({page:'library.html',original_entries:232,no_runtime_errors:true});dom.window.close();
}
fs.writeFileSync(path.join(__dirname,'dom-report.json'),JSON.stringify({checked:'2026-10-31',method:'jsdom 26 DOM simulation; no browser or visual layout testing',checks:reports,all_pass:true},null,2));console.log('PASS: DOM simulation for 5 pages, 16 answers, 6 quiz questions, diagrams, memory and creed tools.');
