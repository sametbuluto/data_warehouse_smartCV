export interface Candidate {
  id: number;
  name: string;
  email?: string | null;
  phone?: string | null;
  education?: string | null;
  experience_years: number;
  skills: string[];
  file_path?: string | null;
  created_at: string;
}

export interface CandidateListItem {
  id: number;
  name: string;
  email?: string | null;
  skills_count: number;
  experience_years: number;
  created_at: string;
}

export interface Job {
  id: number;
  title: string;
  description: string;
  required_skills: string[];
  min_experience: number;
  education_level: string;
  created_at: string;
}

export interface MatchResult {
  id: number;
  candidate_id: number;
  candidate_name: string;
  job_id: number;
  job_title: string;
  skill_score: number;
  experience_score: number;
  education_score: number;
  semantic_score: number;
  final_score: number;
  matched_skills: string[];
  missing_skills: string[];
  created_at: string;
}

export interface MatchExplanation extends MatchResult {
  explanation: string;
}

export interface DashboardStats {
  total_candidates: number;
  total_jobs: number;
  total_matches: number;
  avg_match_score: number;
  candidates_with_email: number;
  candidates_with_phone: number;
  candidates_with_education: number;
  avg_skills_per_candidate: number;
  jobs_with_matches: number;
  top_skills: { name: string; count: number }[];
  best_candidates: { id: number; name: string; avg_score: number }[];
  score_distribution: { range: string; count: number }[];
}

export interface JobCreatePayload {
  title: string;
  description: string;
  required_skills: string[];
  min_experience: number;
  education_level: string;
}
