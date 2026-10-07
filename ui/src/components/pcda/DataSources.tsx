import { useRef, useState, type Dispatch, type SetStateAction } from "react";
import { FileSpreadsheet, FileText, FileType, Upload, X, Database, RotateCcw, CheckCircle2, Loader2, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";
import { buildDataset } from "@/lib/csv";
import { DEMO_FILES, formatSize, type SourceFile } from "@/lib/demo-data";
import { DemoTag, IconButton, Panel } from "./primitives";

const FORMATS = ["CSV", "XLS", "XLSX", "PDF", "TXT"];
const MAX_PARSE_BYTES = 8_000_000;

const TYPE_STYLE: Record<string, string> = {
  CSV: "bg-success-soft text-success",
  XLS: "bg-info-soft text-info",
  XLSX: "bg-info-soft text-info",
  PDF: "bg-destructive-soft text-destructive",
  TXT: "bg-muted text-muted-foreground",
};

function iconFor(type: string) {
  if (type === "PDF" || type === "TXT") return FileText;
  if (type === "CSV" || type === "XLS" || type === "XLSX") return FileSpreadsheet;
  return FileType;
}

export function SourceCard({ file, onRemove }: { file: SourceFile; onRemove: () => void }) {
  const Icon = iconFor(file.type);
  const state = file.state ?? "ready";
  return (
    <li className="animate-rise group flex items-center gap-3 rounded-lg border bg-card px-3 py-2.5 transition-all hover:-translate-y-px hover:border-primary/30 hover:shadow-card">
      <div className={cn("flex size-9 shrink-0 items-center justify-center rounded-lg", TYPE_STYLE[file.type] ?? "bg-primary-soft text-primary")}>
        <Icon className="size-4" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <span className="truncate font-mono text-sm font-medium">{file.name}</span>
          {file.demo && <DemoTag />}
        </div>
        <div className="mt-0.5 flex flex-wrap items-center gap-x-2 text-xs text-muted-foreground">
          <span className="font-mono">{file.type}</span>
          <span>·</span>
          <span className="tabular">{formatSize(file.size)}</span>
          {file.dataset && (
            <>
              <span>·</span>
              <span className="tabular">{file.dataset.rows.toLocaleString("en-IN")} rows</span>
            </>
          )}
          <span>·</span>
          {state === "parsing" && (
            <span className="inline-flex items-center gap-1 text-info">
              <Loader2 className="size-3 animate-spin" /> Profiling…
            </span>
          )}
          {state === "error" && (
            <span className="inline-flex items-center gap-1 text-warning">
              <AlertTriangle className="size-3" /> Preview unavailable
            </span>
          )}
          {state === "ready" && (
            <span className="inline-flex items-center gap-1 text-success">
              <CheckCircle2 className="size-3" /> Ready
            </span>
          )}
        </div>
      </div>
      <button
        type="button"
        onClick={onRemove}
        aria-label={`Remove ${file.name}`}
        className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-destructive-soft hover:text-destructive focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        <X className="size-4" />
      </button>
    </li>
  );
}

export function DataSources({ files, setFiles }: { files: SourceFile[]; setFiles: Dispatch<SetStateAction<SourceFile[]>> }) {
  const [drag, setDrag] = useState(false);
  const input = useRef<HTMLInputElement>(null);

  const patch = (id: string, p: Partial<SourceFile>) => setFiles((prev) => prev.map((f) => (f.id === id ? { ...f, ...p } : f)));

  const add = (list: FileList | null) => {
    if (!list) return;
    const picked = Array.from(list);
    const next: SourceFile[] = picked.map((f) => {
      const type = (f.name.split(".").pop() || "file").toUpperCase();
      return { id: crypto.randomUUID(), name: f.name, size: f.size, type, state: type === "CSV" ? "parsing" : "ready" };
    });
    setFiles((prev) => [...prev, ...next]);

    // Automation: profile every CSV the moment it lands.
    next.forEach((nf, i) => {
      const raw = picked[i];
      if (nf.type !== "CSV" || !raw) return;
      if (raw.size > MAX_PARSE_BYTES) return patch(nf.id, { state: "error" });
      raw
        .text()
        .then((t) => patch(nf.id, { state: "ready", dataset: buildDataset(nf.id, nf.name, t) }))
        .catch(() => patch(nf.id, { state: "error" }));
    });
  };

  const totalSize = files.reduce((a, f) => a + f.size, 0);

  return (
    <Panel
      title="Data Sources"
      description="Upload the files you want the analyst to work with."
      icon={<Database className="size-3.5" />}
      delay={0}
      actions={
        <IconButton onClick={() => setFiles(DEMO_FILES)} title="Restore demo files">
          <RotateCcw className="size-3.5" /> Demo files
        </IconButton>
      }
    >
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDrag(true);
        }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDrag(false);
          add(e.dataTransfer.files);
        }}
        className={cn(
          "flex flex-col items-center rounded-xl border-2 border-dashed px-4 py-6 text-center transition-all",
          drag ? "scale-[1.01] border-primary bg-primary-soft" : "border-input bg-gradient-to-b from-muted/60 to-muted/20",
        )}
      >
        <div className={cn("flex size-11 items-center justify-center rounded-full border bg-card shadow-card transition-transform", drag && "scale-110 text-primary")}>
          <Upload className="size-4" />
        </div>
        <p className="mt-3 text-sm font-medium">{drag ? "Release to add files" : "Drag & drop files here"}</p>
        <p className="text-xs text-muted-foreground">or select multiple files from your computer</p>
        <button
          type="button"
          onClick={() => input.current?.click()}
          className="mt-3 rounded-md bg-foreground px-3.5 py-1.5 text-xs font-medium text-background transition-opacity hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          Browse Files
        </button>
        <input
          ref={input}
          type="file"
          multiple
          accept=".csv,.xls,.xlsx,.pdf,.txt"
          className="hidden"
          onChange={(e) => {
            add(e.target.files);
            e.target.value = "";
          }}
        />
        <div className="mt-3 flex flex-wrap justify-center gap-1">
          {FORMATS.map((f) => (
            <span key={f} className="rounded border bg-card px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
              {f}
            </span>
          ))}
        </div>
      </div>

      {files.length > 0 ? (
        <>
          <div className="mt-4 flex items-center justify-between px-1 text-[11px] text-muted-foreground">
            <span className="eyebrow">{files.length} sources</span>
            <span className="tabular font-mono">{formatSize(totalSize)} total</span>
          </div>
          <ul className="mt-2 space-y-2">
            {files.map((f) => (
              <SourceCard key={f.id} file={f} onRemove={() => setFiles((prev) => prev.filter((x) => x.id !== f.id))} />
            ))}
          </ul>
        </>
      ) : (
        <div className="mt-4 rounded-md border bg-muted/40 px-4 py-5 text-center">
          <p className="text-sm font-medium">No sources attached</p>
          <p className="mt-1 text-xs text-muted-foreground">Add files above, or restore the demo files to continue the walkthrough.</p>
        </div>
      )}
      <p className="mt-3 text-[11px] text-muted-foreground">Files stay in your browser. CSVs are profiled locally the moment you add them.</p>
    </Panel>
  );
}
