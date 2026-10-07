import { useState } from "react";
import {
  AlertOctagon,
  AlertTriangle,
  Check,
  CheckCircle2,
  ChevronDown,
  CircleSlash,
  Code2,
  Copy,
  FileSearch,
  FlaskConical,
  HelpCircle,
  MinusCircle,
  RotateCcw,
  ShieldAlert,
  ShieldCheck,
  XCircle,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { DEMO_ANSWER, EVIDENCE, PROOF_CODE, STATUSES, type ResultStatus } from "@/lib/demo-data";
import { DemoTag, IconButton, Panel, StatusBadge } from "./primitives";

const META: Record<ResultStatus, { tone: "success" | "warning" | "info" | "destructive"; icon: LucideIcon; label: string }> = {
  VERIFIED: { tone: "success", icon: ShieldCheck, label: "Verified" },
  CANNOT_DETERMINE: { tone: "warning", icon: HelpCircle, label: "Cannot determine" },
  CLARIFICATION_REQUIRED: { tone: "info", icon: AlertTriangle, label: "Clarification required" },
  EXECUTION_ERROR: { tone: "destructive", icon: XCircle, label: "Execution error" },
  VERIFICATION_FAILED: { tone: "destructive", icon: ShieldAlert, label: "Verification failed" },
};

export function DemoStatusSelector({ status, onChange }: { status: ResultStatus; onChange: (s: ResultStatus) => void }) {
  return (
    <div className="rounded-lg border border-dashed border-warning/50 bg-warning-soft/60 p-3">
      <div className="mb-2 flex items-center gap-2">
        <FlaskConical className="size-3.5 text-warning" />
        <span className="eyebrow text-warning">Demo scenario</span>
        <span className="text-[11px] text-muted-foreground">Switch outcomes for presentation</span>
      </div>
      <div role="radiogroup" className="flex flex-wrap gap-1.5">
        {STATUSES.map((s) => {
          const m = META[s];
          const Icon = m.icon;
          return (
            <button
              key={s}
              role="radio"
              aria-checked={status === s}
              type="button"
              onClick={() => onChange(s)}
              className={cn(
                "inline-flex items-center gap-1.5 rounded-md border px-2 py-1 font-mono text-[11px] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                status === s ? "border-foreground bg-foreground text-background" : "bg-card text-muted-foreground hover:text-foreground",
              )}
            >
              <Icon className="size-3" /> {s}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function ResultPanel({
  status,
  question,
  loading,
  onRetry,
  onClarify,
}: {
  status: ResultStatus;
  question: string;
  loading: boolean;
  onRetry: () => void;
  onClarify: (q: string) => void;
}) {
  const m = META[status];
  const Icon = m.icon;
  const [clar, setClar] = useState("January 2026 (01 Jan – 31 Jan)");
  const ring = {
    success: "border-l-success",
    warning: "border-l-warning",
    info: "border-l-info",
    destructive: "border-l-destructive",
  }[m.tone];

  return (
    <Panel title="Result" icon={<FileSearch className="size-3.5" />} actions={<DemoTag />} delay={200} className={cn("border-l-4 transition-colors", ring)}>
      {loading ? (
        <div className="space-y-3">
          <div className="h-4 w-32 animate-pulse rounded bg-muted" />
          <div className="h-10 w-64 animate-pulse rounded bg-muted" />
          <div className="h-3 w-full animate-pulse rounded bg-muted" />
          <p className="text-xs text-muted-foreground">Running simulated pipeline…</p>
        </div>
      ) : (
        <div key={status} className="animate-in fade-in-0 slide-in-from-bottom-1 duration-300">
          <div className="flex flex-wrap items-center gap-2">
            <StatusBadge tone={m.tone} className="py-1 text-sm">
              <Icon className="size-4" /> {status}
            </StatusBadge>
            <span className="font-mono text-[11px] text-muted-foreground">— DEMO</span>
          </div>

          <dl className="mt-4 grid gap-1 border-y py-3 text-sm sm:grid-cols-[110px_1fr]">
            <dt className="eyebrow pt-0.5 text-muted-foreground">Question</dt>
            <dd className="font-medium">{question || "—"}</dd>
          </dl>

          {status === "VERIFIED" && (
            <div className="mt-5 rounded-xl border border-success/25 bg-gradient-to-br from-success-soft/70 via-card to-primary-soft/50 p-5">
              <div className="eyebrow text-muted-foreground">Answer</div>
              <div className="mt-1 font-mono text-4xl font-semibold tracking-tight tabular text-brand sm:text-5xl">{DEMO_ANSWER}</div>
              <p className="mt-2 text-sm text-muted-foreground">
                Mean of <code className="font-mono text-foreground">amount</code> across 120 Electronics rows. Answer matches the proof output.
              </p>
            </div>
          )}

          {status === "CANNOT_DETERMINE" && (
            <div className="mt-5 flex gap-3 rounded-md bg-warning-soft p-4">
              <MinusCircle className="mt-0.5 size-5 shrink-0 text-warning" />
              <div>
                <p className="font-medium">No answer is shown.</p>
                <p className="mt-1 text-sm text-muted-foreground">The available data is insufficient to establish a reliable answer.</p>
              </div>
            </div>
          )}

          {status === "CLARIFICATION_REQUIRED" && (
            <div className="mt-5 rounded-md bg-info-soft p-4">
              <p className="text-sm">The requested date range is ambiguous. Please clarify which period should be analyzed.</p>
              <div className="mt-3 flex flex-col gap-2 sm:flex-row">
                <input
                  value={clar}
                  onChange={(e) => setClar(e.target.value)}
                  className="h-9 flex-1 rounded-md border border-input bg-card px-3 text-sm focus-visible:border-info focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-info/30"
                />
                <button
                  type="button"
                  onClick={() => onClarify(`${question.replace(/\?$/, "")} — period: ${clar}?`)}
                  disabled={!clar.trim()}
                  className="h-9 rounded-md bg-info px-4 text-sm font-medium text-primary-foreground hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
                >
                  Update question
                </button>
              </div>
            </div>
          )}

          {status === "EXECUTION_ERROR" && (
            <div className="mt-5 flex flex-col gap-3 rounded-md bg-destructive-soft p-4 sm:flex-row sm:items-center">
              <XCircle className="size-5 shrink-0 text-destructive" />
              <p className="flex-1 text-sm">The demonstration analysis could not be completed.</p>
              <IconButton onClick={onRetry}>
                <RotateCcw className="size-3.5" /> Retry
              </IconButton>
            </div>
          )}

          {status === "VERIFICATION_FAILED" && (
            <div className="mt-5 rounded-md border-2 border-destructive bg-destructive-soft p-4">
              <div className="flex items-center gap-2 text-destructive">
                <AlertOctagon className="size-5" />
                <p className="font-semibold">The answer has NOT been verified.</p>
              </div>
              <div className="mt-4 grid gap-2 sm:grid-cols-2">
                <div className="rounded-md border bg-card p-3">
                  <div className="eyebrow text-muted-foreground">Claimed result</div>
                  <div className="mt-1 font-mono text-xl font-semibold tabular line-through decoration-destructive/60">₹48,900.00</div>
                </div>
                <div className="rounded-md border bg-card p-3">
                  <div className="eyebrow text-muted-foreground">Proof result</div>
                  <div className="mt-1 font-mono text-xl font-semibold tabular">₹45,250.75</div>
                </div>
              </div>
              <p className="mt-3 text-xs text-muted-foreground">Illustrative values. Do not rely on the claimed answer.</p>
            </div>
          )}
        </div>
      )}
    </Panel>
  );
}

function Row({ label, value, state }: { label: string; value: string; state: "ok" | "fail" | "na" }) {
  const I = state === "ok" ? CheckCircle2 : state === "fail" ? XCircle : CircleSlash;
  return (
    <div className="flex items-center gap-3 py-2.5">
      <I className={cn("size-4", state === "ok" ? "text-success" : state === "fail" ? "text-destructive" : "text-muted-foreground")} />
      <span className="flex-1 text-sm">{label}</span>
      <span className={cn("text-sm font-medium", state === "ok" ? "text-success" : state === "fail" ? "text-destructive" : "text-muted-foreground")}>
        {value}
        <span className="ml-1 font-mono text-[10px] font-normal text-muted-foreground">— Demo</span>
      </span>
    </div>
  );
}

export function VerificationPanel({ status, loading }: { status: ResultStatus; loading: boolean }) {
  let rows: { label: string; value: string; state: "ok" | "fail" | "na" }[];
  let head: { tone: "success" | "destructive" | "neutral"; text: string };
  if (status === "VERIFIED") {
    head = { tone: "success", text: "Passed" };
    rows = [
      { label: "Proof execution", value: "Successful", state: "ok" },
      { label: "Verification result", value: "Passed", state: "ok" },
      { label: "Result match", value: "Confirmed", state: "ok" },
    ];
  } else if (status === "VERIFICATION_FAILED") {
    head = { tone: "destructive", text: "Failed" };
    rows = [
      { label: "Proof execution", value: "Successful", state: "ok" },
      { label: "Verification result", value: "Failed", state: "fail" },
      { label: "Result match", value: "Mismatch", state: "fail" },
    ];
  } else {
    head = { tone: "neutral", text: "Unavailable" };
    rows = [
      { label: "Proof execution", value: status === "EXECUTION_ERROR" ? "Failed" : "Not run", state: status === "EXECUTION_ERROR" ? "fail" : "na" },
      { label: "Verification result", value: "Unavailable", state: "na" },
      { label: "Result match", value: "Unavailable", state: "na" },
    ];
  }
  const shell =
    head.tone === "success" ? "bg-success-soft/50 border-success/30" : head.tone === "destructive" ? "bg-destructive-soft border-destructive/50 border-2" : "";
  return (
    <Panel
      title="Verification"
      icon={<ShieldCheck className="size-3.5" />}
      className={cn("transition-colors", !loading && shell)}
      actions={
        loading ? (
          <StatusBadge tone="neutral">Pending</StatusBadge>
        ) : (
          <StatusBadge tone={head.tone}>{head.text}</StatusBadge>
        )
      }
    >
      {loading ? (
        <p className="text-sm text-muted-foreground">Awaiting simulated proof execution…</p>
      ) : (
        <>
          <div className="divide-y">{rows.map((r) => <Row key={r.label} {...r} />)}</div>
          <p className="mt-3 text-[11px] text-muted-foreground">
            Illustrative status only. No real proof was executed or verified in this frontend demo.
          </p>
        </>
      )}
    </Panel>
  );
}

function highlight(line: string) {
  const tokens = line.split(/("[^"]*"|\b(?:print|mean)\b|==|\bdf\b|\bresult\b)/g);
  return tokens.map((t, i) => {
    if (!t) return null;
    let cls = "";
    if (t.startsWith('"')) cls = "text-syn-str";
    else if (t === "print" || t === "mean") cls = "text-syn-fn";
    else if (t === "==") cls = "text-syn-op";
    else if (t === "df" || t === "result") cls = "text-syn-key";
    return (
      <span key={i} className={cls}>
        {t}
      </span>
    );
  });
}

export function ProofViewer({ status }: { status: ResultStatus }) {
  const [open, setOpen] = useState(true);
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(PROOF_CODE);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard unavailable */
    }
  };
  const unavailable = status === "CANNOT_DETERMINE" || status === "CLARIFICATION_REQUIRED";
  return (
    <Panel
      title="Executable Proof"
      icon={<Code2 className="size-3.5" />}
      actions={
        <>
          <DemoTag />
          <IconButton onClick={() => setOpen(!open)} aria-expanded={open} aria-label={open ? "Collapse proof" : "Expand proof"}>
            <ChevronDown className={cn("size-3.5 transition-transform", open && "rotate-180")} />
          </IconButton>
        </>
      }
    >
      {open &&
        (unavailable ? (
          <div className="rounded-md border border-dashed bg-muted/40 px-4 py-6 text-center">
            <p className="text-sm font-medium">No proof generated</p>
            <p className="mt-1 text-xs text-muted-foreground">A proof is only produced once the question can be answered.</p>
          </div>
        ) : (
          <div className="overflow-hidden rounded-md bg-code">
            <div className="flex items-center justify-between border-b border-code-muted/30 px-3 py-2">
              <div className="flex items-center gap-2">
                <span className="flex gap-1">
                  <span className="size-2 rounded-full bg-code-muted/50" />
                  <span className="size-2 rounded-full bg-code-muted/50" />
                  <span className="size-2 rounded-full bg-code-muted/50" />
                </span>
                <span className="font-mono text-[11px] text-code-muted">proof.py · Python · display only</span>
              </div>
              <button
                type="button"
                onClick={copy}
                className="inline-flex items-center gap-1.5 rounded px-2 py-1 font-mono text-[11px] text-code-foreground transition-colors hover:bg-code-muted/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-40"
              >
                {copied ? <Check className="size-3" /> : <Copy className="size-3" />}
                {copied ? "Copied" : "Copy code"}
              </button>
            </div>
            <pre className="overflow-x-auto py-3 font-mono text-[13px] leading-6 text-code-foreground">
              {PROOF_CODE.split("\n").map((l, i) => (
                <div key={i} className="flex">
                  <span className="w-10 shrink-0 select-none pr-3 text-right text-code-muted">{i + 1}</span>
                  <code className="pr-4">{highlight(l)}</code>
                </div>
              ))}
            </pre>
          </div>
        ))}
      {!open && <p className="text-xs text-muted-foreground">Proof collapsed · 2 lines of Python</p>}
    </Panel>
  );
}

export function EvidencePanel({ status }: { status: ResultStatus }) {
  const [open, setOpen] = useState(true);
  const unavailable = status === "CANNOT_DETERMINE" || status === "CLARIFICATION_REQUIRED";
  return (
    <Panel
      title="Evidence"
      description="Explore the information associated with the displayed analysis."
      icon={<FileSearch className="size-3.5" />}
      actions={
        <>
          <DemoTag />
          <IconButton onClick={() => setOpen(!open)} aria-expanded={open} aria-label={open ? "Collapse evidence" : "Expand evidence"}>
            <ChevronDown className={cn("size-3.5 transition-transform", open && "rotate-180")} />
          </IconButton>
        </>
      }
    >
      {open ? (
        unavailable ? (
          <p className="text-sm text-muted-foreground">No evidence is associated with an unanswered question.</p>
        ) : (
          <dl className="divide-y rounded-md border">
            {EVIDENCE.map((e) => (
              <div key={e.label} className="grid grid-cols-[130px_1fr] items-center gap-3 px-3 py-2.5">
                <dt className="eyebrow text-muted-foreground">{e.label}</dt>
                <dd className="font-mono text-sm">{e.value}</dd>
              </div>
            ))}
          </dl>
        )
      ) : (
        <p className="text-xs text-muted-foreground">Evidence collapsed · {EVIDENCE.length} fields</p>
      )}
    </Panel>
  );
}
