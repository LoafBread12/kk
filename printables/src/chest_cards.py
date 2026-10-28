"""Builds ../wonders-chest-cards.html: the four puzzle cards for the "صندوق العجائب" hunt, plus a teacher page.

Codes must match games/wonders-chest.html: 713, 92, 261, 652.
Every answer box on a card carries the same mark (shape or icon) as the matching box on screen,
read left to right as on screen, so children never wonder which digit goes where.
"""
from pathlib import Path

ICONS = {
    "drop": '<path d="M14 2C9 9 6 13 6 17a8 8 0 0 0 16 0c0-4-3-8-8-15z" fill="#4fa3e0"/>',
    "leaf": '<path d="M4 22C4 10 12 4 24 4c0 12-6 20-18 20" fill="#5bb36a"/><path d="M5 23L18 10" stroke="#2d6a36" stroke-width="2"/>',
    "sun": '<circle cx="14" cy="14" r="6" fill="#f0a23a"/><g stroke="#f0a23a" stroke-width="2.4" stroke-linecap="round"><path d="M14 2v3M14 23v3M2 14h3M23 14h3M5.5 5.5l2 2M20.5 20.5l2 2M5.5 22.5l2-2M20.5 7.5l2-2"/></g>',
    "snow": '<g stroke="#a98be6" stroke-width="2.4" stroke-linecap="round"><path d="M14 2v24M3.6 8l20.8 12M3.6 20L24.4 8M14 6l-3-3M14 6l3-3M14 22l-3 3M14 22l3 3"/></g>',
    "flower": '<g fill="#e46f9a"><circle cx="14" cy="8" r="5"/><circle cx="20" cy="14" r="5"/><circle cx="14" cy="20" r="5"/><circle cx="8" cy="14" r="5"/></g><circle cx="14" cy="14" r="4" fill="#f4c04e"/>',
    "mountain": '<path d="M2 24L11 8l5 8 3-4 7 12z" fill="#8a8fa8"/><path d="M11 8l3 5-3 2-2-3z" fill="#fff"/>',
}
icon = lambda k, size="9mm": f'<svg viewBox="0 0 28 28" style="width:{size};height:{size}">{ICONS[k]}</svg>'
SHAPE = {"■": "■", "▲": "▲", "●": "●"}


def code_row(marks, color):
    cells = "".join(f'<div class="cb"><span>{icon(m, "7mm") if m in ICONS else m}</span><i></i></div>' for m in marks)
    return f'<div class="code" style="--c:{color}"><b>الرقم السري:</b><div class="cbs">{cells}</div></div>'


def card(n, title, color, icon_key, body, marks):
    return f'''<div class="card" style="--c:{color}">
  <div class="ch"><span class="no">{"١٢٣٤"[n-1]}</span><h2>{title}</h2>{icon(icon_key, "10mm")}</div>
  <div class="cbody">{body}</div>
  {code_row(marks, color)}
</div>'''


key = "".join(f'<div class="k">{icon(k, "8mm")}<b>{d}</b></div>' for k, d in
              [("drop", "٧"), ("sun", "١"), ("leaf", "٣"), ("flower", "٥"), ("snow", "٩"), ("mountain", "٢")])
c1 = card(1, "قفل الرموز", "#4fa3e0", "drop", f'''
  <p>لكل رمز رقم. استعمل المفتاح لتعرف رقم كل رمز في الأسفل.</p>
  <div class="key">{key}</div>''', ["drop", "sun", "leaf"])

c2 = card(2, "قفل الأنماط", "#5bb36a", "leaf", '''
  <p>أكمل كل نمط، واكتب الرقم الناقص في مربّعه.</p>
  <div class="pat"><span class="m">■</span><span>١ ، ٣ ، ٥ ، ٧ ، <em>؟</em></span></div>
  <div class="pat"><span class="m">●</span><span>١٠ ، ٨ ، ٦ ، ٤ ، <em>؟</em></span></div>''', ["■", "●"])

