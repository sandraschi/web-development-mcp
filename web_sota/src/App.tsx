import {
  Navigate,
  Route,
  BrowserRouter as Router,
  Routes,
} from "react-router-dom";
import { AppLayout } from "@/components/layout/app-layout";
import { Apps } from "@/pages/apps";
import { Build } from "@/pages/build";
import { Chat } from "@/pages/chat";
import { Components } from "@/pages/components";
import { Control } from "@/pages/control";
import { Dashboard } from "@/pages/dashboard";
import { Help } from "@/pages/help";
import { Inbox } from "@/pages/inbox";
import Logging from "@/pages/Logging";
import { Packages } from "@/pages/packages";
import { Projects } from "@/pages/projects";
import { Settings } from "@/pages/settings";
import { Skills } from "@/pages/skills";

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
          <Route path="/inbox" element={<Inbox />} />
          <Route path="/skills" element={<Skills />} />
          <Route path="/help" element={<Help />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;
