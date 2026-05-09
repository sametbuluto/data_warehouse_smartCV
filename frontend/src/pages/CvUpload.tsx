import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { AnimatePresence, motion } from "framer-motion";
import { BrainCircuit, CheckCircle2, FileText, Loader2, UploadCloud } from "lucide-react";

import { getCandidateMatches, getJobs, runCandidateMatching, uploadCV } from "../api/client";
import { ScoreRing } from "../components/matching/score-ring";
import { Badge } from "../components/ui/badge";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { EmptyState } from "../components/ui/empty-state";
import { Progress } from "../components/ui/progress";
import { SectionHeading } from "../components/ui/section-heading";
import { scoreBadgeTone } from "../lib/utils";
import type { Candidate, Job, MatchResult } from "../types/api";

const sleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

const uploadSteps = [
  "Saving PDF securely",
  "Extracting text from resume",
  "Parsing skills, education, and experience",
  "Comparing candidate against job openings",
];

export default function UploadPage() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeStep, setActiveStep] = useState(0);
  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      setUploading(true);
      setError(null);
      setCandidate(null);
      setMatches([]);

      try {
        // Step 0: Saving PDF — start upload and show this step for at least 700ms
        setProgress(10);
        setActiveStep(0);
        const uploadPromise = uploadCV(file);
        await sleep(700);

        // Step 1: Extracting text — show while waiting for upload
        setProgress(28);
        setActiveStep(1);
        await sleep(650);

        // Step 2: Parsing — show briefly, then await upload completion
        setProgress(50);
        setActiveStep(2);
        const uploadedCandidate = await uploadPromise;
        setCandidate(uploadedCandidate);
        await sleep(600);

        if (jobs.length) {
          // Step 3: Matching against job openings
          setProgress(72);
          setActiveStep(3);
          const [candidateMatches] = await Promise.all([
            runCandidateMatching(uploadedCandidate.id).then(() =>
              getCandidateMatches(uploadedCandidate.id),
            ),
            sleep(600),
          ]);
          setMatches(candidateMatches);
        }
        setProgress(100);
        // Redirect to matching page after a short success pause
        await sleep(1500);
        navigate(`/matching?candidate=${uploadedCandidate.id}`);
      } catch (requestError) {
        const fallbackMessage = "Upload failed. Please check the PDF and try again.";
        if (requestError instanceof Error) {
          setError(requestError.message || fallbackMessage);
        } else {
          setError(fallbackMessage);
        }
      } finally {
        setUploading(false);
      }
    },
    [jobs.length],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    disabled: uploading,
  });

  const extractionChecks = candidate
    ? [
        { label: "Name", ok: candidate.name && candidate.name !== "Unknown" },
        { label: "Email", ok: Boolean(candidate.email) },
        { label: "Phone", ok: Boolean(candidate.phone) },
        { label: "Education", ok: Boolean(candidate.education && candidate.education !== "Unknown") },
        { label: "Experience", ok: candidate.experience_years > 0 },
      ]
    : [];

  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Candidate Intake"
        title="Upload a CV and check its job fit"
        description="This page extracts candidate data from a PDF CV and compares the candidate against current job postings."
      />

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <Card className="overflow-hidden">
          <CardContent className="p-6">
            <div
              {...getRootProps()}
              className={[
                "ring-grid relative flex min-h-[420px] cursor-pointer flex-col items-center justify-center rounded-[32px] border border-dashed p-8 text-center transition",
                isDragActive ? "border-primary bg-primary/6" : "border-border bg-secondary/45 hover:border-primary/40 hover:bg-primary/6",
              ].join(" ")}
            >
              <input {...getInputProps()} />
              <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-[28px] bg-[linear-gradient(135deg,var(--primary),var(--chart-2))] text-white shadow-[0_22px_60px_rgba(37,99,235,0.28)]">
                {uploading ? <Loader2 className="h-9 w-9 animate-spin" /> : <UploadCloud className="h-9 w-9" />}
              </div>
              <h3 className="text-2xl font-semibold tracking-tight text-foreground">
                {isDragActive ? "Drop the PDF to start parsing" : "Drag and drop a CV PDF"}
              </h3>
              <p className="mt-3 max-w-lg text-sm leading-7 text-muted-foreground">Upload, parse, store, and match the CV in one flow.</p>
              <div className="mt-6 flex flex-wrap justify-center gap-2">
                <Badge tone="brand">PDF only</Badge>
                <Badge>{jobs.length} active jobs ready</Badge>
                <Badge>SQLite + explainable ranking</Badge>
              </div>
              <Button className="mt-8" size="lg">
                Choose CV File
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Pipeline progress</CardTitle>
              <CardDescription>Simple progress tracking for parsing and matching.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Progress value={progress} className="h-3" />
              <div className="space-y-3">
                {uploadSteps.map((step, index) => {
                  const completed = progress === 100 ? true : index < activeStep;
                  const current = index === activeStep && uploading;

                  return (
                    <div key={step} className="flex items-center gap-3 rounded-[22px] border border-border bg-secondary/55 px-4 py-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-card">
                        {completed ? (
                          <CheckCircle2 className="h-4 w-4 text-success" />
                        ) : current ? (
                          <Loader2 className="h-4 w-4 animate-spin text-primary" />
                        ) : (
                          <span className="text-sm font-semibold text-muted-foreground">{index + 1}</span>
                        )}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-foreground">{step}</p>
                        <p className="text-xs text-muted-foreground">
                          {completed ? "Completed" : current ? "Running now" : "Waiting"}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>After upload</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm leading-7 text-muted-foreground">
              <p>The parser extracts candidate fields from the PDF.</p>
              <p>The candidate is matched against current job postings.</p>
              <p>The results become visible in Dashboard, Candidates, Matching, and Analytics.</p>
            </CardContent>
          </Card>
        </div>
      </div>

      <AnimatePresence initial={false}>
        {error ? (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="rounded-[28px] border border-danger/20 bg-danger/10 px-5 py-4 text-sm text-danger"
          >
            {error}
          </motion.div>
        ) : null}
      </AnimatePresence>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Extracted candidate profile</CardTitle>
            <CardDescription>Structured preview generated by the NLP preprocessing pipeline.</CardDescription>
          </CardHeader>
          <CardContent>
            {candidate ? (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="space-y-4"
              >
                {/* Candidate hero */}
                <div className="hero-panel rounded-[28px] p-4">
                  <p className="text-xs uppercase tracking-[0.22em] text-primary/80">Candidate identified</p>
                  <h3 className="mt-1 text-xl font-semibold tracking-tight text-foreground">{candidate.name}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {candidate.education || "Education unknown"} • {candidate.experience_years} yrs experience
                  </p>
                </div>

                {/* Info grid */}
                <div className="grid gap-3 sm:grid-cols-2">
                  {[
                    { label: "Email", value: candidate.email || "Not detected" },
                    { label: "Phone", value: candidate.phone || "Not detected" },
                  ].map((item) => (
                    <div key={item.label} className="rounded-[24px] border border-border bg-secondary/55 p-4">
                      <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">{item.label}</p>
                      <p className="mt-2 text-sm font-semibold text-foreground">{item.value}</p>
                    </div>
                  ))}
                </div>

                {/* Skills with stagger */}
                <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <p className="text-sm font-semibold text-foreground">Extracted skills</p>
                    <Badge tone="brand">{candidate.skills.length} tags</Badge>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {candidate.skills.map((skill, i) => (
                      <motion.span
                        key={skill}
                        initial={{ opacity: 0, scale: 0.75 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.035, duration: 0.18 }}
                      >
                        <Badge tone="brand">{skill}</Badge>
                      </motion.span>
                    ))}
                  </div>
                </div>

                {/* Extraction quality */}
                <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                  <p className="text-xs uppercase tracking-[0.22em] text-muted-foreground">Extraction quality</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {extractionChecks.map((item) => (
                      <Badge key={item.label} tone={item.ok ? "success" : "warning"}>
                        {item.label}: {item.ok ? "Found" : "Missing"}
                      </Badge>
                    ))}
                  </div>
                </div>
              </motion.div>
            ) : (
              <EmptyState
                icon={FileText}
                title="No CV processed yet"
                description="Upload a resume to preview extracted candidate information and normalized skill tags."
              />
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Best job matches</CardTitle>
            <CardDescription>Cross-job compatibility for the newly uploaded candidate.</CardDescription>
          </CardHeader>
          <CardContent>
            {matches.length ? (
              <div className="space-y-4">
                {matches.slice(0, 5).map((match, i) => (
                  <motion.div
                    key={match.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.08, duration: 0.25 }}
                    className="flex items-center gap-4 rounded-[24px] border border-border bg-secondary/55 p-4"
                  >
                    <ScoreRing score={match.final_score} size={74} />
                    <div className="min-w-0 flex-1">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="text-sm font-semibold text-foreground">{match.job_title}</p>
                          <p className="mt-1 text-xs text-muted-foreground">
                            Skill {match.skill_score.toFixed(1)} • Experience {match.experience_score.toFixed(1)} • Education{" "}
                            {match.education_score.toFixed(1)}
                          </p>
                        </div>
                        <Badge tone={scoreBadgeTone(match.final_score)}>{Math.round(match.final_score)}%</Badge>
                      </div>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {match.matched_skills.slice(0, 4).map((skill) => (
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
                  </motion.div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={BrainCircuit}
                title={jobs.length ? "Awaiting candidate matching" : "No active jobs to compare"}
                description={
                  jobs.length
                    ? "After upload, the candidate can be compared against every job posting and ranked automatically."
                    : "Create job postings first, then uploaded CVs can be matched instantly against them."
                }
              />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
