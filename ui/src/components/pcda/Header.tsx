import { FileCheck2, Lock } from "lucide-react";

export function Header() {
  return (
    <header className="glass sticky top-0 z-40 border-b">
      <div className="mx-auto flex max-w-[1400px] items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <div className="relative flex size-10 items-center justify-center rounded-xl bg-brand text-primary-foreground shadow-glow">
            <FileCheck2 className="size-5" />
            <span className="animate-ping-soft absolute -right-1 -bottom-1 size-3 rounded-full border-2 border-card bg-success" />
          </div>
          <div>
            <h1 className="text-base font-semibold tracking-tight sm:text-lg">
              Proof-Carrying <span className="text-brand">Data Analyst</span>
            </h1>
            <p className="text-xs text-muted-foreground sm:text-sm">
              AI proposes. <span className="font-medium text-foreground">The local system proves.</span>
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="hidden items-center gap-1.5 rounded-full border bg-card px-2.5 py-1 text-[11px] font-medium text-muted-foreground sm:inline-flex">
            <Lock className="size-3 text-success" /> Local-only processing
          </span>
          <span className="rounded-full border border-dashed border-warning/50 bg-warning-soft px-2.5 py-1 font-mono text-[10px] font-semibold tracking-widest text-warning sm:text-[11px]">
            FRONTEND DEMO
          </span>
        </div>
      </div>
    </header>
  );
}
