"""Builds ../one-answer-poster.html: an A3 poster of the 20 one-answer question groups, in the user's own order and wording."""
from pathlib import Path

AR = "٠١٢٣٤٥٦٧٨٩"
ar = lambda n: "".join(AR[int(d)] for d in str(n))

SECTIONS = [
    ("seerah", "أولًا: السيرة", [
        ("الهجرة", ["ماذا سُمّي خروج المسلمين إلى المدينة؟", "في أيّ حدث كان الاختباء في غار ثور؟"]),
        ("بدر", ["ما أول غزوة كبيرة انتصر فيها المسلمون؟", "أيّ غزوة كانت في رمضان في السنة الثانية للهجرة؟", "أيّ غزوة كان عدد المسلمين فيها نحو ثلاثمئة وثلاثة عشر؟"]),
        ("أُحُد", ["ما الجبل القريب من المدينة الذي وقعت عنده غزوة مشهورة؟", "أيّ غزوة ترك فيها الرماة أماكنهم؟", "أيّ غزوة كانت في السنة الثالثة للهجرة؟"]),
        ("حراء", ["في أيّ غار نزل الوحي أول مرة؟", "في أيّ غار كان يتعبّد قبل البعثة؟", "أيّ غار يقع في جبل النور؟"]),
        ("الحبشة", ["إلى أيّ بلد كانت أول هجرة للمسلمين؟", "في أيّ بلد كان الملك العادل الذي أكرم المهاجرين؟", "إلى أيّ بلد هاجر المسلمون مرتين؟"]),
        ("الحديبية", ["ما اسم الصلح الذي كان في السنة السادسة للهجرة؟", "عند أيّ مكان كانت البيعة تحت الشجرة؟", "أيّ صلح ظنّه بعض المسلمين خسارة، فكان بعده خير كثير؟"]),
    ]),
    ("science", "ثانيًا: العلوم", [
        ("الماء", ["ماذا يصير ثلجًا إذا تجمّد؟", "ماذا يتبخّر من البحر فيصير سحابًا؟", "ماذا تحتاج البذرة لتنبت؟", "ممّا يتكوّن أكثر جسم الإنسان؟"]),
        ("الشمس", ["ما النجم الأقرب إلى الأرض؟", "حول أيّ شيء تدور الأرض؟", "ضوء أيّ شيء يعكسه القمر؟"]),
        ("القمر", ["ما الذي نراه هلالًا في أول الشهر؟", "ما الذي لا يضيء بنفسه، بل يعكس ضوء الشمس؟"]),
        ("السحاب", ["من أين ينزل المطر؟", "ماذا يصير بخار الماء إذا برد في السماء؟", "ما الذي تحرّكه الرياح في السماء ويحجب الشمس أحيانًا؟"]),
        ("الثلج", ["ماذا نسمّي الماء المتجمّد؟"]),
        ("الورقة", ["أين يصنع النبات غذاءه؟", "أيّ جزء من النبات فيه اليخضور الأخضر؟", "ماذا تُسقط بعض الأشجار في الخريف؟"]),
        ("القلب", ["أيّ عضو ينبض ولا يستريح؟", "ما العضو الذي يضخّ الدم؟", "ما العضو الذي فيه أربع حجرات؟"]),
        ("الأذن", ["بأيّ عضو نسمع؟", "أين توجد أصغر عظمة في الجسم؟", "أيّ عضو فيه جزء يحفظ توازننا؟"]),
        ("الأنف", ["بأيّ عضو نشمّ؟", "من أين يدخل الهواء إلى الجسم؟", "أيّ عضو نعطس به لنطرد الغبار؟"]),
        ("الجلد", ["ما أكبر عضو في جسم الإنسان؟", "بأيّ عضو نحسّ بالحرارة والبرودة؟", "على أيّ عضو تظهر البصمات؟"]),
    ]),
    ("islam", "ثالثًا: الإسلام", [
        ("الجمعة", ["في أيّ يوم يُستحبّ الاغتسال ولبس أحسن الثياب؟"]),
        ("ركعتان", ["كم ركعة نصلّي إذا دخلنا المسجد قبل أن نجلس؟", "كم ركعة يُستحبّ أن نصلّي بعد الوضوء؟"]),
        ("الوضوء", ["ما الذي يُستحبّ أن نفعله قبل النوم؟", "ما الذي يُستحبّ تجديده لكل صلاة ولو لم ينتقض؟", "بعد أيّ عمل يُستحبّ أن نقول الشهادتين؟"]),
        ("شوّال", ["ما الشهر الذي يأتي بعد رمضان؟", "في أيّ شهر يكون عيد الفطر؟", "في أيّ شهر تُصام الأيام الستّة بعد رمضان؟"]),
    ]),
]