c3 = card(3, "قفل المنطق", "#f0a23a", "sun", '''
  <p>في كل شكل رقم واحد. اقرأ الأدلة كلها:</p>
  <ul class="clues">
    <li>الأرقام الثلاثة <b>مختلفة</b>، وليس فيها صفر.</li>
    <li>رقم <b>■</b> ضعف رقم <b>●</b>.</li>
    <li>رقم <b>▲</b> أكبر من رقم <b>■</b>.</li>
    <li>مجموع الأرقام الثلاثة <b>٩</b>.</li>
  </ul>''', ["■", "▲", "●"])

c4 = card(4, "قفل العجائب", "#a98be6", "snow", '''
  <p>تذكّر عجائب الخلق، واكتب كل جواب في مربّعه:</p>
  <ul class="clues">
    <li><b>■</b> كم ضلعًا لندفة الثلج؟</li>
    <li><b>▲</b> كم حاسّة للإنسان؟</li>
    <li><b>●</b> كم رئة في صدرك؟</li>
  </ul>''', ["■", "▲", "●"])

teacher = '''
<section class="page teacher">
  <h1>صندوق العجائب</h1>
  <p class="lead">لعبة بحث عن الكنز: بطاقات حقيقية في الصف، وصندوق بأربعة أقفال على الشاشة.</p>
  <div class="box"><h3>التجهيز (دقيقتان)</h3><ol>
    <li>اطبع صفحة البطاقات بالألوان، وقُصّها على الخط المتقطّع إلى أربع بطاقات.</li>
    <li>خبّئ البطاقات ٢ و٣ و٤ في ثلاثة أماكن من الصف.</li>
    <li>افتح صفحة اللعبة، وفي «للمعلّم» اكتب أماكن البطاقات. (اختياري: اكتب مكان هدية صغيرة للنهاية.)</li>
    <li>اعرض الصفحة على شاشة الصف، وأعطِ الأطفال البطاقة ١.</li></ol></div>
  <div class="box"><h3>اللعب</h3><ol>
    <li>يحلّ الأطفال لغز البطاقة معًا، ويكتبون الرقم السري في مربعاتها.</li>
    <li>يُدخلون الرقم في القفل على الشاشة. الأشكال فوق المربعات على الشاشة هي نفسها التي على البطاقة.</li>
    <li>إذا فُتح القفل ظهرت معلومة عجيبة، ومكان البطاقة التالية، فيجرون إليها.</li>
    <li>بعد القفل الرابع يُفتح صندوق العجائب.</li></ol>
    <p>إذا أخطؤوا ثلاث مرات في قفل، تنتظر الشاشة خمس ثوانٍ، حتى يفكّروا بدل أن يجرّبوا أرقامًا.</p></div>
  <div class="box ans"><h3>الأجوبة</h3>
    <div class="grid4">
      <div><b>البطاقة ١</b><span dir="ltr">٧١٣</span><small>قطرة ٧، شمس ١، ورقة ٣</small></div>
      <div><b>البطاقة ٢</b><span dir="ltr">٩٢</span><small>■ تسعة، لأن النمط يزيد اثنين كل مرة. ● اثنان، لأنه ينقص اثنين.</small></div>
      <div><b>البطاقة ٣</b><span dir="ltr">٢٦١</span><small>● واحد، إذن ■ اثنان، والباقي من التسعة ستة، فهو ▲.</small></div>
      <div><b>البطاقة ٤</b><span dir="ltr">٦٥٢</span><small>ندفة الثلج ٦، الحواس ٥، الرئتان ٢</small></div>
    </div>
    <p class="why">لماذا للبطاقة ٣ جواب واحد؟ لو كان ● اثنين لكان ■ أربعة، ولبقي لـ▲ ثلاثة، وهي أصغر من أربعة. ولو كان ● ثلاثة لكان ■ ستة، ولم يبقَ لـ▲ إلا الصفر، وهو غير مسموح.</p>
  </div>
</section>'''

