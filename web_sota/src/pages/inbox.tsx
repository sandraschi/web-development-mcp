import { Inbox as InboxIcon } from "lucide-react";
import { useEffect, useState } from "react";
import { cn } from "@/common/utils";

const API_BASE =
  (import.meta as unknown as { env?: { VITE_API_TARGET?: string } }).env
    ?.VITE_API_TARGET ?? "http://127.0.0.1:10853";

type Entry = {
  id: string;
  timestamp: string;
  level: string;
  kind: string;
  detail: string;
};

export function Inbox() {
  const [entries, setEntries] = useState<Entry[]>([]);
  const [total, setTotal] = useState(0);
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_BASE}/api/logs?level=WARNING&limit=50&sort=desc`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = await r.json();
        if (cancelled) return;
        setEntries(data.entries ?? []);
        setTotal(data.total ?? 0);
        setState("ok");
      })
      .catch((e) => {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : "Backend unreachable");
        setState("error");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="space-y-6" data-testid="inbox-page">
      <header>
        <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
          <InboxIcon className="h-7 w-7 text-emerald-500" />
          Inbox
        </h2>
        <p className="mt-2 text-sm text-slate-300">
          Backend warnings and errors needing triage ({total} in ring buffer).
        </p>
      </header>

      {state === "loading" && (
        <p className="text-sm text-slate-300">Loading inbox...</p>
      )}
      {state === "error" && (
        <div className="rounded border border-red-900 p-4">
          <p className="text-sm text-red-300">Inbox unavailable: {error}</p>
          <button
            type="button"
            className="mt-2 text-sm px-3 py-1.5 rounded border border-slate-700 text-slate-200 hover:bg-slate-800"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      )}
      {state === "ok" && entries.length === 0 && (
        <p className="text-sm text-slate-300">
          All quiet — no warnings or errors logged. Healthy systems are boring.
        </p>
      )}
      {state === "ok" && entries.length > 0 && (
        <div className="space-y-2">
          {entries.map((e) => (
            <div
              key={e.id}
              className="flex items-start gap-3 rounded border border-slate-800 bg-slate-950/50 p-3"
            >
              <span
                className={cn(
                  "mt-0.5 rounded px-2 py-0.5 text-sm font-bold",
                  e.level === "ERROR"
                    ? "bg-red-950 text-red-300"
                    : "bg-amber-950 text-amber-300",
                )}
              >
                {e.level}
              </span>
              <div className="flex-1">
                <p className="text-sm text-slate-200">
                  [{e.kind}] {e.detail}
                </p>
                <p className="text-sm text-slate-300">{e.timestamp} UTC</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