# section emblems: no living beings, only places, sky and geometry
ICONS = {
    "seerah": '<svg viewBox="0 0 64 64"><path d="M4 54L24 18l10 16 6-8 20 28z" fill="#c9893a"/><path d="M24 18l5 8-5 4-4-5z" fill="#f6e3bf"/><path d="M27 54c0-6 3-10 7-10s7 4 7 10z" fill="#5a3a1c"/><circle cx="50" cy="14" r="6" fill="#f6e3bf"/><circle cx="53" cy="12" r="5" fill="#7a4a1f"/></svg>',
    "science": '<svg viewBox="0 0 64 64"><circle cx="30" cy="32" r="15" fill="#3d8fe0"/><path d="M22 26c4-3 9-1 8 4s-6 3-8 7-5-1-4-5 2-5 4-6zM34 38c3-1 6 1 4 4s-5 2-6 0z" fill="#5bb36a"/><ellipse cx="30" cy="32" rx="27" ry="8" fill="none" stroke="#f0c25a" stroke-width="3" transform="rotate(-18 30 32)"/><path d="M52 8c-3 5-5 8-5 11a5 5 0 0 0 10 0c0-3-2-6-5-11z" fill="#7cc4f2"/></svg>',
    "islam": '<svg viewBox="0 0 64 64"><path d="M12 56V36a20 20 0 0 1 40 0v20z" fill="#2f8a62"/><path d="M32 16c-2-5-1-9 3-12-6 1-9 6-8 11 1 4 4 6 8 6-2-1-3-3-3-5z" fill="#f0c25a"/><rect x="26" y="40" width="12" height="16" rx="6" fill="#123d2c"/><path d="M6 56h52" stroke="#123d2c" stroke-width="3"/></svg>',
}

THEMES = {
    "seerah": ("#b06a22", "#fbf1e1", "#7a4510"),
    "science": ("#2c6fb8", "#e9f2fb", "#18457a"),
    "islam": ("#24805a", "#e7f5ee", "#135438"),
}


def card(n, answer, qs, kind):
    items = "".join(f"<li>{q}</li>" for q in qs)
    return f'''<article class="card {kind}">
  <header><span class="n">{ar(n)}</span><span class="ans"><small>الجواب</small>{answer}</span></header>
  <ol>{items}</ol>
</article>'''


def build():
    n, body = 0, ""
    for kind, title, groups in SECTIONS:
        cards = ""
        for answer, qs in groups:
            n += 1
            cards += card(n, answer, qs, kind)
        c, soft, deep = THEMES[kind]
        body += f'''<section class="sec {kind}" style="--c:{c};--soft:{soft};--deep:{deep}">
  <div class="sec-head">{ICONS[kind]}<h2>{title}</h2><span class="count">{ar(len(groups))} مجموعات</span></div>
  <div class="grid g-{kind}">{cards}</div>
</section>'''

    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>أسئلة الجواب الواحد</title>
