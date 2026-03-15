import { motion } from "framer-motion";

export default function SettingsPage() {
  return (
    <div className="p-6 lg:p-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-sm text-muted-foreground mt-1">Configure your LeadFlow AI workspace</p>
      </div>
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="glass-card p-8 text-center"
      >
        <p className="text-muted-foreground">Settings panel coming soon.</p>
      </motion.div>
    </div>
  );
}
