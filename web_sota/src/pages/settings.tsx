import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input"; // We'll need to create this or use standard input
import { Label } from "@/components/ui/label"; // We'll need to create this or use standard label

export function Settings() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold tracking-tight text-white">Settings</h2>
                <p className="text-slate-400">Manage MCP endpoints and workspace preferences</p>
            </div>

            <div className="grid gap-6">
                <Card className="border-slate-800 bg-slate-950/50 text-slate-100">
                    <CardHeader>
                        <CardTitle className="text-white">MCP Infrastructure</CardTitle>
                        <CardDescription className="text-slate-400">Backend connectivity and port allocation</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-2">
                            <Label className="text-slate-300">API Endpoint (Backend)</Label>
                            <Input
                                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-400"
                                defaultValue="http://localhost:10853"
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label className="text-slate-300">Frontend Port</Label>
                            <Input
                                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-400"
                                defaultValue="10852"
                            />
                        </div>
                        <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                            Check Backend Health
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50 text-slate-100">
                    <CardHeader>
                        <CardTitle className="text-white">Workspace Standards</CardTitle>
                        <CardDescription className="text-slate-400">Austrian dev standards and project pathing</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-2">
                            <Label className="text-slate-300">Root Workspace</Label>
                            <Input
                                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-400"
                                defaultValue="D:\Dev\repos"
                            />
                        </div>
                        <div className="flex items-center space-x-2">
                            <input type="checkbox" id="strict" className="rounded border-slate-800 bg-slate-900" defaultChecked />
                            <Label htmlFor="strict" className="text-slate-300">Enforce Strict FastMCP (2.14+)</Label>
                        </div>
                        <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                            Save Changes
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
