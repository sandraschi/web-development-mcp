import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Send, Bot, User, Download, Eraser, Loader2 } from "lucide-react";

const STORAGE_KEY = "webdev-mcp-chat-history";
const PERSONALITY_KEY = "webdev-mcp-chat-personality";
const BACKEND_PORT = 10853;
const API_BASE = `http://127.0.0.1:${BACKEND_PORT}`;

type Message = { role: "user" | "assistant"; content: string };
type Personality = { id: string; label: string; prompt: string };

const PERSONALITIES: Personality[] = [
  { id: "fullstack", label: "Full-Stack Dev", prompt: "You are a senior full-stack developer. Provide complete working solutions with both frontend and backend code. Be concise and production-oriented." },
  { id: "ui-designer", label: "UI Designer", prompt: "You are a UI/UX designer specializing in modern web interfaces. Focus on visual design, component architecture, accessibility, and user experience patterns." },
  { id: "summarizer", label: "Quick Summarizer", prompt: "You are a technical summarizer. Provide brief, focused answers. Use bullet points and avoid unnecessary explanation." },
  { id: "custom", label: "Custom", prompt: "" },
];

const EXAMPLE_GROUPS = {
  "Code": [
    "Scaffold a React + Tailwind + Router project",
    "Generate a shadcn/ui card component with hover effects",
    "Add TypeScript interfaces for a user profile API response",
  ],
  "Design": [
    "Create a dark-mode dashboard layout with sidebar navigation",
    "Suggest a color palette for a developer tools SaaS app",
    "Design a responsive pricing table with Tailwind CSS",
  ],
  "Deploy": [
    "Configure vite.config.ts for production builds",
    "Set up GitHub Actions for CI/CD with lint and test stages",
    "Write a Dockerfile for a React + Vite app with Nginx",
  ],
};

function loadHistory(): Message[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}

function saveHistory(messages: Message[]) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.slice(-100))); } catch {}
}

function loadPersonality(): string {
  try { return localStorage.getItem(PERSONALITY_KEY) || "fullstack"; } catch { return "fullstack"; }
}

async function fetchAI(query: string, personality: Personality): Promise<string> {
  const systemPrompt = personality.id === "custom"
    ? (localStorage.getItem("webdev-mcp-custom-prompt") || "You are a helpful web development assistant.")
    : `${personality.prompt}\n\nYou are Web Dev MCP, a web development server for code generation, site preview, and deployment. Respond helpfully to the user's request.`;
  const r = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, system_prompt: systemPrompt }),
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const data = await r.json();
  return data.reply || data.response || data.message || "(no response)";
}

async function checkBackend(): Promise<boolean> {
  try {
    const r = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    return r.ok;
  } catch { return false; }
}

