import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell } from 'recharts';
import { getDashboard } from '../api/client';

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#22c55e', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6', '#f97316', '#a855f7'];
const tooltipStyle = { background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text-primary)' };

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard().then(r => { setStats(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {[1,2,3,4].map(i => <div key={i} className="skeleton h-80 rounded-2xl" />)}
        </div>
      </div>
    );
  }

  const s = stats || { top_skills: [], score_distribution: [], best_candidates: [], total_candidates: 0, total_jobs: 0, total_matches: 0, avg_match_score: 0 };

  return (
    <div className="p-8">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-2xl font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Analytics</h1>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Recruitment intelligence and insights
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Skill Demand */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4 flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
            <BarChart3 size={16} style={{ color: 'var(--accent-blue)' }} /> Skill Distribution
          </h2>
          {s.top_skills.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={s.top_skills}>
                <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={11} angle={-25} textAnchor="end" height={60} />
                <YAxis stroke="var(--text-muted)" fontSize={11} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {s.top_skills.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-72 text-sm" style={{ color: 'var(--text-muted)' }}>
              Upload CVs to see skill analytics
            </div>
          )}
        </motion.div>

        {/* Score Distribution */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            Match Score Distribution
          </h2>
          {s.score_distribution.some(d => d.count > 0) ? (
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={s.score_distribution}>
                <XAxis dataKey="range" stroke="var(--text-muted)" fontSize={11} />
                <YAxis stroke="var(--text-muted)" fontSize={11} />
                <Tooltip contentStyle={tooltipStyle} />
                <Area type="monotone" dataKey="count" stroke="var(--accent-purple)" fill="rgba(139,92,246,0.2)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-72 text-sm" style={{ color: 'var(--text-muted)' }}>
              Run matching to see distributions
            </div>
          )}
        </motion.div>

        {/* Top Candidates */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            Top Performers
          </h2>
          {s.best_candidates.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={s.best_candidates} layout="vertical" margin={{ left: 80 }}>
                <XAxis type="number" domain={[0, 100]} stroke="var(--text-muted)" fontSize={11} />
                <YAxis type="category" dataKey="name" stroke="var(--text-muted)" fontSize={11} width={80} />
                <Tooltip contentStyle={tooltipStyle} />
                <Bar dataKey="avg_score" radius={[0, 6, 6, 0]}>
                  {s.best_candidates.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-72 text-sm" style={{ color: 'var(--text-muted)' }}>
              Match candidates to see rankings
            </div>
          )}
        </motion.div>

        {/* Summary Stats */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            Pipeline Overview
          </h2>
          <div className="grid grid-cols-2 gap-4">
            {[
              { label: 'Candidates Processed', value: s.total_candidates, color: 'var(--accent-blue)' },
              { label: 'Job Descriptions', value: s.total_jobs, color: 'var(--accent-purple)' },
              { label: 'Matches Computed', value: s.total_matches, color: 'var(--accent-cyan)' },
              { label: 'Avg Match Score', value: `${s.avg_match_score.toFixed(1)}%`, color: 'var(--accent-green)' },
            ].map(({ label, value, color }) => (
              <div key={label} className="p-4 rounded-xl text-center" style={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }}>
                <p className="text-2xl font-bold mb-1" style={{ color }}>{value}</p>
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{label}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
