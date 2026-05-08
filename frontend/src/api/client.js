import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ── Candidates ──
export const uploadCV = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/candidates/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getCandidates = () => api.get('/candidates');
export const getCandidate = (id) => api.get(`/candidates/${id}`);
export const deleteCandidate = (id) => api.delete(`/candidates/${id}`);

// ── Jobs ──
export const createJob = (data) => api.post('/jobs', data);
export const getJobs = () => api.get('/jobs');
export const getJob = (id) => api.get(`/jobs/${id}`);
export const deleteJob = (id) => api.delete(`/jobs/${id}`);

// ── Matching ──
export const runMatching = (jobId) => api.post(`/match/${jobId}`);
export const getMatchResults = (jobId) => api.get(`/match/${jobId}/results`);
export const explainMatch = (matchId) => api.get(`/match/explain/${matchId}`);

// ── Analytics ──
export const getDashboard = () => api.get('/analytics/dashboard');

export default api;
