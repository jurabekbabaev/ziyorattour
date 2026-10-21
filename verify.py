from pathlib import Path
from lxml import html,etree
import json
from urllib.parse import urlsplit
root=Path(__file__).parent/'dist'
errors=[];titles=set();n=0
for p in root.rglob('*.html'):
 if p.name in ['404.html','photo-credits.html']:continue
 doc=html.fromstring(p.read_text())
 if doc.xpath('//meta[@http-equiv="refresh"]'):continue  # redirect stub for old URLs
 n+=1
 title=doc.findtext('.//title');assert title and title not in titles,(p,'title');titles.add(title)
 assert len(doc.xpath('//h1'))==1,(p,'h1')
 assert len(doc.xpath('//link[@rel="canonical"]'))==1,(p,'canonical')
 assert len(doc.xpath('//link[@hreflang]'))==3,(p,'hreflang')
 assert doc.xpath('//meta[@name="description"]/@content')[0]
 for script in doc.xpath('//script[@type="application/ld+json"]'):json.loads(script.text)
 for el in doc.xpath('//*[@href or @src]'):
  value=el.get('href') or el.get('src');url=urlsplit(value)
  if url.scheme or not url.path:continue
  target=root/url.path.lstrip('/')
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append((str(p),value))
  elif url.fragment and target.suffix=='.html':
   linked=html.fromstring(target.read_text())
   if not linked.xpath('//*[@id=$id]',id=url.fragment):errors.append((str(p),'Missing fragment '+value))
 assert not doc.xpath('//*[@data-ru]'),(p,'unrendered translations')
for loc in etree.parse(str(root/'sitemap.xml')).xpath('//*[local-name()="loc"]/text()'):
 target=root/urlsplit(loc).path.lstrip('/')
 assert (target/'index.html').exists(),loc
assert not errors,errors
print(f'PASS: {n} pages, unique titles, descriptions, headings, alternate languages, structured JSON, local links, assets, anchors and sitemap.')
