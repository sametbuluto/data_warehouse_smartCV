import { useEffect, useMemo, useState } from "react";
import { BrainCircuit, Eye, Radar, Search, SearchCheck, UsersRound } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import { Input } from "../components/ui/input";

import { explainMatch, getJobs, getMatchResults, runMatching } from "../api/client";
import { MatchExplanationDialog } from "../components/matching/match-explanation-dialog";
import { ScoreRing } from "../components/matching/score-ring";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { Progress } from "../components/ui/progress";
import { SectionHeading } from "../components/ui/section-heading";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { scoreBadgeTone } from "../lib/utils";
import type { Job, MatchExplanation, MatchResult } from "../types/api";

const CATEGORIES = [
  "All",
  "Sales & BD",
  "HR & Training",
  "Supply Chain",
  "Engineering",
  "Legal",
  "Finance",
  "Other",
] as const;

type Category = (typeof CATEGORIES)[number];

function inferCategory(title: string): Category {
  if (/sales|business development|customer success/i.test(title)) return "Sales & BD";
  if (/\bhr\b|human resources|talent|training|learning|compensation|benefit|instructional/i.test(title))
    return "HR & Training";
  if (/supply chain|procurement|sourcing|logistics|distribution/i.test(title)) return "Supply Chain";
  if (/engineer|engineering|mechanical|electrical|manufacturing/i.test(title)) return "Engineering";
  if (/lawyer|legal|\bip\b|attorney/i.test(title)) return "Legal";
  if (/financ|accounti|analyst/i.test(title)) return "Finance";
  return "Other";
}

