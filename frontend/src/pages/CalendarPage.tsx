import { useQuery } from "@tanstack/react-query";
import { api, Lead } from "@/lib/api";
import { toast } from "sonner";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  format,
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  isSameDay,
  addMonths,
  subMonths,
  getDay,
  startOfWeek,
  endOfWeek,
} from "date-fns";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { getScoreType } from "@/components/ScoreBadge";
import { cn } from "@/lib/utils";
import { TableSkeleton } from "@/components/Skeletons";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export default function CalendarPage() {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const { data: leads, isLoading, error } = useQuery({
    queryKey: ["leads"],
    queryFn: api.getLeads,
    retry: 1,
  });

  useEffect(() => {
    if (error) toast.error((error as Error).message);
  }, [error]);

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const calStart = startOfWeek(monthStart);
  const calEnd = endOfWeek(monthEnd);
  const days = eachDayOfInterval({ start: calStart, end: calEnd });

  function getLeadsForDay(day: Date): Lead[] {
    if (!leads) return [];
    return (leads as Lead[]).filter((l) => {
      if (!l.created_at) return false;
      return isSameDay(new Date(l.created_at), day);
    });
  }

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Calendar</h1>
          <p className="text-sm text-muted-foreground mt-1">Lead timeline at a glance</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={() => setCurrentMonth((m) => subMonths(m, 1))} className="text-muted-foreground hover:text-foreground">
            <ChevronLeft className="h-5 w-5" />
          </Button>
          <span className="text-sm font-semibold min-w-[140px] text-center">
            {format(currentMonth, "MMMM yyyy")}
          </span>
          <Button variant="ghost" size="icon" onClick={() => setCurrentMonth((m) => addMonths(m, 1))} className="text-muted-foreground hover:text-foreground">
            <ChevronRight className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {isLoading ? (
        <TableSkeleton rows={6} />
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="glass-card overflow-hidden"
        >
          {/* Weekday headers */}
          <div className="grid grid-cols-7 border-b border-border/50">
            {WEEKDAYS.map((d) => (
              <div key={d} className="p-3 text-center text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                {d}
              </div>
            ))}
          </div>

          {/* Days grid */}
          <div className="grid grid-cols-7">
            {days.map((day, i) => {
              const isCurrentMonth = day.getMonth() === currentMonth.getMonth();
              const isToday = isSameDay(day, new Date());
              const dayLeads = getLeadsForDay(day);

              return (
                <div
                  key={i}
                  className={cn(
                    "min-h-[100px] p-2 border-b border-r border-border/30 transition-colors",
                    !isCurrentMonth && "opacity-30",
                    isToday && "bg-primary/5"
                  )}
                >
                  <span
                    className={cn(
                      "text-xs font-medium inline-flex items-center justify-center h-6 w-6 rounded-full",
                      isToday && "bg-primary text-primary-foreground"
                    )}
                  >
                    {format(day, "d")}
                  </span>
                  <div className="mt-1 space-y-1">
                    {dayLeads.slice(0, 3).map((lead) => {
                      const scoreType = getScoreType(lead.score);
                      return (
                        <div
                          key={lead.id}
                          className={cn(
                            "text-[10px] leading-tight px-1.5 py-1 rounded truncate font-medium",
                            scoreType === "hot" && "bg-hot/15 text-hot",
                            scoreType === "warm" && "bg-warm/15 text-warm",
                            scoreType === "cold" && "bg-cold/15 text-cold"
                          )}
                        >
                          {lead.whatsapp_number?.slice(-6)}
                        </div>
                      );
                    })}
                    {dayLeads.length > 3 && (
                      <span className="text-[10px] text-muted-foreground">+{dayLeads.length - 3} more</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      )}
    </div>
  );
}
