(function(){
var tg=document.querySelector('.menu-tg'),nav=document.getElementById('nav');
if(tg&&nav){tg.addEventListener('click',function(){var o=nav.classList.toggle('open');tg.setAttribute('aria-expanded',o?'true':'false');});}
document.querySelectorAll('.sub-tg').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();var li=b.parentNode,o=li.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){document.querySelectorAll('.has-sub.open').forEach(function(li){li.classList.remove('open');var b=li.querySelector('.sub-tg');if(b)b.setAttribute('aria-expanded','false');});if(nav&&nav.classList.contains('open')){nav.classList.remove('open');tg.setAttribute('aria-expanded','false');tg.focus();}}});
document.addEventListener('click',function(e){if(!e.target.closest('.has-sub')){document.querySelectorAll('.has-sub.open').forEach(function(li){if(window.innerWidth>=960){li.classList.remove('open');var b=li.querySelector('.sub-tg');if(b)b.setAttribute('aria-expanded','false');}});}});
window.dataLayer=window.dataLayer||[];
function gtag(){window.dataLayer.push(arguments);}
window.gtag=gtag;gtag('js',new Date());gtag('config','G-P5V1J7ZCK8');
document.addEventListener('click',function(e){var a=e.target.closest('a[href^="tel:"]');if(a){gtag('event','call_click',{call_location:a.getAttribute('data-call')||'link',page_path:location.pathname});}});
var y=document.querySelector('[data-y]');if(y)y.textContent=new Date().getFullYear();
})();