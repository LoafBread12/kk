"""Builds the four puzzle cards of صندوق العجائب (A4) in ..: wonder-cards.html.

Pages 1-4 are the cards (print one per card, hide them in the place), page 5 is the teacher's key.
Codes: 514 (planets), 13 (flowers), 352 (senses), 312 (water). Only shapes and text: no people, no animals.
Render the PDF with render-pdf.js (Chromium, A4, backgrounds on).
"""
import math
from pathlib import Path

CARDS = []


def flower(n, color, size=100):
    """A flower with n petals (circles around a centre)."""
    r = size * 0.19
    d = size * 0.27
    c = size / 2
    petals = "".join(
        f'<circle cx="{c + d * math.cos(2 * math.pi * i / n - math.pi / 2):.1f}" '
        f'cy="{c + d * math.sin(2 * math.pi * i / n - math.pi / 2):.1f}" r="{r * (1.0 if n < 9 else .8):.1f}" '
        f'fill="{color}" stroke="#fff" stroke-width="1.2" opacity=".92"/>'
        for i in range(n))
    return (f'<svg viewBox="0 0 {size} {size}" class="fl">{petals}'
            f'<circle cx="{c}" cy="{c}" r="{size * .12:.1f}" fill="#f7c948" stroke="#c98a14" stroke-width="1.5"/></svg>')


def empty_flower(size=100):
    return (f'<svg viewBox="0 0 {size} {size}" class="fl"><circle cx="50" cy="50" r="38" fill="none" '
            f'stroke="#9a7b4f" stroke-width="3" stroke-dasharray="6 6"/>'
            f'<text x="50" y="66" text-anchor="middle" font-size="46" font-weight="800" fill="#9a7b4f">؟</text></svg>')


def card(no, title, color, body):
    return f'''<section class="page" style="--c:{color}">
<div class="frame"><div class="head"><span class="no">{no}</span><h1>{title}</h1><span class="of">البطاقة {no} من ٤</span></div>
{body}
<div class="foot">اكتبوا الرقم السري في اللعبة عند محطة صندوق العجائب</div></div></section>'''


# ---------- card 1: planets (514) ----------
planets = ["عطارد", "الزهرة", "الأرض", "المريخ", "المشتري", "زحل", "أورانوس", "نبتون"]
chips = "".join(
    f'<div class="chip"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="{7 + (8 if p in ("المشتري", "زحل") else 4 if p in ("أورانوس", "نبتون") else 0)}" '
    f'fill="{col}"/></svg><b>{p}</b></div>'
    for p, col in zip(planets, ["#a89a8c", "#e8c987", "#4a90d9", "#d9603b", "#d9a066", "#e6cf8f", "#8fd1d9", "#4a62c9"]))
body1 = f'''<p class="lead">هذه الكواكب الثمانية مرتبة من الأقرب إلى الشمس إلى الأبعد. عدّوا مكان كل كوكب في الصف.</p>
<div class="sun">☀ الشمس</div><div class="row8">{chips}</div>
<div class="clues">
<div class="clue"><i>الرقم الأول</i><p>ما ترتيب أكبر الكواكب كلها؟</p><b class="box"></b></div>
<div class="clue"><i>الرقم الثاني</i><p>ما ترتيب أقرب كوكب إلى الشمس؟</p><b class="box"></b></div>
<div class="clue"><i>الرقم الثالث</i><p>ما ترتيب الكوكب الأحمر؟</p><b class="box"></b></div></div>
<p class="note">الرقم السري ثلاثة أرقام بالترتيب: الأول ثم الثاني ثم الثالث.</p>'''
CARDS.append(card("١", "لغز الكواكب", "#7b5cc4", body1))

