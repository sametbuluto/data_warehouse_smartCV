import type { HTMLAttributes } from "react";

import { cn } from "../../lib/utils";

const toneClasses = {
  neutral: "border-border bg-secondary text-secondary-foreground",
  brand: "border-primary/15 bg-primary/10 text-primary",
  success: "border-success/20 bg-success/12 text-success",
  warning: "border-warning/20 bg-warning/12 text-warning",
  danger: "border-danger/20 bg-danger/12 text-danger",
};

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: keyof typeof toneClasses;
}

export function Badge({ className, tone = "neutral", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-3 py-1 text-xs font-medium tracking-wide",
        toneClasses[tone],
        className,
      )}
      {...props}
    />
  );
}
