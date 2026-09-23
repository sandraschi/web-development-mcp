import { useCallback, useEffect, useState } from "react";
import { cn } from "@/common/utils";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const API_BASE =
  (import.meta as unknown as { env?: { VITE_API_TARGET?: string } }).env
    ?.VITE_API_TARGET ?? "http://127.0.0.1:10853";

type Provider = {
  id: string;
  name: string;
  detected: boolean;
  base_url?: string;
  configured?: boolean;
};

function persistProvider(p: string, m: string) {
  try {
    localStorage.setItem("llm_provider", p);
    localStorage.setItem("llm_model", m);
  } catch {
    /* private mode */
  }
}

function LLMSettings() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [selectedProvider, setSelectedProvider] = useState(() => {
    try {
      return localStorage.getItem("llm_provider") || "ollama";
    } catch {
      return "ollama";
    }
  });
  const [models, setModels] = useState<string[]>([]);
  const [modelsFallback, setModelsFallback] = useState(false);
  const [selectedModel, setSelectedModel] = useState(() => {
    try {
      return localStorage.getItem("llm_model") || "";
    } catch {
      return "";
    }
  });
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [error, setError] = useState("");

  const loadModels = useCallback(async (providerId: string) => {
    const r = await fetch(`${API_BASE}/api/llm/models?provider=${providerId}`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const data = await r.json();
    const names: string[] = data.models ?? [];
    setModels(names);
    setModelsFallback(data.fallback === true);
    let saved = "";
    try {
      saved = localStorage.getItem("llm_model") || "";
    } catch {
      /* private mode */
    }
    const pick = saved && names.includes(saved) ? saved : names[0] || "";
    setSelectedModel(pick);
    persistProvider(providerId, pick);
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const r = await fetch(`${API_BASE}/api/llm/providers`);
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = await r.json();
        if (cancelled) return;
        const list: Provider[] = data.providers ?? [];
        setProviders(list);
        const current = (() => {
          try {
            return localStorage.getItem("llm_provider") || "ollama";
          } catch {
            return "ollama";
          }
        })();
        const known = list.some((p) => p.id === current)
          ? current
          : list[0]?.id || "ollama";
        setSelectedProvider(known);
        await loadModels(known);
        if (!cancelled) setState("ok");
      } catch (e) {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : "Backend unreachable");
        setState("error");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [loadModels]);

  const onProviderChange = async (id: string) => {
    setSelectedProvider(id);
    setState("loading");
    try {
      await loadModels(id);
      setState("ok");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Model list failed");
      setState("error");
    }
  };

  const onModelChange = (m: string) => {
    setSelectedModel(m);
    persistProvider(selectedProvider, m);
  };

  return (
    <Card
      className="border-slate-800 bg-slate-950/50 text-slate-100"
      data-testid="llm-settings"
    >
      <CardHeader>
        <CardTitle className="text-white">Local LLM</CardTitle>
        <CardDescription className="text-slate-300">
          Auto-detected providers. Local is free; cloud needs a server-side key
          (see Onboarding).
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {state === "loading" && (
          <p className="text-sm text-slate-300">Probing providers...</p>
        )}
        {state === "error" && (
          <div className="rounded border border-red-900 p-3">
            <p className="text-sm text-red-300">
              Provider discovery failed: {error}
            </p>
            <button
              type="button"
              className="mt-2 text-sm px-3 py-1.5 rounded border border-slate-700 text-slate-200 hover:bg-slate-800"
              onClick={() => window.location.reload()}
            >
              Retry
            </button>
          </div>
        )}
        {state === "ok" && (
          <>
            <div className="grid gap-2" data-testid="llm-provider-cards">
              {providers.map((p) => (
                <button
                  key={p.id}
                  type="button"
                  data-testid={`llm-provider-card-${p.id}`}
                  onClick={() => onProviderChange(p.id)}
                  className={cn(
                    "flex items-center justify-between rounded border px-3 py-2 text-left text-sm",
                    p.id === selectedProvider
                      ? "border-blue-600 bg-blue-950/30"
                      : "border-slate-800 bg-slate-900/40 hover:border-slate-600",
                  )}
                >
                  <span className="text-slate-200">{p.name}</span>
                  <span className="flex items-center gap-1.5 text-sm">
                    <span
                      className={cn(
                        "h-2 w-2 rounded-full",
                        p.detected || p.configured
                          ? "bg-green-500"
                          : "bg-gray-500",
                      )}
                    />
                    <span className="text-slate-300">
                      {p.detected
                        ? "detected"
                        : p.configured
                          ? "key configured"
                          : "not found"}
                    </span>
                  </span>
                </button>
              ))}
            </div>
            <select
              data-testid="llm-provider-select"
              className="h-9 w-full rounded-md border border-slate-700 bg-slate-900 px-3 text-sm text-slate-200"
              value={selectedProvider}
              onChange={(e) => onProviderChange(e.target.value)}
            >
              {providers.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>
            <select
              data-testid="llm-model-select"
              className="h-9 w-full rounded-md border border-slate-700 bg-slate-900 px-3 text-sm text-slate-200"
              value={selectedModel}
              onChange={(e) => onModelChange(e.target.value)}
            >
              {models.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            {modelsFallback && (
              <p className="text-sm text-amber-300">
                Provider not reachable — showing curated fallback list.
              </p>
            )}
            {models.length === 0 && (
              <p className="text-sm text-slate-300">
                No models found. Start Ollama (:11434) or LM Studio (:1234), or
                add a cloud key server-side per docs/ONBOARDING.md.
              </p>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

export function Settings() {
  return (
    <div className="space-y-6" data-testid="settings-page">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">
          Settings
        </h2>
        <p className="text-slate-300">
          Manage MCP endpoints and workspace preferences
        </p>
      </div>

      <div className="grid gap-6">
        <Card className="border-slate-800 bg-slate-950/50 text-slate-100">
          <CardHeader>
            <CardTitle className="text-white">MCP Infrastructure</CardTitle>
            <CardDescription className="text-slate-300">
              Backend connectivity and port allocation
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label className="text-slate-300">API Endpoint (Backend)</Label>
              <Input
                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-300"
                defaultValue="http://localhost:10853"
              />
            </div>
            <div className="grid gap-2">
              <Label className="text-slate-300">Frontend Port</Label>
              <Input
                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-300"
                defaultValue="10852"
              />
            </div>
            <Button
              variant="outline"
              className="border-slate-800 text-slate-300 hover:bg-slate-800"
            >
              Check Backend Health
            </Button>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50 text-slate-100">
          <CardHeader>
            <CardTitle className="text-white">Workspace Standards</CardTitle>
            <CardDescription className="text-slate-300">
              Austrian dev standards and project pathing
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label className="text-slate-300">Root Workspace</Label>
              <Input
                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-300"
                defaultValue="D:\Dev\repos"
              />
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="strict"
                className="rounded border-slate-800 bg-slate-900"
                defaultChecked
              />
              <Label htmlFor="strict" className="text-slate-300">
                Enforce Strict FastMCP (3.4+)
              </Label>
            </div>
            <Button
              variant="outline"
              className="border-slate-800 text-slate-300 hover:bg-slate-800"
            >
              Save Changes
            </Button>
          </CardContent>
        </Card>

        <LLMSettings />
      </div>
    </div>
  );
}
