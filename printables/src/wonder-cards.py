"""Builds the صندوق العجائب printable (A4) in ..: wonder-cards.html.

Page 1: the four cards on one sheet (2x2), cut along the dotted lines.
Page 2: set-up, how to play, and the answers for the teacher.
Codes: 514 (planets), 13 (flowers), 352 (senses), 312 (water). Only shapes and text: no people, no animals.
Render the PDF with render-pdf.js (Chromium, A4, backgrounds on).
"""
import math
from pathlib import Path

COL = {"p": "#7b5cc4", "f": "#3f9d55", "s": "#e08a1e", "w": "#2f8fd0"}
SH = ["■", "▲", "●"]


def flower(n, color):
    c, r, d = 50, 50 * .19 * (1.0 if n < 9 else .8), 50 * .54
    petals = "".join(
        f'<circle cx="{c + d * math.cos(2 * math.pi * i / n - math.pi / 2):.1f}" '
        f'cy="{c + d * math.sin(2 * math.pi * i / n - math.pi / 2):.1f}" r="{r * 2.2:.1f}" fill="{color}" '
        f'stroke="#fff" stroke-width="1.5" opacity=".95"/>' for i in range(n))
    return f'<svg viewBox="0 0 100 100">{petals}<circle cx="50" cy="50" r="9" fill="#f7c948" stroke="#c98a14" stroke-width="2"/></svg>'


def boxes(n, key, marks):
    return ('<div class="code"><span class="lab">الرقم السري:</span><div class="bx">' +
            "".join(f'<div class="b"><i style="color:{COL[key]}">{m}</i><u></u></div>' for m in marks[:n]) + '</div></div>')


def card(no, title, key, icon, lead, visual, qs, marks):
    q = "".join(f'<li><i style="color:{COL[key]}">{SH[i]}</i><span>{t}</span></li>' for i, t in enumerate(qs)) if qs else ""
    return f'''<article class="card" style="--c:{COL[key]}"><header><span class="ic">{icon}</span><h2>البطاقة {no}: {title}</h2></header>
<p class="lead">{lead}</p>{visual}<ul>{q}</ul>{boxes(len(marks), key, marks)}</article>'''


# ---- planets ----
names = ["عطارد", "الزهرة", "الأرض", "المريخ", "المشتري", "زحل", "أورانوس", "نبتون"]
cols = ["#a89a8c", "#e8c987", "#4a90d9", "#d9603b", "#d9a066", "#e6cf8f", "#8fd1d9", "#4a62c9"]
rad = [2.2, 3, 3.2, 2.6, 6.5, 5.5, 4, 3.8]
sp = '<svg viewBox="0 0 93 26" class="vis"><circle cx="83" cy="10" r="9" fill="#ffc83d"/><text x="83" y="24" text-anchor="middle" font-size="3" fill="#8a6a1f">الشمس</text>'
for i, (n, c, r) in enumerate(zip(names, cols, rad)):
    x = 68 - i * 8.6
    sp += f'<circle cx="{x:.1f}" cy="10" r="{r}" fill="{c}"/><text x="{x:.1f}" y="{20 if i % 2 == 0 else 24}" text-anchor="middle" font-size="2.6" fill="#4b3a64">{n}</text>'
sp += "</svg>"
c1 = card("١", "الكواكب", "p", "🪐", "هذه الكواكب بالترتيب من الشمس. رقم الكوكب = مكانه من الشمس (الأقرب رقمه ١).", sp,
          ["ما رقم أكبر كوكب؟", "ما رقم أقرب كوكب إلى الشمس؟", "ما رقم الكوكب الذي بين الأرض والمشتري؟"], SH)

# ---- flowers ----
fl = '<div class="flrow">' + "".join(
    f'<div class="fc">{flower(n, "#e5649a")}<b>{n} بتلات</b></div>' for n in (3, 5, 8)) + \
    '<div class="fc"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="38" fill="none" stroke="#3f9d55" stroke-width="3" stroke-dasharray="6 6"/><text x="50" y="66" text-anchor="middle" font-size="46" font-weight="800" fill="#3f9d55">؟</text></svg><b>كم بتلة؟</b></div></div>'
