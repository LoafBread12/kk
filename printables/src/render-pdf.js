// Usage: NODE_PATH=<dir with playwright> node render-pdf.js ../dark-room-puzzle.html ../dark-room-puzzle.pdf
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const [src, out] = process.argv.slice(2).map(p => path.resolve(p));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + src, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  await browser.close();
})();
