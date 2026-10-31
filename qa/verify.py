"""Static fidelity and navigation checks; no claim of browser layout testing."""
from pathlib import Path
from bs4 import BeautifulSoup as B
import json,hashlib,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];dist=ROOT/'dist'
docs=json.loads((ROOT/'confessions.json').read_text(encoding='utf-8'))['documents']
def text(el):return ''.join(el.stripped_strings)
pages={p.name:B(p.read_text(encoding='utf-8'),'html.parser') for p in dist.glob('*.html')}
ids={name:{x['id'] for x in s.select('[id]')} for name,s in pages.items()}
for name,soup in pages.items():
 allids=[x['id'] for x in soup.select('[id]')];assert len(allids)==len(set(allids)),name
 assert len(soup.select('main'))==1 and soup.select_one('html')['lang']=='zh-CN'
 assert soup.select_one('meta[name=viewport]')
 assert '{{' not in str(soup)
 for a in soup.select('a[href]'):
  href=a['href']
  if '://' in href or href.startswith('mailto:'):continue
  dest,_,anchor=href.partition('#');dest=dest or name
  assert (dist/dest).exists(),(name,href)
  if anchor and dest.endswith('.html'):assert anchor in ids[dest],(name,href)
 for e in soup.select('[src],link[href]'):
  asset=e.get('src') or e.get('href')
  assert '://' not in asset,('external startup asset',name,asset)
  assert (dist/asset).exists(),('missing asset',name,asset)
 for img in soup.select('img'):assert img.has_attr('alt'),(name,'missing alt')
for p in (dist/'assets').glob('*.svg'):
 s=ET.parse(p).getroot();assert s.tag.endswith('svg');assert not any(x.tag.endswith('script') for x in s.iter())
lib=pages['library.html'].select('.library-entry .original');originals=[s for d in docs for s in d['sections']]
assert len(lib)==len(originals)==232
for e,s in zip(lib,originals):
 assert text(e)==text(B(s['html'],'html.parser')),s['title']
 assert hashlib.sha256(s['text'].encode()).hexdigest()==s['sha256'],s['title']
for key in ['apostles','nicene','athanasian']:
 d=next(x for x in docs if x['key']==key)
 assert text(pages['reader-'+key+'.html'].select_one('#creed-text'))==text(B(d['sections'][0]['html'],'html.parser'))
heid=next(d for d in docs if d['key']=='heidelberg')
for e,s in zip(pages['index.html'].select('#primary .source-quote .original')[:2],[s for s in heid['sections'] if s.get('lord_day')==29]):assert text(e)==text(B(s['html'],'html.parser'))
main=pages['index.html'];assert len(main.select('section[data-title]'))==13
assert len(main.select('details.answer[open]'))==16
scripture=json.loads((ROOT/'scripture.json').read_text(encoding='utf-8'));assert [v['number'] for v in scripture['verses']]==list(range(1,31))
assert len(main.select('.scripture p'))==30
sources=json.loads((dist/'source-verification.json').read_text(encoding='utf-8'));assert sources['all_match'] and len(sources['checks'])==11
css=(dist/'style.css').read_text(encoding='utf-8')+(dist/'lesson.css').read_text(encoding='utf-8')
assert '@media(max-width:640px)' in css and '@media(max-width:700px)' in css and 'prefers-reduced-motion' in css
report={'checked':'2026-10-31','checks':{'five_complete_html_pages':True,'unique_ids_and_all_internal_links':True,'all_local_startup_assets_and_svg_parse':True,'all_232_original_entries_match_snapshot':True,'all_snapshot_text_sha256_valid':True,'all_three_clean_creed_readers_exact':True,'questions_78_79_exact':True,'all_11_live_source_checks_pass':True,'complete_30_scripture_verses':True,'all_16_answers_expanded_by_default':True,'responsive_breakpoints_and_reduced_motion_present':True},'browser_visual_check':{'performed':False,'reason':'Local browser use is disabled in Work settings. Browser automation was not bypassed.','limits':'No actual mobile/tablet/desktop screenshots, pixel geometry or overflow measurements are claimed.'}}
(ROOT/'qa/static-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 5 pages; 232 exact original entries; 11 live checks; 30 verses; 16 answers; local links/assets.')
