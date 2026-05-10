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
import { Legend, Line, LineChart } from "recharts";
import { ActivitySquare, BarChart3, ChartPie, DatabaseZap, Trophy, UsersRound } from "lucide-react";

import { getAnalyticsInsights, getCandidates, getDashboard, getJobs } from "../api/client";
import { Badge } from "../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { SectionHeading } from "../components/ui/section-heading";
import { Skeleton } from "../components/ui/skeleton";
import type { AnalyticsInsights, CandidateListItem, DashboardStats, Job } from "../types/api";

const colors = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)"];

export default function AnalyticsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [insights, setInsights] = useState<AnalyticsInsights | null>(null);
  const [candidates, setCandidates] = useState<CandidateListItem[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getDashboard(), getAnalyticsInsights(), getCandidates(), getJobs()])
      .then(([dashboardData, insightsData, candidateData, jobData]) => {
        setStats(dashboardData);
        setInsights(insightsData);
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

  const categoryCoverage = useMemo(() => {
    const categorize = (title: string): string => {
      const t = title.toLowerCase();
      if (/sales|business development|customer success/.test(t)) return "Sales & BD";
      if (/\bhr\b|talent|training|learning|compensation|benefit|instructional/.test(t)) return "HR & Training";
      if (/supply chain|procurement|sourcing|logistics|distribution/.test(t)) return "Supply Chain";
      if (/engineer|engineering|mechanical|electrical|manufacturing/.test(t)) return "Engineering";
      if (/lawyer|legal|\bip\b|attorney|gdpr|privacy/.test(t)) return "Legal";
      if (/financ|accounti|treasury|risk|investment|equity|aml/.test(t)) return "Finance";
      if (/marketing|seo|brand|content/.test(t)) return "Marketing";
      if (/health|clinical|hospital|pharma/.test(t)) return "Healthcare";
      return "Tech";
    };
    const counts = new Map<string, number>();
    jobs.forEach((j) => counts.set(categorize(j.title), (counts.get(categorize(j.title)) ?? 0) + 1));
    return Array.from(counts.entries())
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value);
  }, [jobs]);

  const skillDemand = useMemo(() => {
    const counts = new Map<string, number>();
    jobs.forEach((j) =>
      j.required_skills.forEach((s) => counts.set(s.toLowerCase(), (counts.get(s.toLowerCase()) ?? 0) + 1)),
    );
    return Array.from(counts.entries())
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8);
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

      <div className="grid gap-4 md:grid-cols-3">
        {[
          { icon: DatabaseZap, label: "Candidates", value: stats?.total_candidates ?? 0 },
          { icon: ActivitySquare, label: "Jobs", value: stats?.total_jobs ?? 0 },
          { icon: BarChart3, label: "Matches", value: stats?.total_matches ?? 0 },
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
            <CardTitle>Skill demand vs supply</CardTitle>
            <CardDescription>
              For every top-demanded skill: how many jobs require it (demand) vs how many candidates have it (supply).
              Skills where the gap is small reveal hiring pressure points.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[360px]">
            {insights?.skill_supply_demand.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={insights.skill_supply_demand} margin={{ top: 8, right: 8, left: 0, bottom: 24 }}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="skill" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={11} angle={-25} textAnchor="end" height={50} />
                  <YAxis stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Legend wrapperStyle={{ fontSize: 12 }} />
                  <Bar dataKey="demand" fill="var(--chart-1)" radius={[8, 8, 0, 0]} name="Jobs requiring (demand)" />
                  <Bar dataKey="supply" fill="var(--chart-3)" radius={[8, 8, 0, 0]} name="Candidates with (supply)" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState icon={BarChart3} title="No skills available" description="Add jobs and candidates to see demand vs supply." />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Match quality by category</CardTitle>
            <CardDescription>
              Average top-1 candidate score per category. Higher = a strong champion exists for that role family;
              lower = the talent pool is thin in that area.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[360px]">
            {insights?.category_quality.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={insights.category_quality} layout="vertical" margin={{ left: 16, right: 24 }}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <YAxis type="category" dataKey="category" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} width={120} fontSize={12} />
                  <Tooltip
                    contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }}
                    formatter={((v: unknown, _n: unknown, item: { payload: { job_count: number } }) => [
                      `${Number(v).toFixed(1)}% · ${item.payload.job_count} jobs`,
                      "Avg top score",
                    ]) as never}
                  />
                  <Bar dataKey="avg_top_score" radius={[6, 14, 14, 6]}>
                    {insights.category_quality.map((c, i) => (
                      <Cell key={c.category} fill={colors[i % colors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState icon={ChartPie} title="No category quality yet" description="Run matching to populate category scores." />
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Experience vs avg score</CardTitle>
            <CardDescription>
              Candidates grouped by experience years; line shows the average match score for that band.
              Senior candidates should trend higher — if not, your job descriptions may be skewed.
            </CardDescription>
          </CardHeader>
          <CardContent className="h-[360px]">
            {insights?.experience_score.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={insights.experience_score} margin={{ top: 8, right: 24, left: 0, bottom: 0 }}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
                  <XAxis dataKey="band" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <YAxis domain={[0, 100]} stroke="var(--muted-foreground)" tickLine={false} axisLine={false} fontSize={12} />
                  <Tooltip
                    contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }}
                    formatter={((v: unknown, _n: unknown, item: { payload: { candidates: number } }) => [
                      `${Number(v).toFixed(1)}% · ${item.payload.candidates} candidates`,
                      "Avg score",
                    ]) as never}
                  />
                  <Line type="monotone" dataKey="avg_score" stroke="var(--chart-2)" strokeWidth={3} dot={{ r: 5, fill: "var(--chart-2)" }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState icon={ActivitySquare} title="No experience data" description="Upload candidates and run matching to populate." />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Trophy className="h-4 w-4 text-primary" />
              <CardTitle>Top jobs by champion score</CardTitle>
            </div>
            <CardDescription>The 8 roles with the strongest top-1 candidate in the warehouse.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {insights?.top_jobs_by_champion.length ? (
              insights.top_jobs_by_champion.map((row, idx) => (
                <div key={row.job_id} className="flex items-center justify-between gap-3 rounded-[24px] border border-border bg-secondary/55 p-4">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-primary/10 font-semibold text-primary">
                      {idx + 1}
                    </div>
                    <div className="min-w-0">
                      <p className="truncate text-sm font-semibold text-foreground">{row.job_title}</p>
                      <p className="mt-0.5 text-xs text-muted-foreground">
                        {row.champion_name} · {row.category}
                      </p>
                    </div>
                  </div>
                  <Badge tone="success">{row.top_score.toFixed(1)}%</Badge>
                </div>
              ))
            ) : (
              <EmptyState
                icon={UsersRound}
                title="No champions yet"
                description="Run matching across jobs to surface top candidates."
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
            <CardTitle>Job postings by category</CardTitle>
            <CardDescription>How the live job library is distributed across functional areas.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {categoryCoverage.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categoryCoverage} layout="vertical" margin={{ left: 16, right: 16 }}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" horizontal={false} />
                  <XAxis type="number" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <YAxis type="category" dataKey="name" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} width={110} fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Bar dataKey="value" radius={[6, 14, 14, 6]}>
                    {categoryCoverage.map((c, i) => (
                      <Cell key={c.name} fill={colors[i % colors.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState icon={DatabaseZap} title="No job templates yet" description="Add postings to see category breakdown." />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Most demanded skills (job side)</CardTitle>
            <CardDescription>How often each skill appears in required-skill lists across all postings.</CardDescription>
          </CardHeader>
          <CardContent className="h-[340px]">
            {skillDemand.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={skillDemand} layout="vertical" margin={{ left: 16, right: 16 }}>
                  <CartesianGrid stroke="rgba(148,163,184,0.12)" horizontal={false} />
                  <XAxis type="number" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} />
                  <YAxis type="category" dataKey="name" stroke="var(--muted-foreground)" tickLine={false} axisLine={false} width={110} fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)", borderRadius: 20 }} />
                  <Bar dataKey="count" radius={[6, 14, 14, 6]} fill="var(--chart-4)" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState icon={BarChart3} title="No required skills yet" description="Add postings with required skills to view demand." />
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
