const tripForm=document.getElementById('trip-form');
if(tripForm){
 const ru=document.documentElement.lang==='ru';
 const preference=new URLSearchParams(location.search).get('comfort');
 if(new URLSearchParams(location.search).get('interest')==='saudi')tripForm.elements.wishes.value=ru?'Интересует экскурсионная поездка по Саудовской Аравии: Эр-Рияд, Аль-Ула, Джидда. Хочу обсудить варианты и возможность сочетания с Умрой.':'Saudiya Arabistoni bo‘ylab ekskursiya safari qiziqtiradi: Ar-Riyod, Al-Ula, Jidda. Variantlar va Umra bilan birlashtirish imkoniyatini muhokama qilmoqchiman.';
 if(['standart','komfort','vip'].includes(preference))tripForm.elements.comfort.value={standart:'Standart',komfort:'Komfort',vip:'VIP'}[preference];
 const LEAD_URL='https://jubatravel.uz/lead.php';
 tripForm.addEventListener('submit',async event=>{
  event.preventDefault();if(!tripForm.reportValidity())return;
  const data=new FormData(tripForm),labels=ru?['Желаемые даты','Путешественников','Уровень комфорта','Бюджет на всю поездку (на всех)' ,'Пожелания']:['Istalgan sanalar','Ziyoratchilar soni','Qulaylik darajasi','Butun safar uchun byudjet (barcha ziyoratchilar)' ,'Istaklar'];
  const excursion=new URLSearchParams(location.search).get('interest')==='saudi';
  const details=['dates','travelers','comfort','budget','wishes'].map((key,i)=>labels[i]+': '+(String(data.get(key)||'').trim()||(ru?'Обсудим':'Muhokama qilamiz'))).join('\n');
  const name=String(data.get('name')||'').trim(),phone=String(data.get('phone')||'').trim();
  document.getElementById('trip-brief').value=(excursion?(ru?'Здравствуйте! Хочу подобрать экскурсионную поездку по Саудовской Аравии.':'Assalomu alaykum! Saudiya Arabistoni bo‘ylab ekskursiya safarini tanlamoqchiman.'):(ru?'Здравствуйте! Хочу подобрать индивидуальную поездку на Умру.':'Assalomu alaykum! Individual Umra safarini tanlamoqchiman.'))+'\n'+(ru?'Имя':'Ism')+': '+name+'\n'+(ru?'Телефон':'Telefon')+': '+phone+'\n\n'+details;
  const button=document.getElementById('trip-submit'),sent=document.getElementById('trip-sent'),result=document.getElementById('trip-result');
  button.disabled=true;result.hidden=true;sent.hidden=true;
  try{
   const res=await fetch(LEAD_URL,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,phone,website:String(data.get('website')||''),message:(excursion?(ru?'Экскурсия по Саудовской Аравии':'Saudiya bo‘ylab ekskursiya'):'Umra')+' · '+(ru?'русская версия':'o‘zbekcha versiya')+'\n'+details})});
   if(!res.ok)throw new Error('status '+res.status);
   sent.textContent=ru?'Спасибо, '+name+'! Заявка отправлена. Менеджер свяжется с вами в рабочее время (Пн–Сб, 9:00–18:00).':'Rahmat, '+name+'! Arizangiz yuborildi. Menejer ish vaqtida (Du–Sh, 9:00–18:00) siz bilan bog‘lanadi.';
   sent.hidden=false;tripForm.querySelectorAll('input:not([name=travelers]),textarea:not(#trip-brief)').forEach(el=>{el.value=''});
  }catch(err){
   result.hidden=false;document.getElementById('copy-status').textContent='';document.getElementById('trip-brief').focus();
  }finally{button.disabled=false;}
 });
 document.getElementById('copy-brief').addEventListener('click',async()=>{
  const brief=document.getElementById('trip-brief'),status=document.getElementById('copy-status');
  try{await navigator.clipboard.writeText(brief.value);status.textContent=ru?'Текст скопирован. Откройте наш Telegram и вставьте его в сообщение.':'Matn nusxalandi. Telegram chatimizni ochib, xabarga joylashtiring.';}
  catch{brief.focus();brief.select();status.textContent=ru?'Скопируйте выделенный текст вручную и отправьте в Telegram.':'Belgilangan matnni qo‘lda nusxalab, Telegram orqali yuboring.';}
 });
}

if(tripForm&&new URLSearchParams(location.search).get('interest')==='saudi'){const ru=document.documentElement.lang==='ru',key=new URLSearchParams(location.search).get('route'),names={kingdom:['Qirollik bo‘ylab sayohat','Тур по королевству'],mystery:['Sirli Saudiya','Загадочная Саудия'],treasures:['Saudiya Arabistoni xazinalari','Сокровища Саудовской Аравии']};if(names[key])tripForm.elements.wishes.value=(ru?'Интересует экскурсионный маршрут: ':'Ekskursiya yo‘nalishi qiziqtiradi: ')+names[key][ru?1:0]+'.';}
