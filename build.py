from pathlib import Path
from lxml import html, etree
import json, re
from html import escape
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
BASE='https://ziyorattour.uz'
template=(ROOT/'template.html').read_text()
css=re.search(r'<style>(.*?)</style>',template,re.S).group(1)
(OUT/'assets/site.css').write_text(css.replace("url('assets/","url('")+'\n.program{max-width:850px;margin:auto}.program h1{font-size:52px}.program p,.program li{line-height:1.85}.program img{width:100%;max-height:420px;object-fit:cover;border-radius:14px}.program .breadcrumb{font-size:14px;margin-bottom:30px}.program .actions{margin-top:35px}.program h2{font-size:30px;margin-top:35px}.program ul{padding-left:22px}.program .notice{background:#f2f7f0;padding:24px;border-left:3px solid #42a834}.program .eyebrow{color:#26781d}@media(max-width:650px){.program h1{font-size:40px}}')
(OUT/'assets/site.js').write_text('''const menu=document.querySelector('.menu'),nav=document.getElementById('nav');if(menu&&nav){menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}));}const year=document.getElementById('year');if(year)year.textContent=new Date().getFullYear();''')
with (OUT/'assets/site.js').open('a') as js: js.write('\n'+(ROOT/'request.js').read_text())
# Images are re-encoded without changing their content or composition.
from PIL import Image
for name in ['makkah-konevi','makkah-yasir','madinah-samet']:
 im=Image.open(OUT/f'assets/{name}.jpg');im.save(OUT/f'assets/{name}.webp','WEBP',quality=83,method=6)
