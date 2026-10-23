// Google Apps Script for بستان البذرة.
// Paste this into a Google Sheet (Extensions > Apps Script), then Deploy > New deployment > Web app,
// "Execute as: Me", "Who has access: Anyone". Copy the /exec link into config.js (reportUrl).
// After changing this code: Deploy > Manage deployments > edit (pencil) > Version: New version > Deploy.
// The link stays the same.

// رمز المعلّم: تطلبه لوحة المعلّم قبل بدء الجولات أو إنهائها. غيّره إلى رمز تختاره.
const TEACHER_PIN = "1234";

// عدد أشواط كل جولة بالترتيب: الجولة الأولى ٤ أشواط، والثانية شوطان. وكل شوط ١٥ دقيقة.
// يبدأ المعلّم كل شوط بنفسه، ويتوقّف السقي تلقائيًا عند انتهاء وقته. الجولات بعد آخر رقم تأخذ آخر رقم.
const PARTS_PER_ROUND = [4, 2];
const PART_MINUTES = 15;
const partsFor_ = round => PARTS_PER_ROUND[Math.min(Math.max(1, round), PARTS_PER_ROUND.length) - 1];

const SHEETS = {
  progress: { name: "التقدم", headers: ["الجهاز", "الفريق", "المرحلة", "اسم المرحلة", "المحطات المفتوحة", "انتهى", "آخر تحديث", "النمو بالسقي (سم)", "تعديل المعلّم (سم)", "الطول (سم)", "المجموعة"] },
  log:      { name: "السجل",  headers: ["الوقت", "الجولة", "الجهاز", "الفريق", "المرحلة", "المحطات المفتوحة", "انتهى", "الطول (سم)"] },
  rounds:   { name: "الجولات", headers: ["الجولة", "البداية", "النهاية", "الشوط", "موعد الانتهاء"] },
  items:    { name: "العناصر", headers: ["المعرّف", "الجهاز", "الفريق", "النوع", "المقدار (سم)", "وقت الإعطاء", "وقت الاستخدام"] }
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
const HEIGHTS = [0, 5, 15, 30, 50, 80, 120, 180, 260, 400, 500, 650, 800, 1000];
const STAGE_NAMES = ["بذرة", "تنتفخ البذرة", "الجُذير", "النُّبَيتة", "الفلقتان", "الأوراق", "الشتلة", "الشجيرة", "الإزهار", "الإثمار",
  "شجرة وارفة", "شجرة باسقة", "شجرة عظيمة", "قمّة البستان"];
function stageOf_(h) { let i = 0; while (i < HEIGHTS.length - 1 && h >= HEIGHTS[i + 1]) i++; return i; }
const round1_ = n => Math.round(n * 10) / 10;
function body_(key) {
  const sh = sheet_(key), n = sh.getLastRow() - 1;
  return n > 0 ? sh.getRange(2, 1, n, SHEETS[key].headers.length).getValues() : [];
}
function clear_(key) {
  const sh = sheet_(key), n = sh.getLastRow() - 1;
  if (n > 0) sh.deleteRows(2, n);
}

// status: idle (no round yet) | running (a part is on) | break (between parts) | ended (round over) | over (game over).
// A running part whose time is up reads as break, or ended after the last part, without anyone pressing a button.
function state_() {
  const p = PropertiesService.getScriptProperties();
  let gameId = p.getProperty("gameId");
  if (!gameId) { gameId = "g" + Date.now().toString(36); p.setProperty("gameId", gameId); }
  let status = p.getProperty("status") || "idle";
  const part = Number(p.getProperty("part") || 0);
  const round = Number(p.getProperty("round") || 0), parts = partsFor_(round);
  // prayer time stops everything and holds the running part's clock: it reads the same time left until prayer ends
  const prayer = p.getProperty("prayer") === "1";
  let endsAt = Number(p.getProperty("endsAt") || 0);
  if (prayer && status === "running") endsAt = Date.now() + Number(p.getProperty("prayerLeft") || 0);
  else if (status === "running" && endsAt && Date.now() >= endsAt) status = part >= parts ? "ended" : "break";
  return {
    status: status,
    round: round,
    part: part,
    parts: parts,
    partMinutes: PART_MINUTES,
    lesson: p.getProperty("lesson") === "1",       // lesson time: everything closed except the extra tasks
    prayer: prayer,                                // prayer time: everything closed, the part's clock held
    endsAt: endsAt ? new Date(endsAt).toISOString() : "",
    now: new Date().toISOString(),
    gameId: gameId
  };
}
// write down a part that ran out on its own: its status and its end time in the rounds sheet
function settle_() {
  const p = PropertiesService.getScriptProperties();
  const endsAt = Number(p.getProperty("endsAt") || 0);
  if (p.getProperty("prayer") === "1") return;
  if (p.getProperty("status") !== "running" || !endsAt || Date.now() < endsAt) return;
  closePart_(new Date(endsAt));
  p.setProperty("status", Number(p.getProperty("part") || 0) >= partsFor_(Number(p.getProperty("round") || 0)) ? "ended" : "break");
}
function closePart_(when) {
  const sh = sheet_("rounds"), n = sh.getLastRow();
  if (n >= 2 && !sh.getRange(n, 3).getValue()) sh.getRange(n, 3).setValue(when);
}
function startPart_(round, part) {
  const now = new Date(), ends = new Date(now.getTime() + PART_MINUTES * 60000);
  setState_({ status: "running", round: round, part: part, endsAt: ends.getTime(), prayerLeft: PART_MINUTES * 60000 });
  sheet_("rounds").appendRow([round, now, "", part, ends]);
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
  const group = Math.max(0, Math.min(20, Number(d.group) || 0));
  const row = [id, team, stage + 1, STAGE_NAMES[stage], stations, done, now, growth, adj, height, group];
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

// The teacher gives a team an item (fertilizer or a rain cloud); the team uses it from its own device.
const ITEM_KINDS = ["fert", "rain"];
function give_(d) {
  const id = clean_(d.id, 40);
  const amount = Math.max(1, Math.min(1000, Number(d.delta) || 0));
  const kind = ITEM_KINDS.indexOf(d.kind) >= 0 ? d.kind : "fert";
  const r = body_("progress").find(x => String(x[0]) === id);
  if (!r) return out_({ error: "bad_team" });
  const key = "i" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  sheet_("items").appendRow([key, id, r[1], kind, amount, new Date(), ""]);
  return out_({ ok: true, state: state_() });
}
// A team activates one of its items: mark it used and add its height. Safe to call twice.
function useItem_(d) {
  const st = state_();
  if (d.gameId && d.gameId !== st.gameId) return out_({ ignored: true });
  const id = clean_(d.id, 40), key = String(d.key || "");
  const sh = sheet_("items"), body = body_("items");
  const i = body.findIndex(r => String(r[0]) === key && String(r[1]) === id);
  if (i < 0) return out_({ error: "bad_item" });
  if (body[i][6]) return out_({ ok: true, already: true });
  sh.getRange(i + 2, 7).setValue(new Date());
  return adjust_({ id: id, delta: Number(body[i][4]) || 0 }, st);
}
function pendingItems_(id) {
  return body_("items").filter(r => !r[6] && (!id || String(r[1]) === id))
    .map(r => ({ key: String(r[0]), id: String(r[1]), kind: String(r[3]), amount: Number(r[4]) || 0 }));
}

function control_(d) {
  if (String(d.pin) !== TEACHER_PIN) return out_({ error: "bad_pin" });
  settle_();
  const st = state_();
  const now = new Date();
  if (d.action === "start") {                       // a new round, from its first part
    if (st.status === "idle" || st.status === "ended") startPart_(st.round + 1, 1);
  } else if (d.action === "part") {                 // the next part of the current round
    if (st.status === "break" && st.part < st.parts) startPart_(st.round, st.part + 1);
  } else if (d.action === "end") {                  // end the running part early
    if (st.status === "running") { closePart_(now); setState_({ status: st.part >= st.parts ? "ended" : "break", endsAt: now.getTime() }); }
  } else if (d.action === "endRound") {             // end the whole round now
    if (st.status === "running") closePart_(now);
    if (st.status === "running" || st.status === "break") setState_({ status: "ended", endsAt: now.getTime() });
  } else if (d.action === "over") {
    if (st.status === "running") closePart_(now);
    setState_({ status: "over" });
  } else if (d.action === "prayer") {             // the teacher's prayer button: hold or release the part's clock
    const p = PropertiesService.getScriptProperties(), on = p.getProperty("prayer") === "1";
    const running = p.getProperty("status") === "running", endsAt = Number(p.getProperty("endsAt") || 0);
    if (d.on && !on) setState_({ prayer: "1", prayerLeft: running ? Math.max(0, endsAt - now.getTime()) : 0 });
    if (!d.on && on) {
      if (running) setState_({ endsAt: now.getTime() + Number(p.getProperty("prayerLeft") || 0) });
      setState_({ prayer: "0" });
    }
  } else if (d.action === "lesson") {             // the teacher's lesson button: on or off
    setState_({ lesson: d.on ? "1" : "0" });
  } else if (d.action === "give") {
    return give_(d);
  } else if (d.action === "adjust") {
    return adjust_(d, st);
  } else if (d.action === "new") {
    clear_("progress"); clear_("log"); clear_("rounds"); clear_("items");
    setState_({ status: "idle", round: 0, part: 0, endsAt: 0, lesson: "0", prayer: "0", gameId: "g" + Date.now().toString(36) });
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
    if (d.type === "control") return control_(d);
    if (d.type === "useItem") return useItem_(d);
    return report_(d);
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
      st.items = pendingItems_(id).map(x => ({ key: x.key, kind: x.kind, amount: x.amount }));
    }
    return out_(st);
  }
  if (action === "history") {
    // a part with no end written yet ends at its deadline, or now if that is earlier
    const rounds = body_("rounds").map(r => ({
      round: Number(r[0]), part: Number(r[3]) || 1, start: iso_(r[1]),
      end: r[2] ? iso_(r[2]) : r[4] instanceof Date && r[4].getTime() < Date.now() ? iso_(r[4]) : ""
    }));
    const log = body_("log").map(r => ({
      t: iso_(r[0]), round: Number(r[1]) || 0, id: String(r[2]), team: plain_(r[3]),
      stage: Number(r[4]) || 1, stations: Number(r[5]) || 0, done: r[6] === "نعم", height: Number(r[7]) || 0
    }));
    return out_({ state: st, rounds: rounds, log: log });
  }
  const pending = pendingItems_();
  const rows = body_("progress").map(r => ({
    id: String(r[0]), team: plain_(r[1]), stage: Number(r[2]) || 1, stageName: String(r[3]),
    stations: Number(r[4]) || 0, done: r[5] === "نعم", updated: iso_(r[6]),
    growth: Number(r[7]) || 0, adj: Number(r[8]) || 0, height: Number(r[9]) || 0,
    items: pending.filter(x => x.id === String(r[0])).length,
    group: Number(r[10]) || 0
  }));
  return out_({ state: st, rows: rows });
}
