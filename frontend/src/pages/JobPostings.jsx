import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, Briefcase, Trash2, Play, X } from 'lucide-react';
import { createJob, getJobs, deleteJob, runMatching } from '../api/client';
import { useNavigate } from 'react-router-dom';

const SUGGESTED_SKILLS = [
  'python','java','javascript','react','sql','docker','aws','git',
  'machine learning','typescript','node.js','fastapi','django','kubernetes',
  'tensorflow','data analysis','agile','rest','linux','mongodb',
];

export default function JobPostings() {
  const [jobs, setJobs] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: '', description: '', required_skills: [], min_experience: 0, education_level: 'Bachelor' });
  const [skillInput, setSkillInput] = useState('');
  const [matchingJobId, setMatchingJobId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => { loadJobs(); }, []);
  const loadJobs = () => getJobs().then(r => setJobs(r.data));

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createJob(form);
    setForm({ title: '', description: '', required_skills: [], min_experience: 0, education_level: 'Bachelor' });
    setShowForm(false);
    loadJobs();
  };

  const addSkill = (skill) => {
    if (skill && !form.required_skills.includes(skill.toLowerCase())) {
      setForm(f => ({ ...f, required_skills: [...f.required_skills, skill.toLowerCase()] }));
      setSkillInput('');
    }
  };

  const removeSkill = (skill) => {
    setForm(f => ({ ...f, required_skills: f.required_skills.filter(s => s !== skill) }));
  };

  const handleMatch = async (jobId) => {
    setMatchingJobId(jobId);
    try {
      await runMatching(jobId);
      navigate(`/candidates?job=${jobId}`);
    } finally {
      setMatchingJobId(null);
    }
  };

  return (
    <div className="p-8">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
                  className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Job Postings</h1>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
            Create job descriptions and match candidates
          </p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2">
          <Plus size={16} /> New Job
        </button>
      </motion.div>

      {/* Create Form */}
      {showForm && (
        <motion.form initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                     onSubmit={handleSubmit} className="glass-card p-6 mb-8">
          <h2 className="text-base font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            Create Job Posting
          </h2>

          <div className="grid gap-4">
            <div>
              <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--text-muted)' }}>Job Title</label>
              <input value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
                     placeholder="e.g. Senior Python Developer"
                     className="w-full p-3 rounded-lg text-sm outline-none"
                     style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}
                     required />
            </div>

            <div>
              <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--text-muted)' }}>Description</label>
              <textarea value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                        rows={4} placeholder="Enter job description..."
                        className="w-full p-3 rounded-lg text-sm outline-none resize-none"
                        style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}
                        required />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--text-muted)' }}>Min Experience (years)</label>
                <input type="number" min={0} value={form.min_experience}
                       onChange={e => setForm(f => ({ ...f, min_experience: parseFloat(e.target.value) || 0 }))}
                       className="w-full p-3 rounded-lg text-sm outline-none"
                       style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }} />
              </div>
              <div>
                <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--text-muted)' }}>Education Level</label>
                <select value={form.education_level} onChange={e => setForm(f => ({ ...f, education_level: e.target.value }))}
                        className="w-full p-3 rounded-lg text-sm outline-none"
                        style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }}>
                  <option>High School</option>
                  <option>Associate</option>
                  <option>Bachelor</option>
                  <option>Master</option>
                  <option>PhD</option>
                </select>
              </div>
            </div>

            {/* Skills */}
            <div>
              <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--text-muted)' }}>Required Skills</label>
              <div className="flex gap-2 mb-2">
                <input value={skillInput} onChange={e => setSkillInput(e.target.value)}
                       onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addSkill(skillInput); } }}
                       placeholder="Type a skill and press Enter"
                       className="flex-1 p-3 rounded-lg text-sm outline-none"
                       style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', color: 'var(--text-primary)' }} />
              </div>
              <div className="flex flex-wrap gap-1.5 mb-3">
                {form.required_skills.map(s => (
                  <span key={s} className="skill-badge flex items-center gap-1">
                    {s} <X size={12} className="cursor-pointer" onClick={() => removeSkill(s)} />
                  </span>
                ))}
              </div>
              <p className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>Suggested:</p>
              <div className="flex flex-wrap gap-1.5">
                {SUGGESTED_SKILLS.filter(s => !form.required_skills.includes(s)).slice(0, 12).map(s => (
                  <span key={s} className="skill-badge cursor-pointer hover:border-[var(--accent-blue)]"
                        onClick={() => addSkill(s)}>{s}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <button type="button" onClick={() => setShowForm(false)}
                    className="px-4 py-2 rounded-lg text-sm font-medium"
                    style={{ color: 'var(--text-secondary)', border: '1px solid var(--border)' }}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">Create Job</button>
          </div>
        </motion.form>
      )}

      {/* Job List */}
      <div className="grid gap-4">
        {jobs.map((job, i) => (
          <motion.div key={job.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="glass-card p-5 flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Briefcase size={16} style={{ color: 'var(--accent-purple)' }} />
                <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{job.title}</h3>
              </div>
              <p className="text-xs mb-3 line-clamp-2" style={{ color: 'var(--text-secondary)' }}>
                {job.description}
              </p>
              <div className="flex flex-wrap gap-1.5">
                {(job.required_skills || []).map(s => (
                  <span key={s} className="skill-badge text-[11px]">{s}</span>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-2 ml-4">
              <button onClick={() => handleMatch(job.id)}
                      disabled={matchingJobId === job.id}
                      className="btn-primary flex items-center gap-1.5 text-xs px-3 py-2">
                {matchingJobId === job.id ? (
                  <><span className="animate-spin">⟳</span> Matching...</>
                ) : (
                  <><Play size={14} /> Match</>
                )}
              </button>
              <button onClick={async () => { await deleteJob(job.id); loadJobs(); }}
                      className="p-2 rounded-lg hover:bg-[rgba(239,68,68,0.1)]" title="Delete">
                <Trash2 size={16} style={{ color: 'var(--accent-red)' }} />
              </button>
            </div>
          </motion.div>
        ))}
        {jobs.length === 0 && (
          <div className="text-center py-16" style={{ color: 'var(--text-muted)' }}>
            <Briefcase size={40} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm">No job postings yet. Create one to start matching.</p>
          </div>
        )}
      </div>
    </div>
  );
}
