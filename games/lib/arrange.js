// "رتّب الغرفة" puzzle logic (Tents-style). Shared by the web game and the print-kit builder.
// Board: R x C. tables: set of cells. Each table gets exactly one sofa orthogonally next to it;
// sofas never touch (not even diagonally); wall numbers give sofas per row and column.
(function (root) {
  function makeRng(seed) {
    let s = seed >>> 0 || 1;
    return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
  }
  const orth = (R, C, i) => {
    const r = Math.floor(i / C), c = i % C, o = [];
    if (r > 0) o.push(i - C); if (r < R - 1) o.push(i + C);
    if (c > 0) o.push(i - 1); if (c < C - 1) o.push(i + 1);
    return o;
  };
  const king = (R, C, i) => {
    const r = Math.floor(i / C), c = i % C, o = [];
    for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
      if (!dr && !dc) continue;
      const rr = r + dr, cc = c + dc;
      if (rr >= 0 && rr < R && cc >= 0 && cc < C) o.push(rr * C + cc);
    }
    return o;
  };

  // Count distinct sofa layouts (stops at `limit`).
  function countSolutions(R, C, tables, rows, cols, limit) {
    const T = [...tables];
    const isTable = new Set(T);
    // order tables by fewest options to prune early
    T.sort((a, b) => orth(R, C, a).filter((x) => !isTable.has(x)).length - orth(R, C, b).filter((x) => !isTable.has(x)).length);
    const sofa = new Set(), rowN = new Array(R).fill(0), colN = new Array(C).fill(0);
    const seen = new Set();
    let found = 0;
    (function go(k) {
      if (found >= limit) return;
      if (k === T.length) {
        if (rowN.every((v, r) => v === rows[r]) && colN.every((v, c) => v === cols[c])) {
          const key = [...sofa].sort((a, b) => a - b).join(",");
          if (!seen.has(key)) { seen.add(key); found++; }
        }
        return;
      }
      for (const x of orth(R, C, T[k])) {
        if (isTable.has(x) || sofa.has(x)) continue;
        const r = Math.floor(x / C), c = x % C;
        if (rowN[r] >= rows[r] || colN[c] >= cols[c]) continue;
        if (king(R, C, x).some((y) => sofa.has(y))) continue;
        sofa.add(x); rowN[r]++; colN[c]++;
        go(k + 1);
        sofa.delete(x); rowN[r]--; colN[c]--;
      }
    })(0);
    return found;
  }

  function generate(R, C, n, rng) {
    for (let attempt = 0; attempt < 5000; attempt++) {
      const sofas = [], tables = [], used = new Set(), pair = {};
      const cells = [...Array(R * C).keys()].sort(() => rng() - 0.5);
      for (const x of cells) {
        if (sofas.length === n) break;
        if (used.has(x) || king(R, C, x).some((y) => sofas.includes(y))) continue;
        const spots = orth(R, C, x).filter((y) => !used.has(y) && !sofas.includes(y));
        if (!spots.length) continue;
        const t = spots[Math.floor(rng() * spots.length)];
        sofas.push(x); tables.push(t); used.add(x); used.add(t); pair[t] = x;
      }
      if (sofas.length < n) continue;
      const rows = new Array(R).fill(0), cols = new Array(C).fill(0);
      sofas.forEach((x) => { rows[Math.floor(x / C)]++; cols[x % C]++; });
      if (countSolutions(R, C, tables, rows, cols, 2) === 1) return { R, C, tables, sofas, rows, cols, pair };
    }
    return null;
  }

  const api = { makeRng, orth, king, countSolutions, generate };
  if (typeof module !== "undefined") module.exports = api; else root.Arrange = api;
})(this);
