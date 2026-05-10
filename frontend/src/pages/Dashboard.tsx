import { useEffect, useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { BriefcaseBusiness, DatabaseZap, Target, TrendingUp, UsersRound } from "lucide-react";
import { Link } from "react-router-dom";

import { getCandidates, getDashboard, getJobs } from "../api/client";
import { KpiCard } from "../components/dashboard/kpi-card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { SectionHeading } from "../components/ui/section-heading";
import { Skeleton } from "../components/ui/skeleton";
import { formatPercent, formatRelativeDate } from "../lib/utils";
import type { CandidateListItem, DashboardStats, Job } from "../types/api";

const chartColors = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)"];

function getCoveragePart(value: number, total: number) {
  return total ? formatPercent((value / total) * 100, 0) : "0%";
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [candidates, setCandidates] = useState<CandidateListItem[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getDashboard(), getCandidates(), getJobs()])
      .then(([dashboardData, candidateData, jobData]) => {
        setStats(dashboardData);
        setCandidates(candidateData);
        setJobs(jobData);
      })
      .finally(() => setLoading(false));
  }, []);

  const recentCandidates = useMemo(() => candidates.slice(0, 5), [candidates]);

  if (loading) {
    return (
      <div className="space-y-5 pb-4">
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <Skeleton key={index} className="h-[148px] w-full" />
          ))}
        </div>
        <div className="grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
          <Skeleton className="h-[340px] w-full" />
          <Skeleton className="h-[340px] w-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5 pb-4">
      <SectionHeading
        eyebrow="Overview"
        title="SmartCV data and matching overview"
        action={
          <div className="flex flex-wrap gap-2">
            <Button asChild>
              <Link to="/upload">Upload CV</Link>
            </Button>
            <Button asChild variant="secondary">
              <Link to="/jobs">Create Job</Link>
            </Button>
          </div>
        }
      />

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          title="Candidates"
          value={String(stats?.total_candidates ?? 0)}
          icon={UsersRound}
        />
        <KpiCard
          title="Job Postings"
          value={String(stats?.total_jobs ?? 0)}
          icon={BriefcaseBusiness}
          accentClassName="bg-[linear-gradient(160deg,rgba(124,58,237,0.12),transparent)]"
        />
        <KpiCard
          title="Match Results"
          value={String(stats?.total_matches ?? 0)}
          icon={Target}
          accentClassName="bg-[linear-gradient(160deg,rgba(8,145,178,0.14),transparent)]"
        />
        <KpiCard
          title="Average Score"
          value={formatPercent(stats?.avg_match_score ?? 0, 1)}
          icon={TrendingUp}
          accentClassName="bg-[linear-gradient(160deg,rgba(245,158,11,0.16),transparent)]"
        />
      </section>

      <section className="grid gap-5 xl:grid-cols-[1.15fr_0.85fr]">
        <Card>
          <CardHeader>
            <CardTitle>Data quality</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Email coverage</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
                  {getCoveragePart(stats?.candidates_with_email ?? 0, stats?.total_candidates ?? 0)}
                </p>
              </div>
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Phone coverage</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
                  {getCoveragePart(stats?.candidates_with_phone ?? 0, stats?.total_candidates ?? 0)}
                </p>
              </div>
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Education coverage</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
                  {getCoveragePart(stats?.candidates_with_education ?? 0, stats?.total_candidates ?? 0)}
                </p>
              </div>
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Avg. skills / candidate</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
                  {(stats?.avg_skills_per_candidate ?? 0).toFixed(1)}
                </p>
              </div>
            </div>

            <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Matching coverage</p>
                <Badge tone="brand">
                  {stats?.jobs_with_matches ?? 0} / {stats?.total_jobs ?? 0} jobs
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Latest candidates</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentCandidates.length ? (
              recentCandidates.map((candidate) => (
                <div key={candidate.id} className="rounded-[24px] border border-border bg-secondary/55 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-foreground">{candidate.name}</p>
                      <p className="mt-1 text-xs text-muted-foreground">
                        {candidate.skills_count} skills • {candidate.experience_years} years
                      </p>
                    </div>
                    <Badge>{formatRelativeDate(candidate.created_at)}</Badge>
                  </div>
                </div>
              ))
            ) : (
              <EmptyState
                icon={DatabaseZap}
                title="No candidate data yet"
                description="Upload a CV or seed the database to populate the dataset."
                className="min-h-[260px]"
              />
            )}
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <CardHeader>
            <CardTitle>Top skills</CardTitle>
          </CardHeader>
          <CardContent className="h-[330px]">
            {stats?.top_skills.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.top_skills}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Bar dataKey="count" radius={[14, 14, 6, 6]}>
                    {stats.top_skills.map((item, index) => (
                      <Cell key={item.name} fill={chartColors[index % chartColors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={DatabaseZap}
                title="No skill distribution yet"
                description="Candidate uploads will populate this chart."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Score distribution</CardTitle>
          </CardHeader>
          <CardContent className="h-[330px]">
            {stats?.score_distribution.some((item) => item.count > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={stats.score_distribution}>
                  <defs>
                    <linearGradient id="dashboardArea" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="5%" stopColor="var(--chart-2)" stopOpacity={0.44} />
                      <stop offset="95%" stopColor="var(--chart-2)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="range" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Area type="monotone" dataKey="count" stroke="var(--chart-2)" strokeWidth={3} fill="url(#dashboardArea)" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={Target}
                title="No score distribution yet"
                description="Run job matching to create score records."
              />
            )}
          </CardContent>
        </Card>
      </section>

      <section>
        <Card>
          <CardHeader>
            <CardTitle>Recent job postings</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {jobs.slice(0, 6).map((job) => (
              <div key={job.id} className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-sm font-semibold text-foreground">{job.title}</p>
                <p className="mt-1 text-xs text-muted-foreground">
                  {job.min_experience}+ years • {job.education_level}
                </p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {job.required_skills.slice(0, 3).map((skill) => (
                    <Badge key={skill}>{skill}</Badge>
                  ))}
                </div>
              </div>
            ))}
            {!jobs.length ? (
              <EmptyState
                icon={BriefcaseBusiness}
                title="No jobs created yet"
                description="Add a role to start producing candidate rankings."
                className="md:col-span-2 xl:col-span-3"
              />
            ) : null}
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
