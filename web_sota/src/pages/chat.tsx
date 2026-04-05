import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Send, Bot, User } from "lucide-react";

export function Chat() {
    return (
        <div className="flex h-[calc(100vh-8rem)] flex-col space-y-4">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">AI Command</h2>
                    <p className="text-slate-400">Natural language tool orchestration and code generation</p>
                </div>
            </div>

            <Card className="flex-1 border-slate-800 bg-slate-950/50 flex flex-col overflow-hidden">
                <CardContent className="flex-1 overflow-y-auto p-4 space-y-4 font-sans">
                    <div className="flex gap-3">
                        <div className="h-8 w-8 rounded-full bg-blue-900/20 flex items-center justify-center border border-blue-800">
                            <Bot className="h-4 w-4 text-blue-400" />
                        </div>
                        <div className="flex-1 space-y-1">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium text-blue-400">WebDev AI</span>
                                <span className="text-xs text-slate-500">System Ready</span>
                            </div>
                            <div className="text-sm text-slate-300 bg-blue-950/10 p-3 rounded-md border border-blue-900/30 inline-block">
                                <p>Greetings, Sandra. I am connected to the **WebDev Hub** toolchain (Port 10853).</p>
                                <p className="mt-2">I can assist with:</p>
                                <ul className="mt-1 list-inside list-disc text-blue-300/80">
                                    <li>Scaffolding React/Next.js/Vue apps</li>
                                    <li>Managing npm/yarn dependencies</li>
                                    <li>Generating SOTA components & tests</li>
                                    <li>Orchestrating Vite builds and audits</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-3">
                        <div className="h-8 w-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
                            <User className="h-4 w-4 text-slate-400" />
                        </div>
                        <div className="flex-1 space-y-1">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium text-slate-200">Sandra</span>
                                <span className="text-xs text-slate-500">Active Session</span>
                            </div>
                            <p className="text-sm text-slate-300 bg-slate-900/50 p-3 rounded-md border border-slate-800 inline-block italic">
                                Scaffolding a new React project with Tailwind and router...
                            </p>
                        </div>
                    </div>

                    <div className="flex gap-3">
                        <div className="h-8 w-8 rounded-full bg-blue-900/20 flex items-center justify-center border border-blue-800">
                            <Bot className="h-4 w-4 text-blue-400" />
                        </div>
                        <div className="flex-1 space-y-1">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium text-blue-400">WebDev AI</span>
                                <span className="text-xs text-slate-500">Processing...</span>
                            </div>
                            <div className="text-sm text-slate-300 bg-blue-950/10 p-3 rounded-md border border-blue-900/30 inline-block">
                                <p>Initiating `scaffolding_tools:create_react_app`...</p>
                                <p className="mt-2 font-mono text-emerald-400 text-xs">
                                    [MOCK] Creating project: my-sota-app <br />
                                    [MOCK] Installing dependencies (Vite, React, Router)...<br />
                                    [MOCK] Configuring Tailwind CSS...
                                </p>
                            </div>
                        </div>
                    </div>
                </CardContent>
                <div className="p-4 border-t border-slate-800 bg-slate-900/30">
                    <div className="flex gap-2">
                        <input
                            className="flex-1 bg-slate-950 border border-slate-800 rounded-md px-4 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none"
                            placeholder="Type a development command (e.g., 'Add shadcn/ui to this project')..."
                        />
                        <Button size="icon" className="bg-blue-600 hover:bg-blue-700">
                            <Send className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    );
}
