import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { uploadCV } from '../api/client';

export default function CvUpload() {
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (files) => {
    const file = files[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const res = await uploadCV(file);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-2xl font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Upload Resume</h1>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          Upload a PDF resume to extract skills and candidate data using NLP
        </p>
      </motion.div>

      {/* Dropzone */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          {uploading ? (
            <div className="flex flex-col items-center gap-3">
              <Loader2 size={40} className="animate-spin" style={{ color: 'var(--accent-blue)' }} />
              <p className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                Processing with NLP pipeline...
              </p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                Extracting text → Parsing → Skill Detection
              </p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center"
                   style={{ background: 'rgba(99,102,241,0.1)', border: '1px solid rgba(99,102,241,0.2)' }}>
                <Upload size={28} style={{ color: 'var(--accent-blue)' }} />
              </div>
              <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                {isDragActive ? 'Drop your PDF here' : 'Drag & drop a PDF resume here'}
              </p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                or click to browse • PDF only
              </p>
            </div>
          )}
        </div>
      </motion.div>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                      className="mt-6 p-4 rounded-xl flex items-center gap-3"
                      style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)' }}>
            <AlertCircle size={20} style={{ color: 'var(--accent-red)' }} />
            <p className="text-sm" style={{ color: 'var(--accent-red)' }}>{error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Result */}
      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                      className="mt-6 glass-card p-6">
            <div className="flex items-center gap-2 mb-5">
              <CheckCircle2 size={20} style={{ color: 'var(--accent-green)' }} />
              <h2 className="text-base font-semibold" style={{ color: 'var(--text-primary)' }}>
                Resume Parsed Successfully
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
              {[
                { label: 'Name', value: result.name },
                { label: 'Email', value: result.email || 'Not found' },
                { label: 'Phone', value: result.phone || 'Not found' },
                { label: 'Education', value: result.education || 'Not found' },
                { label: 'Experience', value: `${result.experience_years} years` },
                { label: 'Skills Found', value: result.skills?.length || 0 },
              ].map(({ label, value }) => (
                <div key={label} className="p-3 rounded-lg" style={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }}>
                  <p className="text-xs font-medium mb-1" style={{ color: 'var(--text-muted)' }}>{label}</p>
                  <p className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{value}</p>
                </div>
              ))}
            </div>

            {/* Skills */}
            {result.skills?.length > 0 && (
              <div>
                <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-muted)' }}>Extracted Skills</p>
                <div className="flex flex-wrap gap-2">
                  {result.skills.map(skill => (
                    <span key={skill} className="skill-badge">{skill}</span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
