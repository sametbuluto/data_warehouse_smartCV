import { useDeferredValue, useEffect, useMemo, useState } from "react";
import { FileSearch, Radar, Search, Trash2, UsersRound } from "lucide-react";

import {
  deleteCandidate,
  getCandidate,
  getCandidateMatches,
  getCandidates,
  runCandidateMatching,
} from "../api/client";
import { ScoreRing } from "../components/matching/score-ring";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { SectionHeading } from "../components/ui/section-heading";
import { Skeleton } from "../components/ui/skeleton";
import { formatRelativeDate } from "../lib/utils";
import type { Candidate, CandidateListItem, MatchResult } from "../types/api";

const pageSize = 8;

export default function CandidatesPage() {
  const [candidates, setCandidates] = useState<CandidateListItem[]>([]);
  const [selectedCandidateId, setSelectedCandidateId] = useState<number | null>(null);
  const [candidateDetail, setCandidateDetail] = useState<Candidate | null>(null);
  const [candidateMatches, setCandidateMatches] = useState<MatchResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [profileLoading, setProfileLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  const refreshCandidates = async () => {
    const data = await getCandidates();
    setCandidates(data);
    if (!selectedCandidateId && data.length) setSelectedCandidateId(data[0].id);
    if (selectedCandidateId && !data.some((candidate) => candidate.id === selectedCandidateId)) {
      setSelectedCandidateId(data[0]?.id ?? null);
    }
  };

  useEffect(() => {
    refreshCandidates().finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedCandidateId) {
      setCandidateDetail(null);
      setCandidateMatches([]);
      return;
    }

    setProfileLoading(true);
    Promise.all([
      getCandidate(selectedCandidateId),
      getCandidateMatches(selectedCandidateId).catch(() => [] as MatchResult[]),
    ])
      .then(([detail, matches]) => {
        setCandidateDetail(detail);
        setCandidateMatches(matches);
      })
      .finally(() => setProfileLoading(false));
  }, [selectedCandidateId]);

  const deferredSearch = useDeferredValue(search);

  const filteredCandidates = useMemo(() => {
    const query = deferredSearch.toLowerCase().trim();
    if (!query) return candidates;

    return candidates.filter((candidate) => {
      return (
        candidate.name.toLowerCase().includes(query) ||
        (candidate.email ?? "").toLowerCase().includes(query)
      );
    });
  }, [candidates, deferredSearch]);

  const totalPages = Math.max(1, Math.ceil(filteredCandidates.length / pageSize));
  const paginatedCandidates = filteredCandidates.slice((page - 1) * pageSize, page * pageSize);

  useEffect(() => {
    setPage(1);
  }, [deferredSearch]);

  const selectedSummary = candidates.find((candidate) => candidate.id === selectedCandidateId);

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Talent Workspace"
        title="Review parsed candidates and their compatibility across your job library."
        description="The candidate view combines CV metadata with reusable match history, so you can show both raw extraction quality and hiring fit in one place."
      />

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <CardHeader className="gap-4">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <CardTitle>Candidate directory</CardTitle>
                <CardDescription>Sortable talent list with persistent profile selection.</CardDescription>
              </div>
              <div className="relative w-full lg:max-w-sm">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input className="pl-9" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by candidate or email..." />
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-3">
                {Array.from({ length: 6 }).map((_, index) => (
                  <Skeleton key={index} className="h-20 w-full" />
                ))}
              </div>
            ) : filteredCandidates.length ? (
              <div className="overflow-hidden rounded-[28px] border border-border">
                <div className="max-h-[620px] overflow-auto">
                  <table className="min-w-full divide-y divide-border text-left">
                    <thead className="sticky top-0 bg-popover/90 backdrop-blur-xl">
                      <tr className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                        <th className="px-4 py-3 font-medium">Candidate</th>
                        <th className="px-4 py-3 font-medium">Experience</th>
                        <th className="px-4 py-3 font-medium">Skills</th>
                        <th className="px-4 py-3 font-medium">Created</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border">
                      {paginatedCandidates.map((candidate) => (
                        <tr
                          key={candidate.id}
                          className={[
                            "cursor-pointer transition hover:bg-accent/70",
                            candidate.id === selectedCandidateId ? "bg-primary/8" : "",
                          ].join(" ")}
                          onClick={() => setSelectedCandidateId(candidate.id)}
                        >
                          <td className="px-4 py-4">
                            <div>
                              <p className="font-medium text-foreground">{candidate.name}</p>
                              <p className="text-sm text-muted-foreground">{candidate.email || "No email extracted"}</p>
                            </div>
                          </td>
                          <td className="px-4 py-4 text-sm text-foreground">{candidate.experience_years} yrs</td>
                          <td className="px-4 py-4 text-sm text-foreground">{candidate.skills_count}</td>
                          <td className="px-4 py-4 text-sm text-muted-foreground">{formatRelativeDate(candidate.created_at)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="flex items-center justify-between border-t border-border px-4 py-3 text-sm text-muted-foreground">
                  <span>
                    Page {page} of {totalPages}
                  </span>
                  <div className="flex gap-2">
                    <Button variant="secondary" size="sm" disabled={page === 1} onClick={() => setPage((current) => current - 1)}>
                      Prev
                    </Button>
                    <Button
                      variant="secondary"
                      size="sm"
                      disabled={page === totalPages}
                      onClick={() => setPage((current) => current + 1)}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              </div>
            ) : (
              <EmptyState
                icon={UsersRound}
                title="No candidates found"
                description="Upload resumes to populate the candidate workspace and unlock ranking flows."
              />
            )}
          </CardContent>
        </Card>

        <Card className="h-fit xl:sticky xl:top-[104px]">
          <CardHeader>
            <CardTitle>Candidate profile</CardTitle>
            <CardDescription>Detailed extraction preview plus cross-job match visibility for the selected CV.</CardDescription>
          </CardHeader>
          <CardContent>
            {profileLoading ? (
              <div className="space-y-3">
                <Skeleton className="h-28 w-full" />
                <Skeleton className="h-20 w-full" />
                <Skeleton className="h-52 w-full" />
              </div>
            ) : candidateDetail && selectedSummary ? (
              <div className="space-y-5">
                <div className="rounded-[28px] border border-border bg-secondary/55 p-5">
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <h3 className="text-xl font-semibold tracking-tight text-foreground">{candidateDetail.name}</h3>
                      <p className="mt-1 text-sm text-muted-foreground">{candidateDetail.email || "No email extracted"}</p>
                      <p className="text-sm text-muted-foreground">{candidateDetail.phone || "No phone extracted"}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="secondary"
                        onClick={async () => {
                          await runCandidateMatching(candidateDetail.id);
                          const matches = await getCandidateMatches(candidateDetail.id).catch(() => [] as MatchResult[]);
                          setCandidateMatches(matches);
                        }}
                      >
                        <Radar className="h-4 w-4" />
                        Refresh matches
                      </Button>
                      <Button
                        variant="danger"
                        onClick={async () => {
                          await deleteCandidate(candidateDetail.id);
                          await refreshCandidates();
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  <div className="mt-4 grid gap-3 sm:grid-cols-3">
                    <div className="rounded-[22px] border border-border bg-card/60 p-4">
                      <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Experience</p>
                      <p className="mt-2 text-sm font-semibold text-foreground">{candidateDetail.experience_years} years</p>
                    </div>
                    <div className="rounded-[22px] border border-border bg-card/60 p-4">
                      <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Education</p>
                      <p className="mt-2 text-sm font-semibold text-foreground">{candidateDetail.education || "Unknown"}</p>
                    </div>
                    <div className="rounded-[22px] border border-border bg-card/60 p-4">
                      <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Skills</p>
                      <p className="mt-2 text-sm font-semibold text-foreground">{selectedSummary.skills_count} extracted</p>
                    </div>
                  </div>

                  <div className="mt-4 flex flex-wrap gap-2">
                    {candidateDetail.skills.map((skill) => (
                      <Badge key={skill} tone="brand">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-semibold text-foreground">Job compatibility</h4>
                    <Badge>{candidateMatches.length} stored matches</Badge>
                  </div>
                  {candidateMatches.length ? (
                    candidateMatches.slice(0, 4).map((match) => (
                      <div key={match.id} className="flex items-center gap-4 rounded-[24px] border border-border bg-secondary/55 p-4">
                        <ScoreRing score={match.final_score} size={68} />
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-semibold text-foreground">{match.job_title}</p>
                          <p className="mt-1 text-xs text-muted-foreground">
                            Skill {match.skill_score.toFixed(1)} • Semantic {match.semantic_score.toFixed(1)}
                          </p>
                          <div className="mt-3 flex flex-wrap gap-2">
                            {match.matched_skills.slice(0, 3).map((skill) => (
                              <Badge key={skill} tone="success">
                                {skill}
                              </Badge>
                            ))}
                            {match.missing_skills.slice(0, 2).map((skill) => (
                              <Badge key={skill} tone="danger">
                                {skill}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <EmptyState
                      icon={FileSearch}
                      title="No cross-job matches yet"
                      description="Run candidate matching to show how this CV scores against every job posting."
                      className="min-h-[240px]"
                    />
                  )}
                </div>
              </div>
            ) : (
              <EmptyState
                icon={UsersRound}
                title="Select a candidate"
                description="Choose a resume from the table to inspect extracted profile details and job fit."
              />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
