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

// UI components
function Card({ children, className }: { children: React.ReactNode; className?: string }) {
    return (
        <div className={cn("rounded-lg border bg-slate-950/30 shadow-sm border-slate-800", className)}>
            {children}
        </div>
    );
}


interface Metrics {
    cpu: number;
    memory: number;
    tasks: number;
}

export function Dashboard() {
    const [metrics, setMetrics] = useState<Metrics>({
        cpu: 0,
        memory: 0,
        tasks: 0,
    });

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                // Backend port 10853
                const response = await fetch('http://localhost:10853/metrics');
                const data = await response.json();
                setMetrics(data);
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        };

        fetchMetrics();
        const interval = setInterval(fetchMetrics, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-6">
            <header>
                <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
                    <LayoutDashboard className="h-8 w-8 text-emerald-500" />
                    Development Overview
                </h1>
                <p className="mt-2 text-slate-400">
                    Real-time status of your development environment and active project scaffolds.
                </p>
            </header>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <MetricCard label="Active Processes" value={metrics.tasks} unit="" icon={Terminal} color="text-emerald-500" />
                <MetricCard label="CPU Load" value={metrics.cpu} unit="%" icon={Cpu} color="text-blue-500" />
                <MetricCard label="Memory Usage" value={metrics.memory} unit="%" icon={Database} color="text-purple-500" />
                <MetricCard label="Build Queue" value={0} unit=" jobs" icon={Activity} color="text-amber-500" />
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
                    <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
                        <Hammer className="h-5 w-5 text-emerald-500" />
                        Quick Actions
                    </h3>
                    <div className="grid grid-cols-2 gap-3">
                        <ActionButton label="Scaffold App" icon={Hammer} href="/scaffolder" />
                        <ActionButton label="Manage Packages" icon={Package} href="/packages" disabled />
                        <ActionButton label="Components" icon={Component} href="/components" disabled />
                        <ActionButton label="Tool Lab" icon={Terminal} href="/tools" disabled />
                    </div>
                </Card>

                <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
                    <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
                        <Activity className="h-5 w-5 text-amber-500" />
                        Recent Activity
                    </h3>
                    <div className="space-y-3">
                        <ActivityItem label="Scaffolded test-project" time="5m ago" status="success" />
                        <ActivityItem label="Updated bridge version" time="1h ago" status="info" />
                        <ActivityItem label="Server initialized" time="2h ago" status="success" />
                    </div>
                </Card>
            </div>
        </div>
    );
}

function MetricCard({ label, value, unit, icon: Icon, color }: any) {
    return (
        <Card className="p-6 bg-slate-900/40 border-slate-800 backdrop-blur-sm">
            <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-400">{label}</span>
                <Icon className={cn("h-4 w-4", color)} />
            </div>
            <div className="mt-2 text-2xl font-bold text-white">
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
            <Icon className="h-5 w-5 text-slate-400" />
            <span className="text-sm font-medium text-slate-300">{label}</span>
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
            <span className="text-slate-500 text-xs">{time}</span>
        </div>
    );
}