# ---------- card 2: flowers (13) ----------
counts = [2, 3, 5, 8]
cols = ["#e58fb5", "#f0a23a", "#9b7be0", "#4fa3e0"]
fl = "".join(f'<div class="cell">{flower(n, c)}</div>' for n, c in zip(counts, cols)) + f'<div class="cell">{empty_flower()}</div>'
body2 = f'''<p class="lead">في الطبيعة أزهار كثيرة يتبع عدد بتلاتها قاعدة جميلة. عدّوا بتلات كل زهرة، ثم اكتشفوا القاعدة.</p>
<div class="flrow">{fl}</div>
<div class="clues one">
<div class="clue wide"><i>السؤال</i><p>كم بتلة في الزهرة الأخيرة التي ليس لها رسم؟</p><b class="box big"></b></div></div>
<p class="note">تلميح: انظروا ماذا يحدث إذا جمعتم عددين متجاورين.</p>'''
CARDS.append(card("٢", "لغز الأزهار", "#3f9d55", body2))

# ---------- card 3: senses (352) ----------
body3 = '''<p class="lead">لكل موقف عضو نستعمله أكثر من غيره. اقرؤوا الجدول، ثم اكتبوا رقم العضو المناسب لكل موقف.</p>
<div class="keybox"><div><b>١</b> العين</div><div><b>٢</b> الأذن</div><div><b>٣</b> الأنف</div><div><b>٤</b> اللسان</div><div><b>٥</b> الجلد</div></div>
<div class="clues">
<div class="clue"><i>الموقف الأول</i><p>تعرفون من بعيد أن الخبز خرج من الفرن قبل أن تروه.</p><b class="box"></b></div>
<div class="clue"><i>الموقف الثاني</i><p>تضعون يدكم في الماء لتعرفوا هل هو دافئ أم بارد.</p><b class="box"></b></div>
<div class="clue"><i>الموقف الثالث</i><p>تعرفون من داخل البيت أن وقت الأذان قد جاء.</p><b class="box"></b></div></div>
<p class="note">الرقم السري ثلاثة أرقام بالترتيب: الموقف الأول ثم الثاني ثم الثالث.</p>'''
CARDS.append(card("٣", "لغز الحواس", "#e08a1e", body3))

# ---------- card 4: water (312) ----------
body4 = '''<p class="lead">يغيّر الماء حالته حين يتغير الحر والبرد. اقرؤوا الجدول، ثم اكتبوا رقم التغيّر المناسب لكل موقف.</p>
<div class="keybox"><div><b>١</b> يتجمّد</div><div><b>٢</b> يتبخّر</div><div><b>٣</b> يذوب</div><div><b>٤</b> يتكاثف</div></div>
<div class="clues">
<div class="clue"><i>الموقف الأول</i><p>قطعة ثلج تُركت في الشمس في يوم حارّ.</p><b class="box"></b></div>
<div class="clue"><i>الموقف الثاني</i><p>كأس ماء وُضعت ليلة كاملة في مُجمِّد شديد البرودة.</p><b class="box"></b></div>
<div class="clue"><i>الموقف الثالث</i><p>ماء في إبريق على النار يغلي ويخرج منه بخار.</p><b class="box"></b></div></div>
<p class="note">الرقم السري ثلاثة أرقام بالترتيب: الموقف الأول ثم الثاني ثم الثالث.</p>'''
CARDS.append(card("٤", "لغز الماء", "#2f8fd0", body4))

# ---------- teacher key ----------
key = '''<section class="page key"><div class="frame"><div class="head"><span class="no">★</span><h1>مفتاح المعلّم</h1><span class="of">لا يُوزَّع على الطلاب</span></div>
<table><tr><th>البطاقة</th><th>الحل</th><th>الرقم السري</th><th>الحرف</th></tr>
<tr><td>١ الكواكب</td><td>المشتري ٥، عطارد ١، المريخ ٤</td><td class="code">٥١٤</td><td class="code">ر</td></tr>
<tr><td>٢ الأزهار</td><td>٢، ٣، ٥، ٨، ثم ١٣ (كل عدد مجموع اللذين قبله)</td><td class="code">١٣</td><td class="code">ا</td></tr>
<tr><td>٣ الحواس</td><td>الأنف ٣، الجلد ٥، الأذن ٢</td><td class="code">٣٥٢</td><td class="code">ث</td></tr>
<tr><td>٤ الماء</td><td>يذوب ٣، يتجمّد ١، يتبخّر ٢</td><td class="code">٣١٢</td><td class="code">م</td></tr></table>
<p class="big">الحروف الأربعة (ر، ا، ث، م) تُرتَّب فتصير الكلمة المخفية: <b>ثمار</b></p>
<p class="note">يمكنكم إخفاء البطاقات في أي أماكن، وكتابة مكان كل بطاقة في <code>where</code> داخل config.js ليخبر اللعبةُ الفريقَ أين يبحث عن البطاقة التالية.</p></div></section>'''

