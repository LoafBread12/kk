// Google Apps Script for بستان البذرة.
// Paste this into a Google Sheet (Extensions > Apps Script), then Deploy > New deployment > Web app,
// "Execute as: Me", "Who has access: Anyone". Copy the /exec link into config.js (reportUrl).

const SHEET_NAME = "التقدم";
const HEADERS = ["الجهاز", "الفريق", "المرحلة", "اسم المرحلة", "المحطات المفتوحة", "انتهى", "آخر تحديث"];

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
    sh.setRightToLeft(true);
  }
  return sh;
}

// Text that starts like a formula is stored as plain text.
function clean_(v, max) {
  let s = String(v == null ? "" : v).slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  const id = clean_(d.id, 40);
  if (!id) return ContentService.createTextOutput("missing id");
  const row = [
    id,
    clean_(d.team, 30),
    Math.max(1, Math.min(10, Number(d.stage) || 1)),
    clean_(d.stageName, 30),
    Math.max(0, Math.min(99, Number(d.stations) || 0)),
    d.done ? "نعم" : "لا",
    new Date()
  ];
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_();
    const n = sh.getLastRow() - 1;
    const ids = n > 0 ? sh.getRange(2, 1, n, 1).getValues().map(r => String(r[0])) : [];
    const i = ids.indexOf(id);
    if (i >= 0) sh.getRange(i + 2, 1, 1, row.length).setValues([row]);
    else sh.appendRow(row);
  } finally {
    lock.releaseLock();
  }
  return ContentService.createTextOutput("ok");
}

function doGet() {
  const sh = sheet_();
  const n = sh.getLastRow() - 1;
  const values = n > 0 ? sh.getRange(2, 1, n, HEADERS.length).getValues() : [];
  const rows = values.map(r => ({
    id: String(r[0]),
    team: String(r[1]).replace(/^'/, ""),
    stage: Number(r[2]) || 1,
    stageName: String(r[3]),
    stations: Number(r[4]) || 0,
    done: r[5] === "نعم",
    updated: r[6] instanceof Date ? r[6].toISOString() : String(r[6])
  }));
  return ContentService.createTextOutput(JSON.stringify(rows)).setMimeType(ContentService.MimeType.JSON);
}
