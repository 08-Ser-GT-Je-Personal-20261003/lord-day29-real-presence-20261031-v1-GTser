"""Build the independent Lord's Day 29 website. --verify-live rechecks CCI text."""
from pathlib import Path
import json,re,html,hashlib,concurrent.futures,sys,urllib.request
import requests
from bs4 import BeautifulSoup as B

ROOT=Path(__file__).resolve().parent; DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True)
SLUG='lord-day29-real-presence-20261031-v1-GTser';ORG='08-Ser-GT-Je-Personal-20261003'
REPO=f'https://github.com/{ORG}/{SLUG}';PAGES=f'https://{ORG.lower()}.github.io/{SLUG}/';SURGE=f'https://{SLUG.lower()}.surge.sh/'
corpus=json.loads((ROOT/'confessions.json').read_text(encoding='utf-8'))
docs={d['key']:d for d in corpus['documents']}
learning=json.loads((ROOT/'learning.json').read_text(encoding='utf-8'))
def esc(s):return html.escape(s,quote=True)
def norm(s):return re.sub(r'\s+','',s)
def number(s):return int(re.match(r'\d+',s['title']).group())
def request(url):
 r=requests.get(url,timeout=30,proxies=urllib.request.getproxies());r.raise_for_status();return r
selected=[(k,s) for k in ['apostles','nicene','athanasian'] for s in docs[k]['sections']]
selected += [('heidelberg',s) for s in docs['heidelberg']['sections'] if number(s) in [47,48,78,79]]
selected += [('belgic',docs['belgic']['sections'][n-1]) for n in [19,33,35]]
dort14=next(s for s in docs['dort']['sections'] if s['source'].endswith('/section5/14'))
selected.append(('dort',dort14))

if '--verify-live' in sys.argv:
 urls=list(dict.fromkeys(s['source'] for _,s in selected))
 def fetch(url):
  r=request(url);return B(r.content,'html.parser'),hashlib.sha256(r.content).hexdigest()
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:fetched=dict(zip(urls,pool.map(fetch,urls)))
 checks=[]
 for key,s in selected:
  soup,raw=fetched[s['source']]
  if key in ['apostles','nicene','athanasian']:el=soup.select_one('.article-body .alert-primary')
  elif key=='heidelberg':el=next(x for x in soup.select('#block-tulip-content .entity-reference > span > article') if re.match(r'\d+',x.select_one('h4').get_text().strip()).group()==str(number(s)))
  else:el=soup.select_one('#block-tulip-content > article > div')
  assert el,s['source']
  for remove in el.select('nav,script,style'):remove.decompose()
  same=norm(''.join(el.stripped_strings))==norm(''.join(B(s['html'],'html.parser').stripped_strings))
  checks.append({'document':key,'section':s['title'],'source':s['source'],'same_words_punctuation_and_numbers_ignoring_layout_whitespace':same,'snapshot_text_sha256':s['sha256'],'live_raw_sha256':raw})
  if not same:raise RuntimeError('Source changed; inspect explicitly: '+s['source'])
 (DIST/'source-verification.json').write_text(json.dumps({'checked':'2026-10-31','snapshot':'2026-10-17','policy':'Do not change source words, punctuation, numbering, or footnotes. Only layout whitespace excluded from live comparison.','checks':checks,'all_match':all(c['same_words_punctuation_and_numbers_ignoring_layout_whitespace'] for c in checks)},ensure_ascii=False,indent=2),encoding='utf-8')
else:
 assert (DIST/'source-verification.json').exists(),'First build: run python build.py --verify-live'

scripture_file=ROOT/'scripture.json'
if not scripture_file.exists():
 url='https://www.biblegateway.com/passage/?search=Luke%2022%3A1-30&version=CUVS'
 r=request(url);soup=B(r.content,'html.parser');verses=[]
 for n in range(1,31):
  spans=soup.select(f'.passage-text span.text.Luke-22-{n}');assert spans,n
  texts=[]
  for span in spans:
   for x in span.select('sup,.crossreference,.footnote'):x.decompose()
   texts.append(norm(span.get_text()))
  verses.append({'number':n,'text':''.join(texts)})
 scripture_file.write_text(json.dumps({'title':'路加福音22:1–30','source':url,'version':'CUVS','fetched':'2026-10-31','verses':verses},ensure_ascii=False,indent=2),encoding='utf-8')
scripture=json.loads(scripture_file.read_text(encoding='utf-8'))

