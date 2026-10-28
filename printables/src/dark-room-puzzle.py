"""Builds the dark-room jigsaw puzzle (A3) in ..: dark-room-puzzle.html.

Page 1 is the puzzle: print it on A3, cut along the dotted lines into 10 pieces, shuffle.
Page 2 is the teacher's key. Render the PDF with render-pdf.js (Chromium, A3, backgrounds on).
Everything is drawn as shapes and patterns: no people and no animals.
"""
import math
import random
from pathlib import Path

W, H = 297.0, 420.0                      # A3 in mm; one SVG unit is one millimetre
X0, Y0, AW, AH = 8.5, 10.0, 280.0, 400.0  # the puzzle area, inside the printer's margins
COLS, ROWS = 2, 5
CW, RH = AW / COLS, AH / ROWS
CX = X0 + AW / 2
rng = random.Random(7)

LINES = ["اسم البيعة", "التي كانت تحت", "الشجرة؟"]
ANSWER = "الرضوان"


def f(*xs):
    return ",".join(f"{x:.2f}" for x in xs)


# ---------- jigsaw cut lines ----------
KNOB = [((0.42, 0), (0.45, 0.03), (0.44, 0.07)), ((0.43, 0.11), (0.40, 0.13), (0.41, 0.17)),
        ((0.42, 0.24), (0.58, 0.24), (0.59, 0.17)), ((0.60, 0.13), (0.57, 0.11), (0.56, 0.07)),
        ((0.55, 0.03), (0.58, 0), (0.62, 0))]


def edge(x0, y0, x1, y1, s, shift):
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    K = min(length, 76.0)          # knob size in mm: the same on long and short edges

    def P(u, v):                   # u: 0..1 across the knob template, v: height in template units
        a = length * (.5 + shift) + (u - .5) * K
        return f(x0 + ux * a + nx * v * K * s, y0 + uy * a + ny * v * K * s)

    out = ["M" + f(x0, y0), "L" + P(0.38, 0)]
    for c1, c2, e in KNOB:
        out.append("C" + " ".join(P(u, v) for u, v in (c1, c2, e)))
    out.append("L" + f(x1, y1))
    return " ".join(out)


def cut_lines():
    paths = []
    for r in range(ROWS):
        for c in range(1, COLS):
            x = X0 + c * CW
            paths.append(edge(x, Y0 + r * RH, x, Y0 + (r + 1) * RH, rng.choice((-1, 1)), rng.uniform(-.05, .05)))
    for r in range(1, ROWS):
        for c in range(COLS):
            y = Y0 + r * RH
            paths.append(edge(X0 + c * CW, y, X0 + (c + 1) * CW, y, rng.choice((-1, 1)), rng.uniform(-.05, .05)))
    return " ".join(paths)


