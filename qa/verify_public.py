"""Verify public HTTP files; no browser or visual rendering is involved."""
from pathlib import Path
import requests,urllib.request,hashlib,json,subprocess,concurrent.futures
ROOT=Path(__file__).resolve().parents[1];dist=ROOT/'dist'
slug='lord-day29-real-presence-20261031-v1-GTser';org='08-Ser-GT-Je-Personal-20261003'
targets={'github_pages':f'https://{org.lower()}.github.io/{slug}/','surge':f'https://{slug.lower()}.surge.sh/'}
files=[p.relative_to(dist).as_posix() for p in dist.rglob('*') if p.is_file() and not p.name.startswith('.') and p.name!='CNAME']
def digest(b):return hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()
def platform_check(item):
 platform,base=item;session=requests.Session();session.proxies.update(urllib.request.getproxies());checks=[]
 for name in ['']+files:
  local=dist/(name or 'index.html');record={'platform':platform,'url':base+name,'local_file':name or 'index.html'}
  for attempt in range(3):
   try:
    r=session.get(base+name,timeout=18);record.update(status=r.status_code,normalized_sha256=digest(r.content),local_sha256=digest(local.read_bytes()))
    record['matches_local_ignoring_line_endings']=r.status_code==200 and record['normalized_sha256']==record['local_sha256']
    if record['matches_local_ignoring_line_endings']:break
   except requests.RequestException as e:record['error_type']=type(e).__name__;record['matches_local_ignoring_line_endings']=False
  checks.append(record)
 print(platform+': '+str(sum(bool(c['matches_local_ignoring_line_endings']) for c in checks))+'/'+str(len(checks))+' HTTP file checks match',flush=True)
 session.close();return checks
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:checks=[c for group in pool.map(platform_check,targets.items()) for c in group]
runs=json.loads(subprocess.check_output(['gh','run','list','--limit','3','--json','databaseId,status,conclusion,headSha'],cwd=ROOT,text=True))
success=next((r for r in runs if r['status']=='completed' and r['conclusion']=='success'),None)
result={'checked':'2026-10-31','version':'v1.0.0','repo':f'https://github.com/{org}/{slug}','content_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'public_urls':targets,'github_pages_successful_workflow':success,'http_checks':checks,'all_public_files_match':all(c['matches_local_ignoring_line_endings'] for c in checks),'visual_verification':{'performed':False,'reason':'Local browser use is disabled in Work settings; no bypass used.','dom_simulation':'Passed; see qa/dom-report.json','layout_limit':'Responsive CSS supplied; actual device overlap/overflow not measured.'}}
(ROOT/'deployment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert result['all_public_files_match'],[c for c in checks if not c['matches_local_ignoring_line_endings']]
assert success,'No successful GitHub Pages workflow found'
print('PASS: both public sites and all static files match local release.')
