// Google Apps Script for بستان البذرة.
// Paste this into a Google Sheet (Extensions > Apps Script), then Deploy > New deployment > Web app,
// "Execute as: Me", "Who has access: Anyone". Copy the /exec link into config.js (reportUrl).
// After changing this code: Deploy > Manage deployments > edit (pencil) > Version: New version > Deploy.
// The link stays the same.

// رمز المعلّم: تطلبه لوحة المعلّم قبل بدء الجولات أو إنهائها. غيّره إلى رمز تختاره.
const TEACHER_PIN = "1234";

const SHEETS = {
  progress: { name: "التقدم", headers: ["الجهاز", "الفريق", "المرحلة", "اسم المرحلة", "المحطات المفتوحة", "انتهى", "آخر تحديث", "النمو بالسقي (سم)", "تعديل المعلّم (سم)", "الطول (سم)"] },
  log:      { name: "السجل",  headers: ["الوقت", "الجولة", "الجهاز", "الفريق", "المرحلة", "المحطات المفتوحة", "انتهى", "الطول (سم)"] },
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
  } else if (sh.getRange(1, def.headers.length).getValue() !== def.headers[def.headers.length - 1]) {
    sh.getRange(1, 1, 1, def.headers.length).setValues([def.headers]);   // sheet from an older version
  }
  return sh;
}

// Height in cm where each stage begins (same table as the game).
const HEIGHTS = [0, 5, 15, 30, 50, 80, 120, 180, 260, 400];
const STAGE_NAMES = ["بذرة", "تنتفخ البذرة", "الجُذير", "النُّبَيتة", "الفلقتان", "الأوراق", "الشتلة", "الشجيرة", "الإزهار", "الإثمار"];
function stageOf_(h) { let i = 0; while (i < 9 && h >= HEIGHTS[i + 1]) i++; return i; }
const round1_ = n => Math.round(n * 10) / 10;
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
  const stations = Math.max(0, Math.min(99, Number(d.stations) || 0));
  const team = clean_(d.team, 30);
  const done = d.done ? "نعم" : "لا";
  const growth = round1_(Math.max(0, Math.min(1000, Number(d.growth) || 0)));
  const progress = sheet_("progress");
  const body = body_("progress");
  const i = body.findIndex(r => String(r[0]) === id);
  const adj = i >= 0 ? Number(body[i][8]) || 0 : 0;
  const height = round1_(Math.max(0, growth + adj));
  const stage = stageOf_(height);
  const row = [id, team, stage + 1, STAGE_NAMES[stage], stations, done, now, growth, adj, height];
  if (i >= 0) progress.getRange(i + 2, 1, 1, row.length).setValues([row]);
  else progress.appendRow(row);
  sheet_("log").appendRow([now, st.round, id, team, stage + 1, stations, done, height]);
  return out_({ ok: true, state: st });
}

// The teacher adds to (delta > 0) or takes from (delta < 0) one team's height.
function adjust_(d, st) {
  const id = clean_(d.id, 40);
  const delta = Math.max(-1000, Math.min(1000, Number(d.delta) || 0));
  const progress = sheet_("progress");
  const body = body_("progress");
  const i = body.findIndex(r => String(r[0]) === id);
  if (i < 0 || !delta) return out_({ error: "bad_team" });
  const r = body[i], now = new Date();
  const growth = Number(r[7]) || 0, adj = round1_((Number(r[8]) || 0) + delta);
  const height = round1_(Math.max(0, growth + adj)), stage = stageOf_(height);
  progress.getRange(i + 2, 1, 1, 10).setValues([[r[0], r[1], stage + 1, STAGE_NAMES[stage], r[4], r[5], now, growth, adj, height]]);
  sheet_("log").appendRow([now, st.round, r[0], r[1], stage + 1, r[4], r[5], height]);
  return out_({ ok: true, state: state_() });
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
  } else if (d.action === "adjust") {
    return adjust_(d, st);
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
  if (action === "state") {
    const id = e.parameter.id;
    if (id) {
      const r = body_("progress").find(x => String(x[0]) === id);
      st.adj = r ? Number(r[8]) || 0 : 0;
    }
    return out_(st);
  }
  if (action === "history") {
    const rounds = body_("rounds").map(r => ({ round: Number(r[0]), start: iso_(r[1]), end: iso_(r[2]) }));
    const log = body_("log").map(r => ({
      t: iso_(r[0]), round: Number(r[1]) || 0, id: String(r[2]), team: plain_(r[3]),
      stage: Number(r[4]) || 1, stations: Number(r[5]) || 0, done: r[6] === "نعم", height: Number(r[7]) || 0
    }));
    return out_({ state: st, rounds: rounds, log: log });
  }
  const rows = body_("progress").map(r => ({
    id: String(r[0]), team: plain_(r[1]), stage: Number(r[2]) || 1, stageName: String(r[3]),
    stations: Number(r[4]) || 0, done: r[5] === "نعم", updated: iso_(r[6]),
    growth: Number(r[7]) || 0, adj: Number(r[8]) || 0, height: Number(r[9]) || 0
  }));
  return out_({ state: st, rows: rows });
}
