import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Flame, Thermometer, Snowflake, Users } from "lucide-react";
import { motion } from "framer-motion";
import { KpiSkeleton } from "@/components/Skeletons";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useEffect } from "react";

const dummyChartData = [
  { day: "Mon", leads: 4 },
  { day: "Tue", leads: 7 },
  { day: "Wed", leads: 3 },
  { day: "Thu", leads: 9 },
  { day: "Fri", leads: 6 },
  { day: "Sat", leads: 12 },
  { day: "Sun", leads: 8 },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};
const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { duration: 0.35 } },
};

export default function Dashboard() {
  const { data: metrics, isLoading, error } = useQuery({
    queryKey: ["metrics"],
    queryFn: api.getMetrics,
    retry: 1,
  });

  useEffect(() => {
    if (error) toast.error((error as Error).message);
  }, [error]);

  const kpis = metrics
    ? [
        { label: "Total Leads", value: metrics.total_leads, icon: Users, color: "text-foreground", glowClass: "" },
        { label: "Hot Leads", value: metrics.hot_leads, icon: Flame, color: "text-hot", glowClass: "glow-hot" },
        { label: "Warm Leads", value: metrics.warm_leads, icon: Thermometer, color: "text-warm", glowClass: "glow-warm" },
        { label: "Cold Leads", value: metrics.cold_leads, icon: Snowflake, color: "text-cold", glowClass: "glow-cold" },
      ]
    : [];

  return (
    <div className="p-6 lg:p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-sm text-muted-foreground mt-1">Real-time overview of your lead pipeline</p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => <KpiSkeleton key={i} />)}
        </div>
      ) : (
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          {kpis.map((kpi) => (
            <motion.div key={kpi.label} variants={item} className={`glass-card p-6 ${kpi.glowClass}`}>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">{kpi.label}</span>
                <kpi.icon className={`h-5 w-5 ${kpi.color}`} />
              </div>
              <p className={`text-3xl font-bold ${kpi.color}`}>{kpi.value}</p>
            </motion.div>
          ))}
        </motion.div>
      )}

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="glass-card p-6"
      >
        <h2 className="text-sm font-semibold mb-6">Leads over the last 7 days</h2>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={dummyChartData}>
              <defs>
                <linearGradient id="colorLeads" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(24, 100%, 55%)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="hsl(24, 100%, 55%)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(240, 4%, 16%)" />
              <XAxis dataKey="day" stroke="hsl(240, 5%, 55%)" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="hsl(240, 5%, 55%)" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(240, 6%, 8%)",
                  border: "1px solid hsl(240, 4%, 18%)",
                  borderRadius: "0.75rem",
                  color: "hsl(0, 0%, 95%)",
                  fontSize: 13,
                }}
              />
              <Area
                type="monotone"
                dataKey="leads"
                stroke="hsl(24, 100%, 55%)"
                strokeWidth={2}
                fill="url(#colorLeads)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </div>
  );
}
