import { Skeleton } from "@/components/ui/skeleton";

export function KpiSkeleton() {
  return (
    <div className="glass-card p-6 space-y-3">
      <Skeleton className="h-4 w-24 bg-secondary" />
      <Skeleton className="h-8 w-16 bg-secondary" />
      <Skeleton className="h-3 w-32 bg-secondary" />
    </div>
  );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <Skeleton key={i} className="h-14 w-full bg-secondary rounded-lg" />
      ))}
    </div>
  );
}

export function ChatSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className={`flex ${i % 2 === 0 ? "justify-end" : "justify-start"}`}>
          <Skeleton className={`h-16 bg-secondary rounded-xl ${i % 2 === 0 ? "w-2/3" : "w-1/2"}`} />
        </div>
      ))}
    </div>
  );
}
