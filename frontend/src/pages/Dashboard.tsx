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
import {
  ArrowRight,
  BriefcaseBusiness,
  BrainCircuit,
  Target,
  TrendingUp,
  Trophy,
  UsersRound,
} from "lucide-react";
import { Link } from "react-router-dom";

import { getCandidates, getDashboard, getJobs } from "../api/client";
import { KpiCard } from "../components/dashboard/kpi-card";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { SectionHeading } from "../components/ui/section-heading";
import { Skeleton } from "../components/ui/skeleton";
import { formatPercent, formatRelativeDate } from "../lib/utils";
import type { CandidateListItem, DashboardStats, Job } from "../types/api";

const chartColors = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)"];

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

  const experienceBuckets = useMemo(() => {
    const buckets = [
      { name: "0-2 yrs", value: 0 },
      { name: "3-5 yrs", value: 0 },
      { name: "6-8 yrs", value: 0 },
      { name: "9+ yrs", value: 0 },
    ];

    candidates.forEach((candidate) => {
      if (candidate.experience_years <= 2) buckets[0].value += 1;
      else if (candidate.experience_years <= 5) buckets[1].value += 1;
      else if (candidate.experience_years <= 8) buckets[2].value += 1;
      else buckets[3].value += 1;
    });

    return buckets.filter((bucket) => bucket.value > 0);
  }, [candidates]);

  const topCandidate = stats?.best_candidates[0];

  if (loading) {
    return (
      <div className="space-y-6 pb-4">
        <Skeleton className="h-[220px] w-full" />
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <Skeleton key={index} className="h-[172px] w-full" />
          ))}
        </div>
        <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
          <Skeleton className="h-[380px] w-full" />
          <Skeleton className="h-[380px] w-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-4">
      <section className="hero-panel ring-grid overflow-hidden rounded-[36px] p-6 sm:p-8">
        <div className="grid gap-8 xl:grid-cols-[1.3fr_0.9fr]">
          <div className="space-y-5">
            <SectionHeading
              eyebrow="AI Recruiting Control Center"
              title="A stable, presentation-ready recruitment intelligence dashboard."
              description="Track candidate volume, active hiring demand, skill coverage, and explainable match quality from a polished enterprise workspace."
              action={
                <div className="flex flex-wrap gap-3">
                  <Button asChild size="lg">
                    <Link to="/upload">
                      Upload CV
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </Button>
                  <Button asChild variant="secondary" size="lg">
                    <Link to="/matching">Open Matching</Link>
                  </Button>
                </div>
              }
            />

            <div className="grid gap-4 sm:grid-cols-3">
              <div className="glass-panel rounded-[28px] p-4">
                <p className="text-xs font-medium uppercase tracking-[0.22em] text-muted-foreground">Precision Formula</p>
                <p className="mt-2 text-sm text-foreground">40% skills • 30% experience • 20% education • 10% semantic fit</p>
              </div>
              <div className="glass-panel rounded-[28px] p-4">
                <p className="text-xs font-medium uppercase tracking-[0.22em] text-muted-foreground">Data Footprint</p>
                <p className="mt-2 text-sm text-foreground">
                  {stats?.total_candidates ?? 0} candidates across {stats?.total_jobs ?? 0} live job templates
                </p>
              </div>
              <div className="glass-panel rounded-[28px] p-4">
                <p className="text-xs font-medium uppercase tracking-[0.22em] text-muted-foreground">Best Candidate</p>
                <p className="mt-2 text-sm text-foreground">
                  {topCandidate ? `${topCandidate.name} • ${formatPercent(topCandidate.avg_score, 1)}` : "Awaiting match history"}
                </p>
              </div>
            </div>
          </div>

          <Card className="overflow-hidden">
            <CardHeader>
              <CardTitle>Live pipeline health</CardTitle>
              <CardDescription>Recent job templates ready for ranking and AI candidate explanations.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {jobs.slice(0, 4).map((job) => (
                <div key={job.id} className="rounded-[24px] border border-border bg-secondary/60 p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-sm font-semibold text-foreground">{job.title}</p>
                      <p className="mt-1 text-xs text-muted-foreground">Created {formatRelativeDate(job.created_at)}</p>
                    </div>
                    <Badge tone="brand">{job.min_experience}+ yrs</Badge>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {job.required_skills.slice(0, 4).map((skill) => (
                      <Badge key={skill}>{skill}</Badge>
                    ))}
                  </div>
                </div>
              ))}
              {!jobs.length ? (
                <EmptyState
                  icon={BriefcaseBusiness}
                  title="No jobs created yet"
                  description="Create job templates to unlock ranking, analytics, and AI fit explanations."
                  className="min-h-[220px]"
                />
              ) : null}
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          title="Total Candidates"
          value={String(stats?.total_candidates ?? 0)}
          subtitle="Parsed and available in the candidate workspace"
          icon={UsersRound}
        />
        <KpiCard
          title="Active Jobs"
          value={String(stats?.total_jobs ?? 0)}
          subtitle="Templates feeding the ranking engine"
          icon={BriefcaseBusiness}
          accentClassName="bg-[linear-gradient(160deg,rgba(124,58,237,0.12),transparent)]"
        />
        <KpiCard
          title="Average Match Score"
          value={formatPercent(stats?.avg_match_score ?? 0, 1)}
          subtitle="Mean quality across all computed match results"
          icon={TrendingUp}
          accentClassName="bg-[linear-gradient(160deg,rgba(8,145,178,0.14),transparent)]"
        />
        <KpiCard
          title="Best Candidate"
          value={topCandidate ? topCandidate.name : "N/A"}
          subtitle={topCandidate ? `${formatPercent(topCandidate.avg_score, 1)} average fit across jobs` : "Run matching to surface leaders"}
          icon={Trophy}
          accentClassName="bg-[linear-gradient(160deg,rgba(245,158,11,0.16),transparent)]"
        />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Top skill distribution</CardTitle>
            <CardDescription>Candidate supply by normalized skill tags extracted from uploaded CVs.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {stats?.top_skills.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.top_skills}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip
                    cursor={{ fill: "rgba(148,163,184,0.06)" }}
                    contentStyle={{
                      background: "var(--popover)",
                      border: "1px solid var(--border)",
                      borderRadius: 20,
                    }}
                  />
                  <Bar dataKey="count" radius={[14, 14, 6, 6]}>
                    {stats.top_skills.map((item, index) => (
                      <Cell key={item.name} fill={chartColors[index % chartColors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={BrainCircuit}
                title="Skill analytics will appear here"
                description="Upload CVs or seed data to populate NLP-extracted skills and distribution charts."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Candidate experience mix</CardTitle>
            <CardDescription>Current talent pool segmented by years of professional experience.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {experienceBuckets.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={experienceBuckets} dataKey="value" nameKey="name" innerRadius={72} outerRadius={110} paddingAngle={3}>
                    {experienceBuckets.map((entry, index) => (
                      <Cell key={entry.name} fill={chartColors[index % chartColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: "var(--popover)",
                      border: "1px solid var(--border)",
                      borderRadius: 20,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={UsersRound}
                title="No candidate experience data"
                description="Once resumes are parsed, experience buckets will help show depth across the talent pool."
              />
            )}
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Card>
          <CardHeader>
            <CardTitle>Score distribution trend</CardTitle>
            <CardDescription>Weighted match quality bucketed across every saved match result in the database.</CardDescription>
          </CardHeader>
          <CardContent className="h-[320px]">
            {stats?.score_distribution.some((item) => item.count > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={stats?.score_distribution}>
                  <defs>
                    <linearGradient id="scoreTrend" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.45} />
                      <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="range" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <Tooltip
                    contentStyle={{
                      background: "var(--popover)",
                      border: "1px solid var(--border)",
                      borderRadius: 20,
                    }}
                  />
                  <Area type="monotone" dataKey="count" stroke="var(--chart-1)" strokeWidth={3} fill="url(#scoreTrend)" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState
                icon={Target}
                title="Matching history is empty"
                description="Launch matching from a job posting to generate scores, rankings, and explainable AI output."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top candidates</CardTitle>
            <CardDescription>Highest average fit scores across all jobs in the current demo database.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {stats?.best_candidates.length ? (
              stats.best_candidates.map((candidate, index) => (
                <div key={candidate.id} className="flex items-center justify-between rounded-[22px] border border-border bg-secondary/60 px-4 py-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-[18px] bg-primary/10 font-semibold text-primary">
                      {index + 1}
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-foreground">{candidate.name}</p>
                      <p className="text-xs text-muted-foreground">Across stored match results</p>
                    </div>
                  </div>
                  <Badge tone="brand">{formatPercent(candidate.avg_score, 1)}</Badge>
                </div>
              ))
            ) : (
              <EmptyState
                icon={Trophy}
                title="No ranked leaders yet"
                description="Once match results exist, this panel will highlight the strongest candidates."
                className="min-h-[240px]"
              />
            )}
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
