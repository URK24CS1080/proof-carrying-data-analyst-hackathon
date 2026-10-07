import { useState } from "react";
import { AlertTriangle, ChevronDown, Columns3, Copy, Rows3, ShieldCheck, Table2, TriangleAlert, type LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Dataset } from "@/lib/demo-data";
import { DemoTag, Panel, StatusBadge, useCountUp } from "./primitives";

function Stat({ label, value, icon: Icon, warn }: { label: string; value: number; icon: LucideIcon; warn?: boolean }) {
  const v = useCountUp(value);
  return (
    <div className="group rounded-xl border bg-gradient-to-br from-card to-muted/40 px-3 py-3 transition-all hover:-translate-y-0.5 hover:shadow-lift">
      <div className="flex items-center justify-between">
        <div className="eyebrow text-muted-foreground">{label}</div>
        <Icon className={cn("size-3.5", warn && value > 0 ? "text-warning" : "text-primary/60")} />
      </div>
      <div className={cn("mt-1 font-mono text-2xl font-semibold tabular", warn && value > 0 && "text-warning")}>
        {Math.round(v).toLocaleString("en-IN")}
      </div>
    </div>
  );
}

export function DatasetOverview({
  datasets,
  activeId,
  onSelect,
}: {
  datasets: Dataset[];
  activeId: string;
  onSelect: (id: string) => void;
}) {
  const [showCols, setShowCols] = useState(false);
  const d = datasets.find((x) => x.id === activeId) ?? datasets[0];

  if (!d) {
    return (
      <Panel title="Dataset Overview" icon={<Table2 className="size-3.5" />} delay={80}>
        <div className="rounded-md border border-dashed bg-muted/40 px-4 py-8 text-center">
          <p className="text-sm font-medium">No tabular dataset yet</p>
          <p className="mt-1 text-xs text-muted-foreground">Add a CSV file and its schema, quality score and preview appear here automatically.</p>
        </div>
      </Panel>
    );
  }

  return (
    <Panel
      title="Dataset Overview"
      description={`${d.name} — primary analysis table`}
      icon={<Table2 className="size-3.5" />}
      actions={d.demo ? <DemoTag /> : <StatusBadge tone="success">Live</StatusBadge>}
      delay={80}
    >
      {datasets.length > 1 && (
        <div className="mb-4 flex flex-wrap gap-1.5" role="tablist">
          {datasets.map((x) => (
            <button
              key={x.id}
              role="tab"
              aria-selected={x.id === d.id}
              onClick={() => onSelect(x.id)}
              className={cn(
                "rounded-full border px-3 py-1 font-mono text-xs transition-colors",
                x.id === d.id ? "border-primary bg-primary text-primary-foreground" : "bg-card text-muted-foreground hover:text-foreground",
              )}
            >
              {x.name}
            </button>
          ))}
        </div>
      )}

      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <Stat label="Rows" value={d.rows} icon={Rows3} />
        <Stat label="Columns" value={d.columns.length} icon={Columns3} />
        <Stat label="Missing" value={d.missing} icon={TriangleAlert} warn />
        <Stat label="Duplicates" value={d.duplicates} icon={Copy} warn />
      </div>

      <button
        type="button"
        onClick={() => setShowCols(!showCols)}
        aria-expanded={showCols}
        className="mt-4 flex w-full items-center justify-between rounded-md px-1 py-1 text-left text-xs font-medium text-muted-foreground hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        <span className="eyebrow">Column schema · {d.columns.length}</span>
        <ChevronDown className={cn("size-4 transition-transform", showCols && "rotate-180")} />
      </button>
      {showCols && (
        <div className="mt-2 max-h-72 overflow-auto rounded-lg border animate-in fade-in-0">
          <table className="w-full text-sm">
            <thead className="sticky top-0 bg-muted text-left">
              <tr>
                <th className="eyebrow px-3 py-2 text-muted-foreground">Column</th>
                <th className="eyebrow px-3 py-2 text-muted-foreground">Type</th>
                <th className="eyebrow px-3 py-2 text-right text-muted-foreground">Missing</th>
              </tr>
            </thead>
            <tbody>
              {d.columns.map((c) => (
                <tr key={c.name} className="border-t">
                  <td className="px-3 py-1.5 font-mono text-xs">{c.name}</td>
                  <td className="px-3 py-1.5">
                    <span className="rounded bg-accent px-1.5 py-0.5 font-mono text-[11px] text-accent-foreground">{c.type}</span>
                  </td>
                  <td className={cn("px-3 py-1.5 text-right font-mono text-xs tabular", c.missing ? "text-warning" : "text-muted-foreground")}>{c.missing}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="mt-4">
        <div className="eyebrow mb-2 px-1 text-muted-foreground">Data preview · first {d.preview.length} rows</div>
        <div className="overflow-x-auto rounded-lg border">
          <table className="w-full text-xs" style={{ minWidth: Math.max(480, d.columns.length * 105) }}>
            <thead className="bg-muted/70">
              <tr>
                {d.columns.map((c) => (
                  <th key={c.name} className="whitespace-nowrap px-3 py-2 text-left font-mono font-semibold text-muted-foreground">
                    {c.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {d.preview.map((r, ri) => (
                <tr key={ri} className="border-t transition-colors even:bg-muted/20 hover:bg-primary-soft/60">
                  {r.map((v, i) => {
                    const col = d.columns[i];
                    const numeric = col?.type === "int64" || col?.type === "float64";
                    return (
                      <td
                        key={i}
                        className={cn(
                          "whitespace-nowrap px-3 py-2",
                          numeric && "text-right font-mono tabular",
                          i === 0 && "font-mono text-muted-foreground",
                          v === "—" && "text-warning",
                        )}
                      >
                        {col?.name === "status" ? (
                          <StatusBadge
                            tone={v === "completed" ? "success" : v === "refunded" ? "destructive" : "warning"}
                            className="px-1.5 py-0 text-[10px] font-medium"
                          >
                            {v}
                          </StatusBadge>
                        ) : (
                          v
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Panel>
  );
}

function Gauge({ pct }: { pct: number }) {
  const r = 34;
  const c = 2 * Math.PI * r;
  const shown = useCountUp(pct, 1100);
  const tone = pct >= 98 ? "text-success" : pct >= 90 ? "text-warning" : "text-destructive";
  return (
    <div className="relative size-[88px] shrink-0">
      <svg viewBox="0 0 88 88" className="size-full -rotate-90">
        <circle cx="44" cy="44" r={r} fill="none" strokeWidth="8" className="stroke-muted" />
        <circle
          cx="44"
          cy="44"
          r={r}
          fill="none"
          strokeWidth="8"
          strokeLinecap="round"
          className={cn("stroke-current transition-colors", tone)}
          strokeDasharray={c}
          strokeDashoffset={c - (c * shown) / 100}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-lg font-semibold tabular leading-none">{shown.toFixed(1)}</span>
        <span className="text-[10px] text-muted-foreground">% complete</span>
      </div>
    </div>
  );
}

export function DataQuality({ dataset: d }: { dataset: Dataset | undefined }) {
  const [open, setOpen] = useState(false);
  if (!d) return null;
  const cells = Math.max(1, d.rows * d.columns.length);
  const completeness = Math.max(0, 100 - (d.missing / cells) * 100);
  const withGaps = d.columns.filter((c) => c.missing > 0);
  const grade = completeness >= 98 && d.duplicates <= 1 ? { tone: "success" as const, label: "Good", msg: "Minor gaps detected. Safe for most aggregate questions." }
    : completeness >= 90 ? { tone: "warning" as const, label: "Fair", msg: "Noticeable gaps. Check filters before trusting averages." }
    : { tone: "destructive" as const, label: "Poor", msg: "Significant gaps. Answers may be unreliable." };

  return (
    <Panel
      title="Data Quality"
      icon={<ShieldCheck className="size-3.5" />}
      actions={d.demo ? <DemoTag /> : <StatusBadge tone="success">Live</StatusBadge>}
      delay={160}
    >
      <div className="flex items-center gap-4">
        <Gauge pct={completeness} />
        <div className="min-w-0 flex-1">
          <StatusBadge tone={grade.tone}>{grade.label}</StatusBadge>
          <p className="mt-1.5 text-xs text-muted-foreground">{grade.msg}</p>
        </div>
      </div>

      <div className="mt-4 divide-y rounded-lg border">
        <div className="flex items-center gap-3 px-3 py-2.5 text-sm">
          <AlertTriangle className={cn("size-4", d.missing ? "text-warning" : "text-success")} />
          <span className="flex-1">Missing values</span>
          <span className="font-mono text-xs tabular text-muted-foreground">
            {d.missing} cells · {withGaps.length} columns
          </span>
        </div>
        <div className="flex items-center gap-3 px-3 py-2.5 text-sm">
          <Copy className={cn("size-4", d.duplicates ? "text-warning" : "text-success")} />
          <span className="flex-1">Duplicate rows</span>
          <span className="font-mono text-xs tabular text-muted-foreground">{d.duplicates} rows</span>
        </div>
      </div>

      {withGaps.length > 0 && (
        <>
          <button
            type="button"
            onClick={() => setOpen(!open)}
            aria-expanded={open}
            className="mt-3 flex items-center gap-1 text-xs font-medium text-primary hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            {open ? "Hide" : "Show"} column details
            <ChevronDown className={cn("size-3.5 transition-transform", open && "rotate-180")} />
          </button>
          {open && (
            <ul className="mt-2 space-y-2 animate-in fade-in-0">
              {withGaps.map((c) => (
                <li key={c.name} className="flex items-center gap-3 text-xs">
                  <span className="w-28 truncate font-mono">{c.name}</span>
                  <div className="h-1.5 flex-1 rounded-full bg-muted">
                    <div className="h-full rounded-full bg-warning transition-all duration-700" style={{ width: `${(c.missing / Math.max(1, d.missing)) * 100}%` }} />
                  </div>
                  <span className="w-28 text-right font-mono tabular text-muted-foreground">
                    {c.missing} · {((c.missing / Math.max(1, d.rows)) * 100).toFixed(2)}%
                  </span>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </Panel>
  );
}
