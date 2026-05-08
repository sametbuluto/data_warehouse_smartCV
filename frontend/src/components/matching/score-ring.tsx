import { cn } from "../../lib/utils";

interface ScoreRingProps {
  score: number;
  size?: number;
  label?: string;
}

const toneByScore = (score: number) => {
  if (score >= 80) return "var(--success)";
  if (score >= 60) return "var(--primary)";
  if (score >= 45) return "var(--warning)";
  return "var(--danger)";
};

export function ScoreRing({ score, size = 70, label }: ScoreRingProps) {
  const radius = (size - 10) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.max(0, Math.min(100, score));
  const dashOffset = circumference - (progress / 100) * circumference;
  const stroke = toneByScore(score);

  return (
    <div className={cn("inline-flex flex-col items-center gap-2")} style={{ width: size }}>
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="rgba(148, 163, 184, 0.14)" strokeWidth="8" />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={stroke}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={dashOffset}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-base font-semibold text-foreground">{Math.round(score)}</span>
          <span className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">Fit</span>
        </div>
      </div>
      {label ? <span className="text-xs text-muted-foreground">{label}</span> : null}
    </div>
  );
}
