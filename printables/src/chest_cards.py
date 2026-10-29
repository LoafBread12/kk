"""Builds ../wonders-chest-cards.html: the four puzzle cards for the "صندوق العجائب" hunt, plus a teacher page.

Codes must match games/wonders-chest.html: 463, 3158, 246, 421.
Every answer box on a card carries the same mark (shape or icon) as the matching box on screen,
read left to right as on screen, so children never wonder which digit goes where.
"""
from pathlib import Path

ICONS = {
    "drop": '<path d="M14 2C9 9 6 13 6 17a8 8 0 0 0 16 0c0-4-3-8-8-15z" fill="#4fa3e0"/>',
    "leaf": '<path d="M4 22C4 10 12 4 24 4c0 12-6 20-18 20" fill="#5bb36a"/><path d="M5 23L18 10" stroke="#2d6a36" stroke-width="2"/>',
    "sun": '<circle cx="14" cy="14" r="6" fill="#f0a23a"/><g stroke="#f0a23a" stroke-width="2.4" stroke-linecap="round"><path d="M14 2v3M14 23v3M2 14h3M23 14h3M5.5 5.5l2 2M20.5 20.5l2 2M5.5 22.5l2-2M20.5 7.5l2-2"/></g>',
    "planet": '<circle cx="14" cy="14" r="7" fill="#a98be6"/><ellipse cx="14" cy="14" rx="13" ry="4" fill="none" stroke="#a98be6" stroke-width="2" transform="rotate(-20 14 14)"/>',
    "heart": '<path d="M14 24C6 18 3 14 3 10a5.5 5.5 0 0 1 11-1 5.5 5.5 0 0 1 11 1c0 4-3 8-11 14z" fill="#f0a23a"/>',
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


PLANETS = [("عطارد", "#9a9aa6", ""), ("الزهرة", "#e8c77a", ""), ("الأرض", "#3d8fe0", "earth"), ("المريخ", "#d0573a", ""),
           ("المشتري", "#d9a066", "bands"), ("زحل", "#e3c16b", "ring"), ("أورانوس", "#8fd6e0", ""), ("نبتون", "#3f5fd0", "")]


def planet(color, kind, size="9mm"):
    extra = ""
    if kind == "earth":
        extra = '<path d="M9 10c3-2 6 0 5 3s-4 2-5 5-3-1-3-3 1-4 3-5zM17 17c2-1 4 0 3 2s-3 2-4 1z" fill="#5bb36a"/>'
    elif kind == "bands":
        extra = '<path d="M4 11h20M3.6 16h20.8" stroke="#b07a42" stroke-width="2"/>'
    ring = '<ellipse cx="14" cy="14" rx="13.5" ry="4" fill="none" stroke="#b8963f" stroke-width="2" transform="rotate(-20 14 14)"/>' if kind == "ring" else ""
    r = 8 if kind == "ring" else 10
    return f'<svg viewBox="0 0 28 28" style="width:{size};height:{size};overflow:visible"><circle cx="14" cy="14" r="{r}" fill="{color}"/>{extra}{ring}</svg>'


SUN = '<svg viewBox="0 0 28 28" style="width:11mm;height:11mm"><circle cx="14" cy="14" r="11" fill="#f4c04e"/><circle cx="14" cy="14" r="7" fill="#f8d77a"/></svg>'
strip = SUN + "".join(f'<div class="pl">{planet(c, k, "7.5mm")}<small>{n}</small></div>' for n, c, k in PLANETS)
c1 = card(1, "قفل الكواكب", "#a98be6", "planet", f"""
  <p>هذه الكواكب بالترتيب، من الأقرب إلى الشمس إلى الأبعد:</p>
  <div class="strip">{strip}</div>
  <p>اعرف كل كوكب، ثم عُدّ مكانه من الشمس. (الأقرب إلى الشمس رقمه ١)</p>
  <ul class="clues">
    <li><b>■</b> الكوكب الأحمر.</li>
    <li><b>▲</b> الكوكب الذي حوله حلقات كبيرة.</li>
    <li><b>●</b> الكوكب الذي نعيش عليه.</li>
  </ul>""", ["■", "▲", "●"])

SOIL = '<rect x="0" y="40" width="60" height="20" fill="#b98a5a"/><path d="M0 40h60" stroke="#8a5f36" stroke-width="2"/>'
STAGES = {
    "seed": SOIL + '<ellipse cx="30" cy="48" rx="7" ry="4.5" fill="#7a4a24"/>',
    "root": SOIL + '<ellipse cx="30" cy="46" rx="7" ry="4.5" fill="#7a4a24"/><path d="M30 50c0 3-2 5-1 9M30 52c3 2 5 3 7 6" stroke="#f1e3c8" stroke-width="2" fill="none" stroke-linecap="round"/>',
    "sprout": SOIL + '<path d="M30 52V26" stroke="#3f8a4b" stroke-width="3"/><path d="M30 32c-10-1-14-7-14-12 8 0 13 5 14 12zM30 30c9-2 13-8 13-13-8 0-12 6-13 13z" fill="#5bb36a"/><path d="M30 52c0 3-2 5-1 7M30 53c3 2 5 3 6 6" stroke="#f1e3c8" stroke-width="2" fill="none"/>',
    "flower": SOIL + '<path d="M30 52V18" stroke="#3f8a4b" stroke-width="3"/><path d="M30 40c-10-1-14-6-14-11 8 0 13 4 14 11zM30 34c9-2 13-7 13-12-8 0-12 5-13 12z" fill="#5bb36a"/><g fill="#e46f9a"><circle cx="30" cy="9" r="5"/><circle cx="36" cy="14" r="5"/><circle cx="30" cy="19" r="5"/><circle cx="24" cy="14" r="5"/></g><circle cx="30" cy="14" r="3.5" fill="#f4c04e"/>',
}
pics = "".join(f'<div class="stage"><svg viewBox="0 0 60 60">{STAGES[k]}</svg><b>{d}</b></div>' for k, d in
               [("flower", "٨"), ("root", "١"), ("seed", "٣"), ("sprout", "٥")])
c2 = card(2, "قفل النبات", "#5bb36a", "leaf", f"""
  <p>هذه مراحل نمو نبتة واحدة، لكنها مخلوطة! رتّبها من البداية إلى النهاية، واكتب رقم كل مرحلة في مربّعها.</p>
  <div class="stages">{pics}</div>
  <p class="small">المرحلة الأولى في المربع ذي النقطة الواحدة، والثانية في المربع ذي النقطتين، وهكذا.</p>""", ["•", "••", "•••", "••••"])

c3 = card(3, "قفل جسمي", "#f0a23a", "heart", """
  <p>فكّر في جسمك، واكتب كل جواب في مربّعه:</p>
  <ul class="clues">
    <li><b>■</b> كم رئة في صدرك؟</li>
    <li><b>▲</b> في القلب حجرات، وعددها <b>ضعف</b> عدد الرئتين. كم حجرة في القلب؟</li>
    <li><b>●</b> اجمع رقم <b>■</b> ورقم <b>▲</b>.</li>
  </ul>""", ["■", "▲", "●"])

CYCLE = """<svg class="cycle" viewBox="0 0 200 120">
  <defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5 0 10z" fill="#4fa3e0"/></marker></defs>
  <path d="M0 100q50-10 100 0t100 0v20H0z" fill="#7cc0ef"/>
  <g fill="#fff" stroke="#b8c7d8" stroke-width="1.5"><circle cx="88" cy="22" r="11"/><circle cx="102" cy="16" r="13"/><circle cx="117" cy="24" r="10"/><rect x="84" y="22" width="36" height="12" rx="6" stroke="none"/></g>
  <circle cx="176" cy="20" r="10" fill="#f4c04e"/>
  <path d="M46 90C40 70 50 40 76 30" fill="none" stroke="#4fa3e0" stroke-width="2.5" stroke-dasharray="4 4" marker-end="url(#ar)"/>
  <path d="M130 34c14 10 20 30 18 52" fill="none" stroke="#4fa3e0" stroke-width="2.5" marker-end="url(#ar)"/>
  <g fill="#4fa3e0"><path d="M150 50l-2 6h4z"/><path d="M160 60l-2 6h4z"/><path d="M142 66l-2 6h4z"/></g>
  <g font-family="Readex Pro" font-weight="800" font-size="11" text-anchor="middle" fill="#1d4f91">
    <text x="100" y="114">١ البحر</text><text x="34" y="60">٢ يتبخّر</text><text x="104" y="48">٣ سحابة</text><text x="172" y="88">٤ مطر</text></g>
</svg>"""
c4 = card(4, "قفل الماء", "#4fa3e0", "drop", f"""
  <p>هذه رحلة قطرة الماء. اتبع الأسهم:</p>
  {CYCLE}
  <ul class="clues">
    <li><b>■</b> القطرة الآن في السحابة. ما رقم الخطوة التي بعدها؟</li>
    <li><b>▲</b> ما رقم الخطوة التي قبل السحابة؟</li>
    <li><b>●</b> نزل المطر في البحر. ما رقم الخطوة التي تبدأ بها الرحلة من جديد؟</li>
  </ul>""", ["■", "▲", "●"])

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
      <div><b>البطاقة ١: الكواكب</b><span dir="ltr">٤٦٣</span><small>المريخ رابع كوكب، وزحل سادس كوكب، والأرض ثالث كوكب.</small></div>
      <div><b>البطاقة ٢: النبات</b><span dir="ltr">٣١٥٨</span><small>بذرة (٣)، ثم يخرج الجذر (١)، ثم نبتة بورقتين (٥)، ثم زهرة (٨).</small></div>
      <div><b>البطاقة ٣: جسمي</b><span dir="ltr">٢٤٦</span><small>رئتان، وفي القلب أربع حجرات، ومجموعهما ستة.</small></div>
      <div><b>البطاقة ٤: الماء</b><span dir="ltr">٤٢١</span><small>بعد السحابة المطر (٤)، وقبلها التبخّر (٢)، وتبدأ الرحلة من البحر (١).</small></div>
    </div>

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
.cb i { width: 11mm; height: 12mm; border: .6mm solid var(--c); border-radius: 2mm; background: #fff; }
.strip { display: flex; align-items: flex-end; gap: 1mm; justify-content: space-between; background: #11142c; border-radius: 2.5mm; padding: 2mm 2.5mm; }
.pl { display: flex; flex-direction: column; align-items: center; gap: .6mm; }
.pl small { font-size: 6.5pt; color: #e8e4f4; }
.stages { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2mm; }
.stage { border: .4mm solid #e2dfe8; border-radius: 2.5mm; overflow: hidden; display: flex; flex-direction: column; align-items: center; background: #eef6ff; }
.stage svg { width: 100%; display: block; }
.stage b { font-size: 16pt; padding: .5mm 0; }
.small { font-size: 9.5pt !important; color: #6a6474; }
.cycle { width: 100%; max-height: 32mm; display: block; }
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
