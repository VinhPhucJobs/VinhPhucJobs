"""Snapshot public recruitment metadata only; no candidate or account data."""
import urllib.request,json,concurrent.futures,time,math,html,re,pathlib
from lxml import html as lh
ROOT=pathlib.Path(__file__).resolve().parents[1]
CACHE=ROOT/'.cache/public-import';CACHE.mkdir(parents=True,exist_ok=True)
HEAD={'User-Agent':'Mozilla/5.0 VPJ-public-metadata/1.0'}
def get(url):
 for n in range(4):
  try:
   r=urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=45)
   return r.read(),r.headers
  except Exception:
   if n==3: raise
   time.sleep(2+n)
def page(i):
 f=CACHE/f'{i}.json'
 if f.exists():return json.loads(f.read_text())
 u=f'https://vinhphuc.work/wp-json/wp/v2/posts?per_page=100&page={i}&_fields=id,date,link,title,class_list,featured_media,content'
 b,h=get(u);f.write_bytes(b);print('Downloaded page',i,flush=True);return json.loads(b)
b,h=get('https://vinhphuc.work/wp-json/wp/v2/posts?per_page=1&_fields=id');total=int(h['X-WP-Total']);pages=math.ceil(total/100)
print('Public posts',total,'pages',pages,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 allposts=[p for batch in pool.map(page,range(1,pages+1)) for p in batch]
result=[]
for p in allposts:
 classes=p.get('class_list',[])
 title=html.unescape(p['title']['rendered']);slugs=[s[8:] for s in classes if s.startswith('company-')]
 loc=next((x for slug,x in [('vinh-yen','Vĩnh Yên'),('phuc-yen','Phúc Yên'),('binh-xuyen','Bình Xuyên'),('tam-duong','Tam Dương'),('yen-lac','Yên Lạc'),('vinh-tuong','Vĩnh Tường'),('lap-thach','Lập Thạch'),('song-lo','Sông Lô'),('tam-dao','Tam Đảo')] if 'category-'+slug in classes),'Vĩnh Phúc')
 category=next((cat for keys,cat in [(['kiem-soat-chat-luong','qa','qc'],'QC'),(['ke-toan'],'Kế toán'),(['hanh-chinh','van-phong','nhan-su'],'Văn phòng'),(['ky-su','co-khi','dien-tu','ky-thuat'],'Kỹ thuật'),(['ban-hang','marketing','dich-vu'],'Dịch vụ')] if any(any(k in c for k in keys) for c in classes)), 'Sản xuất')
 company=re.split(r'\s+(?:[Tt]uyển|TUYỂN)',title)[0]
 company=re.sub(r'^(?:Tháng\s+\d+/\d+\s*[–-]\s*)','',company)
 imgs=lh.fromstring('<div>'+p['content']['rendered']+'</div>').xpath('//img/@src')
 result.append({'id':p['id'],'title':title,'company':company,'companySlug':slugs[0] if slugs else '', 'location':loc,'address':loc,'category':category,'min':0,'max':0,'salaryText':'Xem tại nguồn','exp':'Xem tại nguồn','type':'Xem tại nguồn','days':max(0,(time.time()-time.mktime(time.strptime(p['date'][:10],'%Y-%m-%d')))//86400),'published':p['date'][:10],'sourceUrl':p['link'],'logoUrl':'','posterUrl':imgs[0] if imgs else '', 'deadline':'','logo':'','color':'#f3f6fb','ink':'#165dcc'})
result.sort(key=lambda x:x['published'],reverse=True)
(ROOT/'dist/data/jobs.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')))
(ROOT/'dist/data/import-status.json').write_text(json.dumps({'source':'https://vinhphuc.work','importedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'publicPostCount':total,'recruitmentCount':len(result),'pagesFetched':pages,'complete':len(allposts)==total,'scope':'Public recruitment metadata. Original descriptions and applications remain at source.'},ensure_ascii=False,indent=2))
print('COMPLETE',len(result),'recruitment records',flush=True)
