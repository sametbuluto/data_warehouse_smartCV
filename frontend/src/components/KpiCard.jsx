import { motion } from 'framer-motion';

export default function KpiCard({ title, value, subtitle, icon: Icon, color = 'var(--accent-blue)' }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="kpi-card"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center"
             style={{ background: `${color}15`, border: `1px solid ${color}30` }}>
          <Icon size={20} style={{ color }} />
        </div>
      </div>
      <p className="text-2xl font-bold tracking-tight mb-1" style={{ color: 'var(--text-primary)' }}>
        {value}
      </p>
      <p className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>{title}</p>
      {subtitle && (
        <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>{subtitle}</p>
      )}
    </motion.div>
  );
}