<link href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=Readex+Pro:wght@400;600;800&display=swap" rel="stylesheet">
<style>
@page {{ size: A3; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #e7e3da; }}
body {{ font-family: "Readex Pro", sans-serif; color: #1f2430; direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.poster {{ width: 297mm; height: 420mm; margin: 10mm auto; position: relative; overflow: hidden; background: #fbf8f2;
           display: flex; flex-direction: column; box-shadow: 0 4px 24px rgba(0,0,0,.15); }}
@media print {{ html, body {{ background: #fff; }} .poster {{ margin: 0; box-shadow: none; }} }}

/* header: night sky with an eight-point star pattern */
.top {{ position: relative; padding: 11mm 16mm 10mm; color: #fff; text-align: center;
        background: radial-gradient(circle at 20% 30%, #ffffff30 0 .6mm, transparent .8mm) 0 0/22mm 22mm,
                    radial-gradient(circle at 70% 60%, #ffffff22 0 .45mm, transparent .65mm) 0 0/17mm 17mm,
                    linear-gradient(160deg, #1d2a52, #101731 70%); }}
.top::after {{ content: ""; position: absolute; inset: auto 0 0 0; height: 7mm;
               background: repeating-linear-gradient(45deg, #f0c25a 0 2mm, transparent 2mm 5mm),
                           repeating-linear-gradient(-45deg, #f0c25a 0 2mm, transparent 2mm 5mm); opacity: .9;
               -webkit-mask: linear-gradient(#000, #000); }}
.top h1 {{ font-family: "Reem Kufi", sans-serif; font-weight: 700; font-size: 58pt; line-height: 1.05; color: #f6d27a; }}
.top p {{ margin-top: 3mm; font-size: 15pt; color: #e3e7f5; }}
.stars {{ position: absolute; top: 9mm; width: 26mm; height: 26mm; opacity: .9; }}
.stars.r {{ right: 14mm; }} .stars.l {{ left: 14mm; }}

main {{ flex: 1; padding: 7mm 12mm 5mm; display: flex; flex-direction: column; justify-content: space-between; gap: 6mm; }}
.sec-head {{ display: flex; align-items: center; gap: 3.5mm; margin-bottom: 3mm; }}
.sec-head svg {{ width: 13mm; height: 13mm; flex: none; }}
.sec-head h2 {{ font-family: "Reem Kufi", sans-serif; font-weight: 700; font-size: 25pt; color: var(--deep); }}
.sec-head .count {{ margin-inline-start: auto; font-size: 11pt; font-weight: 600; color: var(--c); border: .5mm solid var(--c); border-radius: 20px; padding: .7mm 4mm; }}
.sec-head::after {{ content: ""; order: 2; flex: 1; height: .6mm; background: linear-gradient(to left, var(--c), transparent); }}
.sec-head .count {{ order: 3; margin-inline-start: 0; }}

.grid {{ display: grid; gap: 3.5mm; }}
.g-seerah {{ grid-template-columns: repeat(3, 1fr); }}
.g-science {{ grid-template-columns: repeat(5, 1fr); }}
.g-islam {{ grid-template-columns: repeat(4, 1fr); }}

.card {{ background: #fff; border-radius: 4mm; overflow: hidden; border: .5mm solid color-mix(in srgb, var(--c) 35%, #fff);
         display: flex; flex-direction: column; box-shadow: 0 1mm 0 color-mix(in srgb, var(--c) 25%, #fff); }}
.card header {{ display: flex; align-items: center; gap: 2.5mm; padding: 2.4mm 3mm;
               background: linear-gradient(135deg, var(--c), var(--deep)); color: #fff; }}
.card .n {{ flex: none; width: 8.5mm; height: 8.5mm; border-radius: 50%; background: #ffffff30; display: grid; place-items: center; font-weight: 800; font-size: 12pt; }}
.card .ans {{ font-family: "Reem Kufi", sans-serif; font-weight: 700; font-size: 19pt; line-height: 1.25; }}
.card .ans small {{ display: block; font-family: "Readex Pro", sans-serif; font-weight: 400; font-size: 8pt; line-height: 1.2; margin-bottom: 1.6mm; opacity: .85; }}
.card ol {{ list-style: none; padding: 2.6mm 3mm 3mm; display: grid; gap: 1.6mm; align-content: start; background:
            radial-gradient(circle at 0 0, var(--soft) 0 30%, transparent 30.5%), #fff; flex: 1; }}
.card li {{ position: relative; padding-inline-start: 4mm; font-size: 10.6pt; line-height: 1.45; }}
.card li::before {{ content: ""; position: absolute; inset-inline-start: 0; top: 2.1mm; width: 2mm; height: 2mm;
                    background: var(--c); transform: rotate(45deg); border-radius: .4mm; }}
.g-science .card li {{ font-size: 9.5pt; }}
.g-science .card .ans {{ font-size: 17pt; }}

.foot {{ padding: 0 12mm 5mm; text-align: center; font-size: 10pt; color: #6b6a72; }}
</style></head><body>
<div class="poster">
  <div class="top">
    <svg class="stars r" viewBox="0 0 40 40"><g fill="none" stroke="#f0c25a" stroke-width="1.6"><rect x="9" y="9" width="22" height="22"/><rect x="9" y="9" width="22" height="22" transform="rotate(45 20 20)"/><circle cx="20" cy="20" r="5"/></g></svg>
    <svg class="stars l" viewBox="0 0 40 40"><g fill="none" stroke="#f0c25a" stroke-width="1.6"><rect x="9" y="9" width="22" height="22"/><rect x="9" y="9" width="22" height="22" transform="rotate(45 20 20)"/><circle cx="20" cy="20" r="5"/></g></svg>
    <h1>أسئلة الجواب الواحد</h1>
    <p>في كل بطاقة أسئلة كثيرة… وجوابها كلها كلمة واحدة!</p>
  </div>
  <main>{body}</main>
  <div class="foot">من يعرف الجواب من السؤال الأول يأخذ ٣ نقاط، ومن الثاني نقطتين، ومن الثالث نقطة واحدة.</div>
</div>
</body></html>'''
    (Path(__file__).parent.parent / "one-answer-poster.html").write_text(html)


if __name__ == "__main__":
    build()
