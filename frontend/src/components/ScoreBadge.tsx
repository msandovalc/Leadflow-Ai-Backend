import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type ScoreType = "hot" | "warm" | "cold";

function getScoreType(score: string): ScoreType {
  const s = score?.toLowerCase() || "";
  if (s.includes("hot") || s.includes("high")) return "hot";
  if (s.includes("warm") || s.includes("medium")) return "warm";
  return "cold";
}

export function ScoreBadge({ score }: { score: string }) {
  const type = getScoreType(score);

  return (
    <Badge
      className={cn(
        "font-semibold text-xs border-0 px-3 py-1",
        type === "hot" && "bg-hot/15 text-hot",
        type === "warm" && "bg-warm/15 text-warm",
        type === "cold" && "bg-cold/15 text-cold"
      )}
    >
      {score}
    </Badge>
  );
}

export { getScoreType };
export type { ScoreType };
