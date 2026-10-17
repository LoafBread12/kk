// Google Apps Script for بستان البذرة.
// Paste this into a Google Sheet (Extensions > Apps Script), then Deploy > New deployment > Web app,
// "Execute as: Me", "Who has access: Anyone". Copy the /exec link into config.js (reportUrl).
// After changing this code: Deploy > Manage deployments > edit (pencil) > Version: New version > Deploy.
// The link stays the same.

// رمز المعلّم: تطلبه لوحة المعلّم قبل بدء الجولات أو إنهائها. غيّره إلى رمز تختاره.
const TEACHER_PIN = "1234";

const SHEETS = {
  progress: { name: "التقدم", headers: ["الجهاز", "الفريق", "المرحلة", "اسم المرحلة", "المحطات المفتوحة", "انتهى", "آخر تحديث"] },
  log:      { name: "السجل",  headers: ["الوقت", "الجولة", "الجهاز", "الفريق", "المرحلة", "المحطات المفتوحة", "انتهى"] },
  rounds:   { name: "الجولات", headers: ["الجولة", "البداية", "النهاية"] }
};

function sheet_(key) {
  const def = SHEETS[key];
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(def.name);
  if (!sh) {
    sh = ss.insertSheet(def.name);
    sh.appendRow(def.headers);
    sh.setFrozenRows(1);
    sh.setRightToLeft(true);
  }
  return sh;
}
function body_(key) {
  const sh = sheet_(key), n = sh.getLastRow() - 1;
  return n > 0 ? sh.getRange(2, 1, n, SHEETS[key].headers.length).getValues() : [];
}
function clear_(key) {
  const sh = sheet_(key), n = sh.getLastRow() - 1;
  if (n > 0) sh.deleteRows(2, n);
}

function state_() {
  const p = PropertiesService.getScriptProperties();
  let gameId = p.getProperty("gameId");
  if (!gameId) { gameId = "g" + Date.now().toString(36); p.setProperty("gameId", gameId); }
  return {
    status: p.getProperty("status") || "idle",   // idle | running | ended | over
    round: Number(p.getProperty("round") || 0),
    gameId: gameId
  };
}
function setState_(patch) {
  const p = PropertiesService.getScriptProperties();
  Object.keys(patch).forEach(k => p.setProperty(k, String(patch[k])));
}

// Text that starts like a formula is stored as plain text.
function clean_(v, max) {
  let s = String(v == null ? "" : v).slice(0, max);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}
const plain_ = v => String(v).replace(/^'/, "");
const iso_ = v => v instanceof Date ? v.toISOString() : String(v || "");
function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function report_(d) {
  const id = clean_(d.id, 40);
  if (!id) return out_({ error: "missing_id" });
  const st = state_();
  if (d.gameId && d.gameId !== st.gameId) return out_({ ignored: true, state: st });
  const now = new Date();
  const stage = Math.max(1, Math.min(10, Number(d.stage) || 1));
  const stations = Math.max(0, Math.min(99, Number(d.stations) || 0));
  const team = clean_(d.team, 30);
  const done = d.done ? "نعم" : "لا";
  const row = [id, team, stage, clean_(d.stageName, 30), stations, done, now];
  const progress = sheet_("progress");
  const ids = body_("progress").map(r => String(r[0]));
  const i = ids.indexOf(id);
  if (i >= 0) progress.getRange(i + 2, 1, 1, row.length).setValues([row]);
  else progress.appendRow(row);
  sheet_("log").appendRow([now, st.round, id, team, stage, stations, done]);
  return out_({ ok: true, state: st });
}

function control_(d) {
  if (String(d.pin) !== TEACHER_PIN) return out_({ error: "bad_pin" });
  const st = state_();
  const now = new Date();
  const rounds = sheet_("rounds");
  const closeRound = () => {
    const n = rounds.getLastRow();
    if (n >= 2 && !rounds.getRange(n, 3).getValue()) rounds.getRange(n, 3).setValue(now);
  };
  if (d.action === "start") {
    if (st.status !== "running" && st.status !== "over") {
      setState_({ status: "running", round: st.round + 1 });
      rounds.appendRow([st.round + 1, now, ""]);
    }
  } else if (d.action === "end") {
    if (st.status === "running") { closeRound(); setState_({ status: "ended" }); }
  } else if (d.action === "over") {
    if (st.status === "running") closeRound();
    setState_({ status: "over" });
  } else if (d.action === "new") {
    clear_("progress"); clear_("log"); clear_("rounds");
    setState_({ status: "idle", round: 0, gameId: "g" + Date.now().toString(36) });
  } else {
    return out_({ error: "bad_action" });
  }
  return out_({ ok: true, state: state_() });
}

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    return d.type === "control" ? control_(d) : report_(d);
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  const action = (e && e.parameter && e.parameter.action) || "rows";
  const st = state_();
  if (action === "state") return out_(st);
  if (action === "history") {
    const rounds = body_("rounds").map(r => ({ round: Number(r[0]), start: iso_(r[1]), end: iso_(r[2]) }));
    const log = body_("log").map(r => ({
      t: iso_(r[0]), round: Number(r[1]) || 0, id: String(r[2]), team: plain_(r[3]),
      stage: Number(r[4]) || 1, stations: Number(r[5]) || 0, done: r[6] === "نعم"
    }));
    return out_({ state: st, rounds: rounds, log: log });
  }
  const rows = body_("progress").map(r => ({
    id: String(r[0]), team: plain_(r[1]), stage: Number(r[2]) || 1, stageName: String(r[3]),
    stations: Number(r[4]) || 0, done: r[5] === "نعم", updated: iso_(r[6])
  }));
  return out_({ state: st, rows: rows });
}
