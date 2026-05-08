import { Bell, Menu, Search, Sparkles } from "lucide-react";

import { Avatar } from "../ui/avatar";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { ThemeToggle } from "./theme-toggle";

interface TopbarProps {
  title: string;
  description: string;
  onOpenMobileNav: () => void;
}

export function Topbar({ title, description, onOpenMobileNav }: TopbarProps) {
  return (
    <header className="sticky top-0 z-30">
      <div className="mx-auto flex max-w-[1600px] items-center gap-3 px-4 pb-4 pt-4 sm:px-6 lg:px-8">
        <div className="glass-panel flex w-full items-center gap-3 rounded-[28px] px-4 py-3">
          <Button variant="secondary" size="icon" className="lg:hidden" onClick={onOpenMobileNav} aria-label="Open menu">
            <Menu className="h-4 w-4" />
          </Button>

          <div className="min-w-0 flex-1">
            <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-primary/80">SmartCV Workspace</p>
            <div className="flex items-center gap-2">
              <h1 className="truncate text-lg font-semibold tracking-tight text-foreground sm:text-xl">{title}</h1>
              <Sparkles className="hidden h-4 w-4 text-primary sm:block" />
            </div>
            <p className="hidden text-xs text-muted-foreground sm:block">{description}</p>
          </div>

          <div className="hidden flex-[0_1_360px] items-center lg:flex">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input className="pl-10" placeholder="Search candidates, jobs, skills..." />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <ThemeToggle />
            <Button variant="secondary" size="icon" aria-label="Notifications">
              <Bell className="h-4 w-4" />
            </Button>
            <Avatar initials="SC" />
          </div>
        </div>
      </div>
    </header>
  );
}
