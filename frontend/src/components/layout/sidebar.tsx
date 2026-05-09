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
import { Link, NavLink } from "react-router-dom";

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
    <div className="flex h-full flex-col gap-4 rounded-none border-r border-[var(--sidebar-border)] bg-[var(--sidebar)] px-3 py-4 backdrop-blur-2xl lg:rounded-r-[30px]">
      <div className="flex items-center justify-between gap-2 px-1">
        <Link to="/" className={cn("flex items-center gap-2.5 rounded-xl transition-opacity hover:opacity-80", collapsed && "justify-center")}>
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[16px] bg-[linear-gradient(135deg,var(--primary),var(--chart-2))] text-white shadow-[0_8px_24px_rgba(37,99,235,0.28)]">
            <Sparkles className="h-4 w-4" />
          </div>
          {!collapsed ? (
            <div>
              <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-primary/80">SmartCV</p>
              <h1 className="text-sm font-semibold tracking-tight text-[var(--sidebar-foreground)] leading-tight">
                Recruitment OS
              </h1>
            </div>
          ) : null}
        </Link>
        <Button
          variant="ghost"
          size="icon"
          className="hidden lg:inline-flex h-7 w-7"
          onClick={onToggleCollapse}
          aria-label="Toggle sidebar"
        >
          <ChevronLeft className={cn("h-3.5 w-3.5 transition-transform", collapsed && "rotate-180")} />
        </Button>
      </div>

      <nav className="flex-1 space-y-0.5">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} onClick={onItemClick}>
            {({ isActive }) => (
              <motion.div
                whileHover={{ x: collapsed ? 0 : 3 }}
                className={cn(
                  "group flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground shadow-[0_8px_24px_rgba(37,99,235,0.18)]"
                    : "text-muted-foreground hover:bg-accent hover:text-foreground",
                  collapsed && "justify-center px-2",
                )}
              >
                <Icon className="h-4 w-4 shrink-0" />
                {!collapsed ? <span>{label}</span> : null}
              </motion.div>
            )}
          </NavLink>
        ))}
      </nav>
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
