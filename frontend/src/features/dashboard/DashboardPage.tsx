import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, FolderPlus, FileText, Settings, Rocket } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

// Mock data - replace with actual API calls
const mockStats = [
  { name: 'Total Projects', value: '12', icon: <FolderPlus className="h-5 w-5 text-primary" /> },
  { name: 'Active Projects', value: '8', icon: <Rocket className="h-5 w-5 text-green-500" /> },
  { name: 'Templates', value: '5', icon: <FileText className="h-5 w-5 text-blue-500" /> },
  { name: 'Settings', value: '3', icon: <Settings className="h-5 w-5 text-purple-500" /> },
];

const recentProjects = [
  { id: 1, name: 'E-commerce Platform', type: 'React', lastModified: '2 hours ago' },
  { id: 2, name: 'Portfolio Site', type: 'Next.js', lastModified: '1 day ago' },
  { id: 3, name: 'Admin Dashboard', type: 'Vue', lastModified: '3 days ago' },
];

export default function DashboardPage() {
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Simulate loading data
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-8rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="flex flex-col justify-between space-y-4 md:flex-row md:items-center md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Welcome back!</h1>
          <p className="text-muted-foreground">
            Here's what's happening with your projects today.
          </p>
        </div>
        <Button onClick={() => navigate('/projects/new')}>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {mockStats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <div className="h-5 w-5">{stat.icon}</div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Recent Projects */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Recent Projects</CardTitle>
              <CardDescription>Your most recently modified projects</CardDescription>
            </div>
            <Button variant="ghost" size="sm" onClick={() => navigate('/projects')}>
              View all
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentProjects.map((project) => (
              <div
                key={project.id}
                className="flex items-center justify-between rounded-lg border p-4 hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => navigate(`/projects/${project.id}`)}
              >
                <div>
                  <h3 className="font-medium">{project.name}</h3>
                  <p className="text-sm text-muted-foreground">{project.type}</p>
                </div>
                <div className="text-sm text-muted-foreground">
                  Updated {project.lastModified}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common tasks to get you started</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Button
              variant="outline"
              className="h-24 flex-col items-center justify-center space-y-2"
              onClick={() => navigate('/projects/new')}
            >
              <Plus className="h-6 w-6" />
              <span>New Project</span>
            </Button>
            <Button
              variant="outline"
              className="h-24 flex-col items-center justify-center space-y-2"
              onClick={() => navigate('/templates')}
            >
              <FileText className="h-6 w-6" />
              <span>Browse Templates</span>
            </Button>
            <Button
              variant="outline"
              className="h-24 flex-col items-center justify-center space-y-2"
              onClick={() => navigate('/settings')}
            >
              <Settings className="h-6 w-6" />
              <span>Settings</span>
            </Button>
            <Button
              variant="outline"
              className="h-24 flex-col items-center justify-center space-y-2"
              onClick={() => window.open('https://github.com/yourusername/web-development-mcp', '_blank')}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-6 w-6"
              >
                <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
                <path d="M9 18c-4.51 2-5-2-7-2" />
              </svg>
              <span>GitHub</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
