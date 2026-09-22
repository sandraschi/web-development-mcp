"""Web Development MCP - webapp REST backend (fleet-start uvicorn target ``server:app``).

Serves the web_sota dashboard: health/status, capabilities, real process
metrics, activity logs, file-backed skills, live LLM provider discovery
(Ollama/LM Studio probed over TCP — no hardcoding, no mocks), an Ollama
chat proxy (honest 503 when no provider is running), diagnostics, and an
orderly shutdown endpoint for the fleet launcher.
"""

import json
import os
import platform
import socket
import sys
import threading
import time
from collections import deque
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

import requests
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, Response, StreamingResponse

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
BACKEND_PORT = int(os.getenv("WEB_PORT", "10853"))
FRONTEND_PORT = int(os.getenv("VITE_PORT", "10852"))
VERSION = "0.1.0"
STARTED_AT = time.time()

# Fleet CORS standard (mcp-central-docs/standards/CORS_STANDARD.md):
# explicit origins + unconditional tailnet/LAN/Tauri regex. Never ["*"].
_CORS_ORIGINS = [
    f"http://localhost:{FRONTEND_PORT}",
    f"http://127.0.0.1:{FRONTEND_PORT}",
    f"http://localhost:{BACKEND_PORT}",
    f"http://127.0.0.1:{BACKEND_PORT}",
    # Tauri WebView (always include, harmless when not in Tauri)
    "tauri://localhost",
    "http://tauri.localhost",
    "https://tauri.localhost",
]
_CORS_REGEX = r"https?://(?:[a-zA-Z0-9-]+\.ts\.net|.*?\.tail-[a-f0-9]+\.ts\.net|tauri\.localhost|localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|100\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$|^tauri://localhost$"


class ActivityLog:
    def __init__(self, max_entries=2000):
        self.max_entries = max_entries
        self._entries = deque(maxlen=max_entries)

    def add(self, level, kind, detail, meta=None):
        eid = f"{time.time():.6f}.{uuid4().hex[:6]}"
        self._entries.append(
            {
                "id": eid,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
                "level": level.upper(),
                "kind": kind,
                "detail": detail,
                "meta": meta or {},
            }
        )
        return eid

    def info(self, kind, detail, **meta):
        return self.add("INFO", kind, detail, meta)

    def warn(self, kind, detail, **meta):
        return self.add("WARNING", kind, detail, meta)

    def error(self, kind, detail, **meta):
        return self.add("ERROR", kind, detail, meta)

    def query(self, limit=50, offset=0, level=None, kind=None, search=None, sort="desc", after_id=None):
        entries = list(self._entries)
        if after_id:
            try:
                at = float(after_id.split(".")[0])
                entries = [e for e in entries if float(e["id"].split(".")[0]) > at]
            except Exception:
                pass
        if level:
            lo = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
            ml = lo.get(level.upper(), 1)
            entries = [e for e in entries if lo.get(e["level"], 1) >= ml]
        if kind:
            entries = [e for e in entries if e["kind"] == kind]
        if search:
            q = search.lower()
            entries = [e for e in entries if q in e["detail"].lower()]
        entries.sort(key=lambda e: e["id"], reverse=(sort == "desc"))
        total = len(entries)
        page = entries[offset : offset + limit]
        return {
            "entries": page,
            "total": total,
            "limit": limit,
            "offset": offset,
            "max_entries": self.max_entries,
            "sort": sort,
        }

    def stats(self):
        levels, kinds = {}, {}
        for e in self._entries:
            levels[e["level"]] = levels.get(e["level"], 0) + 1
            kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
        return {"total": len(self._entries), "max_entries": self.max_entries, "levels": levels, "kinds": kinds}

    def export(self, format="json", **filters):
        result = self.query(limit=self.max_entries, **filters)
        if format == "csv":
            import csv
            import io

            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(["id", "timestamp", "level", "kind", "detail", "meta"])
            for e in result["entries"]:
                w.writerow([e["id"], e["timestamp"], e["level"], e["kind"], e["detail"], json.dumps(e["meta"])])
            return buf.getvalue()
        return json.dumps(result["entries"], indent=2)

    def clear(self):
        self._entries.clear()


al = ActivityLog()


# --- live LLM discovery (real TCP probes, fail-soft) --------------------------
OLLAMA_URL = "http://127.0.0.1:11434"
LMSTUDIO_URL = "http://127.0.0.1:1234"


