import * as React from "react";

import { cn } from "../../lib/utils";

const Textarea = React.forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        ref={ref}
        className={cn(
          "flex min-h-[132px] w-full rounded-3xl border border-border bg-input px-4 py-3 text-sm text-foreground shadow-sm outline-none transition placeholder:text-muted-foreground/90 focus-visible:border-primary/40 focus-visible:ring-4 focus-visible:ring-ring/40",
          className,
        )}
        {...props}
      />
    );
  },
);
Textarea.displayName = "Textarea";

export { Textarea };
