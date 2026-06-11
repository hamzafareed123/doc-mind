import { useState, useRef, useEffect } from "react";
import './index.css'

type Message = { role: "user" | "assistant"; content: string };

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [collection, setCollection] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState("session_" + Date.now());
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch("http://127.0.0.1:8000/upload/post-file", { method: "POST", body: formData });
    const data = await res.json();
    setCollection(data["collection-name"]);
    setMessages([{ role: "assistant", content: `"${file.name}" uploaded! Ask me anything.` }]);
  };

  const handleAsk = async () => {
    if (!input.trim() || !collection) return;
    const query = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, collection_name: collection, session_id: sessionId }),
    });
    const data = await res.json();
    setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 py-4 bg-white border-b border-gray-200">
        <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-medium text-sm">D</div>
        <div>
          <h1 className="text-sm font-medium text-gray-900">DocMind</h1>
          <p className="text-xs text-gray-500">Ask anything about your document</p>
        </div>
      </div>

      {/* Upload bar */}
      <div className="flex items-center gap-3 px-4 py-2 bg-gray-100 border-b border-gray-200">
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files?.[0] || null)} className="text-sm text-gray-600 flex-1" />
        {collection && <span className="text-xs px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full">{file?.name}</span>}
        <button onClick={handleUpload} disabled={!file} className="text-sm px-4 py-1.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-40">Upload</button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3">
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-400 gap-2 mt-20">
            <span className="text-4xl">📄</span>
            <p className="text-sm">Upload a document to get started</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-2 max-w-[85%] ${msg.role === "user" ? "self-end flex-row-reverse" : "self-start"}`}>
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium flex-shrink-0 ${msg.role === "user" ? "bg-indigo-100 text-indigo-700" : "bg-emerald-100 text-emerald-700"}`}>
              {msg.role === "user" ? "U" : "AI"}
            </div>
            <div className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${msg.role === "user" ? "bg-indigo-600 text-white rounded-br-sm" : "bg-white border border-gray-200 text-gray-800 rounded-bl-sm"}`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-2 self-start">
            <div className="w-7 h-7 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-xs font-medium">AI</div>
            <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl rounded-bl-sm flex gap-1 items-center">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="flex items-center gap-2 px-4 py-3 bg-white border-t border-gray-200">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder="Ask a question about your document..."
          className="flex-1 text-sm px-4 py-2 rounded-xl border border-gray-200 bg-gray-50 focus:outline-none focus:border-indigo-400"
        />
        <button onClick={handleAsk} disabled={!input.trim() || !collection || loading}
          className="w-9 h-9 bg-indigo-600 text-white rounded-xl flex items-center justify-center hover:bg-indigo-700 disabled:opacity-40">
          ↑
        </button>
      </div>
    </div>
  );
}

export default App;