# ---------- the picture ----------
def octagram(cx, cy, R, k=0.62):
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5 - 90)
        r = R if i % 2 == 0 else R * k
        pts.append(f(cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(pts)


def crescent(ax, ay, ro, bx, by, ri):
    d = math.hypot(bx - ax, by - ay)
    a = math.atan2(by - ay, bx - ax)
    al = math.acos((d * d + ro * ro - ri * ri) / (2 * d * ro))
    be = math.acos((d * d + ri * ri - ro * ro) / (2 * d * ri))
    outer = [(ax + ro * math.cos(t), ay + ro * math.sin(t)) for t in
             [a + al + (2 * math.pi - 2 * al) * i / 80 for i in range(81)]]
    inner = [(bx + ri * math.cos(t), by + ri * math.sin(t)) for t in
             [a + math.pi - be + 2 * be * i / 60 for i in range(61)]]
    last = outer[-1]
    if math.hypot(inner[0][0] - last[0], inner[0][1] - last[1]) > math.hypot(inner[-1][0] - last[0], inner[-1][1] - last[1]):
        inner.reverse()
    return "M" + " L".join(f(*p) for p in outer + inner) + "Z"


def art():
    o = []
    o.append(f'<rect x="{X0}" y="{Y0}" width="{AW}" height="{AH}" fill="url(#sky)"/>')
    o.append(f'<rect x="{X0}" y="{Y0}" width="{AW}" height="{AH}" fill="url(#glow)"/>')
    # geometric star tiling: every cell gets its own tint, so every piece looks different
    S = 35.0
    tints = ["#ffcf70", "#59d2c0", "#f08aa0", "#8db4ff"]
    for j in range(13):
        for i in range(8):
            cx, cy = X0 + S / 2 + i * S, Y0 + S / 2 + j * S
            o.append(f'<polygon points="{octagram(cx, cy, 15)}" fill="{rng.choice(tints)}" fill-opacity="{rng.uniform(.02, .17):.3f}" '
                     f'stroke="#ffcf70" stroke-opacity=".28" stroke-width=".35"/>')
            o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="5.2" fill="none" stroke="#ffcf70" stroke-opacity=".2" stroke-width=".3"/>')
            dx, dy = cx + S / 2, cy + S / 2
            o.append(f'<polygon points="{f(dx, dy - 6.5)} {f(dx + 6.5, dy)} {f(dx, dy + 6.5)} {f(dx - 6.5, dy)}" fill="none" '
                     f'stroke="#ffcf70" stroke-opacity=".2" stroke-width=".3"/>')
    # stars
    for _ in range(260):
        x, y = rng.uniform(X0, X0 + AW), rng.uniform(Y0, Y0 + AH)
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rng.uniform(.25, .9):.2f}" fill="#fff" fill-opacity="{rng.uniform(.35, 1):.2f}"/>')
    for _ in range(34):
        x, y, r = rng.uniform(X0 + 5, X0 + AW - 5), rng.uniform(Y0 + 5, Y0 + AH - 5), rng.uniform(1.4, 3.2)
        o.append(f'<path d="M{f(x, y - r)}L{f(x + r * .28, y - r * .28)}L{f(x + r, y)}L{f(x + r * .28, y + r * .28)}'
                 f'L{f(x, y + r)}L{f(x - r * .28, y + r * .28)}L{f(x - r, y)}L{f(x - r * .28, y - r * .28)}Z" fill="#fff6d6" fill-opacity=".9"/>')
    # moon
    o.append(f'<circle cx="245" cy="52" r="30" fill="url(#moonGlow)"/>')
    o.append(f'<path d="{crescent(245, 52, 17, 252, 47, 14)}" fill="#ffe9a6"/>')
    # lantern
    o.append('<circle cx="48" cy="54" r="30" fill="url(#lanternGlow)"/>')
    o.append('<g stroke="#c9a26a" stroke-width="1" stroke-linecap="round" fill="none">'
             '<path d="M48 10V32"/><path d="M42 32a6 6 0 0 1 12 0"/></g>'
             '<path d="M37 40L41 33H55L59 40Z" fill="#8a5a2b"/>'
             '<rect x="40" y="40" width="16" height="25" rx="2" fill="#ffcf70" fill-opacity=".38" stroke="#c9a26a" stroke-width="1.1"/>'
             '<path d="M44 40V65M52 40V65" stroke="#c9a26a" stroke-width=".7"/>'
             '<path d="M48 45C54 51 54 58 48 61C42 58 42 51 48 45Z" fill="#fff1bf"/>'
             '<rect x="37" y="65" width="22" height="4" rx="1" fill="#8a5a2b"/>')
    # ground and tree
    o.append(f'<ellipse cx="{CX}" cy="{Y0 + AH + 6}" rx="170" ry="30" fill="#0a2c2a"/>')
    o.append('<path d="M140 410C142 388 144 372 143 352L155 352C154 372 155 390 157 410Z" fill="#3a2412"/>')
    o.append('<path d="M149 372C140 366 133 360 128 352M149 366C158 360 164 354 168 348" stroke="#3a2412" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    for (x, y, r, c) in [(122, 346, 26, "#0b3a2c"), (175, 346, 26, "#0b3a2c"), (148.5, 336, 32, "#0e4a37"), (135, 318, 24, "#11553f"),
                         (162, 318, 24, "#11553f"), (148.5, 306, 22, "#15614a")]:
        o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
    for (x, y) in [(135, 330), (160, 340), (148, 318), (122, 350), (176, 350), (145, 350), (166, 322)]:
        o.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#ffd98a" fill-opacity=".9"/>')
    # the question, lit from behind
    ys = [138, 198, 258]
    for i, (line, y) in enumerate(zip(LINES, ys)):
        for sw, op in ((7, .10), (4.2, .18)):
            o.append(f'<text class="q" x="{CX}" y="{y}" fill="none" stroke="#ffcf70" stroke-opacity="{op}" stroke-width="{sw}" stroke-linejoin="round">{line}</text>')
        o.append(f'<text class="q" x="{CX}" y="{y}" fill="#ffe08f" stroke="#6b3d00" stroke-width="1.1" stroke-linejoin="round" paint-order="stroke">{line}</text>')
    return "\n".join(o)


def numbers():
    o = []
    for r in range(ROWS):
        for c in range(COLS):
            n = r * COLS + c + 1
            x, y = X0 + (c + .5) * CW, Y0 + (r + .5) * RH
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.2" fill="#fff" fill-opacity=".9" stroke="#222" stroke-width=".4"/>'
                     f'<text x="{x:.1f}" y="{y + 2.1:.1f}" text-anchor="middle" font-family="Tajawal" font-weight="800" font-size="6" fill="#222">{n}</text>')
    return "".join(o)


