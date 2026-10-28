// Builds ../arrange-room-kit.html, the paper version of "رتّب الغرفة".
// Run: node arrange_kit.js   (puzzles come from ../../games/lib/arrange.js and each has exactly one solution)
const fs = require("fs");
const path = require("path");
const A = require("../../games/lib/arrange.js");

const AR = (n) => String(n).replace(/\d/g, (d) => "٠١٢٣٤٥٦٧٨٩"[d]);
const COLORS = [["#2f7f86", "#3fa0a8"], ["#c9962e", "#e0b04a"], ["#8a3b4f", "#a8546a"], ["#56703a", "#6f8f4c"], ["#3f4f8f", "#5468ad"]];
const TABLE = `<svg viewBox="0 0 40 40"><circle cx="20" cy="21" r="14" fill="rgba(0,0,0,.15)"/><circle cx="20" cy="20" r="14" fill="#8a5a35"/>
  <circle cx="20" cy="20" r="11" fill="#a8744a"/><circle cx="20" cy="20" r="4" fill="#f4ecdc"/><path d="M20 12c2 3 2 5 0 8-2-3-2-5 0-8z" fill="#5fa36a"/></svg>`;
const sofa = (rot, k) => {
  const [b, c] = COLORS[k % COLORS.length];
  return `<svg viewBox="0 0 40 40"><g transform="rotate(${rot} 20 20)"><rect x="3" y="7" width="34" height="26" rx="5" fill="${b}"/>
    <rect x="3" y="7" width="34" height="8" rx="4" fill="${b}" stroke="rgba(0,0,0,.25)"/><rect x="3" y="11" width="6" height="22" rx="3" fill="${b}" stroke="rgba(0,0,0,.25)"/>
    <rect x="31" y="11" width="6" height="22" rx="3" fill="${b}" stroke="rgba(0,0,0,.25)"/><rect x="9.5" y="15.5" width="10" height="15" rx="2.5" fill="${c}"/>
    <rect x="20.5" y="15.5" width="10" height="15" rx="2.5" fill="${c}"/></g></svg>`;
};
const facing = (P, i) => {
  const t = new Set(P.tables), o = A.orth(P.R, P.C, i);
  for (const [j, rot] of [[i + P.C, 0], [i - 1, 90], [i - P.C, 180], [i + 1, 270]]) if (o.includes(j) && t.has(j)) return rot;
  return 0;
};

function grid(P, cell, withSolution) {
  const t = new Set(P.tables), s = new Set(P.sofas);
  let h = `<div class="g" style="--c:${P.C};--cell:${cell}mm">`;
  for (let c = 0; c < P.C; c++) h += `<div class="cl top">${AR(P.cols[c])}</div>`;
  h += `<div></div>`;
  for (let r = 0; r < P.R; r++) {
    for (let c = 0; c < P.C; c++) {
      const i = r * P.C + c;
      const inner = t.has(i) ? TABLE : withSolution && s.has(i) ? sofa(facing(P, i), i) : "";
      h += `<div class="sq${(r + c) % 2 ? " alt" : ""}">${inner}</div>`;
    }
    h += `<div class="cl">${AR(P.rows[r])}</div>`;
  }
  return h + "</div>";
}

const RULES = `
  <div class="rules">
    <div><span>١</span><p>لكل <b>طاولة</b> أريكة واحدة بجانبها: فوقها أو تحتها أو يمينها أو يسارها.</p></div>
    <div><span>٢</span><p>الأرائك <b>لا تتلامس</b>، ولا من الزاوية.</p></div>
    <div><span>٣</span><p>الرقم على الجدار = <b>كم أريكة</b> في ذلك الصف أو العمود.</p></div>
  </div>`;

const rng = A.makeRng(20261028);
const puzzles = [[5, 5, 4], [5, 5, 4], [6, 6, 6], [6, 6, 6]].map(([R, C, n]) => A.generate(R, C, n, rng));
puzzles.forEach((P) => { if (!P || A.countSolutions(P.R, P.C, P.tables, P.rows, P.cols, 2) !== 1) throw new Error("puzzle without a single solution"); });

