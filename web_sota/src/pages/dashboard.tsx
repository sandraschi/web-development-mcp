import {
  Activity,
  Component,
  Cpu,
  Database,
  Hammer,
  LayoutDashboard,
  Package,
  Terminal,
} from "lucide-react";
import { useEffect, useState } from "react";
import { cn } from "@/common/utils";

// API base comes from Vite env (fleet-start ApiTargetEnv) with a local default.
type ViteEnv = { VITE_API_TARGET?: string };
const API_BASE =
  (import.meta as unknown as { env?: ViteEnv }).env?.VITE_API_TARGET ??
  "http://127.0.0.1:10853";

// UI components
function Card({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-slate-950/30 shadow-sm border-slate-800",
        className,
      )}
    >
      {children}
    </div>
  );
}

interface Metrics {
  uptime_seconds: number;
  tasks: number;
  pid: number;
}

interface LogEntry {
  id: string;
  timestamp: string;
  level: string;
  kind: string;
  detail: string;
}

function formatUptime(totalSeconds: number): string {
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m`;
  return `${Math.floor(totalSeconds)}s`;
}

export function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [activity, setActivity] = useState<LogEntry[]>([]);
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [error, setError] = useState<string>("");
  const [llmDetected, setLlmDetected] = useState<boolean | null>(null);
  const [onboarded, setOnboarded] = useState<boolean>(() => {
    try {
      return localStorage.getItem("webdev-onboarded") === "1";
    } catch {
      return false;
    }
  });

  const markOnboarded = () => {
    try {
      localStorage.setItem("webdev-onboarded", "1");
    } catch {
      /* private mode */
    }
    setOnboarded(true);
  };

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      try {
        const [mRes, lRes] = await Promise.all([
          fetch(`${API_BASE}/api/metrics`),
          fetch(`${API_BASE}/api/logs?limit=5&sort=desc`),
        ]);
        if (!mRes.ok || !lRes.ok)
          throw new Error(`HTTP ${mRes.status}/${lRes.status}`);
        const mData = await mRes.json();
        const lData = await lRes.json();
        if (cancelled) return;
        setMetrics(mData);
        setActivity(lData.entries ?? []);
        setState("ok");
      } catch (e) {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : "Backend unreachable");
        setState("error");
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    fetch(`${API_BASE}/api/llm/discover`)
      .then(async (r) => {
        if (!r.ok) return;
        const data = await r.json();
        if (!cancelled) {
          setLlmDetected(
            (data.providers ?? []).some(
              (p: { detected: boolean }) => p.detected,
            ),
          );
        }
      })
      .catch(() => {
        if (!cancelled) setLlmDetected(false);
      });
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="space-y-6" data-testid="dashboard">
      <header>
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <LayoutDashboard className="h-8 w-8 text-emerald-500" />
          Development Overview
        </h1>
        <p className="mt-2 text-slate-300">
          Real-time status of your development environment and active project
          scaffolds.
        </p>
      </header>

      {!onboarded && llmDetected === false && (
        <Card
          data-testid="onboarding-cue"
          className="p-6 bg-red-950/40 border-red-700 backdrop-blur-sm"
        >
          <h2 className="text-lg font-semibold text-white">
            Finish onboarding: connect an LLM
          </h2>
          <p className="mt-1 text-sm text-slate-200">
            No local LLM detected. Chat needs Ollama (:11434) or LM Studio
            (:1234), or a cloud key — see docs/ONBOARDING.md. All numbers on
            this page are live backend data (no samples, nothing mocked).
          </p>
          <div className="mt-3 flex gap-2">
            <a
              href="/settings"
              className="text-sm px-4 py-2 rounded bg-red-600 hover:bg-red-500 text-white font-medium"
            >
              Open Settings
            </a>
            <button
              type="button"
              onClick={markOnboarded}
              className="text-sm px-4 py-2 rounded border border-slate-600 text-slate-200 hover:bg-slate-800"
            >
              Mark onboarded
            </button>
          </div>
        </Card>
      )}

      {state === "loading" && (
        <Card className="p-6 bg-slate-900/40 border-slate-800">
          <p className="text-sm text-slate-300">Connecting to backend...</p>
        </Card>
      )}

      {state === "error" && (
        <Card className="p-6 bg-slate-900/40 border-red-900">
          <p className="text-sm text-red-300">Backend unreachable: {error}</p>
          <button
            type="button"
            className="mt-3 text-sm px-3 py-1.5 rounded border border-slate-700 text-slate-200 hover:bg-slate-800"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </Card>
      )}

      {state === "ok" && metrics && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            label="Logged events"
            value={String(metrics.tasks)}
            unit=""
            icon={Terminal}
            color="text-emerald-500"
          />
          <MetricCard
            label="Backend uptime"
            value={formatUptime(metrics.uptime_seconds)}
            unit=""
            icon={Cpu}
            color="text-blue-500"
          />
          <MetricCard
            label="Backend PID"
            value={String(metrics.pid)}
            unit=""
            icon={Database}
            color="text-purple-500"
          />
          <MetricCard
            label="Backend status"
            value="Online"
            unit=""
            icon={Activity}
            color="text-amber-500"
          />
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <Hammer className="h-5 w-5 text-emerald-500" />
            Quick Actions
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <ActionButton label="Scaffold App" icon={Hammer} href="/projects" />
            <ActionButton
              label="Manage Packages"
              icon={Package}
              href="/packages"
              disabled={false}
            />
            <ActionButton
              label="Components"
              icon={Component}
              href="/components"
              disabled={false}
            />
            <ActionButton
              label="Tool Lab"
              icon={Terminal}
              href="/tools"
              disabled={false}
            />
          </div>
        </Card>

        <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <Activity className="h-5 w-5 text-amber-500" />
            Recent Activity
          </h3>
          {activity.length === 0 ? (
            <p className="text-sm text-slate-300">
              No backend activity yet. Send a chat message or scaffold a project
              to get started.
            </p>
          ) : (
            <div className="space-y-3">
              {activity.map((e) => (
                <ActivityItem
                  key={e.id}
                  label={`${e.kind}: ${e.detail}`}
                  time={e.timestamp}
                  status={
                    e.level === "ERROR"
                      ? "error"
                      : e.level === "WARNING"
                        ? "info"
                        : "success"
                  }
                />
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

type IconComponent = React.ComponentType<{ className?: string }>;

function MetricCard({
  label,
  value,
  unit,
  icon: Icon,
  color,
}: {
  label: string;
  value: string;
  unit: string;
  icon: IconComponent;
  color: string;
}) {
  return (
    <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-300">{label}</span>
        <Icon className={cn("h-4 w-4", color)} />
      </div>
      <div
        className="mt-2 text-2xl font-bold text-white"
        data-testid={`kpi-${label.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
      >
        {value}
        {unit}
      </div>
    </Card>
  );
}

