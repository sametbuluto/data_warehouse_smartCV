import { useMemo, useState } from "react";
import { useLocation } from "react-router-dom";

import { useLocalStorage } from "../../hooks/use-local-storage";
import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";

interface RouteMeta {
  path: string;
  title: string;
  description: string;
}

interface AppShellProps {
  routes: RouteMeta[];
  children: React.ReactNode;
}

export function AppShell({ routes, children }: AppShellProps) {
  const location = useLocation();
  const [collapsed, setCollapsed] = useLocalStorage("smartcv-sidebar-collapsed", false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const currentRoute = useMemo(() => {
    return routes.find((route) => route.path === location.pathname) ?? routes[0];
  }, [location.pathname, routes]);

  return (
    <div className="app-shell-grid mx-auto grid min-h-screen max-w-[1800px]" data-collapsed={collapsed}>
      <Sidebar
        collapsed={collapsed}
        onToggleCollapse={() => setCollapsed((value) => !value)}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      <div className="min-w-0">
        <Topbar
          title={currentRoute.title}
          description={currentRoute.description}
          onOpenMobileNav={() => setMobileOpen(true)}
        />
        <main className="mx-auto max-w-[1600px] px-4 pb-8 sm:px-6 lg:px-8">{children}</main>
      </div>
    </div>
  );
}
