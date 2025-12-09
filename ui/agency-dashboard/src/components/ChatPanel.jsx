'use client';
import { useState, useRef, useEffect } from 'react';
import { Send, Trash2, Download, MessageSquare } from 'lucide-react';

export default function ChatPanel({ messages, isTyping, onSendMessage, onClearChat, onExportChat, connected }) {
  const [input, setInput] = useState('');
  const endRef = useRef(null);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, isTyping]);
  const handleSubmit = (e) => { e.preventDefault(); if (input.trim()) { onSendMessage(input); setInput(''); } };
  const handleKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(e); } };
  const fmt = (d) => new Date(d).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

  return (
    <main className="flex-1 flex flex-col bg-cyber-black/50 min-w-0">
      <div className="panel-header px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3"><MessageSquare className="w-5 h-5 text-cyber-blue" /><h2 className="font-display text-sm font-semibold text-cyber-blue tracking-wider">COMMAND INTERFACE</h2></div>
        <div className="flex items-center gap-2">
          <button onClick={onExportChat} disabled={!messages.length} className="p-2 rounded border border-cyber-blue/30 text-cyber-blue/60 hover:text-cyber-blue disabled:opacity-30"><Download className="w-4 h-4" /></button>
          <button onClick={onClearChat} disabled={!messages.length} className="p-2 rounded border border-cyber-red/30 text-cyber-red/60 hover:text-cyber-red disabled:opacity-30"><Trash2 className="w-4 h-4" /></button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {!messages.length ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-20 h-20 rounded-full bg-cyber-dark border border-cyber-blue/30 flex items-center justify-center mb-4"><MessageSquare className="w-10 h-10 text-cyber-blue/40" /></div>
            <h3 className="font-display text-lg text-cyber-blue/60 mb-2">AWAITING COMMAND</h3>
            <p className="text-sm text-cyber-blue/40 max-w-md">{connected ? 'Enter your request below.' : 'Backend offline. Start server to connect.'}</p>
          </div>
        ) : (<>
          {messages.map((m) => (
            <div key={m.id} className={`${m.role === 'user' ? 'message-user' : 'message-agent'} rounded-lg p-4`}>
              <div className="flex items-center gap-2 mb-2"><span className={`text-xs font-semibold ${m.role === 'user' ? 'text-cyber-blue' : 'text-cyber-green'}`}>{m.role === 'user' ? 'YOU' : m.agent?.toUpperCase()}</span><span className="text-xs text-gray-500">{fmt(m.timestamp)}</span></div>
              <div className="text-sm text-gray-200 whitespace-pre-wrap leading-relaxed">{m.content}</div>
            </div>
          ))}
          {isTyping && <div className="message-agent rounded-lg p-4"><div className="flex items-center gap-2 mb-2"><span className="text-xs font-semibold text-cyber-green">CEO</span><span className="text-xs text-gray-500">typing</span></div><div className="flex items-center gap-1"><div className="typing-dot w-2 h-2 bg-cyber-green rounded-full" /><div className="typing-dot w-2 h-2 bg-cyber-green rounded-full" /><div className="typing-dot w-2 h-2 bg-cyber-green rounded-full" /></div></div>}
          <div ref={endRef} />
        </>)}
      </div>
      <div className="p-4 border-t border-cyber-blue/20">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKey} placeholder="Enter command..." rows={1} className="cyber-input flex-1 px-4 py-3 rounded-lg resize-none font-mono text-sm" style={{ minHeight: '48px', maxHeight: '120px' }} />
          <button type="submit" disabled={!input.trim() || isTyping} className="cyber-btn px-6 rounded-lg flex items-center gap-2"><Send className="w-4 h-4" /><span className="hidden sm:inline">SEND</span></button>
        </form>
        <div className="mt-2 text-xs text-cyber-blue/30 text-center">Press Enter to send • Shift+Enter for new line</div>
      </div>
    </main>
  );
}
