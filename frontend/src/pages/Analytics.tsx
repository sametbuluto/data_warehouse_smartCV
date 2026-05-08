import { useEffect, useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ActivitySquare, BarChart3, ChartPie, DatabaseZap, UsersRound } from "lucide-react";

import { getCandidates, getDashboard, getJobs } from "../api/client";
import { Badge } from "../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { SectionHeading } from "../components/ui/section-heading";
import { Skeleton } from "../components/ui/skeleton";
import { formatPercent } from "../lib/utils";
import type { CandidateListItem, DashboardStats, Job } from "../types/api";

const colors = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)"];

export default function AnalyticsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [candidates, setCandidates] = useState<CandidateListItem[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getDashboard(), getCandidates(), getJobs()])
      .then(([dashboardData, candidateData, jobData]) => {
        setStats(dashboardData);
        setCandidates(candidateData);
        setJobs(jobData);
      })
      .catch(() => setError("Analytics verisi alınamadı. Backend bağlantısını ve mevcut veriyi kontrol et."))
      .finally(() => setLoading(false));
  }, []);

  const educationMix = useMemo(() => {
    const counts = new Map<string, number>();
    jobs.forEach((job) => {
      counts.set(job.education_level, (counts.get(job.education_level) ?? 0) + 1);
    });

    return Array.from(counts.entries()).map(([name, value]) => ({ name, value }));
  }, [jobs]);

  const candidateExperience = useMemo(() => {
    const buckets = [
      { name: "0-2", value: 0 },
      { name: "3-5", value: 0 },
      { name: "6-8", value: 0 },
      { name: "9+", value: 0 },
    ];

    candidates.forEach((candidate) => {
      if (candidate.experience_years <= 2) buckets[0].value += 1;
      else if (candidate.experience_years <= 5) buckets[1].value += 1;
      else if (candidate.experience_years <= 8) buckets[2].value += 1;
      else buckets[3].value += 1;
    });

    return buckets;
  }, [candidates]);

  const dataQuality = useMemo(() => {
    const totalCandidates = stats?.total_candidates ?? 0;
    const totalJobs = stats?.total_jobs ?? 0;

    return [
      {
        label: "Email completeness",
        value: formatPercent(totalCandidates ? ((stats?.candidates_with_email ?? 0) / totalCandidates) * 100 : 0, 0),
        helper: `${stats?.candidates_with_email ?? 0} / ${totalCandidates}`,
      },
      {
        label: "Phone completeness",
        value: formatPercent(totalCandidates ? ((stats?.candidates_with_phone ?? 0) / totalCandidates) * 100 : 0, 0),
        helper: `${stats?.candidates_with_phone ?? 0} / ${totalCandidates}`,
      },
      {
        label: "Education completeness",
        value: formatPercent(totalCandidates ? ((stats?.candidates_with_education ?? 0) / totalCandidates) * 100 : 0, 0),
        helper: `${stats?.candidates_with_education ?? 0} / ${totalCandidates}`,
      },
      {
        label: "Job match coverage",
        value: formatPercent(totalJobs ? ((stats?.jobs_with_matches ?? 0) / totalJobs) * 100 : 0, 0),
        helper: `${stats?.jobs_with_matches ?? 0} / ${totalJobs}`,
      },
    ];
  }, [stats]);

  if (loading) {
    return (
      <div className="space-y-6 pb-4">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <Skeleton key={index} className="h-[150px] w-full" />
          ))}
        </div>
        <div className="grid gap-6 xl:grid-cols-2">
          <Skeleton className="h-[340px] w-full" />
          <Skeleton className="h-[340px] w-full" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6 pb-4">
        <SectionHeading eyebrow="Analytics" title="Project analytics" description="Warehouse-style metrics for dataset quality and matching coverage." />
        <div className="rounded-[28px] border border-danger/20 bg-danger/10 p-5 text-sm text-danger">{error}</div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Analytics"
        title="Data quality and matching analytics"
        description="A simpler analytics page focused on dataset completeness, extraction quality, and score coverage."
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {[
          { icon: DatabaseZap, label: "Candidates", value: stats?.total_candidates ?? 0 },
          { icon: ActivitySquare, label: "Jobs", value: stats?.total_jobs ?? 0 },
          { icon: BarChart3, label: "Matches", value: stats?.total_matches ?? 0 },
          { icon: ChartPie, label: "Avg score", value: `${(stats?.avg_match_score ?? 0).toFixed(1)}%` },
        ].map((item) => (
          <Card key={item.label}>
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <p className="text-sm text-muted-foreground">{item.label}</p>
                <p className="mt-2 text-3xl font-semibold tracking-tight text-foreground">{item.value}</p>
              </div>
              <div className="flex h-14 w-14 items-center justify-center rounded-[22px] bg-primary/10 text-primary">
                <item.icon className="h-5 w-5" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Data completeness</CardTitle>
            <CardDescription>How complete the current candidate and matching dataset is.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3 sm:grid-cols-2">
            {dataQuality.map((item) => (
              <div key={item.label} className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground">{item.value}</p>
                <p className="mt-1 text-sm text-muted-foreground">{item.helper}</p>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Best candidates overview</CardTitle>
            <CardDescription>Top average candidates across all stored match results.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {stats?.best_candidates.length ? (
              stats.best_candidates.map((candidate) => (
                <div key={candidate.id} className="flex items-center justify-between rounded-[24px] border border-border bg-secondary/55 p-4">
                  <div>
                    <p className="text-sm font-semibold text-foreground">{candidate.name}</p>
                    <p className="mt-1 text-xs text-muted-foreground">Average score across matched jobs</p>
                  </div>
                  <Badge tone="brand">{candidate.avg_score.toFixed(1)}%</Badge>
                </div>
              ))
            ) : (
              <EmptyState
                icon={UsersRound}
                title="Leaderboard unavailable"
                description="Candidate rankings will appear after the first matching run."
                className="min-h-[240px]"
              />
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top extracted skills</CardTitle>
            <CardDescription>Normalized skill frequency across all parsed resumes.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {stats?.top_skills.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.top_skills}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Bar dataKey="count" radius={[14, 14, 6, 6]}>
                    {stats.top_skills.map((skill, index) => (
                      <Cell key={skill.name} fill={colors[index % colors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={BarChart3}
                title="No skill analytics yet"
                description="Seed or upload candidates to populate the skill frequency chart."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Match score distribution</CardTitle>
            <CardDescription>Distribution of final weighted scores across saved ranking results.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {stats?.score_distribution.some((item) => item.count > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={stats.score_distribution}>
                  <defs>
                    <linearGradient id="analyticsArea" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="5%" stopColor="var(--chart-2)" stopOpacity={0.44} />
                      <stop offset="95%" stopColor="var(--chart-2)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="range" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Area type="monotone" dataKey="count" stroke="var(--chart-2)" strokeWidth={3} fill="url(#analyticsArea)" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={ActivitySquare}
                title="No scoring history yet"
                description="Run matching to populate score distribution analytics."
              />
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Candidate experience bands</CardTitle>
            <CardDescription>Distribution of uploaded profiles by professional experience range.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {candidateExperience.some((item) => item.value > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={candidateExperience} dataKey="value" nameKey="name" innerRadius={70} outerRadius={110}>
                    {candidateExperience.map((segment, index) => (
                      <Cell key={segment.name} fill={colors[index % colors.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={ChartPie}
                title="No candidate experience data"
                description="Upload candidate CVs to view experience band distribution."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Job education requirements</CardTitle>
            <CardDescription>How education requirements are distributed across job templates.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {educationMix.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={educationMix}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Bar dataKey="value" radius={[14, 14, 6, 6]} fill="var(--chart-3)" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={DatabaseZap}
                title="No job templates available"
                description="Create job postings to visualize requirement distribution."
              />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
