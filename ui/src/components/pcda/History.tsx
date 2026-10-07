import { History as HistoryIcon, RotateCcw, Trash2 } from "lucide-react";
import type { HistoryItem } from "@/lib/demo-data";
import { Panel, StatusBadge } from "./primitives";

const TONE = {
  VERIFIED: "success",
  CANNOT_DETERMINE: "warning",
  CLARIFICATION_REQUIRED: "info",
  EXECUTION_ERROR: "destructive",
  VERIFICATION_FAILED: "destructive",
} as const;

export function HistoryBoard({ items, onReplay, onClear }: { items: HistoryItem[]; onReplay: (h: HistoryItem) => void; onClear: () => void }) {
  return (
    <Panel
      title="Recent Analyses"
      description="Every run is logged automatically. Click one to replay it."
      icon={<HistoryIcon className="size-3.5" />}
      delay={240}
      actions={
        items.length > 0 ? (
          <button type="button" onClick={onClear} className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-destructive">
            <Trash2 className="size-3.5" /> Clear
          </button>
        ) : undefined
      }
    >
      {items.length === 0 ? (
        <p className="rounded-md border border-dashed bg-muted/40 px-4 py-5 text-center text-xs text-muted-foreground">No analyses yet — run one and it will appear here.</p>
      ) : (
        <ul className="space-y-2">
          {items.map((h) => (
            <li key={h.id} className="animate-rise">
              <button
                type="button"
                onClick={() => onReplay(h)}
                className="group flex w-full items-center gap-3 rounded-lg border bg-card px-3 py-2 text-left transition-all hover:-translate-y-px hover:border-primary/30 hover:shadow-card"
              >
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium">{h.question}</p>
                  <p className="mt-0.5 font-mono text-[11px] text-muted-foreground">
                    {h.source} · {new Date(h.at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </p>
                </div>
                <StatusBadge tone={TONE[h.status]} className="text-[10px]">
                  {h.status}
                </StatusBadge>
                <RotateCcw className="size-3.5 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
              </button>
            </li>
          ))}
        </ul>
      )}
    </Panel>
  );
}
