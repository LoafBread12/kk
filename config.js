// إعدادات لعبة بستان البذرة — تقرؤها صفحة اللعبة وصفحة المعلّم.
window.GAME_CONFIG = {
  // ضع هنا رابط Google Apps Script بعد نشره (ينتهي بـ /exec). اتركه فارغًا لإيقاف الإرسال.
  reportUrl: "https://script.google.com/macros/s/AKfycbzXtAE-kksow9uUfr5THfL75AGyrGLdvZVJNPjBWpZ6K7XcSJjVaysUj9MpOiRAJbCl/exec",

  // أسماء المحطات وكلمات السر
  stations: [
    { id: "s1", name: "محطة الشمس",  icon: "sun",      code: "101" },
    { id: "s2", name: "محطة الغيمة", icon: "cloud",    code: "202" },
    { id: "s3", name: "محطة الجبل",  icon: "mountain", code: "303" },
    { id: "s4", name: "محطة النجمة", icon: "star",     code: "404" },
    { id: "s5", name: "محطة القمر",  icon: "moon",     code: "505" },
    { id: "s6", name: "محطة القطرة", icon: "drop",     code: "606" }
  ]
};