CUTS = cut_lines()
HTML = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>الحجرة المظلمة: لغز السؤال (A3)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lalezar&family=Tajawal:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  @page {{ size: 297mm 420mm; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: #d9dedc; }}
  body {{ font-family: "Tajawal", sans-serif; color: #22282b; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  .page {{ width: 297mm; height: 420mm; margin: 8mm auto; background: #fff; overflow: hidden; position: relative; break-after: page; box-shadow: 0 2px 12px rgba(0,0,0,.2); }}
  @media print {{ html, body {{ background: #fff; }} .page {{ margin: 0; box-shadow: none; }} }}
  svg.sheet {{ display: block; width: 297mm; height: 420mm; }}
  .q {{ font-family: "Lalezar", "Tajawal", sans-serif; font-size: 47px; text-anchor: middle; direction: rtl; }}
  .key {{ padding: 14mm 16mm; display: grid; grid-template-columns: 160mm 1fr; gap: 12mm; align-content: start; }}
  .key header {{ grid-column: 1 / -1; display: flex; justify-content: space-between; align-items: center; border-bottom: 2.5px solid #22282b; padding-bottom: 5mm; }}
  .key h1 {{ font-size: 30pt; font-weight: 800; line-height: 1.1; }}
  .key h1 span {{ color: #2c4f86; }}
  .tag {{ border: 2px solid #b5523f; color: #b5523f; border-radius: 20px; padding: 1mm 5mm; font-weight: 800; font-size: 13pt; }}
  .key .pic {{ width: 160mm; height: 228.6mm; display: block; border-radius: 3mm; box-shadow: 0 0 0 2px #22282b; }}
  .side {{ display: grid; gap: 6mm; align-content: start; }}
  .box {{ border-radius: 4mm; padding: 5mm 6mm; background: #eaf0f8; font-size: 13.5pt; line-height: 1.65; }}
  .box h2 {{ font-size: 15pt; color: #2c4f86; margin-bottom: 1.5mm; }}
  .box ol {{ padding-inline-start: 6mm; display: grid; gap: 2mm; }}
  .box.warm {{ background: #f8ece8; }}
  .box.warm h2 {{ color: #b5523f; }}
  .q-big {{ font-size: 19pt; font-weight: 800; }}
  .ans {{ display: inline-block; margin-top: 1.5mm; font-size: 17pt; font-weight: 800; background: #fff; border: 2px dashed #b5523f; border-radius: 3mm; padding: .5mm 5mm; }}
  .rows {{ grid-column: 1 / -1; font-size: 11pt; color: #5d686c; }}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#06112b"/><stop offset=".55" stop-color="#0e2b55"/><stop offset="1" stop-color="#0a3040"/>
    </linearGradient>
    <radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="{CX}" cy="198" r="175">
      <stop offset="0" stop-color="#ffcf70" stop-opacity=".42"/><stop offset=".6" stop-color="#ffb347" stop-opacity=".12"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="moonGlow"><stop offset="0" stop-color="#ffe9a6" stop-opacity=".45"/><stop offset="1" stop-color="#ffe9a6" stop-opacity="0"/></radialGradient>
    <radialGradient id="lanternGlow"><stop offset="0" stop-color="#ffcf70" stop-opacity=".6"/><stop offset="1" stop-color="#ffcf70" stop-opacity="0"/></radialGradient>
    <clipPath id="area"><rect x="{X0}" y="{Y0}" width="{AW}" height="{AH}"/></clipPath>
    <g id="art" clip-path="url(#area)">
{art()}
    </g>
    <g id="cuts" fill="none" stroke-linejoin="round" stroke-linecap="round">
      <path d="{CUTS}" stroke="#000" stroke-opacity=".35" stroke-width=".9"/>
      <path d="{CUTS}" stroke="#fff" stroke-width=".55" stroke-dasharray="2.4 1.6"/>
      <rect x="{X0}" y="{Y0}" width="{AW}" height="{AH}" stroke="#000" stroke-opacity=".35" stroke-width=".9"/>
      <rect x="{X0}" y="{Y0}" width="{AW}" height="{AH}" stroke="#fff" stroke-width=".55" stroke-dasharray="2.4 1.6"/>
    </g>
  </defs>
</svg>

<section class="page">
  <svg class="sheet" viewBox="0 0 {W:g} {H:g}" role="img" aria-label="لغز: قطّعوه ثم رتّبوا القطع لتقرؤوا السؤال">
    <use href="#art"/><use href="#cuts"/>
  </svg>
</section>

<section class="page key">
  <header>
    <h1>الحجرة المظلمة: <span>مفتاح اللغز</span></h1>
    <span class="tag">للمعلّم فقط</span>
  </header>
  <svg class="pic" viewBox="{X0} {Y0} {AW} {AH}" role="img" aria-label="اللغز بعد ترتيبه">
    <use href="#art"/><use href="#cuts"/>{numbers()}
  </svg>
  <div class="side">
    <div class="box">
      <h2>التجهيز</h2>
      <ol>
        <li>اطبع الصفحة الأولى على ورق <b>A3</b> بألوانها (ورق سميك أفضل، أو غلّفها).</li>
        <li>قُصّ على الخطوط المنقّطة لتحصل على <b>١٠ قطع</b>.</li>
        <li>اخلط القطع وضعها في ظرف، وأخفِه في الحجرة المظلمة ليبحث عنه الطلاب.</li>
        <li>بعد كل مجموعة، اخلط القطع من جديد للمجموعة التالية.</li>
      </ol>
    </div>
    <div class="box">
      <h2>ماذا يفعل الفريق؟</h2>
      <ol>
        <li>يجد الظرف ويرتّب القطع حتى يظهر السؤال.</li>
        <li>يكتب السؤال في اللعبة في الخطوة الأولى من «الحجرة المظلمة» فيحصل على جزء من الماء.</li>
        <li>ثم يبحث عن الجواب ويكتبه في الخطوة الثانية فيكمل الماء.</li>
      </ol>
    </div>
    <div class="box warm">
      <h2>السؤال المخفيّ</h2>
      <div class="q-big">{" ".join(LINES)}</div>
      <h2 style="margin-top:4mm">الجواب (الخطوة الثانية)</h2>
      <span class="ans">{ANSWER}</span>
    </div>
    <div class="box">
      <h2>نصيحة</h2>
      الأرقام على الصورة تساعدك أنت في التحقّق من القطع، وهي غير مطبوعة على لغز الطلاب.
    </div>
  </div>
</section>
</body>
</html>
"""

Path(__file__).resolve().parent.parent.joinpath("dark-room-puzzle.html").write_text(HTML, encoding="utf-8")
print("ok", len(HTML) // 1024, "KB")
