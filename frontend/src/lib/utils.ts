import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPercent(value: number, digits = 0) {
  return `${value.toFixed(digits)}%`;
}

export function formatRelativeDate(input: string) {
  const date = new Date(input);

  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date);
}

export function getScoreTone(score: number) {
  if (score >= 80) return "excellent";
  if (score >= 65) return "strong";
  if (score >= 45) return "average";
  return "weak";
}
