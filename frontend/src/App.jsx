import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import CvUpload from './pages/CvUpload';
import JobPostings from './pages/JobPostings';
import Candidates from './pages/Candidates';
import Analytics from './pages/Analytics';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen" style={{ background: 'var(--bg-primary)' }}>
        <Sidebar />
        <main className="flex-1 ml-[240px] min-h-screen">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<CvUpload />} />
            <Route path="/jobs" element={<JobPostings />} />
            <Route path="/candidates" element={<Candidates />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
