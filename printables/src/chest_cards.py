"""Builds ../wonders-chest-cards.html: the four puzzle cards for the "صندوق العجائب" hunt, plus a teacher page.

Codes must match games/wonders-chest.html: 514, 13, 352, 312.
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
    "senses": '<g fill="#f0a23a"><circle cx="14" cy="5" r="3.2"/><circle cx="23" cy="11" r="3.2"/><circle cx="20" cy="22" r="3.2"/><circle cx="8" cy="22" r="3.2"/><circle cx="5" cy="11" r="3.2"/></g><circle cx="14" cy="14" r="3" fill="#f0a23a" opacity=".5"/>',
    "melt": '<rect x="6" y="5" width="14" height="13" rx="2" fill="#bfe3ff" stroke="#4fa3e0" stroke-width="1.5"/><path d="M4 24c4-3 16-3 20 0" stroke="#4fa3e0" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M13 19v3" stroke="#4fa3e0" stroke-width="2" stroke-linecap="round"/>',
    "steam": '<path d="M9 24c-3-4 3-6 0-10s2-6 0-9M15 24c-3-4 3-6 0-10s2-6 0-9M21 24c-3-4 3-6 0-10s2-6 0-9" stroke="#8fa7bf" stroke-width="2" fill="none" stroke-linecap="round"/>',
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


import math

# planets drawn bigger or smaller to show which is large (not to true scale)
PLANETS = [("عطارد", "#9a9aa6", 3.2, ""), ("الزهرة", "#e8c77a", 5, ""), ("الأرض", "#3d8fe0", 5.3, "earth"), ("المريخ", "#d0573a", 4, ""),
           ("المشتري", "#d9a066", 14, "bands"), ("زحل", "#e3c16b", 8.5, "ring"), ("أورانوس", "#8fd6e0", 7, ""), ("نبتون", "#3f5fd0", 7, "")]


def planet_strip():
    # sun on the right, planets going left (reading direction)
    x, parts = 292, ['<circle cx="306" cy="30" r="22" fill="#f4c04e"/><circle cx="306" cy="30" r="15" fill="#f8d77a"/>']
    for name, color, r, kind in PLANETS:
        x -= max(r, 6) + 8
        cx = x
        body = f'<circle cx="{cx}" cy="30" r="{r}" fill="{color}"/>'
        if kind == "earth":
            body += f'<path d="M{cx-2} {30-3}c2-1 3 1 2 2s-2 1-3 2-2-1-1-2z" fill="#5bb36a"/>'
        elif kind == "bands":
            body += f'<path d="M{cx-13} 26h26M{cx-13.5} 33h27" stroke="#b07a42" stroke-width="2"/>'
        elif kind == "ring":
            body += f'<ellipse cx="{cx}" cy="30" rx="{r+6}" ry="3.5" fill="none" stroke="#b8963f" stroke-width="2" transform="rotate(-18 {cx} 30)"/>'
        parts.append(body + f'<text x="{cx}" y="58" text-anchor="middle" font-size="7" fill="#e8e4f4" font-family="Readex Pro">{name}</text>')
        x -= max(r, 6) + 8
    return f'<svg class="strip" viewBox="{x} 0 {340 - x} 64">{"".join(parts)}</svg>'


c1 = card(1, "قفل الكواكب", "#a98be6", "planet", f"""
  <p>هذه الكواكب بالترتيب من الشمس. <b>رقم الكوكب = مكانه من الشمس</b> (الأقرب رقمه ١).</p>
  {planet_strip()}
  <ul class="clues">
    <li><b>■</b> ما رقم أكبر كوكب؟</li>
    <li><b>▲</b> ما رقم أقرب كوكب إلى الشمس؟</li>
    <li><b>●</b> ما رقم الكوكب الذي بين الأرض والمشتري؟</li>
  </ul>""", ["■", "▲", "●"])


def flower(n):
    if n == 0:
        return ('<svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="24" fill="none" stroke="#5bb36a" stroke-width="2" stroke-dasharray="4 4"/>'
                '<text x="30" y="40" text-anchor="middle" font-size="28" font-weight="800" fill="#5bb36a" font-family="Readex Pro">؟</text></svg>')
    petals = "".join(f'<ellipse cx="30" cy="13" rx="{max(3.2, 9 - n * .45):.1f}" ry="12" fill="#e46f9a" stroke="#c04f7a" stroke-width="1" transform="rotate({360 * k / n:.1f} 30 30)"/>'
                     for k in range(n))
    return f'<svg viewBox="0 0 60 60">{petals}<circle cx="30" cy="30" r="7" fill="#f4c04e"/></svg>'


flowers = "".join(f'<div class="fl">{flower(n)}<b>{lbl}</b></div>' for n, lbl in [(3, "٣ بتلات"), (5, "٥ بتلات"), (8, "٨ بتلات"), (0, "كم بتلة؟")])
c2 = card(2, "قفل الأزهار", "#5bb36a", "leaf", f"""
  <p>عُدّ بتلات كل زهرة. هناك سرّ يربط بين الأعداد! اكتشفه، واعرف عدد بتلات الزهرة الأخيرة.</p>
  <div class="flowers">{flowers}</div>
  <p class="small">تلميح: انظر إلى الزهرتين الأوليين، ثم إلى الثالثة. ماذا تلاحظ؟</p>""", ["✿", "✿"])

ORGANS = "".join(f'<div class="o"><b>{d}</b>{n}</div>' for d, n in [("١", "العين"), ("٢", "الأذن"), ("٣", "الأنف"), ("٤", "اللسان"), ("٥", "الجلد")])
c3 = card(3, "قفل الحواس", "#f0a23a", "senses", f"""
  <p>لكل عضو رقم. أيّ عضو تستعمل في كل موقف؟</p>
  <div class="organs">{ORGANS}</div>
  <ul class="clues">
    <li><b>■</b> عرفتُ أن الخبز طازج من رائحته.</li>
    <li><b>▲</b> أحسستُ أن الماء بارد حين لمسته.</li>
    <li><b>●</b> عرفتُ أن المطر بدأ من صوته على النافذة.</li>
  </ul>""", ["■", "▲", "●"])

STATES = "".join(f'<div class="o"><b>{d}</b>{icon(k, "6mm")}{n}</div>' for d, k, n in [("١", "melt", "يذوب"), ("٢", "snow", "يتجمّد"), ("٣", "steam", "يتبخّر")])
c4 = card(4, "قفل الماء", "#4fa3e0", "drop", f"""
  <p>الماء يتغيّر! ماذا يحدث له في كل موقف؟ اكتب رقم الجواب في مربّعه.</p>
  <div class="organs three">{STATES}</div>
  <ul class="clues">
    <li><b>■</b> قِدر ماء يغلي على النار مدة طويلة.</li>
    <li><b>▲</b> مكعب ثلج على صحن تحت الشمس.</li>
    <li><b>●</b> كوب ماء في المجمّد طوال الليل.</li>
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
      <div><b>البطاقة ١: الكواكب</b><span dir="ltr">٥١٤</span><small>أكبر كوكب المشتري (الخامس)، وأقربها عطارد (الأول)، وبين الأرض والمشتري المريخ (الرابع).</small></div>
      <div><b>البطاقة ٢: الأزهار</b><span dir="ltr">١٣</span><small>كل عدد مجموع العددين قبله: ٣ + ٥ = ٨، ثم ٥ + ٨ = ١٣.</small></div>
      <div><b>البطاقة ٣: الحواس</b><span dir="ltr">٣٥٢</span><small>الرائحة بالأنف (٣)، والبرودة بالجلد (٥)، والصوت بالأذن (٢).</small></div>
      <div><b>البطاقة ٤: الماء</b><span dir="ltr">٣١٢</span><small>الماء الذي يغلي يتبخّر (٣)، والثلج في الشمس يذوب (١)، والماء في المجمّد يتجمّد (٢).</small></div>
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
.flowers { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2mm; }
.fl { display: flex; flex-direction: column; align-items: center; gap: 1mm; background: #f3faf4; border-radius: 2.5mm; padding: 2mm 1mm; }
.fl svg { width: 17mm; height: 17mm; }
.fl b { font-size: 10pt; }
.organs { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1.5mm; }
.organs.three { grid-template-columns: repeat(3, 1fr); }
.o { border: .4mm solid #e2dfe8; border-radius: 2.5mm; padding: 1.5mm 1mm; display: flex; flex-direction: column; align-items: center; gap: .6mm; font-size: 10.5pt; font-weight: 600; }
.o b { width: 7mm; height: 7mm; border-radius: 50%; background: var(--c); color: #fff; display: grid; place-items: center; font-size: 11pt; }
svg.strip { width: 100%; display: block; background: #11142c; border-radius: 2.5mm; }
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
