import { useState, useEffect } from 'react';
import {
    LayoutDashboard,
    Terminal,
    Cpu,
    Database,
    Activity,
    Hammer,
    Component,
    Package
} from 'lucide-react';
import { cn } from '@/common/utils';

// API base comes from Vite env (fleet-start ApiTargetEnv) with a local default.
const API_BASE = (import.meta as any).env?.VITE_API_TARGET ?? 'http://127.0.0.1:10853';

// UI components
function Card({ children, className }: { children: React.ReactNode; className?: string }) {
    return (
        <div className={cn("rounded-lg border bg-slate-950/30 shadow-sm border-slate-800", className)}>
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
    const [state, setState] = useState<'loading' | 'ok' | 'error'>('loading');
    const [error, setError] = useState<string>('');

    useEffect(() => {
        let cancelled = false;
        const fetchData = async () => {
            try {
                const [mRes, lRes] = await Promise.all([
                    fetch(`${API_BASE}/api/metrics`),
                    fetch(`${API_BASE}/api/logs?limit=5&sort=desc`),
                ]);
                if (!mRes.ok || !lRes.ok) throw new Error(`HTTP ${mRes.status}/${lRes.status}`);
                const mData = await mRes.json();
                const lData = await lRes.json();
                if (cancelled) return;
                setMetrics(mData);
                setActivity(lData.entries ?? []);
                setState('ok');
            } catch (e) {
                if (cancelled) return;
                setError(e instanceof Error ? e.message : 'Backend unreachable');
                setState('error');
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 10000);
        return () => { cancelled = true; clearInterval(interval); };
    }, []);

    return (
        <div className="space-y-6" data-testid="dashboard">
            <header>
                <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
                    <LayoutDashboard className="h-8 w-8 text-emerald-500" />
                    Development Overview
                </h1>
                <p className="mt-2 text-slate-300">
                    Real-time status of your development environment and active project scaffolds.
                </p>
            </header>

            {state === 'loading' && (
                <Card className="p-6 bg-slate-900/40 border-slate-800">
                    <p className="text-sm text-slate-300">Connecting to backend…</p>
                </Card>
            )}

            {state === 'error' && (
                <Card className="p-6 bg-slate-900/40 border-red-900">
                    <p className="text-sm text-red-300">Backend unreachable: {error}</p>
                    <button
                        className="mt-3 text-sm px-3 py-1.5 rounded border border-slate-700 text-slate-200 hover:bg-slate-800"
                        onClick={() => window.location.reload()}
                    >
                        Retry
                    </button>
                </Card>
            )}

            {state === 'ok' && metrics && (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                    <MetricCard label="Logged events" value={String(metrics.tasks)} unit="" icon={Terminal} color="text-emerald-500" />
                    <MetricCard label="Backend uptime" value={formatUptime(metrics.uptime_seconds)} unit="" icon={Cpu} color="text-blue-500" />
                    <MetricCard label="Backend PID" value={String(metrics.pid)} unit="" icon={Database} color="text-purple-500" />
                    <MetricCard label="Backend status" value="Online" unit="" icon={Activity} color="text-amber-500" />
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
                        <ActionButton label="Manage Packages" icon={Package} href="/packages" disabled={false} />
                        <ActionButton label="Components" icon={Component} href="/components" disabled={false} />
                        <ActionButton label="Tool Lab" icon={Terminal} href="/tools" disabled={false} />
                    </div>
                </Card>

                <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
                    <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
                        <Activity className="h-5 w-5 text-amber-500" />
                        Recent Activity
                    </h3>
                    {activity.length === 0 ? (
                        <p className="text-sm text-slate-300">
                            No backend activity yet. Send a chat message or scaffold a project to get started.
                        </p>
                    ) : (
                        <div className="space-y-3">
                            {activity.map((e) => (
                                <ActivityItem
                                    key={e.id}
                                    label={`${e.kind}: ${e.detail}`}
                                    time={e.timestamp}
                                    status={e.level === 'ERROR' ? 'error' : e.level === 'WARNING' ? 'info' : 'success'}
                                />
                            ))}
                        </div>
                    )}
                </Card>
            </div>
        </div>
    );
}

function MetricCard({ label, value, unit, icon: Icon, color }: any) {
    return (
        <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
            <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">{label}</span>
                <Icon className={cn("h-4 w-4", color)} />
            </div>
            <div className="mt-2 text-2xl font-bold text-white" data-testid={`kpi-${label.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`}>
                {value}{unit}
            </div>
        </Card>
    );
}

function ActionButton({ label, icon: Icon, href, disabled }: any) {
    return (
        <a
            href={disabled ? '#' : href}
            className={cn(
                "flex items-center gap-3 p-3 rounded-lg border border-slate-800 bg-slate-950/50 transition-all duration-200",
                disabled ? "opacity-40 cursor-not-allowed" : "hover:bg-slate-800 hover:border-slate-700 hover:scale-[1.02]"
            )}
        >
            <Icon className="h-5 w-5 text-slate-300" />
            <span className="text-sm font-medium text-slate-200">{label}</span>
        </a>
    );
}

function ActivityItem({ label, time, status }: any) {
    return (
        <div className="flex items-center justify-between text-sm py-2 border-b border-slate-800 last:border-0">
            <div className="flex items-center gap-2">
                <div className={cn(
                    "h-2 w-2 rounded-full",
                    status === 'success' ? 'bg-emerald-500' : status === 'info' ? 'bg-blue-500' : 'bg-amber-500'
                )} />
                <span className="text-slate-200">{label}</span>
            </div>
            <span className="text-slate-300 text-sm">{time}</span>
        </div>
    );
}