CSS = '''
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #e8e6ea; }
body { font-family: "Readex Pro", sans-serif; color: #22202a; direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; margin: 10mm auto; background: #fff; overflow: hidden; break-after: page; box-shadow: 0 2px 12px rgba(0,0,0,.12); }
@media print { html, body { background: #fff; } .page { margin: 0; box-shadow: none; } }
h1, h2, h3 { font-family: "Lalezar", "Readex Pro", sans-serif; font-weight: 400; }
.cards { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; height: 100%; }
.card { border: .4mm dashed #9aa0b4; padding: 7mm 7mm 6mm; display: flex; flex-direction: column; gap: 3mm;
        background: radial-gradient(circle at 100% 0, color-mix(in srgb, var(--c) 16%, #fff) 0 30%, #fff 30.5%); }
.ch { display: flex; align-items: center; gap: 2.5mm; border-bottom: .8mm solid var(--c); padding-bottom: 2mm; }
.ch h2 { font-size: 21pt; line-height: 1; flex: 1; color: #2a2235; }
.no { width: 10mm; height: 10mm; border-radius: 50%; background: var(--c); color: #fff; font-weight: 800; font-size: 15pt; display: grid; place-items: center; }
.cbody { flex: 1; display: flex; flex-direction: column; gap: 2.5mm; }
.cbody p { font-size: 12.5pt; line-height: 1.6; }
.key { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2mm; }
.k { display: flex; align-items: center; justify-content: center; gap: 2mm; border: .4mm solid #e2dfe8; border-radius: 2.5mm; padding: 1.5mm; }
.k b { font-size: 22pt; }
.k svg { width: 11mm !important; height: 11mm !important; }
.k { padding: 3mm 1.5mm; }
.pat { display: flex; align-items: center; gap: 3mm; font-size: 23pt; padding-block: 4mm !important; font-weight: 800; background: #f6f6f9; border-radius: 2.5mm; padding: 2mm 3mm; }
.pat em { font-style: normal; color: var(--c); }
.m { color: var(--c); font-size: 16pt; }
.clues { list-style: none; display: grid; gap: 1.6mm; }
.clues li { font-size: 13pt; line-height: 1.6; background: #f6f6f9; border-radius: 2mm; padding: 1.3mm 3mm; }
.clues b { color: var(--c); }
.code { border-top: .4mm solid #e2dfe8; padding-top: 2.5mm; display: flex; align-items: center; justify-content: space-between; gap: 3mm; }
.code > b { font-size: 11pt; }
.cbs { direction: ltr; display: flex; gap: 2mm; }
.cb { display: flex; flex-direction: column; align-items: center; gap: .5mm; }
.cb span { height: 7mm; display: grid; place-items: center; color: var(--c); font-size: 14pt; }
.cb i { width: 12mm; height: 13mm; border: .6mm solid var(--c); border-radius: 2mm; background: #fff; }
.teacher { padding: 14mm; display: flex; flex-direction: column; gap: 5mm; }
.teacher h1 { font-size: 34pt; color: #4a3346; line-height: 1; }
.lead { color: #6a6474; font-size: 12pt; }
.box { border: .4mm solid #ddd6e2; border-radius: 3mm; padding: 4mm 5mm; }
.box h3 { font-size: 16pt; color: #4a3346; margin-bottom: 2mm; }
.box ol { padding-inline-start: 5mm; list-style: arabic-indic; font-size: 11.5pt; line-height: 1.8; }
.box p { font-size: 11pt; line-height: 1.7; margin-top: 2mm; color: #4d4858; }
.grid4 { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.grid4 div { background: #f6f6f9; border-radius: 2.5mm; padding: 3mm; display: grid; gap: 1mm; }
.grid4 span { font-size: 22pt; font-weight: 800; color: #4a3346; }
.grid4 small { font-size: 10pt; color: #6a6474; }
'''

html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>صندوق العجائب: البطاقات</title>
<link href="https://fonts.googleapis.com/css2?family=Lalezar&family=Readex+Pro:wght@400;600;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<section class="page"><div class="cards">{c1}{c2}{c3}{c4}</div></section>
{teacher}
</body></html>'''
(Path(__file__).parent.parent / "wonders-chest-cards.html").write_text(html)
