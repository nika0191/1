import type { ReactNode } from "react";

export function ShowcaseSection({
  id,
  title,
  description,
  children,
}: {
  id: string;
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <section className="scroll-mt-24 py-10" id={id}>
      <div className="mb-6 border-b border-separator pb-4">
        <h2 className="text-2xl font-semibold text-foreground">{title}</h2>
        <p className="mt-1 text-muted">{description}</p>
      </div>
      <div className="grid gap-6 sm:grid-cols-2">{children}</div>
    </section>
  );
}

export function ShowcaseCard({
  title,
  className,
  children,
}: {
  title: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-xl border border-separator bg-surface p-6 shadow-surface">
      <h3 className="mb-4 text-xs font-medium tracking-wide text-muted uppercase">
        {title}
      </h3>
      <div className={className ?? "flex flex-wrap items-center gap-4"}>
        {children}
      </div>
    </div>
  );
}
