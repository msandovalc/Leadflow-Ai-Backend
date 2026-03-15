import { useQuery } from "@tanstack/react-query";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { useEffect } from "react";
import { motion } from "framer-motion";
import { format } from "date-fns";
import { ArrowLeft, Phone, Target, DollarSign, MapPin, Brain, Bot, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScoreBadge } from "@/components/ScoreBadge";
import { KpiSkeleton, ChatSkeleton } from "@/components/Skeletons";
import { cn } from "@/lib/utils";

export default function LeadDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: lead, isLoading, error } = useQuery({
    queryKey: ["lead", id],
    queryFn: () => api.getLead(id!),
    enabled: !!id,
    retry: 1,
  });

  useEffect(() => {
    if (error) toast.error((error as Error).message);
  }, [error]);

  const profileItems = lead
    ? [
        { label: "Phone", value: lead.whatsapp_number, icon: Phone },
        { label: "Intent", value: lead.intent, icon: Target },
        { label: "Budget", value: lead.budget, icon: DollarSign },
        { label: "Zone", value: lead.zone, icon: MapPin },
      ]
    : [];

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" onClick={() => navigate("/leads")} className="text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Lead Detail</h1>
          <p className="text-sm text-muted-foreground mt-0.5">CRM & Conversation Timeline</p>
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="space-y-4">{[1, 2, 3, 4].map((i) => <KpiSkeleton key={i} />)}</div>
          <div className="lg:col-span-2 glass-card p-6"><ChatSkeleton /></div>
        </div>
      ) : !lead ? (
        <div className="text-center text-muted-foreground py-16">Lead not found</div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-6"
        >
          {/* Left: Profile */}
          <div className="space-y-4">
            {profileItems.map((p) => (
              <div key={p.label} className="glass-card p-4 flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary">
                  <p.icon className="h-4 w-4 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-[11px] uppercase tracking-wider text-muted-foreground">{p.label}</p>
                  <p className="text-sm font-medium capitalize">{p.value || "—"}</p>
                </div>
              </div>
            ))}
            <div className="glass-card p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary">
                  <Brain className="h-4 w-4 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-[11px] uppercase tracking-wider text-muted-foreground">AI Score</p>
                </div>
              </div>
              <ScoreBadge score={lead.score} />
            </div>
          </div>

          {/* Right: Chat Timeline */}
          <div className="lg:col-span-2 glass-card p-6">
            <h2 className="text-sm font-semibold mb-6">WhatsApp Timeline</h2>
            {!lead.interactions?.length ? (
              <p className="text-muted-foreground text-sm text-center py-8">No interactions recorded</p>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                {lead.interactions.map((msg, i) => {
                  const isUser = msg.type === "user";
                  return (
                    <motion.div
                      key={msg.id || i}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.05, duration: 0.25 }}
                      className={cn("flex", isUser ? "justify-start" : "justify-end")}
                    >
                      <div
                        className={cn(
                          "max-w-[75%] rounded-2xl px-4 py-3 text-sm",
                          isUser
                            ? "bg-secondary text-foreground rounded-bl-md"
                            : "bg-primary/15 text-primary border border-primary/20 rounded-br-md"
                        )}
                      >
                        <div className="flex items-center gap-1.5 mb-1">
                          {isUser ? <User className="h-3 w-3" /> : <Bot className="h-3 w-3" />}
                          <span className="text-[10px] font-semibold uppercase tracking-wider opacity-70">
                            {isUser ? "Customer" : "AI Evaluation"}
                          </span>
                        </div>
                        <p>{msg.message}</p>
                        {msg.timestamp && (
                          <p className="text-[10px] opacity-50 mt-1.5">
                            {format(new Date(msg.timestamp), "MMM d, HH:mm")}
                          </p>
                        )}
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}
