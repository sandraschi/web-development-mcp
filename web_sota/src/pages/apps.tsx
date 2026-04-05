import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Grid, Search, Plus, ExternalLink, ShieldCheck, Zap, Server, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Apps() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Apps Hub</h2>
                    <p className="text-slate-400">Fleet discovery and real-time application registry</p>
                </div>
                <div className="flex gap-2">
                    <div className="relative">
                        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-500" />
                        <input
                            placeholder="Search fleet..."
                            className="bg-slate-900 border-slate-800 rounded-md pl-9 pr-4 py-2 text-sm text-slate-300 focus:outline-none focus:ring-1 focus:ring-blue-500 w-64"
                        />
                    </div>
                    <Button className="bg-blue-600 hover:bg-blue-700">
                        <Plus className="mr-2 h-4 w-4" />
                        Register App
                    </Button>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {[
                    { name: 'Developer Hub', status: 'Online', port: 10852, type: 'Dashboard', color: 'blue', icon: Grid },
                    { name: 'Email Hub', status: 'Online', port: 10720, type: 'Utility', color: 'emerald', icon: Zap },
                    { name: 'Tapo Camera', status: 'Standby', port: 10740, type: 'IoT', color: 'amber', icon: Server },
                    { name: 'Central Docs', status: 'Online', port: 80, type: 'Docs', color: 'purple', icon: Globe },
                    { name: 'Universal Actuator', status: 'Running', port: 10700, type: 'Core', color: 'indigo', icon: ShieldCheck },
                ].map((app) => (
                    <Card key={app.name} className="border-slate-800 bg-slate-950/50 hover:border-slate-700 transition-all cursor-pointer group">
                        <CardHeader className="pb-4">
                            <div className="flex items-start justify-between">
                                <div className={`p-2 bg-${app.color}-500/10 rounded-lg`}>
                                    <app.icon className={`h-6 w-6 text-${app.color}-400`} />
                                </div>
                                <Badge variant="outline" className={`border-${app.color}-500/30 bg-${app.color}-500/10 text-${app.color}-400`}>
                                    {app.status}
                                </Badge>
                            </div>
                            <CardTitle className="text-white mt-4">{app.name}</CardTitle>
                            <CardDescription className="text-slate-500 text-xs">Port: {app.port} • Local Domain</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center justify-between text-xs mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                <span className={`text-${app.color}-400`}>{app.type} Protocol</span>
                                <ExternalLink className="h-3 w-3 text-slate-500" />
                            </div>
                        </CardContent>
                    </Card>
                ))}

                <Card className="border-dashed border-slate-800 bg-transparent hover:bg-slate-900/20 transition-colors cursor-pointer flex items-center justify-center p-8">
                    <div className="text-center group">
                        <div className="inline-flex p-3 bg-slate-800/50 rounded-full mb-3 group-hover:bg-slate-700 transition-colors">
                            <Plus className="h-6 w-6 text-slate-500" />
                        </div>
                        <div className="text-sm font-medium text-slate-400">Add New Deployment</div>
                    </div>
                </Card>
            </div>

            <Card className="border-slate-800 bg-slate-950/50">
                <CardHeader>
                    <CardTitle className="text-white text-base">Global Fleet Metrics</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid gap-8 md:grid-cols-3">
                        <div className="space-y-1">
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Total Uptime</div>
                            <div className="text-xl font-bold text-emerald-400">99.98%</div>
                        </div>
                        <div className="space-y-1">
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Aggregate Traffic</div>
                            <div className="text-xl font-bold text-white">4.2 GB/day</div>
                        </div>
                        <div className="space-y-1">
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Active Workers</div>
                            <div className="text-xl font-bold text-blue-400">18 Nodes</div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
