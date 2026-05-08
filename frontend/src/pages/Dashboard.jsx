import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, Briefcase, Target, TrendingUp, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { getDashboard } from '../api/client';
import KpiCard from '../components/KpiCard';

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#22c55e', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6'];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard().then(r => { setStats(r.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
          {[1,2,3,4].map(i => <div key={i} className="skeleton h-32 rounded-2xl" />)}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div className="skeleton h-80 rounded-2xl" />
          <div className="skeleton h-80 rounded-2xl" />
        </div>
      </div>
    );
  }

  const s = stats || { total_candidates: 0, total_jobs: 0, total_matches: 0, avg_match_score: 0, top_skills: [], best_candidates: [], score_distribution: [] };

  return (
    <div className="p-8">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-2xl font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Dashboard</h1>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          AI-powered recruitment intelligence overview
        </p>
      </motion.div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <KpiCard title="Total Candidates" value={s.total_candidates} icon={Users} color="var(--accent-blue)" />
        <KpiCard title="Active Jobs" value={s.total_jobs} icon={Briefcase} color="var(--accent-purple)" />
        <KpiCard title="Matches Run" value={s.total_matches} icon={Target} color="var(--accent-cyan)" />
        <KpiCard title="Avg Match Score" value={`${s.avg_match_score.toFixed(1)}%`} icon={TrendingUp} color="var(--accent-green)" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-8">
        {/* Top Skills Chart */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
                    className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4 flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
            <Zap size={16} style={{ color: 'var(--accent-amber)' }} /> Top Skills
          </h2>
          {s.top_skills.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={s.top_skills} layout="vertical" margin={{ left: 60 }}>
                <XAxis type="number" stroke="var(--text-muted)" fontSize={12} />
                <YAxis type="category" dataKey="name" stroke="var(--text-muted)" fontSize={12} width={80} />
                <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text-primary)' }} />
                <Bar dataKey="count" fill="var(--accent-blue)" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-60 text-sm" style={{ color: 'var(--text-muted)' }}>
              Upload CVs to see skill analytics
            </div>
          )}
        </motion.div>

        {/* Score Distribution */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
                    className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            Score Distribution
          </h2>
          {s.score_distribution.some(d => d.count > 0) ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={s.score_distribution.filter(d => d.count > 0)} dataKey="count" nameKey="range"
                     cx="50%" cy="50%" outerRadius={100} label={({ range, count }) => `${range}: ${count}`}>
                  {s.score_distribution.filter(d => d.count > 0).map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text-primary)' }} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-60 text-sm" style={{ color: 'var(--text-muted)' }}>
              Run matching to see score distribution
            </div>
          )}
        </motion.div>
      </div>

      {/* Best Candidates */}
      {s.best_candidates.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
                    className="glass-card p-6">
          <h2 className="text-base font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Top Candidates</h2>
          <div className="grid gap-3">
            {s.best_candidates.map((c, i) => (
              <div key={c.id} className="flex items-center justify-between p-3 rounded-lg"
                   style={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }}>
                <div className="flex items-center gap-3">
                  <span className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold"
                        style={{ background: 'var(--gradient-primary)', color: 'white' }}>
                    {i + 1}
                  </span>
                  <span className="font-medium text-sm">{c.name}</span>
                </div>
                <span className="text-sm font-semibold" style={{ color: 'var(--accent-green)' }}>
                  {c.avg_score.toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
