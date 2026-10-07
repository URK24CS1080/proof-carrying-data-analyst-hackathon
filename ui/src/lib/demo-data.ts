// All values in this file are illustrative demo content.
// Replace with real backend responses when integrating.

export type ResultStatus =
  | "VERIFIED"
  | "CANNOT_DETERMINE"
  | "CLARIFICATION_REQUIRED"
  | "EXECUTION_ERROR"
  | "VERIFICATION_FAILED";

export const STATUSES: ResultStatus[] = [
  "VERIFIED",
  "CANNOT_DETERMINE",
  "CLARIFICATION_REQUIRED",
  "EXECUTION_ERROR",
  "VERIFICATION_FAILED",
];

export type Dataset = {
  id: string;
  name: string;
  rows: number;
  columns: { name: string; type: string; missing: number }[];
  missing: number;
  duplicates: number;
  preview: string[][];
  demo?: boolean;
};

export type SourceFile = {
  id: string;
  name: string;
  size: number;
  type: string;
  demo?: boolean;
  state?: "parsing" | "ready" | "error" | undefined;
  dataset?: Dataset | undefined;
};

export const DEMO_FILES: SourceFile[] = [
  { id: "d1", name: "sales.csv", size: 184_320, type: "CSV", demo: true },
  { id: "d2", name: "customers.xlsx", size: 92_160, type: "XLSX", demo: true },
  { id: "d3", name: "annual_report.pdf", size: 2_411_724, type: "PDF", demo: true },
];

export const OVERVIEW = { rows: 1248, columns: 8, missing: 5, duplicates: 1 };

export const COLUMNS = [
  { name: "transaction_id", type: "string", missing: 0 },
  { name: "customer", type: "string", missing: 0 },
  { name: "category", type: "category", missing: 0 },
  { name: "amount", type: "float64", missing: 2 },
  { name: "date", type: "datetime", missing: 0 },
  { name: "city", type: "string", missing: 3 },
  { name: "status", type: "category", missing: 0 },
  { name: "rating", type: "int64", missing: 0 },
];

export const PREVIEW_ROWS = [
  ["TX-10421", "Ananya Rao", "Electronics", "48,999.00", "2026-01-04", "Bengaluru", "completed", "5"],
  ["TX-10422", "Rohit Mehta", "Furniture", "12,450.50", "2026-01-04", "Pune", "completed", "4"],
  ["TX-10423", "Priya Nair", "Electronics", "39,120.00", "2026-01-05", "Kochi", "refunded", "3"],
  ["TX-10424", "Karan Shah", "Apparel", "2,349.00", "2026-01-06", "—", "completed", "4"],
  ["TX-10425", "Meera Iyer", "Electronics", "51,780.25", "2026-01-07", "Chennai", "pending", "5"],
];

export const DEMO_DATASET: Dataset = {
  id: "demo",
  name: "sales.csv",
  rows: OVERVIEW.rows,
  columns: COLUMNS,
  missing: OVERVIEW.missing,
  duplicates: OVERVIEW.duplicates,
  preview: PREVIEW_ROWS,
  demo: true,
};

export type HistoryItem = { id: string; question: string; status: ResultStatus; at: number; source: string };

export const EXAMPLE_QUESTIONS = [
  "What was the average sales amount for Electronics?",
  "How many transactions were completed?",
  "Which category had the highest average amount?",
  "What was the total revenue in January?",
  "Can this question be answered reliably?",
];

export const PROOF_CODE = `result = df[df["category"] == "Electronics"]["amount"].mean()
print(result)`;

export const EVIDENCE = [
  { label: "Source file", value: "sales.csv" },
  { label: "Operation", value: "AVERAGE" },
  { label: "Filter", value: 'category = "Electronics"' },
  { label: "Selected column", value: "amount" },
  { label: "Rows analyzed", value: "120" },
];

export const DEMO_QUESTION = "What was the average sales amount for Electronics?";
export const DEMO_ANSWER = "₹45,250.75";

export const PIPELINE = [
  { n: "01", title: "Planning", desc: "AI proposes an analytical plan." },
  { n: "02", title: "Validation", desc: "The proposed plan is checked." },
  { n: "03", title: "Local execution", desc: "The approved operation is performed locally." },
  { n: "04", title: "Verification", desc: "The result is checked against the proof." },
];

export function formatSize(b: number) {
  if (b < 1024) return `${b} B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(1)} KB`;
  return `${(b / 1024 / 1024).toFixed(1)} MB`;
}