c2 = card("٢", "الأزهار", "f", "✿", "عُدّ بتلات كل زهرة. هناك سرّ يربط بين الأعداد! اكتشفه، واعرف عدد بتلات الزهرة الأخيرة.", fl + '<p class="hint">تلميح: انظر إلى الزهرتين الأوليين، ثم إلى الثالثة. ماذا تلاحظ؟</p>', [], ["✿", "✿"])

# ---- senses ----
organs = [("١", "العين"), ("٢", "الأذن"), ("٣", "الأنف"), ("٤", "اللسان"), ("٥", "الجلد")]
sn = '<div class="org">' + "".join(f'<div><b style="background:{COL["s"]}">{n}</b>{t}</div>' for n, t in organs) + '</div>'
c3 = card("٣", "الحواس", "s", "✺", "لكل عضو رقم. أي عضو تستعمل في كل موقف؟", sn,
          ["عرفتُ أن الخبز طازج من رائحته.", "أحسستُ أن الماء بارد حين لمسته.", "عرفتُ أن المطر بدأ من صوته على النافذة."], SH)

# ---- water ----
wt = '<div class="org w">' + "".join(
    f'<div><b style="background:{COL["w"]}">{n}</b>{t}</div>' for n, t in (("١", "يذوب"), ("٢", "يتجمّد"), ("٣", "يتبخّر"))) + '</div>'
c4 = card("٤", "الماء", "w", "💧".replace("💧", "●"), "الماء يتغيّر! ماذا يحدث له في كل موقف؟ اكتب رقم الجواب في مربّعه.", wt,
          ["قدر ماء يغلي على النار مدة طويلة.", "مكعب ثلج على صحن تحت الشمس.", "كوب ماء في المجمّد طوال الليل."], SH)

ANS = [
    ("البطاقة ١: الكواكب", "٥١٤", "أكبر كوكب المشتري (الخامس)، وأقربها عطارد (الأول)، وبين الأرض والمشتري المريخ (الرابع).", "ر"),
    ("البطاقة ٢: الأزهار", "١٣", "كل عدد مجموع العددين قبله: ٣ + ٥ = ٨، ثم ٥ + ٨ = ١٣.", "ا"),
    ("البطاقة ٣: الحواس", "٣٥٢", "الرائحة بالأنف (٣)، والبرودة بالجلد (٥)، والصوت بالأذن (٢).", "ث"),
    ("البطاقة ٤: الماء", "٣١٢", "الماء الذي يغلي يتبخّر (٣)، والثلج في الشمس يذوب (١)، والماء في المجمّد يتجمّد (٢).", "م"),
]
ans = "".join(f'<div class="a"><h4>{t} <span class="lt">الحرف «{l}»</span></h4><b>{c}</b><p>{d}</p></div>' for t, c, d, l in ANS)

