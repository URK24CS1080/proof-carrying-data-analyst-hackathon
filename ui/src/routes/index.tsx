import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Header } from "@/components/pcda/Header";
import { DataSources } from "@/components/pcda/DataSources";
import { DataQuality, DatasetOverview } from "@/components/pcda/DatasetOverview";
import { Pipeline, QuestionInput } from "@/components/pcda/AskAndPipeline";
import { DemoStatusSelector, EvidencePanel, ProofViewer, ResultPanel, VerificationPanel } from "@/components/pcda/ResultPanels";
import { HistoryBoard } from "@/components/pcda/History";
import { DEMO_DATASET, DEMO_FILES, DEMO_QUESTION, type Dataset, type HistoryItem, type ResultStatus, type SourceFile } from "@/lib/demo-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Proof-Carrying Data Analyst — AI proposes, the local system proves" },
      { name: "description", content: "Ask questions about your data and inspect every answer alongside executable proof, verification status, and evidence." },
      { property: "og:title", content: "Proof-Carrying Data Analyst" },
      { property: "og:description", content: "AI proposes. The local system proves. Answers delivered with executable proof and verification." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

const FAIL_AT: Partial<Record<ResultStatus, number>> = {
  CANNOT_DETERMINE: 1,
  CLARIFICATION_REQUIRED: 0,
  EXECUTION_ERROR: 2,
  VERIFICATION_FAILED: 3,
};

function Index() {
  const [files, setFiles] = useState<SourceFile[]>(DEMO_FILES);
  const [question, setQuestion] = useState(DEMO_QUESTION);
  const [asked, setAsked] = useState(DEMO_QUESTION);
  const [status, setStatus] = useState<ResultStatus>("VERIFIED");
  const [stage, setStage] = useState(4);
  const [autoRun, setAutoRun] = useState(true);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [activeId, setActiveId] = useState("demo");
  const timers = useRef<number[]>([]);
  const loading = stage >= 0 && stage < 4;

  useEffect(() => () => timers.current.forEach(clearTimeout), []);

  // Automation: every parsed CSV becomes a dataset; demo files expose the demo dataset.
  const datasets: Dataset[] = [
    ...(files.some((f) => f.demo) ? [DEMO_DATASET] : []),
    ...files.flatMap((f) => (f.dataset ? [f.dataset] : [])),
  ];
  const active = datasets.find((d) => d.id === activeId) ?? datasets[0];

  const run = (q: string = question, s: ResultStatus = status) => {
    timers.current.forEach(clearTimeout);
    timers.current = [];
    setAsked(q);
    setStatus(s);
    const stop = FAIL_AT[s] ?? 3;
    setStage(0);
    for (let i = 1; i <= stop; i++) timers.current.push(window.setTimeout(() => setStage(i), i * 550));
    timers.current.push(
      window.setTimeout(() => {
        setStage(4);
        setHistory((h) => [{ id: crypto.randomUUID(), question: q, status: s, at: Date.now(), source: active?.name ?? "no source" }, ...h].slice(0, 8));
      }, (stop + 1) * 550),
    );
  };

  // Automation: re-run when the user switches the active dataset.
  const first = useRef(true);
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    if (autoRun && active && files.length > 0) run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [active?.id]);

  return (
    <div className="min-h-screen bg-aurora">
      <Header />
      <main className="mx-auto max-w-[1400px] px-4 py-6 sm:px-6">
        <div className="grid gap-5 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
          <div className="space-y-5">
            <DataSources files={files} setFiles={setFiles} />
            <DatasetOverview datasets={datasets} activeId={active?.id ?? ""} onSelect={setActiveId} />
            <DataQuality dataset={active} />
            <HistoryBoard
              items={history}
              onClear={() => setHistory([])}
              onReplay={(h) => {
                setQuestion(h.question);
                run(h.question, h.status);
              }}
            />
          </div>
          <div className="space-y-5">
            <QuestionInput
              question={question}
              setQuestion={setQuestion}
              onAnalyze={() => run()}
              onPick={(q) => {
                setQuestion(q);
                if (autoRun && files.length > 0) run(q);
              }}
              autoRun={autoRun}
              setAutoRun={setAutoRun}
              loading={loading}
              disabledReason={files.length === 0 ? "Add at least one data source to analyze." : undefined}
            />
            <Pipeline stage={stage} failedAt={FAIL_AT[status]} />
            <DemoStatusSelector status={status} onChange={(s) => { setStatus(s); if (!loading) setStage(4); }} />
            <ResultPanel
              status={status}
              question={asked}
              loading={loading}
              onRetry={() => run(question, "VERIFIED")}
              onClarify={(q) => {
                setQuestion(q);
                setAsked(q);
              }}
            />
            <div className="grid gap-5 xl:grid-cols-2">
              <VerificationPanel status={status} loading={loading} />
              <EvidencePanel status={status} />
            </div>
            <ProofViewer status={status} />
          </div>
        </div>
        <footer className="mt-8 border-t pt-4 text-center text-xs text-muted-foreground">
          Frontend demonstration · all data, results and verification states shown are illustrative.
        </footer>
      </main>
    </div>
  );
}
