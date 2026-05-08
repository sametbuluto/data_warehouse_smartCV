import { motion } from "framer-motion";
import {
  BarChart3,
  BriefcaseBusiness,
  ChevronLeft,
  LayoutDashboard,
  Radar,
  Settings,
  Sparkles,
  UploadCloud,
  UsersRound,
  X,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import { cn } from "../../lib/utils";
import { Button } from "../ui/button";

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/candidates", label: "Candidates", icon: UsersRound },
  { to: "/jobs", label: "Job Postings", icon: BriefcaseBusiness },
  { to: "/matching", label: "Matching", icon: Radar },
  { to: "/upload", label: "CV Upload", icon: UploadCloud },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/settings", label: "Settings", icon: Settings },
];

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  mobileOpen: boolean;
  onCloseMobile: () => void;
}

function SidebarBody({
  collapsed,
  onToggleCollapse,
  onItemClick,
}: {
  collapsed: boolean;
  onToggleCollapse: () => void;
  onItemClick?: () => void;
}) {
  return (
    <div className="flex h-full flex-col gap-6 rounded-none border-r border-[var(--sidebar-border)] bg-[var(--sidebar)] px-4 py-5 backdrop-blur-2xl lg:rounded-r-[30px]">
      <div className="flex items-center justify-between gap-3">
        <div className={cn("flex items-center gap-3", collapsed && "justify-center")}>
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-[22px] bg-[linear-gradient(135deg,var(--primary),var(--chart-2))] text-white shadow-[0_16px_40px_rgba(37,99,235,0.32)]">
            <Sparkles className="h-5 w-5" />
          </div>
          {!collapsed ? (
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-primary/80">SmartCV</p>
              <h1 className="text-lg font-semibold tracking-tight text-[var(--sidebar-foreground)]">
                Recruitment OS
              </h1>
              <p className="text-xs text-muted-foreground">AI candidate matching platform</p>
            </div>
          ) : null}
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="hidden lg:inline-flex"
          onClick={onToggleCollapse}
          aria-label="Toggle sidebar"
        >
          <ChevronLeft className={cn("h-4 w-4 transition-transform", collapsed && "rotate-180")} />
        </Button>
      </div>

      <div className={cn("hero-panel ring-grid rounded-[28px] px-4 py-4", collapsed && "px-3 py-3")}>
        <p className={cn("text-[11px] font-semibold uppercase tracking-[0.24em] text-primary/80", collapsed && "text-center")}>
          AI Engine
        </p>
        {!collapsed ? (
          <>
            <h2 className="mt-2 text-sm font-semibold text-foreground">Explainable matching pipeline</h2>
            <p className="mt-1 text-xs leading-5 text-muted-foreground">
              TF-IDF + weighted scoring across skills, experience, education, and semantic fit.
            </p>
          </>
        ) : null}
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} onClick={onItemClick}>
            {({ isActive }) => (
              <motion.div
                whileHover={{ x: collapsed ? 0 : 4 }}
                className={cn(
                  "group flex items-center gap-3 rounded-2xl px-3 py-3 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground shadow-[0_18px_50px_rgba(37,99,235,0.22)]"
                    : "text-muted-foreground hover:bg-accent hover:text-foreground",
                  collapsed && "justify-center px-2",
                )}
              >
                <Icon className="h-4.5 w-4.5 shrink-0" />
                {!collapsed ? <span>{label}</span> : null}
              </motion.div>
            )}
          </NavLink>
        ))}
      </nav>

      <div className={cn("glass-panel rounded-[24px] p-4", collapsed && "px-2 py-3")}>
        {!collapsed ? (
          <>
            <p className="text-xs font-semibold text-foreground">Demo Ready</p>
            <p className="mt-1 text-xs leading-5 text-muted-foreground">
              Live presentation mode with CV upload, ranking, and AI insights.
            </p>
          </>
        ) : (
          <div className="flex justify-center text-primary">
            <Sparkles className="h-4 w-4" />
          </div>
        )}
      </div>
    </div>
  );
}

export function Sidebar({ collapsed, onToggleCollapse, mobileOpen, onCloseMobile }: SidebarProps) {
  return (
    <>
      <aside className="sticky top-0 hidden h-svh lg:block">
        <SidebarBody collapsed={collapsed} onToggleCollapse={onToggleCollapse} />
      </aside>

      {mobileOpen ? (
        <div className="fixed inset-0 z-50 bg-slate-950/56 backdrop-blur-sm lg:hidden" onClick={onCloseMobile}>
          <motion.div
            initial={{ x: -28, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -28, opacity: 0 }}
            transition={{ duration: 0.18 }}
            className="h-full w-[86vw] max-w-[320px]"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex h-16 items-center justify-end px-4">
              <Button variant="ghost" size="icon" onClick={onCloseMobile} aria-label="Close menu">
                <X className="h-4 w-4" />
              </Button>
            </div>
            <SidebarBody collapsed={false} onToggleCollapse={onCloseMobile} onItemClick={onCloseMobile} />
          </motion.div>
        </div>
      ) : null}
    </>
  );
}
