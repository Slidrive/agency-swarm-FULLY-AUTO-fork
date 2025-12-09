'use client';
import { Users } from 'lucide-react';

export default function AgentPanel({ agents, selectedAgent, onSelectAgent }) {
  const getStatusColor = (s) => s === 'online' ? 'bg-cyber-green shadow-[0_0_8px_#00ff88]' : s === 'busy' ? 'bg-cyber-yellow shadow-[0_0_8px_#ffcc00]' : 'bg-cyber-red shadow-[0_0_8px_#ff3366]';
  return (
    <aside className="w-72 bg-cyber-darker border-r border-cyber-blue/30 flex flex-col">
      <div className="panel-header px-4 py-3 flex items-center gap-3">
        <Users className="w-5 h-5 text-cyber-blue" />
        <h2 className="font-display text-sm font-semibold text-cyber-blue tracking-wider">AGENTS</h2>
        <span className="ml-auto text-xs text-cyber-blue/50 bg-cyber-dark px-2 py-0.5 rounded">{agents.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {agents.map((a) => (
          <button key={a.id} onClick={() => onSelectAgent(a.id)} className={`agent-card w-full p-3 rounded-lg text-left ${selectedAgent === a.id ? 'active' : ''}`}>
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-lg bg-cyber-dark border border-cyber-blue/30 flex items-center justify-center text-xl">{a.icon}</div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2"><span className="font-semibold text-white truncate">{a.name}</span><div className={`w-2 h-2 rounded-full ${getStatusColor(a.status)}`} /></div>
                <p className="text-xs text-cyber-blue/60 truncate mt-0.5">{a.role}</p>
              </div>
            </div>
            {selectedAgent === a.id && <div className="mt-2 pt-2 border-t border-cyber-blue/20"><span className="text-xs text-cyber-blue">● ACTIVE CHANNEL</span></div>}
          </button>
        ))}
      </div>
      <div className="p-3 border-t border-cyber-blue/20"><div className="text-xs text-cyber-blue/40 text-center">Entry Point: CEO Agent</div></div>
    </aside>
  );
}