agency={'@type':'TravelAgency','@id':BASE+'/#organization','name':'Ziyorat Tour','url':BASE+'/', 'logo':BASE+'/assets/ziyorat-logo.png','image':BASE+'/assets/makkah-konevi.webp','telephone':'+998712000321','email':'sale.juba@gmail.com','address':{'@type':'PostalAddress','streetAddress':'ул. Ислама Каримова, 49, 10 этаж, офис 103','addressLocality':'Ташкент','addressCountry':'UZ'},'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],'opens':'09:00','closes':'18:00'}],'contactPoint':[{'@type':'ContactPoint','telephone':'+998999882220','contactType':'customer service','availableLanguage':['uz','ru']}],'sameAs':['https://t.me/juba_info','https://instagram.com/ziyorattour','https://facebook.com/ziyorattour']}
programs={'standart': {'name': 'Standart', 'ru': 'Стандарт', 'img': 'makkah-yasir', 'uz_desc': 'Byudjetga mos individual Umra safarini tanlash. Sana, mehmonxona va xizmatlar turoperator bilan kelishiladi.', 'ru_desc': 'Индивидуальный подбор Умры с учётом бюджета. Даты, отель и услуги согласуются с туроператором.', 'uz_items': ['Byudjetga mos amaliy variant', 'Sana va davomiylik kelishuv asosida', 'Mavjud takliflardan mehmonxona tanlovi', 'Xizmatlar tarkibi alohida tasdiqlanadi'], 'ru_items': ['Практичный вариант в рамках бюджета', 'Даты и длительность по согласованию', 'Проживание из доступных предложений', 'Состав услуг подтверждается отдельно']}, 'komfort': {'name': 'Komfort', 'ru': 'Комфорт', 'img': 'madinah-samet', 'uz_desc': 'Qulay yashashga e’tibor bilan individual Umra safarini tanlash. Sana, mehmonxona va xizmatlar turoperator bilan kelishiladi.', 'ru_desc': 'Индивидуальный подбор Умры с акцентом на удобство проживания. Даты, отель и услуги согласуются с туроператором.', 'uz_items': ['Yashash qulayligiga ko‘proq e’tibor', 'Mehmonxona joylashuvi istagingizga mos', 'Transport va ovqatlanish muhokama qilinadi', 'Variantlar turoperatorga bog‘liq'], 'ru_items': ['Больше внимания удобству проживания', 'Расположение отеля по вашим пожеланиям', 'Транспорт и питание обсуждаются', 'Варианты зависят от туроператора']}, 'vip': {'name': 'VIP', 'ru': 'VIP', 'img': 'makkah-konevi', 'uz_desc': 'Alohida istaklarga mos individual Umra safarini tanlash. Sana, mehmonxona va xizmatlar turoperator bilan kelishiladi.', 'ru_desc': 'Индивидуальный подбор Умры с особыми пожеланиями к поездке. Даты, отель и услуги согласуются с туроператором.', 'uz_items': ['Safarga individual istaklar', 'Mehmonxona va transport afzalliklari', 'Hamrohlik alohida muhokama qilinadi', 'Imkoniyatlar so‘rov bo‘yicha tasdiqlanadi'], 'ru_items': ['Индивидуальные пожелания к поездке', 'Предпочтения по отелю и транспорту', 'Сопровождение обсуждается отдельно', 'Возможности подтверждаем по запросу']}}
def route(lang,key=None):
 return ('/' if lang=='uz' else '/ru/') if key is None else f'/{lang}/umra-{key}/'
def node(tag,text=None,**attrs):
 el=etree.Element(tag,**attrs)
 if text is not None:el.text=text
 return el
def inner(el,markup):
 for child in list(el):el.remove(child)
 el.text=None
 for part in html.fragments_fromstring(markup):
  if isinstance(part,str):el.text=(el.text or '')+part
  else:el.append(part)
def base_doc(lang):
 doc=html.document_fromstring(template)
 if lang=='ru':
  for el in doc.xpath('//*[@data-ru]'):inner(el,el.get('data-ru'))
 for el in doc.xpath('//*[@data-ru]'):
  del el.attrib['data-ru']
 doc.set('lang',lang)
 for el in doc.xpath('//style|//script|//dialog'):
  el.getparent().remove(el)
 head=doc.find('head');head.append(node('link',rel='stylesheet',href='/assets/site.css'))
 doc.find('body').append(node('script',src='/assets/site.js',defer='defer'))
 for el in doc.xpath('//*[@src]'):
  src=el.get('src')
  if src.startswith('assets/'):el.set('src','/'+src.replace('.jpg','.webp'))
 for el in doc.xpath('//a[@href]'):
  href=el.get('href')
  if href.startswith('#'):el.set('href',route(lang)+href)
  elif el.get('data-saudi-request'):el.set('href',route(lang)+'?interest=saudi&route='+el.get('data-saudi-request')+'#selection')
  elif href=='photo-credits.html':el.set('href','/photo-credits.html')
 for el in doc.xpath('//*[@id="language"]'):
  el.tag='a';el.set('href',route('ru' if lang=='uz' else 'uz'));el.text='RU' if lang=='uz' else 'UZ'
  el.set('aria-label','Русская версия' if lang=='uz' else 'O‘zbekcha versiya')
 for el in doc.xpath('//*[@aria-label="Ziyorat Tour bosh sahifa"]'):el.set('aria-label','Ziyorat Tour — главная' if lang=='ru' else 'Ziyorat Tour bosh sahifa')
 for el in doc.xpath('//*[@class="menu"]'):el.set('aria-label','Открыть меню' if lang=='ru' else 'Menyuni ochish')
 for el in doc.xpath('//img'):
  if el.get('class')=='brandlogo':continue
  if lang=='ru':
   src=el.get('src','')
   cities={'riyadh':'Современный Эр-Рияд','alula':'Историческая Аль-Ула','jeddah':'Красное море у Джидды'}
   match=next((v for k,v in cities.items() if k in src),None)
   if match:el.set('alt',match);continue
   el.set('alt','Мечеть Пророка в Медине' if 'madinah' in src else 'Кааба и паломники в мечети Масджид аль-Харам, Мекка')
 for el in doc.xpath('//article[@class="card"]//h3'):
  if lang=='ru' and el.text in ['Standart','Komfort']:el.text={'Standart':'Стандарт','Komfort':'Комфорт'}[el.text]
 for el in doc.xpath('//nav[@class="mobilebar"]'):el.set('aria-label','Быстрая связь' if lang=='ru' else 'Tezkor aloqa')
 for el in doc.xpath('//*[@data-tour]'):
  key=el.get('data-tour').lower();el.tag='a';el.set('href',route(lang,key));del el.attrib['data-tour']
 for el in doc.xpath('//*[@class="fine center"]'):
  el.text=('Bu qulaylik darajalari — tayyor paketlar emas. Narx, sana, mehmonxona va xizmatlar turoperator bilan kelishilgandan keyin tasdiqlanadi.' if lang=='uz' else 'Это ориентиры по комфорту, а не фиксированные пакеты. Стоимость, даты, отель и услуги подтверждаем после согласования с туроператором.')
 for el in doc.xpath('//*[@class="footertext"]'):
  if 'konsepsiyasi' in (el.text or '') or 'концепция' in (el.text or ''):el.text='Umra · Toshkent · Makka · Madina' if lang=='uz' else 'Умра · Ташкент · Мекка · Медина'
 return doc
urls=[]
for lang in ['uz','ru']:
 for key in [None,*programs]:
  doc=base_doc(lang);path=route(lang,key);url=BASE+path;head=doc.find('head')
  if key:
   data=programs[key];name=data['name'] if lang=='uz' else data['ru'];desc=data[f'{lang}_desc'];title=(f'Umra {name} Toshkentdan — dastur va maslahat | Ziyorat Tour' if lang=='uz' else f'Умра {name} из Ташкента — индивидуальный подбор | Ziyorat Tour')
   main=doc.find('.//main');main.clear();main.set('class','wrap program');main.set('style','padding-top:55px;padding-bottom:70px')
   home='Bosh sahifa' if lang=='uz' else 'Главная';heading=f'Umra {name} — Toshkentdan' if lang=='uz' else f'Умра {name} из Ташкента'
   notice='Bu tayyor paket emas, qulaylik darajasi bo‘yicha yo‘nalish. Yakuniy sana, mehmonxona, narx va xizmatlar turoperator bilan kelishilgandan keyin tasdiqlanadi. Fotosuratlar ziyorat manzillarini ko‘rsatadi.' if lang=='uz' else 'Это ориентир по уровню комфорта, а не фиксированный тур. Итоговые даты, проживание, стоимость и состав услуг подтверждаем после согласования с туроператором. Фотографии иллюстрируют места паломничества.'
   markup=f'''<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{route(lang)}">{home}</a> / Umra {escape(name)}</nav><span class="eyebrow">ZIYORAT TOUR · UMRA</span><h1>{heading}</h1><p>{escape(desc)}</p><img src="/assets/{data['img']}.webp" alt="{'Makka va Madina ziyorat manzillari' if lang=='uz' else 'Места паломничества в Мекке и Медине'}" width="1200" height="800"><h2>{'Tanlashda nimalarni muhokama qilamiz?' if lang=='uz' else 'Что обсудим при подборе'}</h2><ul>{''.join('<li>'+escape(t)+'</li>' for t in data[f'{lang}_items'])}</ul><p class="notice">{notice}</p><h2>{'Narx va safar sanalarini bilish' if lang=='uz' else 'Узнать стоимость и даты поездки'}</h2><p>{'Istalgan safar sanasi, ziyoratchilar soni va mehmonxona bo‘yicha istaklaringizni ayting. Ofisimiz: Toshkent, Islom Karimov ko‘chasi, 49, 10-qavat, 103-ofis. Du–Sh, 9:00–18:00.' if lang=='uz' else 'Сообщите желаемые даты, количество путешественников и пожелания к проживанию. Наш офис: Ташкент, ул. Ислама Каримова, 49, 10 этаж, офис 103. Пн–Сб, 9:00–18:00.'}</p><div class="actions"><a class="btn" href="{route(lang)}?comfort={key}#selection">{'Safarni tanlash' if lang=='uz' else 'Подобрать поездку'}</a><a class="btn light" href="https://t.me/juba_info" target="_blank" rel="noopener">{'Telegram orqali yozish' if lang=='uz' else 'Написать в Telegram'} ↗</a><a class="btn outline" href="tel:+998712000321">+998 71 200 03 21</a><a class="textlink" href="{route(lang)}#tours">{'Barcha qulaylik darajalari' if lang=='uz' else 'Все уровни комфорта'}</a></div>'''
   inner(main,markup)
  else:
   title='Toshkentdan individual Umra safarini tanlash | Ziyorat Tour' if lang=='uz' else 'Индивидуальная Умра из Ташкента — подбор поездки | Ziyorat Tour'
   desc='Toshkentdan individual Umra safarini tanlash. Sana, byudjet va xizmatlar turoperator takliflari asosida kelishiladi. Ziyorat Tour: +998 71 200 03 21.' if lang=='uz' else 'Индивидуальный подбор Умры из Ташкента. Даты, бюджет, проживание и услуги согласуем по предложениям туроператора. Ziyorat Tour: +998 71 200 03 21.'
   hero=doc.xpath('//div[@class="hero"]//*[@class="eyebrow"]')[0];hero.text='TOSHKENTDAN UMRA · MAKKA · MADINA' if lang=='uz' else 'УМРА ИЗ ТАШКЕНТА · МЕККА · МЕДИНА'
  head.find('title').text=title
  head.xpath('./meta[@name="description"]')[0].set('content',desc)
  for alt in ['uz','ru']:
   head.append(node('link',rel='alternate',hreflang=alt,href=BASE+route(alt,key)))
  head.append(node('link',rel='alternate',hreflang='x-default',href=BASE+route('uz',key)))
  head.append(node('link',rel='canonical',href=url))
  head.append(node('meta',name='robots',content='index,follow,max-image-preview:large'))
  head.append(node('meta',name='theme-color',content='#42a834'))
  for prop,value in {'og:type':'website','og:site_name':'Ziyorat Tour','og:title':title,'og:description':desc,'og:url':url,'og:locale':'uz_UZ' if lang=='uz' else 'ru_UZ','og:image':BASE+'/assets/makkah-konevi.webp','og:image:alt':'Кааба, Мекка — Konevi / Pexels'}.items():head.append(node('meta',property=prop,content=value))
  head.append(node('meta',name='twitter:card',content='summary_large_image'))
  head.append(node('link',rel='icon',href='/assets/favicon.png',type='image/png'))
  website={'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Ziyorat Tour','publisher':{'@id':agency['@id']},'inLanguage':['uz','ru']}
  web={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':website['@id']},'about':{'@id':agency['@id']}}
  graph=[agency,website,web]
  if key:
   service={'@type':'Service','@id':url+'#service','name':heading,'serviceType':'Umra pilgrimage travel','description':desc,'url':url,'provider':{'@id':agency['@id']},'areaServed':{'@type':'Country','name':'Uzbekistan'}}
   graph.extend([service,{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':home,'item':BASE+route(lang)},{'@type':'ListItem','position':2,'name':heading,'item':url}]}])
   language=doc.xpath('//*[@id="language"]')[0];language.set('href',route('ru' if lang=='uz' else 'uz',key))
  else:
   graph.append({'@type':'ItemList','name':'Umra dasturlari' if lang=='uz' else 'Программы Умры','itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+route(lang,k),'name':'Umra '+v['name']} for i,(k,v) in enumerate(programs.items())]})
  data=node('script',type='application/ld+json');data.text=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/');head.append(data)
  output=OUT/('index.html' if path=='/' else path.strip('/')+'/index.html');output.parent.mkdir(parents=True,exist_ok=True);output.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html'))
  urls.append(url)
# Preserve the mark's original geometry when making the favicon.
logo=Image.open(OUT/'assets/ziyorat-logo.png').convert('RGBA');icon=logo.crop((680,0,936,280));icon.thumbnail((64,64));canvas=Image.new('RGBA',(64,64),'white');canvas.alpha_composite(icon,((64-icon.width)//2,(64-icon.height)//2));canvas.save(OUT/'assets/favicon.png')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT/'404.html').write_text('<!doctype html><html lang="uz"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Sahifa topilmadi | Ziyorat Tour</title><h1>Sahifa topilmadi / Страница не найдена</h1><p><a href="/">Bosh sahifa</a> · <a href="/ru/">Главная</a></p></html>')
ht=r'''# Apache deployment only. Existing Node.js hosting must be configured separately.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} ^www\.ziyorattour\.uz$ [NC]
RewriteRule ^ https://ziyorattour.uz%{REQUEST_URI} [R=301,L,NE]
RewriteRule ^uz/?$ / [R=301,L]
'''
for n,k in enumerate(programs,1):
 for lang in ['ru','uz']:ht+=f'RewriteRule ^blog-{n}/{lang}/?$ {route(lang,k)} [R=301,L]\n'
ht+='''<IfModule mod_headers.c>
<FilesMatch "\\.(webp|jpg|png|css|js)$">
Header set Cache-Control "public, max-age=86400"
</FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/ld+json application/xml text/plain
</IfModule>
'''
(OUT/'.htaccess').write_text(ht)
# Credits are not landing pages for organic search.
credits=OUT/'photo-credits.html';c=credits.read_text();
if 'name="robots"' not in c:c=c.replace('<title>','<meta name="robots" content="noindex,follow"><title>')
credits.write_text(c)
print('Built',len(urls),'indexable, fully rendered pages.')

# GitHub Pages: no .htaccess, so old addresses get small redirect pages (canonical + meta refresh).
REDIRECTS={'uz':'/','blog-1/ru':'/ru/umra-standart/','blog-1/uz':'/uz/umra-standart/','blog-2/ru':'/ru/umra-komfort/','blog-2/uz':'/uz/umra-komfort/','blog-3/ru':'/ru/umra-vip/','blog-3/uz':'/uz/umra-vip/'}
for old,new in REDIRECTS.items():
 target=OUT/old/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(f'<!doctype html><meta charset="utf-8"><title>Ziyorat Tour</title><link rel="canonical" href="{BASE}{new}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={new}"><a href="{new}">Ziyorat Tour</a>')
(OUT/'CNAME').write_text('ziyorattour.uz\n')
(OUT/'.nojekyll').write_text('')
