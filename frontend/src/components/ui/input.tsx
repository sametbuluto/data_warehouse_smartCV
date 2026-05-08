import * as React from "react";

import { cn } from "../../lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          "flex h-11 w-full rounded-2xl border border-border bg-input px-4 text-sm text-foreground shadow-sm outline-none transition placeholder:text-muted-foreground/90 focus-visible:border-primary/40 focus-visible:ring-4 focus-visible:ring-ring/40",
          className,
        )}
        {...props}
      />
    );
  },
);
Input.displayName = "Input";

export { Input };