export default function MatchingPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const jobQuery = searchParams.get("job");
  const candidateQuery = searchParams.get("candidate");

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string>(jobQuery ?? "");
  const [selectedCategory, setSelectedCategory] = useState<Category>("All");
  const [jobSearch, setJobSearch] = useState("");
  const [results, setResults] = useState<MatchResult[]>([]);
  const [selectedMatchId, setSelectedMatchId] = useState<number | null>(null);
  const [explanation, setExplanation] = useState<MatchExplanation | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [activeTab, setActiveTab] = useState<"rankings" | "insights">("rankings");

  useEffect(() => {
    getJobs()
      .then((data) => {
        setJobs(data);
        if (!jobQuery && data.length) {
          setSelectedJobId(String(data[0].id));
        }
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedJobId) {
      setResults([]);
      setExplanation(null);
      return;
    }

    getMatchResults(Number(selectedJobId))
      .then((data) => {
        setResults(data);

        if (candidateQuery) {
          const match = data.find((r) => String(r.candidate_id) === candidateQuery);
          if (match) {
            setSelectedMatchId(match.id);
            setActiveTab("insights");
            return;
          }
        }

        setSelectedMatchId(data[0]?.id ?? null);
      })
      .catch(() => {
        setResults([]);
        setSelectedMatchId(null);
        setExplanation(null);
      });
  }, [selectedJobId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!selectedMatchId) {
      setExplanation(null);
      return;
    }

    explainMatch(selectedMatchId)
      .then((data) => setExplanation(data))
      .catch(() => setExplanation(null));
  }, [selectedMatchId]);

  const selectedJob = useMemo(
    () => jobs.find((job) => String(job.id) === selectedJobId) ?? null,
    [jobs, selectedJobId],
  );

  const categorizedJobs = useMemo(() => {
    const byCategory = selectedCategory === "All" ? jobs : jobs.filter((j) => inferCategory(j.title) === selectedCategory);
    const q = jobSearch.trim().toLowerCase();
    if (!q) return byCategory;
    return byCategory.filter(
      (j) =>
        j.title.toLowerCase().includes(q) ||
        j.required_skills.some((s) => s.toLowerCase().includes(q)),
    );
  }, [jobs, selectedCategory, jobSearch]);

  const availableCategories = useMemo(() => {
    const used = new Set(jobs.map((j) => inferCategory(j.title)));
    return CATEGORIES.filter((c) => c === "All" || used.has(c));
  }, [jobs]);

  const handleRunMatching = async () => {
    if (!selectedJobId) return;
    setRunning(true);
    try {
      await runMatching(Number(selectedJobId));
    } catch {
      setRunning(false);
      return;
    }
    try {
      const refreshed = await getMatchResults(Number(selectedJobId));
      setResults(refreshed);
      setSelectedMatchId(refreshed[0]?.id ?? null);
    } catch {
      // results couldn't be fetched
    }
    setActiveTab("rankings");
    setRunning(false);
  };

  const handleSelectJob = (jobId: string) => {
    setSelectedJobId(jobId);
    setSearchParams(jobId ? { job: jobId } : {});
  };

  const handleSelectCandidate = (matchId: number) => {
    setSelectedMatchId(matchId);
    setActiveTab("insights");
  };

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Ranking Engine"
        title="Inspect ranked candidates and explainable AI fit signals for each role."
        description="Browse job postings by category, select a role, and view AI-ranked candidates with explainable scores."
        action={
          <Button onClick={handleRunMatching} disabled={!selectedJobId || running}>
            <Radar className="h-4 w-4" />
            {running ? "Recomputing..." : "Run Matching"}
          </Button>
        }
      />

      {loading ? null : !jobs.length ? (
        <EmptyState
          icon={SearchCheck}
          title="No job postings available"
          description="Create a job posting first, then this page will rank candidates and explain every score."
        />
      ) : (
        <>
          {/* ── Category + Job selector ── */}
          <div className="space-y-3">
            <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <p className="text-sm text-muted-foreground">
                {categorizedJobs.length} job{categorizedJobs.length === 1 ? "" : "s"} in {selectedCategory}
                {jobSearch ? ` matching "${jobSearch}"` : ""}
              </p>
              <div className="relative w-full lg:max-w-sm">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  className="pl-9"
                  value={jobSearch}
                  onChange={(event) => setJobSearch(event.target.value)}
                  placeholder="Search jobs by title or required skill..."
                />
              </div>
            </div>
            {/* Category scroll bar */}
            <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
              {availableCategories.map((cat) => (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  className={[
                    "shrink-0 rounded-full px-4 py-1.5 text-sm font-medium transition",
                    selectedCategory === cat
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "border border-border bg-secondary/60 text-muted-foreground hover:bg-accent hover:text-foreground",
                  ].join(" ")}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Job cards horizontal scroll */}
            <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-none">
              {categorizedJobs.map((job) => {
                const isActive = String(job.id) === selectedJobId;
                return (
                  <button
                    key={job.id}
                    type="button"
                    onClick={() => handleSelectJob(String(job.id))}
                    className={[
                      "shrink-0 rounded-2xl border p-4 text-left transition w-[220px]",
                      isActive
                        ? "border-primary/40 bg-primary/8 shadow-[0_8px_24px_rgba(37,99,235,0.12)]"
                        : "border-border bg-secondary/55 hover:bg-accent",
                    ].join(" ")}
                  >
                    <p className="text-[11px] font-medium uppercase tracking-widest text-muted-foreground mb-1">
                      {inferCategory(job.title)}
                    </p>
                    <p className="text-sm font-semibold text-foreground leading-snug line-clamp-2">{job.title}</p>
                    <div className="mt-2 flex gap-1.5 flex-wrap">
                      <span className="rounded-full bg-primary/10 px-2 py-0.5 text-[11px] text-primary font-medium">
                        {job.min_experience}+ yrs
                      </span>
                      <span className="rounded-full bg-primary/10 px-2 py-0.5 text-[11px] text-primary font-medium">
                        {job.required_skills.length} skills
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* ── Rankings + Insights ── */}

          {/* Narrow screens: tab layout */}
          <div className="xl:hidden">
            <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as typeof activeTab)}>
              <TabsList className="mb-4">
                <TabsTrigger value="rankings" className="flex items-center gap-2">
                  <UsersRound className="h-4 w-4" />
                  Rankings
                  {results.length ? (
                    <span className="rounded-full bg-primary/15 px-2 py-0.5 text-[11px] font-semibold text-primary">
                      {results.length}
                    </span>
                  ) : null}
                </TabsTrigger>
                <TabsTrigger value="insights" className="flex items-center gap-2">
                  <BrainCircuit className="h-4 w-4" />
                  AI Insights
                  {explanation ? <span className="h-2 w-2 rounded-full bg-success" /> : null}
                </TabsTrigger>
              </TabsList>

              <TabsContent value="rankings">
                <RankingCard
                  selectedJob={selectedJob}
                  results={results}
                  selectedMatchId={selectedMatchId}
                  onSelect={handleSelectCandidate}
                />
              </TabsContent>

              <TabsContent value="insights">
                <InsightsCard explanation={explanation} onOpenDialog={() => setDialogOpen(true)} sticky={false} />
              </TabsContent>
            </Tabs>
          </div>

          {/* Wide screens: two-column layout */}
          <div className="hidden gap-6 xl:grid xl:grid-cols-[1.05fr_0.95fr]">
            <RankingCard
              selectedJob={selectedJob}
              results={results}
              selectedMatchId={selectedMatchId}
              onSelect={handleSelectCandidate}
            />
            <InsightsCard explanation={explanation} onOpenDialog={() => setDialogOpen(true)} sticky />
          </div>
        </>
      )}

      <MatchExplanationDialog open={dialogOpen} onOpenChange={setDialogOpen} explanation={explanation} />
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────────

interface RankingCardProps {
  selectedJob: Job | null;
  results: MatchResult[];
  selectedMatchId: number | null;
  onSelect: (id: number) => void;
}

function RankingCard({ selectedJob, results, selectedMatchId, onSelect }: RankingCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{selectedJob?.title || "Candidate ranking"}</CardTitle>
        <CardDescription>
          {selectedJob
            ? `${selectedJob.min_experience}+ years • ${selectedJob.education_level} • ${selectedJob.required_skills.length} required skills`
            : "Select a job to review rankings"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {results.length ? (
          <div className="space-y-4">
            {results.map((result, index) => (
              <button
                key={result.id}
                type="button"
                className={[
                  "w-full rounded-[28px] border p-5 text-left transition",
                  result.id === selectedMatchId
                    ? "border-primary/30 bg-primary/8 shadow-[0_18px_50px_rgba(37,99,235,0.12)]"
                    : "border-border bg-secondary/55 hover:bg-accent",
                ].join(" ")}
                onClick={() => onSelect(result.id)}
              >
                <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
                  <div className="flex items-center gap-4">
                    <div className="flex h-11 w-11 items-center justify-center rounded-[18px] bg-primary/10 font-semibold text-primary">
                      {index + 1}
                    </div>
                    <ScoreRing score={result.final_score} size={72} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                      <div>
                        <h3 className="text-lg font-semibold tracking-tight text-foreground">{result.candidate_name}</h3>
                        <div className="mt-1 flex items-center gap-2">
                          <Badge tone={scoreBadgeTone(result.final_score)}>{Math.round(result.final_score)}%</Badge>
                          <span className="text-sm text-muted-foreground">
                            Skill {result.skill_score.toFixed(1)} • Exp {result.experience_score.toFixed(1)} • Edu{" "}
                            {result.education_score.toFixed(1)} • Sem {result.semantic_score.toFixed(1)}
                          </span>
                        </div>
                      </div>
                      <div className="min-w-[180px] space-y-2">
                        <Progress value={result.final_score} />
                        <p className="text-right text-xs text-muted-foreground">Weighted final score</p>
                      </div>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {result.matched_skills.slice(0, 4).map((skill) => (
                        <Badge key={skill} tone="success">{skill}</Badge>
                      ))}
                      {result.missing_skills.slice(0, 3).map((skill) => (
                        <Badge key={skill} tone="danger">{skill}</Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <EmptyState
            icon={UsersRound}
            title="No ranked candidates yet"
            description="Run matching for this job to generate candidate ordering, skill gaps, and AI explanations."
          />
        )}
      </CardContent>
    </Card>
  );
}

interface InsightsCardProps {
  explanation: MatchExplanation | null;
  onOpenDialog: () => void;
  sticky: boolean;
}

function InsightsCard({ explanation, onOpenDialog, sticky }: InsightsCardProps) {
  return (
    <Card className={["h-fit", sticky ? "xl:sticky xl:top-[104px]" : ""].join(" ")}>
      <CardHeader>
        <CardTitle>AI Insights</CardTitle>
        <CardDescription>Explainable recommendation panel for the selected match result.</CardDescription>
      </CardHeader>
      <CardContent>
        {explanation ? (
          <div className="space-y-5">
            <div className="hero-panel rounded-[30px] p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.22em] text-primary/80">Candidate summary</p>
                  <h3 className="mt-2 text-xl font-semibold tracking-tight text-foreground">{explanation.candidate_name}</h3>
                  <p className="mt-2 text-sm leading-7 text-muted-foreground">{explanation.job_title}</p>
                </div>
                <ScoreRing score={explanation.final_score} size={88} />
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              {[
                { label: "Matched skills", value: explanation.matched_skills.length, color: "success" as const },
                { label: "Missing skills", value: explanation.missing_skills.length, color: "danger" as const },
                { label: "Experience score", value: explanation.experience_score.toFixed(1), color: "brand" as const },
                { label: "Semantic score", value: explanation.semantic_score.toFixed(1), color: "brand" as const },
              ].map((item) => (
                <div key={item.label} className="rounded-[24px] border border-border bg-secondary/55 p-4">
                  <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{item.label}</p>
                  <div className="mt-2">
                    <Badge tone={item.color}>{item.value}</Badge>
                  </div>
                </div>
              ))}
            </div>

            <div className="space-y-3">
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-sm font-semibold text-foreground">Matched skills</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {explanation.matched_skills.length ? (
                    explanation.matched_skills.map((skill) => (
                      <Badge key={skill} tone="success">{skill}</Badge>
                    ))
                  ) : (
                    <Badge>No matched skills</Badge>
                  )}
                </div>
              </div>
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-sm font-semibold text-foreground">Missing skills</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {explanation.missing_skills.length ? (
                    explanation.missing_skills.map((skill) => (
                      <Badge key={skill} tone="danger">{skill}</Badge>
                    ))
                  ) : (
                    <Badge tone="success">No critical skill gaps</Badge>
                  )}
                </div>
              </div>
            </div>

            <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
              <div className="mb-2 flex items-center gap-2">
                <BrainCircuit className="h-4 w-4 text-primary" />
                <p className="text-sm font-semibold text-foreground">Recommendation</p>
              </div>
              <p className="text-sm leading-7 text-muted-foreground">{explanation.explanation}</p>
            </div>

            <Button variant="secondary" className="w-full" onClick={onOpenDialog}>
              <Eye className="h-4 w-4" />
              Open Full Explanation
            </Button>
          </div>
        ) : (
          <EmptyState
            icon={BrainCircuit}
            title="Select a ranked candidate"
            description="Choose a candidate from the ranking panel to inspect AI-generated matching details."
          />
        )}
      </CardContent>
    </Card>
  );
}
