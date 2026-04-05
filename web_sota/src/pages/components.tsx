import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Box, Copy, Layers, Layout, Palette, Code, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function Components() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Component Factory</h2>
                    <p className="text-slate-400">Design, prototype, and export SOTA UI components</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-900">
                        <Palette className="mr-2 h-4 w-4" />
                        Theme Editor
                    </Button>
                    <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">
                        <Check className="mr-2 h-4 w-4" />
                        Verify All
                    </Button>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-4">
                <Card className="border-slate-800 bg-slate-950/50 md:col-span-1">
                    <CardHeader>
                        <CardTitle className="text-white text-sm">Library</CardTitle>
                        <CardDescription>Core Atoms & Molecules</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-1">
                        {['Button', 'Input', 'Card', 'Badge', 'Dialog', 'Popover', 'Tabs', 'Toast'].map((item) => (
                            <div key={item} className="flex items-center justify-between p-2 rounded hover:bg-slate-900 cursor-pointer group">
                                <span className="text-sm text-slate-300">{item}</span>
                                <Badge variant="outline" className="text-[10px] py-0 border-slate-800 opacity-0 group-hover:opacity-100 transition-opacity">SOTA</Badge>
                            </div>
                        ))}
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50 md:col-span-3">
                    <CardHeader className="border-b border-slate-800 flex flex-row items-center justify-between space-y-0 py-4">
                        <div className="flex items-center gap-3">
                            <Box className="h-5 w-5 text-indigo-400" />
                            <CardTitle className="text-white">Button.tsx</CardTitle>
                        </div>
                        <div className="flex gap-2">
                            <Button size="icon" variant="ghost" className="h-8 w-8 text-slate-400"><Code className="h-4 w-4" /></Button>
                            <Button size="icon" variant="ghost" className="h-8 w-8 text-slate-400"><Copy className="h-4 w-4" /></Button>
                            <Button size="icon" variant="ghost" className="h-8 w-8 text-slate-400"><Layers className="h-4 w-4" /></Button>
                        </div>
                    </CardHeader>
                    <CardContent className="p-12 flex flex-col items-center justify-center min-h-[400px] bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:20px_20px]">
                        <div className="space-y-8 text-center">
                            <div className="flex gap-4 items-center">
                                <Button className="bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-500/20">Primary SOTA</Button>
                                <Button variant="outline" className="border-slate-700 bg-slate-900/50 backdrop-blur-sm">Glass Secondary</Button>
                                <Button variant="ghost" className="text-slate-400 hover:text-white">Ghost Subtle</Button>
                            </div>
                            <div className="text-xs text-slate-500 font-mono">
                                Component Preview: Interactive State Lab
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white flex items-center gap-2">
                            <Layout className="h-4 w-4 text-blue-400" />
                            Prop Explorer
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                            <span className="text-sm font-mono text-slate-400">variant</span>
                            <Badge className="bg-indigo-500/20 text-indigo-400">"primary" | "secondary" | "ghost"</Badge>
                        </div>
                        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                            <span className="text-sm font-mono text-slate-400">size</span>
                            <Badge className="bg-indigo-500/20 text-indigo-400">"default" | "sm" | "lg" | "icon"</Badge>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-mono text-slate-400">asChild</span>
                            <Badge className="bg-slate-800 text-slate-400">boolean</Badge>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white flex items-center gap-2">
                            <Code className="h-4 w-4 text-emerald-400" />
                            Auto-Scaffold JSX
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <pre className="p-4 bg-slate-900 border border-slate-800 rounded font-mono text-xs text-emerald-400/80 overflow-x-auto">
                            {`<Button 
  variant="primary" 
  size="default"
  className="shadow-indigo-500/20"
>
  Start Building
</Button>`}
                        </pre>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
