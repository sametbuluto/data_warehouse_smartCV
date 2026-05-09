import { useDeferredValue, useEffect, useMemo, useState } from "react";
import { BriefcaseBusiness, Plus, Radar, Search, Trash2, WandSparkles, X } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { createJob, deleteJob, getJobs, runMatching } from "../api/client";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { Input } from "../components/ui/input";
import { SectionHeading } from "../components/ui/section-heading";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Textarea } from "../components/ui/textarea";
import type { Job, JobCreatePayload } from "../types/api";

const suggestedSkills = [
  "python",
  "react",
  "typescript",
  "sql",
  "docker",
  "aws",
  "fastapi",
  "node.js",
  "machine learning",
  "figma",
  "kubernetes",
  "data analysis",
];

const initialForm: JobCreatePayload = {
  title: "",
  description: "",
  required_skills: [],
  min_experience: 2,
  education_level: "Bachelor",
};

export default function JobPostingsPage() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [form, setForm] = useState<JobCreatePayload>(initialForm);
  const [skillInput, setSkillInput] = useState("");
  const [search, setSearch] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [matchingJobId, setMatchingJobId] = useState<number | null>(null);

  useEffect(() => {
    getJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  const deferredSearch = useDeferredValue(search);

  const filteredJobs = useMemo(() => {
    const query = deferredSearch.toLowerCase().trim();
    if (!query) return jobs;

    return jobs.filter((job) => {
      return (
        job.title.toLowerCase().includes(query) ||
        job.description.toLowerCase().includes(query) ||
        job.required_skills.some((skill) => skill.toLowerCase().includes(query))
      );
    });
  }, [deferredSearch, jobs]);

  const addSkill = (rawSkill: string) => {
    const skill = rawSkill.trim().toLowerCase();
    if (!skill || form.required_skills.includes(skill)) return;

    setForm((current) => ({ ...current, required_skills: [...current.required_skills, skill] }));
    setSkillInput("");
  };

  const removeSkill = (skillToRemove: string) => {
    setForm((current) => ({
      ...current,
      required_skills: current.required_skills.filter((skill) => skill !== skillToRemove),
    }));
  };

  const refreshJobs = async () => {
    const nextJobs = await getJobs();
    setJobs(nextJobs);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);

    try {
      await createJob(form);
      setForm(initialForm);
      setSkillInput("");
      await refreshJobs();
    } finally {
      setSubmitting(false);
    }
  };

  const handleRunMatching = async (jobId: number) => {
    setMatchingJobId(jobId);
    try {
      await runMatching(jobId);
      navigate(`/matching?job=${jobId}`);
    } finally {
      setMatchingJobId(null);
    }
  };

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Hiring Templates"
        title="Create stable job briefs with normalized skills and structured requirements."
        description="This workspace keeps role creation clean, responsive, and presentation-safe while feeding the academic matching engine."
      />

      <div className="grid gap-6 xl:grid-cols-[420px_minmax(0,1fr)]">
        <Card className="h-fit xl:sticky xl:top-[80px] xl:max-h-[calc(100svh-6rem)] xl:overflow-y-auto">
          <CardHeader>
            <CardTitle>Create job posting</CardTitle>
            <CardDescription>Define the role, required skills, minimum experience, and education expectations.</CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={handleSubmit}>
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Job title</label>
                <Input
                  value={form.title}
                  onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
                  placeholder="Senior Python Developer"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Role description</label>
                <Textarea
                  value={form.description}
                  onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))}
                  placeholder="Describe responsibilities, stack, and priorities for this position."
                  required
                />
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Min experience</label>
                  <Input
                    type="number"
                    min={0}
                    value={form.min_experience}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        min_experience: Number(event.target.value) || 0,
                      }))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-foreground">Education</label>
                  <Select
                    value={form.education_level}
                    onValueChange={(value) => setForm((current) => ({ ...current, education_level: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Education level" />
                    </SelectTrigger>
                    <SelectContent>
                      {["High School", "Associate", "Bachelor", "Master", "PhD"].map((level) => (
                        <SelectItem key={level} value={level}>
                          {level}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-3">
                <label className="text-sm font-medium text-foreground">Required skills</label>
                <div className="flex gap-2">
                  <Input
                    value={skillInput}
                    onChange={(event) => setSkillInput(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        event.preventDefault();
                        addSkill(skillInput);
                      }
                    }}
                    placeholder="Type skill and press Enter"
                  />
                  <Button type="button" variant="secondary" onClick={() => addSkill(skillInput)}>
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex min-h-[72px] flex-wrap gap-2 rounded-[24px] border border-border bg-secondary/55 p-3">
                  {form.required_skills.length ? (
                    form.required_skills.map((skill) => (
                      <Badge key={skill} tone="brand" className="gap-2 pr-2">
                        {skill}
                        <button type="button" onClick={() => removeSkill(skill)} className="rounded-full p-0.5 hover:bg-white/10">
                          <X className="h-3 w-3" />
                        </button>
                      </Badge>
                    ))
                  ) : (
                    <span className="text-sm text-muted-foreground">Add skills to shape candidate ranking quality.</span>
                  )}
                </div>
                <div className="flex flex-wrap gap-2">
                  {suggestedSkills
                    .filter((skill) => !form.required_skills.includes(skill))
                    .map((skill) => (
                      <button key={skill} type="button" onClick={() => addSkill(skill)}>
                        <Badge>{skill}</Badge>
                      </button>
                    ))}
                </div>
              </div>

              <Button type="submit" size="lg" className="w-full" disabled={submitting}>
                {submitting ? "Creating role..." : "Create Job Posting"}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="gap-4">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <CardTitle>Live job library</CardTitle>
                <CardDescription>Search, review, and trigger candidate ranking against any role.</CardDescription>
              </div>
              <div className="relative w-full lg:max-w-sm">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input value={search} onChange={(event) => setSearch(event.target.value)} className="pl-9" placeholder="Search roles, skills, keywords..." />
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {filteredJobs.length ? (
              <div className="space-y-4">
                {filteredJobs.map((job) => (
                  <div key={job.id} className="rounded-[28px] border border-border bg-secondary/55 p-5">
                    <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-3">
                          <div className="flex h-10 w-10 items-center justify-center rounded-[18px] bg-primary/10 text-primary">
                            <BriefcaseBusiness className="h-4 w-4" />
                          </div>
                          <div>
                            <h3 className="text-lg font-semibold tracking-tight text-foreground">{job.title}</h3>
                            <p className="text-sm text-muted-foreground">
                              {job.min_experience}+ years • {job.education_level} • {job.required_skills.length} required skills
                            </p>
                          </div>
                        </div>

                        <p className="mt-4 max-w-4xl text-sm leading-7 text-muted-foreground">{job.description}</p>

                        <div className="mt-4 flex flex-wrap gap-2">
                          {job.required_skills.map((skill) => (
                            <Badge key={skill}>{skill}</Badge>
                          ))}
                        </div>
                      </div>

                      <div className="flex shrink-0 gap-2 xl:flex-col">
                        <Button onClick={() => handleRunMatching(job.id)} className="min-w-[160px]">
                          <Radar className="h-4 w-4" />
                          {matchingJobId === job.id ? "Running..." : "Run Matching"}
                        </Button>
                        <Button
                          variant="secondary"
                          onClick={async () => {
                            await deleteJob(job.id);
                            await refreshJobs();
                          }}
                        >
                          <Trash2 className="h-4 w-4" />
                          Delete
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={WandSparkles}
                title="No job postings found"
                description="Create the first role on the left or refine the search query to surface existing templates."
              />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