def head(title):return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="海德堡主日29：耶稣基督真实地临在圣餐中。性质与益处、路加22章释经、认信原文与讨论。"><title>{esc(title)} · GTser</title><link rel="icon" href="assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="lesson.css"><script src="study-data.js" defer></script><script src="app.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><div id="progress" aria-hidden="true"></div>'''
def toolbar(back=False):return f'''<header class="topbar"><a class="brand" href="index.html"><img src="assets/mark.svg" width="30" height="30" alt=""> GTser <span>· 主日29</span></a><div class="tools">{'<a href="index.html#creeds">← 返回讲章</a>' if back else '<button id="toc-toggle" aria-controls="toc" aria-expanded="false">☰ 目录</button>'}<button id="theme" aria-label="切换深浅主题">◐ <span>夜读</span></button><button id="font-size" aria-label="切换正文字号">A＋</button><button id="print">打印</button></div></header>'''
def footer():return f'''<footer><b>GTser · 主日29</b><p>2026.10.31 / v1.0.0 · 原创讲章与教学图示</p><a href="{REPO}">源码与版本</a> · <a href="index.html#sources">来源与说明</a><p>真实相交，确据坚固，感恩服事。</p></footer><a class="to-top" href="#" aria-label="回到顶部">↑</a></body></html>'''
def quote(s):return f'<div class="source-quote"><a class="source-label" href="{s["source"]}" target="_blank" rel="noopener">CCI原文 ↗</a><div class="original">{s["html"]}</div></div>'
body=(ROOT/'content.html').read_text(encoding='utf-8')
body=body.replace('{{SCRIPTURE}}','<article class="scripture"><h3>路加福音22:1–30</h3>'+''.join(f'<p><sup>{v["number"]}</sup> {esc(v["text"])}</p>' for v in scripture['verses'])+'</article>')
body=body.replace('{{HEIDELBERG29}}',''.join(quote(s) for s in docs['heidelberg']['sections'] if s.get('lord_day')==29))
body=body.replace('{{BELGIC33}}',f'<div class="original">{docs["belgic"]["sections"][32]["html"]}</div>')
belgic35=B(docs['belgic']['sections'][34]['html'],'html.parser').find_all('p')[4]
body=body.replace('{{BELGIC35EXCERPT}}',f'<div class="original">{belgic35}</div>')
body=body.replace('{{DORT14}}',f'<div class="original">{dort14["html"]}</div>')
body=body.replace('{{DISCUSSIONS}}',''.join(f'<article class="question"><span>{esc(q["category"])}</span><h3>{esc(q["question"])}</h3><details class="answer" open><summary>答案与分析 · 可收起</summary><p>{esc(q["answer"])}</p><p class="note">{esc(q["analysis"])}</p></details></article>' for q in learning['discussions']))
for key,value in [('PAGES',PAGES),('SURGE',SURGE),('REPO',REPO)]:body=body.replace('{{'+key+'}}',value)
assert '{{' not in body
soup=B(body,'html.parser');toc=''
for s in soup.select('section[data-title]'):
 toc+=f'<a href="#{s["id"]}">{esc(s["data-title"])}</a>'
 if s['id']=='sermon':toc+=''.join(f'<a class="toc-sub" href="#{h["id"]}">{esc(h.get_text().split("：")[0])}</a>' for h in s.select('h3[id]'))
hero='''<div class="hero"><div class="hero-copy"><span class="eyebrow">海德堡要理问答 · 主日29</span><h1>真实相交，<br>不止记念。</h1><p>耶稣基督<br>真实地临在圣餐中</p><div class="hero-meta"><span>路加福音22:1–30</span><span>问78–79</span><span>2026.10.31 · V1</span></div><a class="button" href="#sermon">阅读两点讲章 ↓</a><a class="text-button" href="#presence">互动图解 →</a></div><figure class="hero-art"><img src="assets/presence.svg" width="720" height="560" alt="原创象征插图：开放门窗旁的饼和杯，光照在桌面上；不描绘神或基督形象"><figcaption>饼仍是饼；圣灵使信徒真实有份于主。</figcaption></figure></div>'''
(DIST/'index.html').write_text(head('耶稣基督真实地临在圣餐中')+toolbar()+f'<aside id="toc" aria-label="章节目录"><div class="toc-head"><b>阅读目录</b><button id="toc-close" aria-label="关闭目录">×</button></div>{toc}<a href="library.html">▤ 六份认信原典库</a><small>原文与讲解分开 · 目录可隐藏</small></aside><main id="main">'+hero+body+'</main>'+footer(),encoding='utf-8')

for key in ['apostles','nicene','athanasian']:
 d=docs[key];s=d['sections'][0]
 page=head(d['title']+' · 干净阅读版')+toolbar(True)+f'''<main id="main" class="reader"><div class="reader-heading"><span class="eyebrow">CCI中文原文 · 干净阅读与背诵</span><h1>{d['title']}</h1><p>先读全文，再遮盖回忆；点击或按回车揭示原段。</p><div class="reader-tools"><button id="mask-toggle" aria-pressed="false">开启背诵遮盖</button><button id="speak">▷ 朗读</button><button id="speak-stop">停止</button><a href="{s['source']}" target="_blank" rel="noopener">CCI来源 ↗</a></div><p id="speech-status" class="note" aria-live="polite"></p></div><article class="creed-clean original" id="creed-text">{s['html']}</article><div class="reader-end"><p>遮盖只改变显示，不改动原文字词；打印时恢复全文。本机朗读受设备语音支持限制。</p><a href="index.html#creeds">三经与主日29 →</a><a href="library.html#{key}">完整原典库 →</a></div></main>'''+footer()
 (DIST/f'reader-{key}.html').write_text(page,encoding='utf-8')

def sid(key,s,i):
 if key in ['heidelberg','belgic']:return f'{key}-{i+1}'
 if key=='dort':
  m=re.search(r'/section([^/]+)/(\d+)$',s['source']);return 'dort-'+m.group(1)+'-'+m.group(2)
 return key
library=head('六份认信原典库')+toolbar(True)+'''<main id="main" class="library"><div class="section-head"><span>THE CONFESSIONAL LIBRARY</span><h1>六份认信原典库</h1><p>CCI网站中文原文 · 2026年10月17日快照</p></div><p>三份信经、问47–48／78–79、比利时19／33／35、多特第五项14于2026年10月31日另行在线复核。其余章节不宣称全部当日重抓。原文字词、标点与附经保留，版面空白可调整。多特按该站收录范围，不添加其他译本的独立结语。</p><nav class="library-nav" aria-label="原典目录">'''+''.join(f'<a href="#{key}">{d["title"]}</a>' for key,d in docs.items())+'</nav>'
for key,d in docs.items():
 library+=f'<section id="{key}"><h2>{d["title"]}</h2>'
 for i,s in enumerate(d['sections']):
  anchor=sid(key,s,i);attr=f' id="{anchor}"' if anchor!=key else ''
  library+=f'<article class="library-entry"{attr}><h3>{esc(s["title"])}</h3><a class="source-label" href="{s["source"]}" target="_blank" rel="noopener">CCI原文来源 ↗</a><div class="original">{s["html"]}</div></article>'
 library+='</section>'
(DIST/'library.html').write_text(library+'</main>'+footer(),encoding='utf-8')
(DIST/'study-data.js').write_text('window.STUDY='+json.dumps({k:learning[k] for k in ['story','views','quiz']},ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
(DIST/'.nojekyll').touch()
readme=f'''# 主日29 · 耶稣基督真实地临在圣餐中

