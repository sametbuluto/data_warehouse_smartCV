import { BadgeCheck, BrainCircuit, GraduationCap, ListChecks, Sparkles } from "lucide-react";

import type { MatchExplanation } from "../../types/api";
import { Badge } from "../ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";
import { Progress } from "../ui/progress";
import { ScoreRing } from "./score-ring";

interface MatchExplanationDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  explanation: MatchExplanation | null;
}

const breakdownMeta = [
  { key: "skill_score", label: "Skill Match", icon: ListChecks },
  { key: "experience_score", label: "Experience", icon: Sparkles },
  { key: "education_score", label: "Education", icon: GraduationCap },
  { key: "semantic_score", label: "Semantic Similarity", icon: BrainCircuit },
] as const;

export function MatchExplanationDialog({
  open,
  onOpenChange,
  explanation,
}: MatchExplanationDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {explanation ? (
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{explanation.candidate_name}</DialogTitle>
            <DialogDescription>
              Match details for <span className="font-medium text-foreground">{explanation.job_title}</span>
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-6 lg:grid-cols-[180px_minmax(0,1fr)]">
            <div className="glass-panel rounded-[28px] p-4">
              <ScoreRing score={explanation.final_score} size={120} label="Final match score" />
            </div>

            <div className="space-y-4">
              {breakdownMeta.map(({ key, label, icon: Icon }) => {
                const score = explanation[key];

                return (
                  <div key={key} className="glass-panel rounded-[24px] p-4">
                    <div className="mb-2 flex items-center justify-between gap-3">
                      <div className="flex items-center gap-2 text-sm font-medium text-foreground">
                        <Icon className="h-4 w-4 text-primary" />
                        {label}
                      </div>
                      <span className="text-sm font-semibold text-foreground">{score.toFixed(1)}</span>
                    </div>
                    <Progress value={score} />
                  </div>
                );
              })}
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <div className="glass-panel rounded-[28px] p-5">
              <div className="mb-3 flex items-center gap-2">
                <BadgeCheck className="h-4 w-4 text-success" />
                <h3 className="text-sm font-semibold text-foreground">Matched skills</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {explanation.matched_skills.map((skill) => (
                  <Badge key={skill} tone="success">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="glass-panel rounded-[28px] p-5">
              <div className="mb-3 flex items-center gap-2">
                <ListChecks className="h-4 w-4 text-danger" />
                <h3 className="text-sm font-semibold text-foreground">Missing skills</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {explanation.missing_skills.length ? (
                  explanation.missing_skills.map((skill) => (
                    <Badge key={skill} tone="danger">
                      {skill}
                    </Badge>
                  ))
                ) : (
                  <Badge tone="success">No critical gaps</Badge>
                )}
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-[28px] p-5">
            <h3 className="mb-2 text-sm font-semibold text-foreground">AI Recommendation</h3>
            <p className="text-sm leading-7 text-muted-foreground">{explanation.explanation}</p>
          </div>
        </DialogContent>
      ) : null}
    </Dialog>
  );
}
