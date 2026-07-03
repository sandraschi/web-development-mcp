import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/app-layout';
import { Dashboard } from '@/pages/dashboard';
import { Projects } from '@/pages/projects';
import { Components } from '@/pages/components';
import { Packages } from '@/pages/packages';
import { Build } from '@/pages/build';
import { Chat } from '@/pages/chat';
import { Apps } from '@/pages/apps';
import { Control } from '@/pages/control';
import { Settings } from '@/pages/settings';
import Logging from '@/pages/Logging';

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/components" element={<Components />} />
          <Route path="/packages" element={<Packages />} />
          <Route path="/build" element={<Build />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/apps" element={<Apps />} />
          <Route path="/tools" element={<Control />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/logs" element={<Logging />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}


export default App;
