const tripForm=document.getElementById('trip-form');
if(tripForm){
 const ru=document.documentElement.lang==='ru';
 const preference=new URLSearchParams(location.search).get('comfort');
 if(new URLSearchParams(location.search).get('interest')==='saudi')tripForm.elements.wishes.value=ru?'Интересует экскурсионная поездка по Саудовской Аравии: Эр-Рияд, Аль-Ула, Джидда. Хочу обсудить варианты и возможность сочетания с Умрой.':'Saudiya Arabistoni bo‘ylab ekskursiya safari qiziqtiradi: Ar-Riyod, Al-Ula, Jidda. Variantlar va Umra bilan birlashtirish imkoniyatini muhokama qilmoqchiman.';
 if(['standart','komfort','vip'].includes(preference))tripForm.elements.comfort.value={standart:'Standart',komfort:'Komfort',vip:'VIP'}[preference];
 tripForm.addEventListener('submit',event=>{
  event.preventDefault();if(!tripForm.reportValidity())return;
  const data=new FormData(tripForm),labels=ru?['Желаемые даты','Путешественников','Уровень комфорта','Бюджет на всю поездку (на всех)' ,'Пожелания']:['Istalgan sanalar','Ziyoratchilar soni','Qulaylik darajasi','Butun safar uchun byudjet (barcha ziyoratchilar)' ,'Istaklar'];
  const excursion=new URLSearchParams(location.search).get('interest')==='saudi';
  document.getElementById('trip-brief').value=(excursion?(ru?'Здравствуйте! Хочу подобрать экскурсионную поездку по Саудовской Аравии.':'Assalomu alaykum! Saudiya Arabistoni bo‘ylab ekskursiya safarini tanlamoqchiman.'):(ru?'Здравствуйте! Хочу подобрать индивидуальную поездку на Умру.':'Assalomu alaykum! Individual Umra safarini tanlamoqchiman.'))+'\n\n'+['dates','travelers','comfort','budget','wishes'].map((key,i)=>labels[i]+': '+(String(data.get(key)||'').trim()||(ru?'Обсудим':'Muhokama qilamiz'))).join('\n');
  document.getElementById('trip-result').hidden=false;document.getElementById('copy-status').textContent='';document.getElementById('trip-brief').focus();
 });
 document.getElementById('copy-brief').addEventListener('click',async()=>{
  const brief=document.getElementById('trip-brief'),status=document.getElementById('copy-status');
  try{await navigator.clipboard.writeText(brief.value);status.textContent=ru?'Текст скопирован. Откройте наш Telegram и вставьте его в сообщение.':'Matn nusxalandi. Telegram chatimizni ochib, xabarga joylashtiring.';}
  catch{brief.focus();brief.select();status.textContent=ru?'Скопируйте выделенный текст вручную и отправьте в Telegram.':'Belgilangan matnni qo‘lda nusxalab, Telegram orqali yuboring.';}
 });
}

if(tripForm&&new URLSearchParams(location.search).get('interest')==='saudi'){const ru=document.documentElement.lang==='ru',key=new URLSearchParams(location.search).get('route'),names={kingdom:['Qirollik bo‘ylab sayohat','Тур по королевству'],mystery:['Sirli Saudiya','Загадочная Саудия'],treasures:['Saudiya Arabistoni xazinalari','Сокровища Саудовской Аравии']};if(names[key])tripForm.elements.wishes.value=(ru?'Интересует экскурсионный маршрут: ':'Ekskursiya yo‘nalishi qiziqtiradi: ')+names[key][ru?1:0]+'.';}
