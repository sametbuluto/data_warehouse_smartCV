import { useEffect, useMemo, useState } from "react";
import { BrainCircuit, Eye, Radar, SearchCheck, UsersRound } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import { explainMatch, getJobs, getMatchResults, runMatching } from "../api/client";
import { MatchExplanationDialog } from "../components/matching/match-explanation-dialog";
import { ScoreRing } from "../components/matching/score-ring";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { Progress } from "../components/ui/progress";
import { SectionHeading } from "../components/ui/section-heading";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import type { Job, MatchExplanation, MatchResult } from "../types/api";

export default function MatchingPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const jobQuery = searchParams.get("job");

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string>(jobQuery ?? "");
  const [results, setResults] = useState<MatchResult[]>([]);
  const [selectedMatchId, setSelectedMatchId] = useState<number | null>(null);
  const [explanation, setExplanation] = useState<MatchExplanation | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

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
        setSelectedMatchId(data[0]?.id ?? null);
      })
      .catch(() => {
        setResults([]);
        setSelectedMatchId(null);
        setExplanation(null);
      });
  }, [selectedJobId]);

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

  const handleRunMatching = async () => {
    if (!selectedJobId) return;
    setRunning(true);
    try {
      await runMatching(Number(selectedJobId));
      const refreshed = await getMatchResults(Number(selectedJobId));
      setResults(refreshed);
      setSelectedMatchId(refreshed[0]?.id ?? null);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Ranking Engine"
        title="Inspect ranked candidates and explainable AI fit signals for each role."
        description="This page is built for demos: stable layout, clear score hierarchy, skill-gap visibility, and a dedicated AI insights panel."
        action={
          <div className="flex flex-wrap gap-3">
            <Select
              value={selectedJobId}
              onValueChange={(value) => {
                setSelectedJobId(value);
                setSearchParams(value ? { job: value } : {});
              }}
            >
              <SelectTrigger className="min-w-[260px]">
                <SelectValue placeholder="Select a job" />
              </SelectTrigger>
              <SelectContent>
                {jobs.map((job) => (
                  <SelectItem key={job.id} value={String(job.id)}>
                    {job.title}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={handleRunMatching} disabled={!selectedJobId || running}>
              <Radar className="h-4 w-4" />
              {running ? "Recomputing..." : "Run Matching"}
            </Button>
          </div>
        }
      />

      {loading ? null : !jobs.length ? (
        <EmptyState
          icon={SearchCheck}
          title="No job postings available"
          description="Create a job posting first, then this page will rank candidates and explain every score."
        />
      ) : (
        <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
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
                      onClick={() => setSelectedMatchId(result.id)}
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
                              <p className="mt-1 text-sm text-muted-foreground">
                                Skill {result.skill_score.toFixed(1)} • Experience {result.experience_score.toFixed(1)} • Education{" "}
                                {result.education_score.toFixed(1)} • Semantic {result.semantic_score.toFixed(1)}
                              </p>
                            </div>
                            <div className="min-w-[180px] space-y-2">
                              <Progress value={result.final_score} />
                              <p className="text-right text-xs text-muted-foreground">Weighted final score</p>
                            </div>
                          </div>

                          <div className="mt-4 flex flex-wrap gap-2">
                            {result.matched_skills.slice(0, 4).map((skill) => (
                              <Badge key={skill} tone="success">
                                {skill}
                              </Badge>
                            ))}
                            {result.missing_skills.slice(0, 3).map((skill) => (
                              <Badge key={skill} tone="danger">
                                {skill}
                              </Badge>
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

          <Card className="h-fit xl:sticky xl:top-[104px]">
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
                            <Badge key={skill} tone="success">
                              {skill}
                            </Badge>
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
                            <Badge key={skill} tone="danger">
                              {skill}
                            </Badge>
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

                  <Button variant="secondary" className="w-full" onClick={() => setDialogOpen(true)}>
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
        </div>
      )}

      <MatchExplanationDialog open={dialogOpen} onOpenChange={setDialogOpen} explanation={explanation} />
    </div>
  );
}
