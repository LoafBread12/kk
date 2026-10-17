// إعدادات لعبة بستان البذرة — تقرؤها صفحة اللعبة وصفحة المعلّم.
window.GAME_CONFIG = {
  // ضع هنا رابط Google Apps Script بعد نشره (ينتهي بـ /exec). اتركه فارغًا لإيقاف الإرسال.
  reportUrl: "https://script.google.com/macros/s/AKfycbzXtAE-kksow9uUfr5THfL75AGyrGLdvZVJNPjBWpZ6K7XcSJjVaysUj9MpOiRAJbCl/exec",

  // أسماء المحطات وكلمات السر
  stations: [
    // محطة بخطوتين: السؤال الموجود في الحجرة يعطي ٤٠٪ من ماء المحطة، والجواب يعطي ٦٠٪.
    // accept: الإجابات المقبولة. keywords: تُقبل أي إجابة فيها كل هذه الكلمات.
    { id: "s1", name: "الحجرة المظلمة", icon: "door", steps: [
      { label: "اكتبوا السؤال الذي وجدتموه في الحجرة", button: "أرسل السؤال", water: 0.4,
        accept: ["اسم البيعة التي كانت تحت الشجرة"], keywords: ["بيعة", "شجرة"],
        success: "أحسنتم! حصلتم على بعض الماء. والآن ابحثوا عن الجواب.",
        wrong: "هذا ليس السؤال الموجود في الحجرة. اقرؤوه جيدًا واكتبوه مرة أخرى." },
      { label: "اكتبوا الجواب", button: "أرسل الجواب", water: 0.6,
        accept: ["الرضوان", "رضوان", "بيعة الرضوان"] }
    ] },
    { id: "s2", name: "محطة الغيمة", icon: "cloud",    code: "202" },
    { id: "s3", name: "محطة الجبل",  icon: "mountain", code: "303" },
    { id: "s4", name: "محطة النجمة", icon: "star",     code: "404" },
    { id: "s5", name: "محطة القمر",  icon: "moon",     code: "505" },
    { id: "s6", name: "محطة القطرة", icon: "drop",     code: "606" }
  ]
};
