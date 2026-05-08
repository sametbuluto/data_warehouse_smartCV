import { AnimatePresence, motion } from "framer-motion";
import { lazy, Suspense } from "react";
import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";

import { AppShell } from "./components/layout/app-shell";
import { Skeleton } from "./components/ui/skeleton";

const DashboardPage = lazy(() => import("./pages/Dashboard"));
const CandidatesPage = lazy(() => import("./pages/Candidates"));
const JobPostingsPage = lazy(() => import("./pages/JobPostings"));
const MatchingPage = lazy(() => import("./pages/Matching"));
const UploadPage = lazy(() => import("./pages/CvUpload"));
const AnalyticsPage = lazy(() => import("./pages/Analytics"));
const SettingsPage = lazy(() => import("./pages/Settings"));

const appRoutes = [
  {
    path: "/",
    title: "Dashboard",
    description: "Monitor pipeline health, talent supply, and AI recruiting performance from one place.",
    element: <DashboardPage />,
  },
  {
    path: "/candidates",
    title: "Candidates",
    description: "Review uploaded CVs, candidate metadata, and cross-job fit from a stable talent workspace.",
    element: <CandidatesPage />,
  },
  {
    path: "/jobs",
    title: "Job Postings",
    description: "Create clean, explainable job requirements and launch candidate matching workflows.",
    element: <JobPostingsPage />,
  },
  {
    path: "/matching",
    title: "Matching",
    description: "Inspect ranked candidates, score breakdowns, skill gaps, and AI-generated recommendations.",
    element: <MatchingPage />,
  },
  {
    path: "/upload",
    title: "CV Upload",
    description: "Upload new resumes, parse candidate data, and immediately evaluate job compatibility.",
    element: <UploadPage />,
  },
  {
    path: "/analytics",
    title: "Analytics",
    description: "Explore candidate distribution, hiring intelligence, and dataset-level recruitment insights.",
    element: <AnalyticsPage />,
  },
  {
    path: "/settings",
    title: "Settings",
    description: "Configure the demo environment, review scoring logic, and control presentation readiness.",
    element: <SettingsPage />,
  },
];

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AppShell routes={appRoutes.map(({ path, title, description }) => ({ path, title, description }))}>
      <AnimatePresence mode="wait">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -12 }}
          transition={{ duration: 0.18 }}
        >
          <Suspense
            fallback={
              <div className="space-y-6 pb-4">
                <Skeleton className="h-[220px] w-full" />
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                  {Array.from({ length: 4 }).map((_, index) => (
                    <Skeleton key={index} className="h-[170px] w-full" />
                  ))}
                </div>
              </div>
            }
          >
            <Routes location={location}>
              {appRoutes.map((route) => (
                <Route key={route.path} path={route.path} element={route.element} />
              ))}
            </Routes>
          </Suspense>
        </motion.div>
      </AnimatePresence>
    </AppShell>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  );
}