def _tcp_open(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _discover_providers() -> list:
    ollama = _tcp_open("127.0.0.1", 11434)
    lmstudio = _tcp_open("127.0.0.1", 1234)
    return [
        {"id": "ollama", "name": "Ollama (local, free)", "detected": ollama, "base_url": OLLAMA_URL},
        {"id": "lmstudio", "name": "LM Studio (local, free)", "detected": lmstudio, "base_url": LMSTUDIO_URL},
        {
            "id": "openai",
            "name": "OpenAI (cloud, paid)",
            "detected": False,
            "configured": bool(os.getenv("OPENAI_API_KEY")),
        },
        {
            "id": "anthropic",
            "name": "Anthropic (cloud, paid)",
            "detected": False,
            "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        },
    ]


def _ollama_models() -> tuple:
    """Live model list from Ollama; (models, live: bool)."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        r.raise_for_status()
        names = [m.get("name") for m in r.json().get("models", []) if m.get("name")]
        return names, True
    except Exception:
        return [], False


_FALLBACK_MODELS = ["llama3.1", "qwen2.5", "mistral"]


def _read_skills() -> list:
    """File-backed skill registry: every skills/*/SKILL.md on disk."""
    skills = []
    if not SKILLS_DIR.is_dir():
        return skills
    for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        try:
            skills.append({"id": path.parent.name, "content": path.read_text(encoding="utf-8")})
        except OSError:
            continue
    return skills


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.activity_log = al
    al.info("server", "Server started")
    yield


app = FastAPI(title="Web Development MCP", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_CORS_ORIGINS,
    allow_origin_regex=_CORS_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/api/health")
async def health():
    return {"status": "ok", "server": "Web Development MCP", "version": VERSION}


@app.get("/api/status")
async def status():
    return {
        "status": "ok",
        "server": "Web Development MCP",
        "version": VERSION,
        "uptime_seconds": round(time.time() - STARTED_AT, 1),
        "pid": os.getpid(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "ports": {"backend": BACKEND_PORT, "frontend": FRONTEND_PORT},
    }


@app.get("/api/capabilities")
async def capabilities():
    return {
        "backend": {"port": BACKEND_PORT, "framework": "fastapi"},
        "frontend": {"port": FRONTEND_PORT},
        "features": ["scaffolding", "packages", "build-config", "components", "logs", "chat-proxy", "llm-discovery"],
        "mcp": {"transport": ["stdio", "http"], "path": "/mcp", "port": BACKEND_PORT},
        "skills": [s["id"] for s in _read_skills()],
    }


@app.get("/api/metrics")
async def metrics():
    stats = al.stats()
    return {
        "uptime_seconds": round(time.time() - STARTED_AT, 1),
        "tasks": stats["total"],
        "log_levels": stats["levels"],
        "pid": os.getpid(),
    }


@app.get("/api/skills")
async def skills():
    found = _read_skills()
    if not found:
        return {"skills": [], "message": "No skills installed yet (skills/*/SKILL.md)."}
    return {"skills": [{"id": s["id"], "content": s["content"]} for s in found]}


@app.get("/api/llm/discover")
async def llm_discover():
    return {"providers": _discover_providers()}


@app.get("/api/llm/providers")
async def llm_providers():
    return {"providers": _discover_providers()}


@app.get("/api/llm/models")
async def llm_models(provider: str = "ollama"):
    if provider == "ollama":
        names, live = _ollama_models()
        if live:
            return {"provider": provider, "models": names, "fallback": False}
        return {
            "provider": provider,
            "models": list(_FALLBACK_MODELS),
            "fallback": True,
            "message": "Ollama not reachable — curated fallback list.",
        }
    if provider == "lmstudio":
        return {
            "provider": provider,
            "models": [],
            "fallback": True,
            "message": "LM Studio model listing needs the server running on :1234.",
        }
    return {
        "provider": provider,
        "models": [],
        "fallback": True,
        "message": "Cloud model lists require a configured API key.",
    }


@app.get("/api/llm/onboarding")
async def llm_onboarding():
    providers = _discover_providers()
    local = [p for p in providers if p["id"] in ("ollama", "lmstudio") and p["detected"]]
    return {
        "facts": [
            "Ollama (free, local) serves open models on 127.0.0.1:11434.",
            "LM Studio (free, local) serves OpenAI-compatible models on 127.0.0.1:1234.",
            "Cloud providers need an API key stored server-side (never in the browser).",
        ],
        "recommended": "ollama" if not local else local[0]["id"],
        "detected": [p["id"] for p in local],
    }


def _chat_via_ollama(query: str, system_prompt: str, model: str | None):
    names, live = _ollama_models()
    chosen = model or (names[0] if names else _FALLBACK_MODELS[0])
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": chosen,
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}],
            "stream": False,
        },
        timeout=180,
    )
    r.raise_for_status()
    content = (r.json().get("message") or {}).get("content", "(no response)")
    return {"success": True, "reply": content, "provider": "ollama", "model": chosen}


