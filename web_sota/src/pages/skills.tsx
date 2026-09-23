import { Blocks } from "lucide-react";
import { useEffect, useState } from "react";

const API_BASE =
  (import.meta as unknown as { env?: { VITE_API_TARGET?: string } }).env
    ?.VITE_API_TARGET ?? "http://127.0.0.1:10853";

type Skill = { id: string; content: string };

export function Skills() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [message, setMessage] = useState("");
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_BASE}/api/skills`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = await r.json();
        if (cancelled) return;
        setSkills(data.skills ?? []);
        setMessage(data.message ?? "");
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
    <div className="space-y-6" data-testid="skills-page">
      <header>
        <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
          <Blocks className="h-7 w-7 text-emerald-500" />
          Skills
        </h2>
        <p className="mt-2 text-sm text-slate-300">
          File-backed skill prompts served from <code>skills/*/SKILL.md</code> —
          the same content the Chat page uses as its system preprompt.
        </p>
      </header>

      {state === "loading" && (
        <p className="text-sm text-slate-300">Loading skills...</p>
      )}
      {state === "error" && (
        <div className="rounded border border-red-900 p-4">
          <p className="text-sm text-red-300">Skills unavailable: {error}</p>
          <button
            type="button"
            className="mt-2 text-sm px-3 py-1.5 rounded border border-slate-700 text-slate-200 hover:bg-slate-800"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      )}
      {state === "ok" && skills.length === 0 && (
        <p className="text-sm text-slate-300">
          {message || "No skills installed yet."}
        </p>
      )}
      {state === "ok" &&
        skills.map((s) => (
          <details
            key={s.id}
            className="rounded border border-slate-800 bg-slate-950/50 p-4"
            open={skills.length === 1}
          >
            <summary className="cursor-pointer text-sm font-medium text-slate-200">
              skill:{s.id}
            </summary>
            <pre className="mt-2 overflow-x-auto whitespace-pre-wrap text-sm text-slate-300">
              {s.content}
            </pre>
          </details>
        ))}
    </div>
  );
}