CSS = '''@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Naskh Arabic","Amiri","Noto Sans Arabic",sans-serif;color:#2b2140;direction:rtl}
.sheet{width:210mm;height:297mm;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;page-break-after:always}
.card{padding:7mm 7mm 6mm;display:flex;flex-direction:column;gap:3mm;border:0 dotted #9a8fb5;position:relative;background:#fff}
.card:nth-child(1){border-left-width:.4mm;border-bottom-width:.4mm}
.card:nth-child(2){border-bottom-width:.4mm}
.card:nth-child(3){border-left-width:.4mm}
.card::before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,color-mix(in srgb,var(--c) 10%,#fff),#fff 55%);z-index:0}
.card>*{position:relative;z-index:1}
header{display:flex;align-items:center;gap:3mm;border-bottom:.5mm solid var(--c);padding-bottom:2mm}
.ic{width:9mm;height:9mm;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-size:5.5mm}
h2{margin:0;font-size:6.2mm;color:var(--c)}
.lead{margin:0;font-size:4.4mm;line-height:1.6}
.vis{width:100%}
.hint{margin:0;font-size:3.2mm;color:#6b5f85}
ul{list-style:none;margin:0;padding:0;display:grid;gap:2mm}
li{display:flex;gap:2.5mm;background:rgba(0,0,0,.045);border-radius:2mm;padding:2.6mm 3mm;font-size:4.3mm;line-height:1.45}
li i{font-style:normal;font-size:3.6mm}
.code{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:3mm}
.lab{font-weight:800;font-size:3.8mm}
.bx{display:flex;gap:2.5mm}
.b{display:grid;justify-items:center;gap:.6mm}
.b i{font-style:normal;font-size:3.4mm;line-height:1}
.b u{display:block;width:11mm;height:12mm;border:.6mm solid var(--c);border-radius:2.2mm;background:#fff}
.flrow{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm}
.fc{display:grid;justify-items:center;gap:.6mm;background:#fff;border:.4mm solid #e2ecd9;border-radius:2.5mm;padding:1.5mm}
.fc b{font-size:3.3mm}
.org{display:flex;flex-wrap:wrap;gap:1.5mm}
.org div{flex:1;display:grid;justify-items:center;gap:.6mm;background:#fff;border:.4mm solid #f0dcc0;border-radius:2.5mm;padding:1.5mm 1mm;font-size:3.8mm;min-width:12mm}
.org.w div{border-color:#cfe3f3;font-size:3.6mm;padding:2.5mm 1mm}
.org b{width:5.5mm;height:5.5mm;border-radius:50%;color:#fff;display:grid;place-items:center;font-size:3.3mm}
/* page 2 */
.info{width:210mm;height:296mm;overflow:hidden;padding:12mm 16mm;display:flex;flex-direction:column;gap:4mm;background:#fff}
.info h1{margin:0;font-size:12mm;color:#3b2a66}
.info>p{margin:0;font-size:4.6mm;color:#6b5f85}
.box{background:#fff;border:.4mm solid #e4def0;border-radius:4mm;padding:4mm 6mm}
.box h3{margin:0 0 3mm;font-size:5.4mm}
.box ol{margin:0;padding-right:6mm;display:grid;gap:2mm;font-size:4.1mm;line-height:1.55}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.a{background:#f4f1fa;border-radius:3mm;padding:4mm 5mm}
.a h4{margin:0 0 1mm;font-size:4.4mm;display:flex;justify-content:space-between}
.lt{font-weight:400;color:#6b5f85;font-size:3.8mm}
.a b{font-size:9mm;color:#4b3585}
.a p{margin:1mm 0 0;font-size:3.9mm;line-height:1.6;color:#4a4060}
.fin{font-size:5mm;margin:0}'''

page2 = f'''<div class="info"><h1>صندوق العجائب</h1>
<p>لعبة بحث عن الكنز: أربع بطاقات حقيقية في المكان، وصندوق على الشاشة يكشف كلمة مخفية.</p>
<div class="box"><h3>التجهيز (دقيقتان)</h3><ol>
<li>اطبع صفحة البطاقات بالألوان، وقصّها على الخط المتقطّع إلى أربع بطاقات.</li>
<li>خبّئ البطاقات ٢ و٣ و٤ في ثلاثة أماكن، وأعطِ الفريق البطاقة ١.</li>
<li>اكتب أماكن البطاقات في <code>where</code> داخل خطوات المحطة ٣ في config.js، ليخبر اللعبةُ الفريقَ أين يبحث عن البطاقة التالية (اختياري).</li></ol></div>
<div class="box"><h3>اللعب</h3><ol>
<li>يحلّ الأطفال لغز البطاقة معًا، ويكتبون الرقم السري في مربعاتها.</li>
<li>يدخلون الرقم في محطة صندوق العجائب في اللعبة.</li>
<li>إذا صحّ الرقم ظهر حرف من الكلمة المخفية ومعلومة عجيبة، ويزيد الماء.</li>
<li>بعد الحروف الأربعة (ر، ا، ث، م) يرتّبونها ويكتبون الكلمة المخفية «ثمار» فيمتلئ الإبريق.</li></ol>
<p style="margin:3mm 0 0;font-size:4mm;color:#6b5f85">إذا أخطؤوا ثلاث مرات متتالية، تنتظر الشاشة خمس ثوانٍ حتى يفكروا بدل أن يجرّبوا أرقامًا.</p></div>
<div class="box"><h3>الأجوبة</h3><div class="grid">{ans}</div><p class="fin" style="margin-top:4mm">الكلمة المخفية: <b>ثمار</b></p></div></div>'''

html = (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>بطاقات صندوق العجائب</title><style>{CSS}</style></head>'
        f'<body><div class="sheet">{c1}{c2}{c3}{c4}</div>{page2}</body></html>')
Path(__file__).resolve().parent.parent.joinpath("wonder-cards.html").write_text(html, encoding="utf-8")