const guide = `
<section class="page">
  <header class="hero"><h1>رتّب الغرفة</h1><p>لعبة تفكير من الورق: ضع كل أريكة في مكانها الصحيح.</p></header>
  <div class="box"><h3>القواعد الثلاث</h3>${RULES}</div>
  <div class="two">
    <div class="box"><h3>اصنع اللعبة</h3><ol>
      <li>اطبع الصفحات بالألوان.</li><li>قُصّ الأرائك الصغيرة من صفحة الأرائك.</li>
      <li>ألصق لوحة الغرفة على ورق مقوّى إن أردت أن تدوم.</li><li>احتفظ بصفحة الحلول عند المعلّم.</li></ol></div>
    <div class="box"><h3>كيف نلعب؟</h3><ol>
      <li>اختر غرفة، وعُدّ طاولاتها: لكل طاولة أريكة.</li><li>ضع الأرائك على المربعات، وأدِر كل أريكة لتتّجه إلى طاولتها.</li>
      <li>المربع الذي تعرف أنه فارغ، ضع عليه نقطة بالقلم الرصاص.</li><li>تحقّق من القواعد الثلاث، ثم قارن بصفحة الحلول.</li></ol></div>
  </div>
  <div class="box tip"><h3>نصيحة للبداية</h3><p>ابحث عن صف رقمه <b>٠</b>: لا أريكة فيه أبدًا، فضع نقاطًا في كل مربعاته. وابحث عن طاولة ليس بجانبها إلا مربع واحد فارغ: أريكتها هناك بالتأكيد.</p></div>
  <div class="box"><h3>على أرض الصف</h3><p>ارسموا الشبكة بشريط لاصق، وضعوا كرسيًّا أو صندوقًا مكان كل طاولة، واكتبوا الأرقام على أوراق عند الجدار. ثم يقف الأطفال أنفسهم مكان الأرائك، ويتأكّد زملاؤهم من القواعد الثلاث.</p></div>
</section>`;

const boards = puzzles.map((P, k) => `
<section class="page board">
  <div class="bhead"><h2>الغرفة ${AR(k + 1)}</h2><span class="tag">${AR(P.R)}×${AR(P.C)}</span><span class="tag">${AR(P.tables.length)} طاولات = ${AR(P.tables.length)} أرائك</span></div>
  ${RULES}
  <div class="room"><div class="window"></div><div class="door"></div>${grid(P, 25, false)}</div>
</section>`).join("");

const tokens = `
<section class="page">
  <div class="bhead"><h2>الأرائك</h2><span class="tag">٣٠ أريكة</span></div>
  <p class="lead">قُصّ كل أريكة على خطّها. ضعها على المربع، وأدِرها حتى يتّجه مقعدها إلى الطاولة.</p>
  <div class="tokens">${Array.from({ length: 30 }, (_, i) => `<div class="tok">${sofa(0, i)}</div>`).join("")}</div>
</section>`;

const solutions = `
<section class="page">
  <div class="bhead"><h2>الحلول</h2><span class="tag">للمعلّم</span></div>
  <p class="lead">لكل غرفة حلّ واحد فقط.</p>
  <div class="sols">${puzzles.map((P, k) => `<div class="sol"><h3>الغرفة ${AR(k + 1)}</h3>${grid(P, P.C === 5 ? 12 : 10.5, true)}</div>`).join("")}</div>
</section>`;

