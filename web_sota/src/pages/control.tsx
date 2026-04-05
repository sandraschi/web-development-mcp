import { useState } from "react";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription,
    CardFooter
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/common/utils";
import {
    Terminal,
    Play,
    Search,
    Code,
    Cpu,
    Hammer,
    ShieldAlert,
    CheckCircle2,
    Sparkles,
    History,
    Zap
} from "lucide-react";

export function Control() {
    const [securityApproval, setSecurityApproval] = useState(false);
    const [isAutonomous, setIsAutonomous] = useState(false);
    const [goal, setGoal] = useState("");
    const [auditLog, setAuditLog] = useState<string[]>([]);

    const addLog = (msg: string) => {
        setAuditLog(prev => [`[${new Date().toLocaleTimeString()}] ${msg}`, ...prev].slice(0, 10));
    };

    const handleExecuteWorkflow = () => {
        if (!securityApproval) {
            addLog("ERROR: Security Guard must be enabled for Autonomous Orchestration.");
            return;
        }
        setIsAutonomous(true);
        addLog(`Initiating autonomous workflow: "${goal}"`);
        setTimeout(() => {
            setIsAutonomous(false);
            addLog(`Workflow completed: ${goal}`);
        }, 3000);
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Tools Lab</h2>
                    <p className="text-slate-400">Dynamic analysis and execution of WebDev MCP tools</p>
                </div>
                <div className={cn(
                    "flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-semibold uppercase tracking-wider transition-all duration-300",
                    securityApproval ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" : "bg-red-500/10 text-red-400 border border-red-500/20"
                )}>
                    {securityApproval ? <CheckCircle2 className="h-4 w-4" /> : <ShieldAlert className="h-4 w-4" />}
                    {securityApproval ? "Authorized" : "Unauthorized"}
                </div>
            </div>

            <Card className="border-slate-800 bg-slate-950/40 backdrop-blur-xl border-l-4 border-l-amber-500/50">
                <CardHeader className="pb-3">
                    <div className="flex items-center gap-2 text-amber-500">
                        <ShieldAlert className="h-5 w-5" />
                        <CardTitle className="text-lg">Security Guard</CardTitle>
                    </div>
                    <CardDescription className="text-slate-400">
                        Agentic control and autonomous orchestration require explicit session authorization.
                    </CardDescription>
                </CardHeader>
                <CardFooter>
                    <Button
                        variant={securityApproval ? "destructive" : "default"}
                        onClick={() => {
                            setSecurityApproval(!securityApproval);
                            addLog(`Security Guard ${!securityApproval ? 'ENABLED' : 'DISABLED'}`);
                        }}
                        className={cn(
                            "w-full sm:w-auto font-bold transition-all duration-300",
                            !securityApproval && "bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-900/20"
                        )}
                    >
                        {securityApproval ? "Revoke Authorization" : "Enable Safety Guard"}
                    </Button>
                </CardFooter>
            </Card>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <ToolCategoryCard
                    title="Scaffolding"
                    description="Project initialization"
                    count={5}
                    icon={Cpu}
                    color="text-emerald-400"
                />
                <ToolCategoryCard
                    title="Packages"
                    description="Dependency management"
                    count={4}
                    icon={Code}
                    color="text-blue-400"
                />
                <ToolCategoryCard
                    title="Agentic"
                    description="Autonomous orchestration"
                    count={2}
                    icon={Sparkles}
                    color="text-purple-400"
                />
                <ToolCategoryCard
                    title="Build"
                    description="Pipeline tools"
                    count={4}
                    icon={Hammer}
                    color="text-amber-400"
                />
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
                <Card className="lg:col-span-2 border-slate-800 bg-slate-950/50 backdrop-blur-md">
                    <CardHeader>
                        <div className="flex items-center gap-2 text-purple-400">
                            <Sparkles className="h-5 w-5" />
                            <CardTitle>Autonomous Orchestration</CardTitle>
                        </div>
                        <CardDescription>Achieve high-level goals using SEP-1577 Sampling.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Mission Goal</label>
                            <div className="relative">
                                <Sparkles className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-600" />
                                <input
                                    className="w-full bg-slate-900/50 border border-slate-800 rounded-lg pl-10 pr-3 py-3 text-sm text-slate-200 outline-none focus:ring-2 focus:ring-purple-500/50 transition-all"
                                    placeholder="e.g., Implement a login form with validation..."
                                    value={goal}
                                    onChange={(e) => setGoal(e.target.value)}
                                />
                            </div>
                        </div>
                        <Button
                            className="bg-purple-600 hover:bg-purple-700 text-white font-bold h-12 px-8 transition-transform active:scale-95 disabled:opacity-50 disabled:grayscale"
                            disabled={!securityApproval || !goal || isAutonomous}
                            onClick={handleExecuteWorkflow}
                        >
                            {isAutonomous ? (
                                <>
                                    <Zap className="mr-2 h-4 w-4 animate-bounce" />
                                    Orchestrating...
                                </>
                            ) : (
                                <>
                                    <Play className="mr-2 h-4 w-4" />
                                    Initiate Mission
                                </>
                            )}
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50 backdrop-blur-md flex flex-col">
                    <CardHeader className="pb-3 border-b border-slate-800/50">
                        <div className="flex items-center gap-2 text-slate-400">
                            <History className="h-4 w-4" />
                            <CardTitle className="text-sm uppercase tracking-widest font-bold">Action Audit</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent className="flex-1 p-0 overflow-y-auto">
                        <div className="divide-y divide-slate-800/50">
                            {auditLog.length === 0 ? (
                                <div className="p-8 text-center text-slate-600 italic text-sm">
                                    No actions recorded in this session.
                                </div>
                            ) : (
                                auditLog.map((log, i) => (
                                    <div key={i} className="p-3 text-xs font-mono text-slate-300 hover:bg-white/5 transition-colors">
                                        {log}
                                    </div>
                                ))
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="explorer" className="space-y-4">
                <TabsList className="bg-slate-950/50 border border-slate-800">
                    <TabsTrigger value="explorer" className="data-[state=active]:bg-slate-800">Tool Explorer</TabsTrigger>
                    <TabsTrigger value="active" className="data-[state=active]:bg-slate-800">Active Tasks</TabsTrigger>
                </TabsList>
                <TabsContent value="explorer" className="space-y-4">
                    <Card className="border-slate-800 bg-slate-950/50">
                        <CardHeader>
                            <CardTitle className="text-white text-lg">`scaffolding_tools:create_react_app`</CardTitle>
                            <CardDescription>Creates a new React application with TypeScript and modern tooling.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4 font-sans">
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Project Name</label>
                                        <input className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-2 text-sm text-slate-200 outline-none focus:ring-1 focus:ring-emerald-500" defaultValue="my-new-app" />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Directory</label>
                                        <input className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-2 text-sm text-slate-200 outline-none focus:ring-1 focus:ring-emerald-500" defaultValue="D:\Dev\repos" />
                                    </div>
                                </div>
                                <div className="flex items-center gap-4 py-2">
                                    <div className="flex items-center gap-2">
                                        <input type="checkbox" id="router" className="rounded border-slate-700 bg-slate-800" defaultChecked />
                                        <label htmlFor="router" className="text-sm text-slate-300">React Router</label>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <input type="checkbox" id="testing" className="rounded border-slate-700 bg-slate-800" defaultChecked />
                                        <label htmlFor="testing" className="text-sm text-slate-300">Vitest Setup</label>
                                    </div>
                                </div>
                                <Button className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold" disabled={!securityApproval}>
                                    <Play className="mr-2 h-4 w-4" />
                                    Execute Tool
                                </Button>
                                {!securityApproval && (
                                    <p className="text-xs text-red-400 italic">Authorization required.</p>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}

function ToolCategoryCard({ title, description, count, icon: Icon, color }: any) {
    return (
        <Card className="border-slate-800 bg-slate-950/50 hover:bg-slate-900/50 transition-all cursor-pointer group">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">{title}</CardTitle>
                <Icon className={cn("h-4 w-4", color)} />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold text-white">{count} Tools</div>
                <p className="text-xs text-slate-400 mt-1">{description}</p>
            </CardContent>
        </Card>
    );
}
