import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Upload, Briefcase, BarChart3, Users, Sparkles } from 'lucide-react';

const links = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Upload CV' },
  { to: '/jobs', icon: Briefcase, label: 'Job Postings' },
  { to: '/candidates', icon: Users, label: 'Candidates' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-[240px] flex flex-col py-6 px-4 border-r"
           style={{ background: 'var(--bg-secondary)', borderColor: 'var(--border)' }}>
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-3 mb-10">
        <div className="w-9 h-9 rounded-xl flex items-center justify-center"
             style={{ background: 'var(--gradient-primary)' }}>
          <Sparkles size={18} color="white" />
        </div>
        <div>
          <h1 className="text-sm font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>
            SmartCV
          </h1>
          <p className="text-[10px] font-medium" style={{ color: 'var(--text-muted)' }}>
            AI Matching Platform
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 flex flex-col gap-1">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive ? 'sidebar-active' : 'sidebar-link'
              }`
            }
            style={({ isActive }) => ({
              background: isActive ? 'rgba(99,102,241,0.12)' : 'transparent',
              color: isActive ? 'var(--accent-blue)' : 'var(--text-secondary)',
            })}
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-3 py-3 rounded-lg" style={{ background: 'var(--bg-card)', border: '1px solid var(--border)' }}>
        <p className="text-[11px] font-medium" style={{ color: 'var(--text-muted)' }}>
          Smart CV Analysis v1.0
        </p>
        <p className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
          NLP + ML Pipeline
        </p>
      </div>
    </aside>
  );
}
