import json,pathlib,urllib.request,concurrent.futures,time,re,io
from lxml import html
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1];data=ROOT/'dist/data/jobs.json';jobs=json.loads(data.read_text());companymap={}
H={'User-Agent':'Mozilla/5.0'}
def get(u):
 return urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25).read()
def company(slug):
 try:
  b=html.fromstring(get('https://vinhphuc.work/cong-ty/'+slug))
  imgs=b.xpath('//img[@width="113" or @width="150"]/@src');names=b.xpath('//h1//text()')
  if not imgs:return slug,None
  url=imgs[0]; raw=get(url);im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((160,160))
  file='assets/companies/'+slug+'.webp';out=ROOT/'dist'/file;out.parent.mkdir(exist_ok=True);im.save(out,'WEBP',quality=85)
  return slug,{'logoUrl':file,'company':' '.join(names).strip(),'companyUrl':'https://vinhphuc.work/cong-ty/'+slug,'originalLogo':url}
 except Exception as e:return slug,None
slugs=list(dict.fromkeys(j['companySlug'] for j in jobs[:100] if j['companySlug']))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for slug,record in pool.map(company,slugs):
  if record:companymap[slug]=record
  print('Company avatars',len(companymap),flush=True)
for j in jobs:
 c=companymap.get(j['companySlug'])
 if c:
  j['logoUrl']=c['logoUrl'];j['companyUrl']=c['companyUrl']
  if c['company']:j['company']=c['company']
# Source listings contain salary/deadline fields absent from public REST metadata.
listingmap={}
def listing(page):
 try:
  b=html.fromstring(get('https://vinhphuc.work/tin-tuyen-dung'+('/page/'+str(page) if page>1 else '')))
  out=[]
  for item in b.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," item ")]'):
   links=item.xpath('.//a[contains(@class,"title")]')
   if not links:continue
   spans=[' '.join(s.text_content().split()) for s in item.xpath('.//span[contains(@class,"form-text")]')]
   out.append((links[0].get('href'),spans))
  return out
 except:return []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for rows in pool.map(listing,range(1,7)):
  listingmap.update(rows)
for j in jobs:
 spans=listingmap.get(j['sourceUrl'],[])
 if len(spans)>=3:
  j['salaryText']=spans[0];j['deadline']=spans[1] if re.fullmatch(r'\d{2}/\d{2}/\d{4}',spans[1]) else '';j['address']=spans[2]
data.write_text(json.dumps(jobs,ensure_ascii=False,separators=(',',':')))
(ROOT/'dist/data/companies.json').write_text(json.dumps(companymap,ensure_ascii=False,separators=(',',':')))
print('ENRICH COMPLETE',len(companymap),'company avatars',len(listingmap),'listing details',flush=True)