2026-10-31 · v1.0.0 · GTser

| 公开入口 | 链接 |
| --- | --- |
| GitHub Pages | {PAGES} |
| Surge | {SURGE} |
| 新建源码仓库 | {REPO} |

## 内容

独立的欧陆改革宗讲章网站，按“真实临在的性质、真实临在的益处”两点展开。含路22:1–30完整读经、历史与逐段释经、四条神学脉络、16组详细讨论答案、互动临在图解、动态救赎脉络、原创地图与插图、本机朗读和复习自测。六份认信原典完整保留，三经另有干净阅读／背诵页面。原主日28项目未修改。

## 运行与维护

安装Python依赖：`python -m pip install -r requirements.txt`。

- 离线构建：`python build.py`，读取仓库原文与已核验记录。
- 在线重核：`python build.py --verify-live`。发现词句变化会停止，需人工审阅，不静默替换译文。
- 本地预览：`python -m http.server 4189 -d dist`。
- 内容核验：`python qa/verify.py`。
- 发布目录：`dist/`。GitHub Actions自动发布Pages；Surge可手动发布同目录。

正文源文件：`content.html`；讨论／自测／图解数据：`learning.json`；六份认信快照：`confessions.json`；读经：`scripture.json`。UI在`dist/style.css`与`dist/app.js`，SVG在`dist/assets/`。无需构建框架，无数据库，无运行时第三方依赖。不要提交账号、密码、令牌、.netrc或Surge生成的CNAME到仓库。

## 文本与证据

认信全部采用CCI指定中文原文，不混入其他译本。完整快照日期2026-10-17；三经、问47–48／78–79、比利时19／33／35、多特第五项14另在2026-10-31在线核验，见`dist/source-verification.json`。其余原典不宣称全部当日重抓。全库232条，包括CCI所收多特59条正面教义及4组驳谬，不从别版补结语。

历史推断与经文明言分开；地图是非比例示意，未虚构最后晚餐房址。诗歌按给定编号，未猜歌词曲名。“21篇1–3节”按上下文理解为韵诗编号，实际分节按当地诗本。朗读依赖设备可用中文声音，网站不自带预录音频。

检查报告见`qa/`；公开部署记录见`deployment.json`。原创讲解与图示由本项目编写；第三方译文权利归相应权利人，不对其附加原创授权。
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
(ROOT/'package.json').write_text(json.dumps({'name':SLUG.lower(),'version':'1.0.0','private':True,'scripts':{'build':'python build.py','preview':'python -m http.server 4189 -d dist'}},indent=2),encoding='utf-8')
print(json.dumps({'pages':len(list(DIST.glob('*.html'))),'sections':len(soup.select('section[data-title]')),'questions':len(learning['discussions']),'sermon_characters':len(soup.select_one('.sermon-body').get_text()),'total_study_characters':len(soup.get_text())},ensure_ascii=False))
