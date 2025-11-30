import { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { QueryErrorResetBoundary } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';
import { Loader2 } from 'lucide-react';

// Layouts
const MainLayout = lazy(() => import('@/components/layout/MainLayout'));
const AuthLayout = lazy(() => import('@/components/layout/AuthLayout'));

// Pages
const DashboardPage = lazy(() => import('@/features/dashboard/DashboardPage'));
const ProjectsPage = lazy(() => import('@/features/projects/ProjectsPage'));
const ProjectDetailPage = lazy(() => import('@/features/projects/ProjectDetailPage'));
const TemplatesPage = lazy(() => import('@/features/templates/TemplatesPage'));
const SettingsPage = lazy(() => import('@/features/settings/SettingsPage'));
const LoginPage = lazy(() => import('@/features/auth/LoginPage'));
const NotFoundPage = lazy(() => import('@/components/common/NotFoundPage'));

// Components
const ErrorFallback = lazy(() => import('@/components/common/ErrorFallback'));

// Loading component
const LoadingFallback = () => (
  <div className="flex h-screen w-full items-center justify-center">
    <Loader2 className="h-12 w-12 animate-spin text-primary-500" />
  </div>
);

function App() {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ resetErrorBoundary }) => (
            <ErrorFallback onReset={resetErrorBoundary} />
          )}
        >
          <Suspense fallback={<LoadingFallback />}>
            <Routes>
              {/* Public Routes */}
              <Route element={<AuthLayout />}>
                <Route path="/login" element={<LoginPage />} />
              </Route>

              {/* Protected Routes */}
              <Route element={<MainLayout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/projects" element={<ProjectsPage />} />
                <Route path="/projects/:id" element={<ProjectDetailPage />} />
                <Route path="/templates" element={<TemplatesPage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="*" element={<NotFoundPage />} />
              </Route>
            </Routes>
          </Suspense>
          
          {/* Global Toaster */}
          <Toaster position="top-right" />
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}

export default App;
