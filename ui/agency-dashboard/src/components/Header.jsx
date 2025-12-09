'use client';
import { Cpu, Wifi, WifiOff, Loader2 } from 'lucide-react';

export default function Header({ connected, connecting, threadId }) {
  return (
    <header className="h-16 bg-cyber-darker border-b border-cyber-blue/30 flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <div className="relative">
          <Cpu className="w-8 h-8 text-cyber-blue" />
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-cyber-green rounded-full animate-pulse" />
        </div>
        <div>
          <h1 className="font-display text-xl font-bold text-cyber-blue tracking-wider">AGENCY SWARM</h1>
          <p className="text-xs text-cyber-blue/50 tracking-widest">MULTI-AGENT COMMAND CENTER</p>
        </div>
      </div>
      {threadId && <div className="px-3 py-1 bg-cyber-dark rounded border border-cyber-blue/20 text-sm"><span className="text-cyber-blue/50">THREAD:</span> <span className="text-cyber-blue font-mono">{threadId.slice(0,8)}...</span></div>}
      <div className={`flex items-center gap-2 px-4 py-2 rounded border ${connecting ? 'border-cyber-yellow/50 bg-cyber-yellow/10' : connected ? 'border-cyber-green/50 bg-cyber-green/10' : 'border-cyber-red/50 bg-cyber-red/10'}`}>
        {connecting ? <Loader2 className="w-4 h-4 text-cyber-yellow animate-spin" /> : connected ? <Wifi className="w-4 h-4 text-cyber-green" /> : <WifiOff className="w-4 h-4 text-cyber-red" />}
        <span className={`text-sm font-medium ${connecting ? 'text-cyber-yellow' : connected ? 'text-cyber-green' : 'text-cyber-red'}`}>{connecting ? 'CONNECTING' : connected ? 'ONLINE' : 'OFFLINE'}</span>
      </div>
    </header>
  );
}