export function Chat() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>(loadHistory);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [personalityId, setPersonalityId] = useState(loadPersonality);
  const [backendOk, setBackendOk] = useState<boolean | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  const personality = PERSONALITIES.find(p => p.id === personalityId) || PERSONALITIES[0];

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  useEffect(() => { checkBackend().then(setBackendOk); }, []);

  useEffect(() => {
    saveHistory(messages);
  }, [messages]);

  useEffect(() => {
    localStorage.setItem(PERSONALITY_KEY, personalityId);
  }, [personalityId]);

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || sending) return;
    setSending(true);
    const userMsg: Message = { role: "user", content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    try {
      const reply = await fetchAI(text, personality);
      setMessages(prev => [...prev, { role: "assistant", content: reply }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: "assistant", content: `Error: ${e instanceof Error ? e.message : "Backend unreachable"}` }]);
    } finally {
      setSending(false);
    }
  }, [sending, personality]);

  const handleExport = () => {
    const lines = messages.map(m => {
      const ts = new Date().toISOString();
      return `[${ts}] ${m.role === "user" ? "You" : "Assistant"}: ${m.content}`;
    }).join("\n");
    const blob = new Blob([lines], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `webdev-mcp-chat-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleClear = () => {
    setMessages([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] flex-col space-y-4" data-testid="chat-page">
      <div data-testid="chat-controls" className="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">AI Command</h2>
          <p className="text-slate-400 text-sm">Natural language tool orchestration and code generation</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-xs">
            <span className={`w-2 h-2 rounded-full ${backendOk === null ? "bg-gray-500" : backendOk ? "bg-green-500" : "bg-red-500"}`} />
            <span className="text-slate-400">{backendOk === null ? "Checking..." : backendOk ? "Backend OK" : "Offline"}</span>
          </span>
          <span className="text-xs text-blue-400 bg-blue-950/30 px-2 py-0.5 rounded font-medium">skill:webdev-expert</span>
          <select
            data-testid="personality-select"
            value={personalityId}
            onChange={e => setPersonalityId(e.target.value)}
            className="bg-zinc-800 text-zinc-100 border border-zinc-600 rounded px-2 py-1 text-xs"
          >
            {PERSONALITIES.map(p => (
              <option key={p.id} value={p.id}>{p.label}</option>
            ))}
          </select>
          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-white" onClick={handleExport} disabled={messages.length === 0} data-testid="chat-export" title="Export chat">
            <Download className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-white" onClick={handleClear} disabled={messages.length === 0} data-testid="chat-clear" title="Clear chat">
            <Eraser className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <Card className="flex-1 border-slate-800 bg-slate-950/50 flex flex-col overflow-hidden">
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4" data-testid="chat-messages">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-2">
              <Bot className="h-10 w-10" />
              <p className="text-sm">Send a message to start a conversation with Web Dev MCP.</p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === "assistant" ? "" : "flex-row-reverse"}`}>
              <div className={`h-8 w-8 rounded-full flex items-center justify-center border shrink-0 ${msg.role === "assistant" ? "bg-blue-900/20 border-blue-800" : "bg-slate-800 border-slate-700"}`}>
                {msg.role === "assistant" ? <Bot className="h-4 w-4 text-blue-400" /> : <User className="h-4 w-4 text-slate-400" />}
              </div>
              <div className={`flex-1 space-y-1 ${msg.role === "assistant" ? "" : "text-right"}`}>
                <span className={`text-xs ${msg.role === "assistant" ? "text-blue-400" : "text-slate-200"}`}>
                  {msg.role === "assistant" ? "WebDev AI" : "You"}
                </span>
                <div className={`text-sm p-3 rounded-md inline-block max-w-[80%] text-left whitespace-pre-wrap ${msg.role === "assistant" ? "bg-blue-950/10 border border-blue-900/30 text-slate-300" : "bg-slate-900/50 border border-slate-800 text-slate-200"}`}>
                  {msg.content}
                </div>
              </div>
            </div>
          ))}
          {sending && (
            <div className="flex gap-3">
              <div className="h-8 w-8 rounded-full bg-blue-900/20 flex items-center justify-center border border-blue-800">
                <Bot className="h-4 w-4 text-blue-400" />
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <Loader2 className="h-4 w-4 animate-spin" /> Thinking...
              </div>
            </div>
          )}
          <div ref={endRef} />
        </CardContent>

        <div className="px-4 pb-2 flex flex-wrap gap-2" data-testid="example-prompts">
          {Object.entries(EXAMPLE_GROUPS).map(([group, prompts]) => (
            <div key={group} className="flex items-center gap-1 flex-wrap">
              <span className="text-xs text-slate-500 mr-1">{group}:</span>
              {prompts.map(p => (
                <button
                  key={p}
                  onClick={() => sendMessage(p)}
                  disabled={sending}
                  className="text-xs px-2.5 py-1 rounded-full border border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors disabled:opacity-50"
                >
                  {p}
                </button>
              ))}
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-slate-800 bg-slate-900/30">
          <div className="flex gap-2">
            <input
              data-testid="chat-input"
              className="flex-1 bg-slate-950 border border-slate-800 rounded-md px-4 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none"
              placeholder="Type a development command..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), sendMessage(input))}
            />
            <Button size="icon" className="bg-blue-600 hover:bg-blue-700" onClick={() => sendMessage(input)} disabled={sending || !input.trim()} data-testid="chat-send">
              <Send className="h-4 w-4 text-white" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
