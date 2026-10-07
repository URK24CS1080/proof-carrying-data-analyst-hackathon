import { useEffect, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Panel({
  eyebrow,
  title,
  description,
  actions,
  children,
  className,
  icon,
  delay = 0,
}: {
  delay?: number;
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
  icon?: ReactNode;
}) {
  return (
    <section
      style={{ animationDelay: `${delay}ms` }}
      className={cn(
        "animate-rise group/panel relative overflow-hidden rounded-xl border bg-card shadow-card transition-shadow duration-300 hover:shadow-lift",
        className,
      )}
    >
      <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent" />
      <header className="flex items-start justify-between gap-4 border-b bg-gradient-to-b from-muted/50 to-transparent px-5 py-4">
        <div className="flex min-w-0 items-start gap-3">
          {icon && (
            <div className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-brand text-primary-foreground shadow-sm">
              {icon}
            </div>
          )}
          <div className="min-w-0">
            {eyebrow && <div className="eyebrow text-muted-foreground">{eyebrow}</div>}
            <h2 className="eyebrow text-foreground">{title}</h2>
            {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
          </div>
        </div>
        {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
      </header>
      <div className="p-5">{children}</div>
    </section>
  );
}

/** Smoothly animates a number from 0 → target whenever target changes. */
export function useCountUp(target: number, duration = 900) {
  const [v, setV] = useState(0);
  useEffect(() => {
    let raf = 0;
    const start = performance.now();
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / duration);
      setV(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return v;
}

export function DemoTag({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded border border-dashed border-warning/50 bg-warning-soft px-1.5 py-0.5 font-mono text-[10px] font-medium uppercase tracking-wider text-warning",
        className,
      )}
    >
      Demo
    </span>
  );
}

type Tone = "success" | "warning" | "info" | "destructive" | "neutral" | "primary";
const toneCls: Record<Tone, string> = {
  success: "bg-success-soft text-success border-success/25",
  warning: "bg-warning-soft text-warning border-warning/30",
  info: "bg-info-soft text-info border-info/25",
  destructive: "bg-destructive-soft text-destructive border-destructive/25",
  neutral: "bg-muted text-muted-foreground border-border",
  primary: "bg-primary-soft text-primary border-primary/25",
};

export function StatusBadge({ tone, children, className }: { tone: Tone; children: ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 text-xs font-semibold tracking-wide",
        toneCls[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}

export function IconButton({
  children,
  className,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type="button"
      className={cn(
        "inline-flex h-8 items-center gap-1.5 rounded-md border bg-card px-2.5 text-xs font-medium text-foreground transition-colors hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1 active:translate-y-px disabled:pointer-events-none disabled:opacity-50",
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}
