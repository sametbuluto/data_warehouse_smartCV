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
import { ActivitySquare, BarChart3, ChartPie, DatabaseZap } from "lucide-react";

import { getCandidates, getDashboard, getJobs } from "../api/client";
import { Badge } from "../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { SectionHeading } from "../components/ui/section-heading";
import type { CandidateListItem, DashboardStats, Job } from "../types/api";

const colors = ["var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)"];

export default function AnalyticsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [candidates, setCandidates] = useState<CandidateListItem[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    Promise.all([getDashboard(), getCandidates(), getJobs()]).then(([dashboardData, candidateData, jobData]) => {
      setStats(dashboardData);
      setCandidates(candidateData);
      setJobs(jobData);
    });
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

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Presentation Analytics"
        title="Show the intelligence behind the recruitment demo, not just the interface."
        description="These charts highlight candidate supply, match quality, education requirements, and the normalized skill landscape used by the matching engine."
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

      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top skills</CardTitle>
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
            <CardTitle>Match score trend</CardTitle>
            <CardDescription>Distribution of final weighted scores across every stored ranking result.</CardDescription>
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
                description="Run matching to populate distribution trends for your presentation."
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
                description="Upload candidate CVs to view how the dataset is distributed across experience ranges."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Job education requirements</CardTitle>
            <CardDescription>How academic expectations are distributed across active job templates.</CardDescription>
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
                description="Create job postings to visualize education requirements and role structure."
              />
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Best candidates overview</CardTitle>
          <CardDescription>Quick leaderboard for the strongest average candidates in the current dataset.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          {stats?.best_candidates.length ? (
            stats.best_candidates.map((candidate) => (
              <div key={candidate.id} className="rounded-[24px] border border-border bg-secondary/55 px-4 py-3">
                <p className="text-sm font-semibold text-foreground">{candidate.name}</p>
                <div className="mt-2">
                  <Badge tone="brand">{candidate.avg_score.toFixed(1)}%</Badge>
                </div>
              </div>
            ))
          ) : (
            <EmptyState
              icon={UsersRound}
              title="Leaderboard unavailable"
              description="Candidate rankings will appear after the first matching run."
              className="w-full"
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
