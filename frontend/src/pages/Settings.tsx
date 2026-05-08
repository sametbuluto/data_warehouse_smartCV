import { MoonStar, Palette, ShieldCheck, SlidersHorizontal } from "lucide-react";

import { ThemeToggle } from "../components/layout/theme-toggle";
import { Badge } from "../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { SectionHeading } from "../components/ui/section-heading";

export default function SettingsPage() {
  return (
    <div className="space-y-6 pb-4">
      <SectionHeading
        eyebrow="Platform Settings"
        title="Control the presentation environment and document the academic pipeline."
        description="This section keeps the demo understandable for instructors by exposing theme controls, scoring weights, and system architecture in a polished format."
      />

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Appearance</CardTitle>
            <CardDescription>Persistent dark and light themes with smooth transitions.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="hero-panel rounded-[28px] p-5">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-foreground">Theme mode</p>
                  <p className="mt-1 text-sm leading-7 text-muted-foreground">
                    Switch between a bright SaaS workspace and a premium dark analytics environment.
                  </p>
                </div>
                <ThemeToggle />
              </div>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <div className="mb-2 flex items-center gap-2 text-foreground">
                  <Palette className="h-4 w-4 text-primary" />
                  <span className="text-sm font-semibold">Design system</span>
                </div>
                <p className="text-sm leading-7 text-muted-foreground">
                  Unified radius scale, stable container widths, and theme tokens for every page.
                </p>
              </div>
              <div className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <div className="mb-2 flex items-center gap-2 text-foreground">
                  <MoonStar className="h-4 w-4 text-primary" />
                  <span className="text-sm font-semibold">Persistence</span>
                </div>
                <p className="text-sm leading-7 text-muted-foreground">
                  Theme and sidebar preferences are stored locally for presentation continuity.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Matching formula</CardTitle>
            <CardDescription>The explainable academic weighting used throughout the demo.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3 sm:grid-cols-2">
            {[
              { label: "Skill Match", value: "40%" },
              { label: "Experience Match", value: "30%" },
              { label: "Education Match", value: "20%" },
              { label: "Semantic Similarity", value: "10%" },
            ].map((item) => (
              <div key={item.label} className="rounded-[24px] border border-border bg-secondary/55 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-foreground">{item.value}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Academic architecture</CardTitle>
            <CardDescription>Concise explanation of the demo-friendly ML and data stack.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              "Small curated resume and job datasets keep the demo fast, understandable, and reliable.",
              "spaCy and lightweight text preprocessing normalize content before TF-IDF vectorization.",
              "SQLite persists candidates, skills, jobs, and match results for local repeatability.",
              "Every score is explainable through matched skills, missing skills, and weighted components.",
            ].map((line) => (
              <div key={line} className="rounded-[24px] border border-border bg-secondary/55 p-4 text-sm leading-7 text-muted-foreground">
                {line}
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Presentation checklist</CardTitle>
            <CardDescription>Use this as the final pre-demo sanity panel.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              "Upload at least one CV and confirm candidate extraction fields render correctly.",
              "Create or keep active job postings so cross-job matching stays visible.",
              "Run matching for one featured role before the presentation begins.",
              "Switch themes once during the live demo to showcase polish and responsiveness.",
            ].map((line) => (
              <div key={line} className="flex items-start gap-3 rounded-[24px] border border-border bg-secondary/55 p-4">
                <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                <p className="text-sm leading-7 text-muted-foreground">{line}</p>
              </div>
            ))}

            <div className="rounded-[24px] border border-primary/18 bg-primary/8 p-4">
              <div className="flex items-center gap-2">
                <SlidersHorizontal className="h-4 w-4 text-primary" />
                <p className="text-sm font-semibold text-foreground">Current profile</p>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                <Badge tone="brand">React + TypeScript</Badge>
                <Badge tone="brand">Tailwind CSS</Badge>
                <Badge tone="brand">Framer Motion</Badge>
                <Badge tone="brand">Recharts</Badge>
                <Badge tone="brand">FastAPI + SQLite</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
