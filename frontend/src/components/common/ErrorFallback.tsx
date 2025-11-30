import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';

type ErrorFallbackProps = {
  error: Error;
  resetErrorBoundary: () => void;
};

export function ErrorFallback({ error, resetErrorBoundary }: ErrorFallbackProps) {
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center p-4 text-center">
      <div className="mx-auto max-w-md space-y-4">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-destructive/10">
          <AlertTriangle className="h-6 w-6 text-destructive" />
        </div>
        
        <h2 className="text-2xl font-bold">Something went wrong</h2>
        
        <p className="text-muted-foreground">
          {error.message || 'An unexpected error occurred. Please try again.'}
        </p>
        
        <div className="pt-4">
          <Button
            onClick={resetErrorBoundary}
            variant="outline"
            className="w-full sm:w-auto"
          >
            Try again
          </Button>
        </div>
        
        <div className="pt-4 text-sm text-muted-foreground">
          <p>If the problem persists, please contact support.</p>
        </div>
      </div>
    </div>
  );
}

export default ErrorFallback;
