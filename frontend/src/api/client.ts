import axios from "axios";

import type {
  Candidate,
  CandidateListItem,
  DashboardStats,
  Job,
  JobCreatePayload,
  MatchExplanation,
  MatchResult,
} from "../types/api";

const api = axios.create({
  baseURL: "/api",
});

export const uploadCV = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<Candidate>("/candidates/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};

export const getCandidates = async () => {
  const response = await api.get<CandidateListItem[]>("/candidates");
  return response.data;
};

export const getCandidate = async (id: number) => {
  const response = await api.get<Candidate>(`/candidates/${id}`);
  return response.data;
};

export const deleteCandidate = async (id: number) => {
  await api.delete(`/candidates/${id}`);
};

export const createJob = async (payload: JobCreatePayload) => {
  const response = await api.post<Job>("/jobs", payload);
  return response.data;
};

export const getJobs = async () => {
  const response = await api.get<Job[]>("/jobs");
  return response.data;
};

export const deleteJob = async (id: number) => {
  await api.delete(`/jobs/${id}`);
};

export const runMatching = async (jobId: number) => {
  const response = await api.post(`/match/${jobId}`);
  return response.data;
};

export const getMatchResults = async (jobId: number) => {
  const response = await api.get<MatchResult[]>(`/match/${jobId}/results`);
  return response.data;
};

export const explainMatch = async (matchId: number) => {
  const response = await api.get<MatchExplanation>(`/match/explain/${matchId}`);
  return response.data;
};

export const runCandidateMatching = async (candidateId: number) => {
  const response = await api.post(`/match/candidate/${candidateId}`);
  return response.data;
};

export const getCandidateMatches = async (candidateId: number) => {
  const response = await api.get<MatchResult[]>(`/match/candidate/${candidateId}/results`);
  return response.data;
};

export const getDashboard = async () => {
  const response = await api.get<DashboardStats>("/analytics/dashboard");
  return response.data;
};

export default api;
