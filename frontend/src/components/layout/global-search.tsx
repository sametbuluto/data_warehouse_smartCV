import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { BriefcaseBusiness, Search, Tag, UsersRound } from "lucide-react";

import { getCandidates, getJobs } from "../../api/client";
import { Input } from "../ui/input";
import type { CandidateListItem, Job } from "../../types/api";

type Result =
  | { kind: "candidate"; id: number; label: string; sub: string }
  | { kind: "job"; id: number; label: string; sub: string }
  | { kind: "skill"; label: string; sub: string };

const MAX_PER_GROUP = 4;

export function GlobalSearch() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [candidates, setCandidates] = useState<CandidateListItem[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    Promise.all([getCandidates().catch(() => []), getJobs().catch(() => [])]).then(([c, j]) => {
      setCandidates(c);
      setJobs(j);
    });
  }, []);

  useEffect(() => {
    const onClick = (event: MouseEvent) => {
      if (!containerRef.current) return;
      if (!containerRef.current.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  const results = useMemo<Result[]>(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];

    const candidateHits: Result[] = candidates
      .filter((c) => c.name.toLowerCase().includes(q) || (c.email ?? "").toLowerCase().includes(q))
      .slice(0, MAX_PER_GROUP)
      .map((c) => ({ kind: "candidate", id: c.id, label: c.name, sub: c.email || `${c.experience_years} yrs` }));

    const jobHits: Result[] = jobs
      .filter((j) => j.title.toLowerCase().includes(q) || j.required_skills.some((s) => s.toLowerCase().includes(q)))
      .slice(0, MAX_PER_GROUP)
      .map((j) => ({ kind: "job", id: j.id, label: j.title, sub: `${j.min_experience}+ yrs • ${j.required_skills.length} skills` }));

    const skillSet = new Map<string, number>();
    jobs.forEach((j) =>
      j.required_skills.forEach((s) => {
        if (s.toLowerCase().includes(q)) skillSet.set(s.toLowerCase(), (skillSet.get(s.toLowerCase()) ?? 0) + 1);
      }),
    );
    const skillHits: Result[] = Array.from(skillSet.entries())
      .slice(0, MAX_PER_GROUP)
      .map(([s, n]) => ({ kind: "skill", label: s, sub: `${n} job${n === 1 ? "" : "s"} require this skill` }));

    return [...candidateHits, ...jobHits, ...skillHits];
  }, [query, candidates, jobs]);

  const handleSelect = (r: Result) => {
    setOpen(false);
    setQuery("");
    if (r.kind === "candidate") navigate(`/candidates?q=${encodeURIComponent(r.label)}`);
    else if (r.kind === "job") navigate(`/matching?job=${r.id}`);
    else navigate(`/jobs?q=${encodeURIComponent(r.label)}`);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && results.length) {
      event.preventDefault();
      handleSelect(results[0]);
    } else if (event.key === "Escape") {
      setOpen(false);
    }
  };

  const groupedSections = useMemo(() => {
    const candidatesGroup = results.filter((r) => r.kind === "candidate");
    const jobsGroup = results.filter((r) => r.kind === "job");
    const skillsGroup = results.filter((r) => r.kind === "skill");
    return [
      { title: "Candidates", icon: UsersRound, items: candidatesGroup },
      { title: "Jobs", icon: BriefcaseBusiness, items: jobsGroup },
      { title: "Skills", icon: Tag, items: skillsGroup },
    ].filter((g) => g.items.length > 0);
  }, [results]);

  return (
    <div ref={containerRef} className="relative w-full">
      <div className="relative w-full">
        <Search className="absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
        <Input
          className="pl-9 h-9 text-sm"
          placeholder="Search candidates, jobs, skills..."
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          onKeyDown={handleKeyDown}
        />
      </div>

      {open && query.trim() && (
        <div className="absolute left-0 right-0 top-full z-50 mt-2 max-h-[420px] overflow-y-auto rounded-2xl border border-border bg-popover/95 shadow-2xl backdrop-blur-xl">
          {groupedSections.length ? (
            groupedSections.map((group) => (
              <div key={group.title} className="px-2 py-2">
                <div className="flex items-center gap-2 px-2 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] text-muted-foreground">
                  <group.icon className="h-3 w-3" />
                  {group.title}
                </div>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <button
                      key={`${item.kind}-${"id" in item ? item.id : item.label}`}
                      type="button"
                      onClick={() => handleSelect(item)}
                      className="flex w-full flex-col items-start rounded-xl px-3 py-2 text-left transition hover:bg-accent"
                    >
                      <span className="text-sm font-medium text-foreground">{item.label}</span>
                      <span className="text-xs text-muted-foreground">{item.sub}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="px-4 py-6 text-center text-sm text-muted-foreground">No matches for "{query}"</div>
          )}
        </div>
      )}
    </div>
  );
}
