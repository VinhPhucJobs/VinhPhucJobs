"""Extract factual role names, tools and stated salary bands; keep source links."""
import pathlib,json,re,html as stdhtml,collections,sys
from lxml import html
R=pathlib.Path(__file__).resolve().parents[1]
cache=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else R/'.cache/public-import'
raw={p['id']:p for f in cache.glob('*.json') for p in json.loads(f.read_text())}
jobs=json.loads((R/'dist/data/jobs.json').read_text());shards=collections.defaultdict(dict)
skills=['Excel','Word','PowerPoint','AutoCAD','SolidWorks','CNC','PLC','ERP','SAP','ISO 9001','IATF 16949','5S','Tiếng Anh','Tiếng Nhật','Tiếng Trung','Tiếng Hàn','Photoshop','Illustrator','Premiere','QC','QA']
for j in jobs:
 p=raw.get(j['id'])
 if not p:continue
 b=html.fromstring('<div>'+p['content']['rendered']+'</div>');text=' '.join(b.text_content().split());low=text.lower()
 headings=[re.sub(r'\s+',' ',e.text_content()).strip() for e in b.xpath('//h2|//h3|//h4')]
 roles=[h for h in headings if 3<len(h)<180 and not re.search(r'liên hệ|hồ sơ|quyền lợi|mô tả|yêu cầu|ứng tuyển|thông tin|địa chỉ|nộp|chế độ|tuyển dụng|kết luận',h,re.I)]
 if not roles:
  roles=[re.sub(r'\s+',' ',e.text_content()).strip() for e in b.xpath('//p/strong|//li/strong') if re.match(r'^(?:\d+[.)]\s*)?(?:Nhân viên|Công nhân|Kỹ sư|Kỹ thuật|Chuyên viên|Trưởng|Tổ trưởng|Lái xe|Thợ |Kế toán|Lao động|Phiên dịch|Quản lý|Bảo vệ|Giáo viên)',e.text_content().strip(),re.I) and len(e.text_content())<150]
 roles=list(dict.fromkeys(roles))[:16]
 found=[s for s in skills if re.search(r'(?<!\w)'+re.escape(s)+r'(?!\w)',text,re.I)]
 levels=[s for s in ['Đại học','Cao đẳng','Trung cấp','THPT'] if s.lower() in low]
 salarylines=[];bands=[]
 for e in b.xpath('//li|//p'):
  t=' '.join(e.text_content().split())
  if len(t)>280 or not re.search(r'lương|thu nhập',t,re.I):continue
  for m in re.finditer(r'(\d{1,3}(?:[.,]\d{1,2})?)\s*(?:[-–~]\s*(\d{1,3}(?:[.,]\d{1,2})?))?\s*(?:triệu|tr\b|trđ)',t,re.I):
   a=float(m[1].replace(',','.'));z=float((m[2] or m[1]).replace(',','.'))
   if 1<=a<=150 and a<=z<=200:
    ceiling=bool(re.search(r'upto|up to|tối đa|đến',t[:m.start()],re.I)) and not m[2]
    bands.append({'min':None if ceiling else a,'max':z,'text':t[:180]})
    salarylines.append(t[:180])
 if bands:
  j['min']=max([x['min'] for x in bands if x['min'] is not None],default=0);j['max']=max(x['max'] for x in bands)
  distinct={(x['min'],x['max']) for x in bands}
  j['salaryText']=salarylines[0][:105]
 j['skills']=found;j['positions']=roles[:8];j['positionCount']=len(roles);j['education']=levels
 noexp=bool(re.search(r'không (?:yêu cầu|cần) kinh nghiệm|chưa có kinh nghiệm|không cần kn|không yêu cầu kn',low))
 hasexp=bool(re.search(r'(?:\d+\s*năm kinh nghiệm|kinh nghiệm\s*(?:từ\s*)?\d+)',low))
 j['experienceFlags']=(['none'] if noexp else [])+(['experienced'] if hasexp else [])
 j['exp']='Có vị trí không cần kinh nghiệm' if noexp else ('Có vị trí yêu cầu kinh nghiệm' if hasexp else 'Xem tại nguồn')
 j['type']='Toàn thời gian' if re.search(r'full.?time|toàn thời gian',low) else ('Bán thời gian' if re.search(r'part.?time|bán thời gian',low) else 'Xem tại nguồn')
 details={'id':j['id'],'positions':roles,'skills':found,'education':levels,'salaryStatements':list(dict.fromkeys(salarylines))[:10],'experienceFlags':j['experienceFlags'],'sourceUrl':j['sourceUrl'],'images':list(dict.fromkeys(b.xpath('//img/@src')))[:6]}
 shards[str(j['id']//1000)][str(j['id'])]=details
 j['detailShard']='data/details/'+str(j['id']//1000)+'.json'
(R/'dist/data/jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,separators=(',',':')))
D=R/'dist/data/details';D.mkdir(exist_ok=True)
for key,value in shards.items():(D/(key+'.json')).write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')))
print({'records':len(jobs),'withRoles':sum(bool(j.get('positions')) for j in jobs),'withSalary':sum(j['max']>0 for j in jobs),'withExperience':sum(bool(j.get('experienceFlags')) for j in jobs),'detailShards':len(shards)})