@app.post("/api/llm/chat")
async def llm_chat(payload: dict):
    query = (payload.get("query") or "").strip()
    if not query:
        return JSONResponse(status_code=400, content={"success": False, "message": "Empty query."})
    system_prompt = payload.get("system_prompt") or "You are a helpful web development assistant."
    if not _tcp_open("127.0.0.1", 11434):
        al.warn("chat", "Chat requested with no local LLM running")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "message": "No local LLM detected. Start Ollama (:11434) or LM Studio (:1234), then retry.",
                "providers": _discover_providers(),
            },
        )
    try:
        return _chat_via_ollama(query, system_prompt, payload.get("model"))
    except Exception as e:
        al.error("chat", f"Ollama chat failed: {e}")
        return JSONResponse(status_code=502, content={"success": False, "message": f"LLM request failed: {e}"})


@app.post("/api/llm/chat/stream")
async def llm_chat_stream(payload: dict):
    query = (payload.get("query") or "").strip()
    if not query:
        return JSONResponse(status_code=400, content={"success": False, "message": "Empty query."})
    if not _tcp_open("127.0.0.1", 11434):
        return JSONResponse(status_code=503, content={"success": False, "message": "No local LLM detected."})
    system_prompt = payload.get("system_prompt") or "You are a helpful web development assistant."
    names, live = _ollama_models()
    chosen = payload.get("model") or (names[0] if names else _FALLBACK_MODELS[0])

    def _gen():
        try:
            with requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": chosen,
                    "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}],
                    "stream": True,
                },
                timeout=180,
                stream=True,
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        yield line + b"\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}).encode() + b"\n"

    return StreamingResponse(_gen(), media_type="application/x-ndjson")


@app.get("/api/v1/diagnostics")
async def diagnostics(request: Request):
    routes = sorted({getattr(r, "path", str(r)) for r in request.app.routes})
    log = getattr(request.app.state, "activity_log", None)
    recent_errors = log.query(limit=20, level="ERROR")["entries"] if log else []
    stats = log.stats() if log else {"total": 0}
    return {
        "server": "Web Development MCP",
        "version": VERSION,
        "uptime_seconds": round(time.time() - STARTED_AT, 1),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        "routes": routes,
        "log_stats": stats,
        "recent_errors": recent_errors,
    }


@app.post("/api/shutdown")
async def shutdown():
    """Orderly exit for the fleet launcher: 200 now, process exit 500 ms later."""

    def _exit():
        time.sleep(0.5)
        os._exit(0)

    threading.Thread(target=_exit, daemon=True).start()
    al.warn("server", "Shutdown requested via /api/shutdown")
    return {"success": True, "message": "Shutting down."}


@app.get("/api/logs")
async def get_logs(
    request: Request, limit=50, offset=0, level=None, kind=None, search=None, sort="desc", after_id=None
):
    log = getattr(request.app.state, "activity_log", None)
    if not log:
        return {"entries": [], "total": 0, "limit": limit, "offset": offset, "max_entries": 0, "sort": sort}
    return log.query(limit=limit, offset=offset, level=level, kind=kind, search=search, sort=sort, after_id=after_id)


@app.get("/api/logs/stats")
async def logs_stats(request: Request):
    log = getattr(request.app.state, "activity_log", None)
    if not log:
        return {"total": 0, "max_entries": 0, "levels": {}, "kinds": {}}
    return log.stats()


@app.get("/api/logs/export")
async def logs_export(request: Request, format="json", level=None, kind=None, search=None):
    log = getattr(request.app.state, "activity_log", None)
    if not log:
        return PlainTextResponse("[]", media_type="application/json")
    content = log.export(format=format, level=level, kind=kind, search=search)
    media = "text/csv" if format == "csv" else "application/json"
    return Response(
        content=content, media_type=media, headers={"Content-Disposition": f'attachment; filename="logs.{format}"'}
    )


@app.delete("/api/logs")
async def clear_logs(request: Request):
    log = getattr(request.app.state, "activity_log", None)
    if log:
        log.clear()
    return {"success": True, "message": "Logs cleared."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=BACKEND_PORT)
