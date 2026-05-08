import { cn } from "../../lib/utils";

interface AvatarProps {
  initials: string;
  className?: string;
}

export function Avatar({ initials, className }: AvatarProps) {
  return (
    <div
      className={cn(
        "flex h-10 w-10 items-center justify-center rounded-2xl bg-[linear-gradient(135deg,var(--primary),var(--chart-2))] text-sm font-semibold text-white shadow-[0_14px_36px_rgba(59,130,246,0.28)]",
        className,
      )}
    >
      {initials}
    </div>
  );
}
