import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Network, ZoomIn, ZoomOut, Maximize, Package, ShieldCheck } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function Packages() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Dependency Flow</h2>
                    <p className="text-slate-400">Visualizing registry graph and dependency health</p>
                </div>
                <div className="flex gap-2">
                    <Badge variant="outline" className="border-emerald-500/30 bg-emerald-500/10 text-emerald-400">
                        <ShieldCheck className="mr-1 h-3 w-3" />
                        Audit: Clean
                    </Badge>
                </div>
            </div>

            <Card className="border-slate-800 bg-slate-950/50 overflow-hidden">
                <CardHeader className="border-b border-slate-800 bg-slate-900/30">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Package className="h-5 w-5 text-blue-400" />
                            <div>
                                <CardTitle className="text-white text-base">@sandra/sota-core</CardTitle>
                                <CardDescription className="text-xs text-slate-500">v1.2.4 • Public</CardDescription>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <button className="p-1.5 hover:bg-slate-800 rounded transition-colors text-slate-400"><ZoomIn className="h-4 w-4" /></button>
                            <button className="p-1.5 hover:bg-slate-800 rounded transition-colors text-slate-400"><ZoomOut className="h-4 w-4" /></button>
                            <button className="p-1.5 hover:bg-slate-800 rounded transition-colors text-slate-400"><Maximize className="h-4 w-4" /></button>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="p-0 aspect-[16/9] relative bg-slate-950 flex items-center justify-center">
                    {/* Placeholder for Dependency Graph (e.g. React Flow) */}
                    <div className="text-center space-y-4">
                        <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-blue-900/10 border border-blue-500/20">
                            <Network className="h-8 w-8 text-blue-400/50" />
                        </div>
                        <div>
                            <h3 className="text-lg font-medium text-slate-300">Graph Engine Initializing</h3>
                            <p className="text-sm text-slate-500">Mapping 42 direct and 812 transitive dependencies...</p>
                        </div>
                    </div>

                    {/* Mock Graph Overlays */}
                    <div className="absolute top-10 left-10 p-3 bg-slate-900/80 backdrop-blur rounded border border-slate-800 text-xs text-slate-300">
                        <div className="font-bold text-blue-400 mb-1">Production</div>
                        <div>react@18.3.1</div>
                        <div>lucide-react@0.424.0</div>
                    </div>

                    <div className="absolute bottom-10 right-10 p-3 bg-slate-900/80 backdrop-blur rounded border border-slate-800 text-xs text-slate-300 text-right">
                        <div className="font-bold text-purple-400 mb-1">Development</div>
                        <div>vite@5.4.0</div>
                        <div>typescript@5.5.4</div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
