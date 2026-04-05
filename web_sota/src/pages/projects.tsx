import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus, Rocket, BookOpen, Clock, Settings, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Projects() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Project Lab</h2>
                    <p className="text-slate-400">Scaffold and manage SOTA-compliant projects</p>
                </div>
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                    <Plus className="mr-2 h-4 w-4" />
                    New Project
                </Button>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <Card className="border-slate-800 bg-slate-950/50 hover:bg-slate-900/50 transition-colors cursor-pointer group">
                    <CardHeader>
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-blue-500/10 rounded-lg group-hover:bg-blue-500/20 transition-colors">
                                <Rocket className="h-5 w-5 text-blue-400" />
                            </div>
                            <CardTitle className="text-white">Quick Scaffold</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-slate-400 mb-4">Initialize a new React + Vite + Tailwind project with SOTA protocols pre-configured.</p>
                        <div className="flex items-center text-xs text-blue-400">
                            Start Building <ArrowRight className="ml-1 h-3 w-3" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50 hover:bg-slate-900/50 transition-colors cursor-pointer group">
                    <CardHeader>
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-purple-500/10 rounded-lg group-hover:bg-purple-500/20 transition-colors">
                                <BookOpen className="h-5 w-5 text-purple-400" />
                            </div>
                            <CardTitle className="text-white">Templates</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-slate-400 mb-4">Browse library of industry-standard project structures for microservices, SPAs, and MCP servers.</p>
                        <div className="flex items-center text-xs text-purple-400">
                            Browse Templates <ArrowRight className="ml-1 h-3 w-3" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50 hover:bg-slate-900/50 transition-colors cursor-pointer group">
                    <CardHeader>
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-slate-800 rounded-lg group-hover:bg-slate-700 transition-colors">
                                <Clock className="h-5 w-5 text-slate-400" />
                            </div>
                            <CardTitle className="text-white">Recent Work</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-sm text-slate-400 mb-4">Jump back into your active workspaces: `web-development-mcp`, `robotics-mcp`.</p>
                        <div className="flex items-center text-xs text-slate-400">
                            View History <ArrowRight className="ml-1 h-3 w-3" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Card className="border-slate-800 bg-slate-950/50">
                <CardHeader className="border-b border-slate-800">
                    <CardTitle className="text-white flex items-center gap-2">
                        <Settings className="h-4 w-4 text-slate-400" />
                        Global Scaffolding Config
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                    <div className="grid gap-4 md:grid-cols-2">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Default Target Directory</label>
                            <div className="p-2 bg-slate-900 border border-slate-800 rounded font-mono text-xs text-slate-400">
                                D:\Dev\repos
                            </div>
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Port Range Allocation</label>
                            <div className="p-2 bg-slate-900 border border-slate-800 rounded font-mono text-xs text-slate-400">
                                10700 - 10800
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