const css = `
@page { size: A4; margin: 0; }
:root { --ink: #22202a; --muted: #6a6474; --wall: #4a3346; --wood: #ecc995; --wood2: #d9ad6c; --glow: #f2b630; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #e8e6ea; }
body { font-family: "Readex Pro", sans-serif; color: var(--ink); direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; margin: 10mm auto; padding: 12mm 13mm; background: #fff; display: flex; flex-direction: column; gap: 5mm; overflow: hidden; break-after: page; box-shadow: 0 2px 12px rgba(0,0,0,.12); }
@media print { html, body { background: #fff; } .page { margin: 0; box-shadow: none; } }
h1, h2, h3 { font-family: "Lalezar", "Readex Pro", sans-serif; font-weight: 400; }
.hero { background: #2a2235; border-radius: 4mm; padding: 8mm; text-align: center; color: #fff; }
.hero h1 { font-size: 46pt; line-height: 1; color: #ffd98a; }
.hero p { margin-top: 2mm; font-size: 12pt; color: #e8e1f0; }
.box { border: .4mm solid #ddd6e2; border-radius: 3mm; padding: 4mm 5mm; }
.box h3 { font-size: 16pt; color: var(--wall); margin-bottom: 2mm; }
.box ol { padding-inline-start: 5mm; list-style: arabic-indic; font-size: 11pt; line-height: 1.75; }
.box p { font-size: 11pt; line-height: 1.75; }
.tip { background: #f2fbf5; border-color: #cfe9d8; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.rules { display: grid; gap: 2mm; }
.rules div { display: flex; align-items: center; gap: 3mm; font-size: 12pt; line-height: 1.5; }
.rules span { flex: none; width: 8mm; height: 8mm; border-radius: 50%; background: var(--glow); font-weight: 800; display: grid; place-items: center; }
.bhead { display: flex; align-items: center; gap: 3mm; border-bottom: 2px solid var(--ink); padding-bottom: 2mm; }
.bhead h2 { font-size: 24pt; line-height: 1; }
.tag { border: 1.5px solid var(--ink); border-radius: 20px; padding: .6mm 3mm; font-size: 10pt; font-weight: 600; }
.lead { font-size: 11pt; color: var(--muted); }
.board .rules div { font-size: 10.5pt; }
.board .rules span { width: 6.5mm; height: 6.5mm; }
.room { position: relative; align-self: center; margin-top: 3mm; padding: 9mm 8mm 8mm; background: var(--wall); border-radius: 2mm; }
.room .window { position: absolute; top: 2mm; left: 50%; transform: translateX(-50%); width: 35%; height: 3.5mm; border-radius: 1mm; background: linear-gradient(90deg, #bcd6ff 0 49%, #6d4f68 49% 51%, #bcd6ff 51%); }
.room .door { position: absolute; left: 1.5mm; bottom: 20%; width: 4mm; height: 22mm; background: #6b4a2f; border-radius: 1mm; }
.g { direction: ltr; display: grid; grid-template-columns: repeat(var(--c), var(--cell)) calc(var(--cell) * .6); grid-auto-rows: var(--cell); }
.g .cl { display: grid; place-items: center; font-weight: 800; font-size: calc(var(--cell) * .5); color: #ffd98a; }
.g .cl.top { height: calc(var(--cell) * .6); align-self: end; }
.sq { background: linear-gradient(var(--wood), var(--wood2)); border: .3mm solid #a77a42; display: grid; place-items: center; }
.sq svg { width: 86%; height: 86%; }
.tokens { display: grid; grid-template-columns: repeat(6, 25mm); grid-auto-rows: 25mm; justify-content: center; }
.tok { border: .3mm dashed #9aa0b4; display: grid; place-items: center; background: #fffaf0; }
.tok svg { width: 86%; height: 86%; }
.sols { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.sol { display: flex; flex-direction: column; align-items: center; gap: 2mm; background: var(--wall); border-radius: 2mm; padding: 4mm; }
.sol h3 { color: #ffd98a; font-size: 14pt; }
`;

const html = `<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>رتّب الغرفة: النسخة الورقية</title>
<link href="https://fonts.googleapis.com/css2?family=Lalezar&family=Readex+Pro:wght@400;600;800&display=swap" rel="stylesheet">
<style>${css}</style></head><body>${guide}${boards}${tokens}${solutions}</body></html>`;
fs.writeFileSync(path.join(__dirname, "..", "arrange-room-kit.html"), html);
