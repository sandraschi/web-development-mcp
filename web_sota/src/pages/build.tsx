import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Cpu, Activity, Zap, AlertTriangle, Play, Circle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Build() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Build Forge</h2>
                    <p className="text-slate-400">Continuous integration and production build pipelines</p>
                </div>
                <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                    <Play className="mr-2 h-4 w-4" />
                    Trigger Build
                </Button>
            </div>

            <div className="grid gap-6 md:grid-cols-4">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-medium text-slate-400 uppercase">Avg Build Time</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">42s</div>
                        <p className="text-xs text-emerald-400 flex items-center mt-1">
                            <Zap className="mr-1 h-3 w-3" /> -12s from last week
                        </p>
                    </CardContent>
                </Card>
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-medium text-slate-400 uppercase">Success Rate</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">99.2%</div>
                        <p className="text-xs text-slate-500 mt-1">Last 250 builds</p>
                    </CardContent>
                </Card>
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-medium text-slate-400 uppercase">Active Nodes</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">12</div>
                        <p className="text-xs text-blue-400 mt-1 flex items-center">
                            <Circle className="mr-1 h-2 w-2 fill-current" /> Distributed
                        </p>
                    </CardContent>
                </Card>
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-medium text-slate-400 uppercase">Alerts</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">0</div>
                        <p className="text-xs text-emerald-400 mt-1">All systems nominal</p>
                    </CardContent>
                </Card>
            </div>

            <Card className="border-slate-800 bg-slate-950/50">
                <CardHeader className="border-b border-slate-800">
                    <CardTitle className="text-white flex items-center gap-2 text-base">
                        <Activity className="h-4 w-4 text-purple-400" />
                        Live Build Pipeline
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="divide-y divide-slate-800">
                        {[
                            { id: '#BK-8821', status: 'Running', type: 'Production', runner: 'vienna-01', time: '12s ago', color: 'blue' },
                            { id: '#BK-8820', status: 'Success', type: 'Staging', runner: 'vienna-02', time: '4m ago', color: 'emerald' },
                            { id: '#BK-8819', status: 'Success', type: 'Canary', runner: 'vienna-01', time: '12m ago', color: 'emerald' },
                            { id: '#BK-8818', status: 'Failed', type: 'Production', runner: 'vienna-03', time: '1h ago', color: 'red' },
                        ].map((build) => (
                            <div key={build.id} className="p-4 flex items-center justify-between hover:bg-slate-900/40 transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className="font-mono text-sm text-slate-300">{build.id}</div>
                                    <Badge variant="outline" className={`border-${build.color}-500/30 bg-${build.color}-500/10 text-${build.color}-400`}>
                                        {build.status}
                                    </Badge>
                                    <div className="text-xs text-slate-500 uppercase font-medium">{build.type}</div>
                                </div>
                                <div className="flex items-center gap-6">
                                    <div className="text-xs text-slate-400 flex items-center gap-1">
                                        <Cpu className="h-3 w-3" /> {build.runner}
                                    </div>
                                    <div className="text-xs text-slate-500">{build.time}</div>
                                    <Button variant="ghost" size="sm" className="h-8 text-xs text-slate-400">Logs</Button>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            <div className="grid gap-6 md:grid-cols-2">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white text-base">Code Quality Metrics</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-1">
                            <div className="flex justify-between text-xs">
                                <span className="text-slate-400">Test Coverage</span>
                                <span className="text-emerald-400">92%</span>
                            </div>
                            <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500" style={{ width: '92%' }}></div>
                            </div>
                        </div>
                        <div className="space-y-1">
                            <div className="flex justify-between text-xs">
                                <span className="text-slate-400">Maintainability index</span>
                                <span className="text-blue-400">A</span>
                            </div>
                            <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-blue-500" style={{ width: '85%' }}></div>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-red-500/20 bg-red-500/5">
                    <CardHeader>
                        <CardTitle className="text-red-400 text-base flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4" />
                            Recent Security Findings
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-xs text-slate-400 leading-relaxed">
                            <span className="text-red-400 font-bold">[CRITICAL]</span> Outdated package `fast-xml-parser` detected in `@sandra/infra-tools`.
                            Immediate upgrade to v4.4.1 recommended to mitigate SSRF vulnerability.
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
