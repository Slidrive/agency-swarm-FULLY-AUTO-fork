'use client';
import { Circle, MessageSquare, Hash, Clock } from 'lucide-react';

export default function StatusBar({ connected, messageCount, threadId }) {
  const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  return (
    <footer className="h-8 bg-cyber-darker border-t border-cyber-blue/30 flex items-center justify-between px-4 text-xs">
      <div className="flex items-center gap-1.5"><Circle className={`w-2 h-2 ${connected ? 'fill-cyber-green text-cyber-green' : 'fill-cyber-red text-cyber-red'}`} /><span className="text-gray-500">{connected ? 'Connected to localhost:8000' : 'Disconnected'}</span></div>
      <div className="flex items-center gap-4"><div className="flex items-center gap-1.5 text-gray-500"><MessageSquare className="w-3 h-3" /><span>{messageCount} messages</span></div>{threadId && <div className="flex items-center gap-1.5 text-gray-500"><Hash className="w-3 h-3" /><span className="font-mono">{threadId.slice(0,12)}</span></div>}</div>
      <div className="flex items-center gap-1.5 text-gray-500"><Clock className="w-3 h-3" /><span>{time}</span></div>
    </footer>
  );
}