CSS = '''@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Naskh Arabic","Amiri","Noto Sans Arabic",sans-serif;color:#2b1d10;direction:rtl}
.page{width:210mm;height:297mm;padding:10mm;page-break-after:always;background:#fff}
.frame{height:100%;border:3mm solid var(--c,#555);border-radius:9mm;padding:9mm 11mm;display:flex;flex-direction:column;gap:6mm;
 background:linear-gradient(#fffaf0,#fff6e2)}
.head{display:flex;align-items:center;gap:6mm;border-bottom:1mm dashed var(--c,#555);padding-bottom:5mm}
.no{width:20mm;height:20mm;border-radius:50%;background:var(--c,#555);color:#fff;display:grid;place-items:center;font-size:12mm;font-weight:800}
h1{margin:0;flex:1;font-size:15mm;color:var(--c,#555)}
.of{font-size:5mm;color:#7a6446}
.lead{margin:0;font-size:7mm;line-height:1.6}
.note{margin:0;font-size:5.4mm;color:#7a6446}
.foot{margin-top:auto;text-align:center;font-size:5mm;color:#7a6446;border-top:.5mm dotted #b9a27a;padding-top:4mm}
.sun{align-self:flex-start;background:#ffd35a;border-radius:99px;padding:2mm 7mm;font-size:6.5mm;font-weight:800}
.row8{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}
.chip{background:#fff;border:.6mm solid #d9c7a2;border-radius:5mm;padding:1.5mm;display:grid;justify-items:center;gap:0;font-size:5.6mm}
.chip svg{width:12mm;height:12mm}
.clues{display:grid;gap:4mm}
.clue{display:grid;grid-template-columns:34mm 1fr 24mm;align-items:center;gap:5mm;background:#fff;border:.6mm solid var(--c);border-radius:5mm;padding:3mm 6mm}
.clue i{font-style:normal;font-weight:800;color:var(--c);font-size:5.6mm}
.clue p{margin:0;font-size:6.6mm;line-height:1.5}
.box{width:22mm;height:22mm;border:1mm solid var(--c);border-radius:4mm;background:#fffdf7;display:block}
.clue.wide{grid-template-columns:30mm 1fr 34mm}.box.big{width:32mm;height:32mm}
.flrow{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;align-items:center}
.fl{width:100%}
.cell{background:#fff;border:.6mm solid #d9c7a2;border-radius:5mm;padding:2mm}
.keybox{display:flex;flex-wrap:wrap;gap:3mm}
.keybox div{background:#fff;border:.6mm solid var(--c);border-radius:99px;padding:2mm 6mm;font-size:6.6mm}
.keybox b{display:inline-block;background:var(--c);color:#fff;border-radius:50%;width:9mm;height:9mm;text-align:center;line-height:9mm;margin-left:2mm}
.key .frame{--c:#555}
table{width:100%;border-collapse:collapse;font-size:6mm}
th,td{border:.5mm solid #cdb98f;padding:4mm;text-align:right}
th{background:#f1e4c2}.code{font-weight:800;font-size:9mm;text-align:center}
.big{font-size:7.5mm;margin:0}
code{background:#eee;padding:0 2mm;border-radius:2mm}'''

html = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>بطاقات صندوق العجائب</title><style>{CSS}</style></head><body>{"".join(CARDS)}{key}</body></html>'
Path(__file__).resolve().parent.parent.joinpath("wonder-cards.html").write_text(html, encoding="utf-8")
