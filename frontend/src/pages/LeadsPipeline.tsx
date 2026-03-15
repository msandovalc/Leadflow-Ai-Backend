import { useQuery } from "@tanstack/react-query";
import { api, Lead } from "@/lib/api";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { motion } from "framer-motion";
import { format } from "date-fns";
import { Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScoreBadge } from "@/components/ScoreBadge";
import { TableSkeleton } from "@/components/Skeletons";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function LeadsPipeline() {
  const navigate = useNavigate();
  const { data: leads, isLoading, error } = useQuery({
    queryKey: ["leads"],
    queryFn: api.getLeads,
    retry: 1,
  });

  useEffect(() => {
    if (error) toast.error((error as Error).message);
  }, [error]);

  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Leads Pipeline</h1>
        <p className="text-sm text-muted-foreground mt-1">All captured leads from your WhatsApp channel</p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="glass-card overflow-hidden"
      >
        {isLoading ? (
          <div className="p-6"><TableSkeleton /></div>
        ) : !leads?.length ? (
          <div className="p-12 text-center text-muted-foreground">No leads found</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow className="border-border/50 hover:bg-transparent">
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground">WhatsApp</TableHead>
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground">Intent</TableHead>
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground">Budget</TableHead>
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground">Zone</TableHead>
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground">Date</TableHead>
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground">Score</TableHead>
                <TableHead className="text-xs uppercase tracking-wider text-muted-foreground text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(leads as Lead[]).map((lead, i) => (
                <TableRow
                  key={lead.id}
                  className="border-border/30 hover:bg-secondary/50 cursor-pointer transition-colors"
                  onClick={() => navigate(`/leads/${lead.id}`)}
                  style={{ animationDelay: `${i * 40}ms` }}
                >
                  <TableCell className="font-mono text-sm">{lead.whatsapp_number}</TableCell>
                  <TableCell className="capitalize text-sm">{lead.intent}</TableCell>
                  <TableCell className="text-sm">{lead.budget}</TableCell>
                  <TableCell className="text-sm">{lead.zone}</TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {lead.created_at ? format(new Date(lead.created_at), "MMM d, yyyy") : "—"}
                  </TableCell>
                  <TableCell><ScoreBadge score={lead.score} /></TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-muted-foreground hover:text-foreground"
                      onClick={(e) => { e.stopPropagation(); navigate(`/leads/${lead.id}`); }}
                    >
                      <Eye className="h-4 w-4 mr-1.5" />
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </motion.div>
    </div>
  );
}
