import { Bell, Menu, Sparkles } from "lucide-react";


import { Button } from "../ui/button";
import { GlobalSearch } from "./global-search";
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
            <GlobalSearch />
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
