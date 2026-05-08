import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Users, Search, ChevronDown, ChevronUp, Eye } from 'lucide-react';
import { getCandidates, getJobs, getMatchResults, explainMatch } from '../api/client';
import ScoreRing from '../components/ScoreRing';

export default function Candidates() {
  const [searchParams] = useSearchParams();
  const jobIdParam = searchParams.get('job');

  const [candidates, setCandidates] = useState([]);
  const [matchResults, setMatchResults] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(jobIdParam || '');
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('score');
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getCandidates(), getJobs()])
      .then(([c, j]) => { setCandidates(c.data); setJobs(j.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (selectedJob) {
      getMatchResults(selectedJob).then(r => setMatchResults(r.data)).catch(() => setMatchResults([]));
    } else {
      setMatchResults([]);
    }
  }, [selectedJob]);

  useEffect(() => {
    if (jobIdParam) setSelectedJob(jobIdParam);
  }, [jobIdParam]);

  const showExplanation = async (matchId) => {
    const res = await explainMatch(matchId);
    setExplanation(res.data);
  };

  // Merge candidates with match results
  const displayData = selectedJob && matchResults.length > 0
    ? matchResults
        .filter(m => m.candidate_name.toLowerCase().includes(search.toLowerCase()))
        .sort((a, b) => sortBy === 'score' ? b.final_score - a.final_score : a.candidate_name.localeCompare(b.candidate_name))
    : candidates
        .filter(c => c.name.toLowerCase().includes(search.toLowerCase()))
        .map(c => ({ ...c, candidate_name: c.name, final_score: null }));

  if (loading) {
    return (
      <div className="p-8">
        {[1,2,3,4].map(i => <div key={i} className="skeleton h-20 rounded-xl mb-3" />)}
      </div>
    );
  }

  return (
    <div className="p-8">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-2xl font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Candidates</h1>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          {selectedJob ? 'Ranked candidates for selected job' : 'All uploaded candidates'}
        </p>
      </motion.div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <div className="relative flex-1 min-w-[200px]">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: 'var(--text-muted)' }} />
          <input value={search} onChange={e => setSearch(e.target.value)}
                 placeholder="Search candidates..."
                 className="w-full pl-9 pr-4 py-2.5 rounded-lg text-sm outline-none"
                 style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }} />
        </div>
        <select value={selectedJob} onChange={e => setSelectedJob(e.target.value)}
                className="px-4 py-2.5 rounded-lg text-sm outline-none min-w-[200px]"
                style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}>
          <option value="">All Candidates</option>
          {jobs.map(j => <option key={j.id} value={j.id}>{j.title}</option>)}
        </select>
        {selectedJob && (
          <button onClick={() => setSortBy(s => s === 'score' ? 'name' : 'score')}
                  className="flex items-center gap-1.5 px-4 py-2.5 rounded-lg text-sm"
                  style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-secondary)' }}>
            {sortBy === 'score' ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
            Sort: {sortBy === 'score' ? 'Score' : 'Name'}
          </button>
        )}
      </div>

      {/* Candidate List */}
      <div className="grid gap-3">
        {displayData.map((item, i) => (
          <motion.div key={item.id || i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.03 }}
                      className="glass-card p-4 flex items-center gap-4">
            {/* Rank */}
            {selectedJob && matchResults.length > 0 && (
              <span className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0"
                    style={{ background: i < 3 ? 'var(--gradient-primary)' : 'var(--bg-card)',
                             color: i < 3 ? 'white' : 'var(--text-muted)',
                             border: i >= 3 ? '1px solid var(--border)' : 'none' }}>
                {i + 1}
              </span>
            )}

            {/* Info */}
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-semibold truncate" style={{ color: 'var(--text-primary)' }}>
                {item.candidate_name || item.name}
              </h3>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                {item.email || ''} {item.skills_count != null ? `• ${item.skills_count} skills` : ''}
              </p>
              {/* Matched/Missing skills for match results */}
              {item.matched_skills && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {item.matched_skills.slice(0, 5).map(s => (
                    <span key={s} className="skill-badge matched text-[10px] py-0.5 px-2">{s}</span>
                  ))}
                  {item.missing_skills?.slice(0, 3).map(s => (
                    <span key={s} className="skill-badge missing text-[10px] py-0.5 px-2">{s}</span>
                  ))}
                </div>
              )}
            </div>

            {/* Score */}
            {item.final_score != null && (
              <div className="flex items-center gap-3">
                <ScoreRing score={item.final_score} size={56} />
                <button onClick={() => showExplanation(item.id)}
                        className="p-2 rounded-lg hover:bg-[rgba(99,102,241,0.1)]" title="View explanation">
                  <Eye size={16} style={{ color: 'var(--accent-blue)' }} />
                </button>
              </div>
            )}
          </motion.div>
        ))}
        {displayData.length === 0 && (
          <div className="text-center py-16" style={{ color: 'var(--text-muted)' }}>
            <Users size={40} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm">No candidates found.</p>
          </div>
        )}
      </div>

      {/* Explanation Modal */}
      <AnimatePresence>
        {explanation && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                      className="fixed inset-0 z-50 flex items-center justify-center p-4"
                      style={{ background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)' }}
                      onClick={() => setExplanation(null)}>
            <motion.div initial={{ scale: 0.95 }} animate={{ scale: 1 }} exit={{ scale: 0.95 }}
                        className="glass-card p-6 max-w-lg w-full max-h-[80vh] overflow-y-auto"
                        onClick={e => e.stopPropagation()}>
              <h2 className="text-lg font-bold mb-4" style={{ color: 'var(--text-primary)' }}>
                Match Explanation
              </h2>
              <div className="grid grid-cols-2 gap-3 mb-4">
                {[
                  { label: 'Skill Match (40%)', val: explanation.skill_score, color: 'var(--accent-blue)' },
                  { label: 'Experience (30%)', val: explanation.experience_score, color: 'var(--accent-purple)' },
                  { label: 'Education (20%)', val: explanation.education_score, color: 'var(--accent-cyan)' },
                  { label: 'Semantic (10%)', val: explanation.semantic_score, color: 'var(--accent-amber)' },
                ].map(({ label, val, color }) => (
                  <div key={label} className="p-3 rounded-lg" style={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }}>
                    <p className="text-[11px] mb-1" style={{ color: 'var(--text-muted)' }}>{label}</p>
                    <p className="text-lg font-bold" style={{ color }}>{val.toFixed(1)}</p>
                  </div>
                ))}
              </div>
              <div className="flex items-center justify-center mb-4">
                <div className="text-center">
                  <p className="text-xs mb-1" style={{ color: 'var(--text-muted)' }}>Final Score</p>
                  <ScoreRing score={explanation.final_score} size={80} />
                </div>
              </div>
              {explanation.matched_skills?.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs font-medium mb-1.5" style={{ color: 'var(--accent-green)' }}>✅ Matched Skills</p>
                  <div className="flex flex-wrap gap-1.5">
                    {explanation.matched_skills.map(s => <span key={s} className="skill-badge matched">{s}</span>)}
                  </div>
                </div>
              )}
              {explanation.missing_skills?.length > 0 && (
                <div className="mb-4">
                  <p className="text-xs font-medium mb-1.5" style={{ color: 'var(--accent-red)' }}>❌ Missing Skills</p>
                  <div className="flex flex-wrap gap-1.5">
                    {explanation.missing_skills.map(s => <span key={s} className="skill-badge missing">{s}</span>)}
                  </div>
                </div>
              )}
              <button onClick={() => setExplanation(null)} className="btn-primary w-full mt-2">Close</button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
