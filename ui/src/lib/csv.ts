import type { Dataset } from "./demo-data";

const MISSING = new Set(["", "—", "-", "na", "n/a", "null", "nan", "none"]);

/** Minimal RFC-4180 style CSV parser (handles quotes, escaped quotes, CRLF). */
export function parseCSV(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let inQ = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQ) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          cell += '"';
          i++;
        } else inQ = false;
      } else cell += c;
    } else if (c === '"') inQ = true;
    else if (c === ",") {
      row.push(cell);
      cell = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(cell);
      cell = "";
      if (row.some((v) => v.trim() !== "")) rows.push(row);
      row = [];
    } else cell += c;
  }
  row.push(cell);
  if (row.some((v) => v.trim() !== "")) rows.push(row);
  return rows;
}

const isMissing = (v: string | undefined) => v === undefined || MISSING.has(v.trim().toLowerCase());

function inferType(values: string[], totalRows: number): string {
  const filled = values.filter((v) => !isMissing(v));
  if (filled.length === 0) return "string";
  const nums = filled.map((v) => Number(v.replace(/[,₹$€\s]/g, "")));
  if (nums.every((n) => !Number.isNaN(n))) return nums.every(Number.isInteger) ? "int64" : "float64";
  if (filled.every((v) => /^\d{4}-\d{2}-\d{2}/.test(v) || /^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$/.test(v))) return "datetime";
  const unique = new Set(filled).size;
  if (totalRows > 20 && unique <= 12) return "category";
  return "string";
}

export function buildDataset(id: string, name: string, text: string): Dataset {
  const all = parseCSV(text);
  const header = (all[0] ?? []).map((h) => h.trim());
  const body = all.slice(1);
  const columns = header.map((h, ci) => {
    const col = body.map((r) => r[ci] ?? "");
    return { name: h || `column_${ci + 1}`, type: inferType(col, body.length), missing: col.filter(isMissing).length };
  });
  const seen = new Set<string>();
  let duplicates = 0;
  for (const r of body) {
    const k = r.join("\u0001");
    if (seen.has(k)) duplicates++;
    else seen.add(k);
  }
  return {
    id,
    name,
    rows: body.length,
    columns,
    missing: columns.reduce((a, c) => a + c.missing, 0),
    duplicates,
    preview: body.slice(0, 5).map((r) => header.map((_, i) => (isMissing(r[i]) ? "—" : (r[i] ?? "").trim()))),
  };
}