function ActionButton({
  label,
  icon: Icon,
  href,
  disabled,
}: {
  label: string;
  icon: IconComponent;
  href: string;
  disabled?: boolean;
}) {
  return (
    <a
      href={disabled ? "#" : href}
      className={cn(
        "flex items-center gap-3 p-3 rounded-lg border border-slate-800 bg-slate-950/50 transition-all duration-200",
        disabled
          ? "opacity-40 cursor-not-allowed"
          : "hover:bg-slate-800 hover:border-slate-700 hover:scale-[1.02]",
      )}
    >
      <Icon className="h-5 w-5 text-slate-300" />
      <span className="text-sm font-medium text-slate-200">{label}</span>
    </a>
  );
}

function ActivityItem({
  label,
  time,
  status,
}: {
  label: string;
  time: string;
  status: string;
}) {
  return (
    <div className="flex items-center justify-between text-sm py-2 border-b border-slate-800 last:border-0">
      <div className="flex items-center gap-2">
        <div
          className={cn(
            "h-2 w-2 rounded-full",
            status === "success"
              ? "bg-emerald-500"
              : status === "info"
                ? "bg-blue-500"
                : "bg-amber-500",
          )}
        />
        <span className="text-slate-200">{label}</span>
      </div>
      <span className="text-slate-300 text-sm">{time}</span>
    </div>
  );
}
