import { ArrowRight, Check, Cpu, Lightbulb, Loader2, MessageSquareText, ScanSearch, ShieldCheck, Workflow } from "lucide-react";
import { cn } from "@/lib/utils";
import { EXAMPLE_QUESTIONS, PIPELINE } from "@/lib/demo-data";
import { DemoTag, Panel } from "./primitives";

export function QuestionInput({
  question,
  setQuestion,
  onAnalyze,
  onPick,
  autoRun,
  setAutoRun,
  loading,
  disabledReason,
}: {
  question: string;
  setQuestion: (q: string) => void;
  onAnalyze: () => void;
  onPick: (q: string) => void;
  autoRun: boolean;
  setAutoRun: (v: boolean) => void;
  loading: boolean;
  disabledReason?: string | undefined;
}) {
  const disabled = loading || !question.trim() || !!disabledReason;
  return (
    <Panel
      title="Ask Your Data"
      description="Ask a question about the uploaded sources."
      icon={<MessageSquareText className="size-3.5" />}
      className="border-primary/25 ring-4 ring-primary-soft"
      delay={40}
    >
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && !disabled) onAnalyze();
        }}
        rows={3}
        placeholder="Ask a question about your data..."
        className="w-full resize-none rounded-md border border-input bg-background px-4 py-3 text-base leading-relaxed placeholder:text-muted-foreground/70 focus-visible:border-primary focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-primary-soft"
      />
      <div className="mt-3 flex flex-wrap gap-2">
        {EXAMPLE_QUESTIONS.map((q) => (
          <button
            key={q}
            type="button"
            onClick={() => onPick(q)}
            className={cn(
              "rounded-md border px-2.5 py-1.5 text-left text-xs transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
              question === q
                ? "border-primary/40 bg-primary-soft text-primary"
                : "bg-card text-muted-foreground hover:border-primary/30 hover:text-foreground",
            )}
          >
            {q}
          </button>
        ))}
      </div>
      <label className="mt-3 inline-flex cursor-pointer items-center gap-2 text-xs text-muted-foreground">
        <button
          type="button"
          role="switch"
          aria-checked={autoRun}
          onClick={() => setAutoRun(!autoRun)}
          className={cn("relative h-5 w-9 rounded-full transition-colors", autoRun ? "bg-primary" : "bg-input")}
        >
          <span className={cn("absolute top-0.5 left-0.5 size-4 rounded-full bg-card shadow transition-transform", autoRun && "translate-x-4")} />
        </button>
        <span>
          <span className="font-medium text-foreground">Auto-analyze</span> when I pick an example or change the data source
        </span>
      </label>
      <div className="mt-4 flex flex-col-reverse items-stretch justify-between gap-3 sm:flex-row sm:items-center">
        <p className="text-xs text-muted-foreground">
          {disabledReason ?? (
            <>
              Press <kbd className="rounded border bg-muted px-1 font-mono text-[10px]">⌘ Enter</kbd> to analyze · results are simulated
            </>
          )}
        </p>
        <button
          type="button"
          onClick={onAnalyze}
          disabled={disabled}
          className="inline-flex h-11 items-center justify-center gap-2 rounded-lg bg-brand px-6 text-sm font-semibold text-primary-foreground shadow-glow transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 active:translate-y-px disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-none"
        >
          {loading ? (
            <>
              <Loader2 className="size-4 animate-spin" /> Analyzing…
            </>
          ) : (
            <>
              Analyze <ArrowRight className="size-4" />
            </>
          )}
        </button>
      </div>
    </Panel>
  );
}

const ICONS = [Lightbulb, ScanSearch, Cpu, ShieldCheck];

/** stage: -1 idle, 0..3 running stage index, 4 complete */
export function Pipeline({ stage, failedAt }: { stage: number; failedAt?: number | undefined }) {
  return (
    <Panel title="Analysis Pipeline" icon={<Workflow className="size-3.5" />} actions={<DemoTag />} delay={120}>
      <div className="mb-4 h-1 overflow-hidden rounded-full bg-muted">
        <div
          className={cn("h-full rounded-full transition-all duration-500", failedAt !== undefined && stage >= 4 ? "bg-destructive" : "bg-brand")}
          style={{ width: `${stage >= 4 ? 100 : Math.max(0, ((stage + 0.5) / 4) * 100)}%` }}
        />
      </div>
      <ol className="grid gap-3 sm:grid-cols-4 sm:gap-0">
        {PIPELINE.map((p, i) => {
          const Icon = ICONS[i] ?? Lightbulb;
          const failed = failedAt === i && stage >= 4;
          const done = !failed && (stage > i || (stage >= 4 && (failedAt === undefined || i < failedAt)));
          const active = stage === i;
          const skipped = failedAt !== undefined && stage >= 4 && i > failedAt;
          return (
            <li key={p.n} className="relative flex gap-3 sm:flex-col sm:pr-4">
              {i < PIPELINE.length - 1 && (
                <div className="absolute top-4 left-9 hidden h-px w-[calc(100%-2.5rem)] bg-border sm:block">
                  <div className={cn("h-full bg-primary transition-all duration-500", done ? "w-full" : "w-0")} />
                </div>
              )}
              <div
                className={cn(
                  "relative z-10 flex size-8 shrink-0 items-center justify-center rounded-full border-2 bg-card transition-colors",
                  done && "border-success bg-success text-primary-foreground",
                  active && "border-primary text-primary ring-4 ring-primary-soft",
                  failed && "border-destructive bg-destructive text-destructive-foreground",
                  !done && !active && !failed && "text-muted-foreground",
                )}
              >
                {active ? <Loader2 className="size-4 animate-spin" /> : done ? <Check className="size-4" /> : <Icon className="size-3.5" />}
              </div>
              <div className={cn(skipped && "opacity-40")}>
                <div className="font-mono text-[10px] text-muted-foreground">{p.n}</div>
                <div className={cn("eyebrow", active ? "text-primary" : failed ? "text-destructive" : "text-foreground")}>{p.title}</div>
                <p className="mt-0.5 text-xs leading-snug text-muted-foreground">{p.desc}</p>
              </div>
            </li>
          );
        })}
      </ol>
    </Panel>
  );
}
