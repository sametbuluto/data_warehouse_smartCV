import { Bell, Menu, Search, Sparkles } from "lucide-react";


import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { ThemeToggle } from "./theme-toggle";

interface TopbarProps {
  title: string;
  onOpenMobileNav: () => void;
}

export function Topbar({ title, onOpenMobileNav }: TopbarProps) {
  return (
    <header className="sticky top-0 z-30">
      <div className="mx-auto flex max-w-[1600px] items-center gap-3 px-4 pb-3 pt-3 sm:px-6 lg:px-8">
        <div className="glass-panel flex w-full items-center gap-3 rounded-[20px] px-4 py-2.5">
          <Button variant="secondary" size="icon" className="lg:hidden h-8 w-8" onClick={onOpenMobileNav} aria-label="Open menu">
            <Menu className="h-4 w-4" />
          </Button>

          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <h1 className="truncate text-base font-semibold tracking-tight text-foreground sm:text-lg">{title}</h1>
              <Sparkles className="hidden h-3.5 w-3.5 text-primary sm:block" />
            </div>
          </div>

          <div className="hidden flex-[0_1_320px] items-center lg:flex">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
              <Input className="pl-9 h-9 text-sm" placeholder="Search candidates, jobs, skills..." />
            </div>
          </div>

          <div className="flex items-center gap-1.5">
            <ThemeToggle />
            <Button variant="secondary" size="icon" className="h-8 w-8" aria-label="Notifications">
              <Bell className="h-3.5 w-3.5" />
            </Button>

          </div>
        </div>
      </div>
    </header>
  );
}
