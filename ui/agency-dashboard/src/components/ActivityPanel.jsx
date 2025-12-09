'use client';
import { Activity, Trash2, MessageCircle, Zap, AlertCircle, Brain } from 'lucide-react';

export default function ActivityPanel({ activities, onClearActivities }) {
  const icon = (t) => t === 'message' ? <MessageCircle className="w-3 h-3 text-cyber-blue" /> : t === 'action' ? <Zap className="w-3 h-3 text-cyber-green" /> : t === 'error' ? <AlertCircle className="w-3 h-3 text-cyber-red" /> : t === 'thinking' ? <Brain className="w-3 h-3 text-cyber-purple" /> : <Activity className="w-3 h-3 text-cyber-yellow" />;
  const cls = (t) => t === 'message' ? 'type-message' : t === 'action' ? 'type-action' : t === 'error' ? 'type-error' : t === 'thinking' ? 'type-thinking' : '';
  const fmt = (d) => new Date(d).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  return (
    <aside className="w-80 bg-cyber-darker border-l border-cyber-blue/30 flex flex-col">
      <div className="panel-header px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3"><Activity className="w-5 h-5 text-cyber-blue" /><h2 className="font-display text-sm font-semibold text-cyber-blue tracking-wider">ACTIVITY LOG</h2></div>
        <button onClick={onClearActivities} disabled={!activities.length} className="p-1.5 rounded border border-cyber-blue/30 text-cyber-blue/60 hover:text-cyber-blue disabled:opacity-30"><Trash2 className="w-3 h-3" /></button>
      </div>
      <div className="flex-1 overflow-y-auto">
        {!activities.length ? <div className="h-full flex flex-col items-center justify-center p-4"><Activity className="w-8 h-8 text-cyber-blue/20 mb-2" /><p className="text-xs text-cyber-blue/40">Activity will appear here</p></div> : (
          <div className="divide-y divide-cyber-blue/10">
            {activities.map((a) => (
              <div key={a.id} className={`activity-item px-4 py-3 ${cls(a.type)}`}>
                <div className="flex items-start gap-2"><div className="mt-0.5">{icon(a.type)}</div><div className="flex-1 min-w-0"><p className="text-xs text-gray-300 leading-relaxed">{a.message}</p><div className="flex items-center gap-2 mt-1"><span className="text-[10px] text-gray-500 font-mono">{fmt(a.timestamp)}</span>{a.agent && <span className="text-[10px] text-cyber-blue/50 uppercase">{a.agent}</span>}</div></div></div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="p-3 border-t border-cyber-blue/20">
        <div className="grid grid-cols-2 gap-2 text-[10px]">
          <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-cyber-blue" /><span className="text-gray-500">Message</span></div>
          <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-cyber-green" /><span className="text-gray-500">Action</span></div>
          <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-cyber-purple" /><span className="text-gray-500">Thinking</span></div>
          <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-cyber-red" /><span className="text-gray-500">Error</span></div>
        </div>
      </div>
    </aside>
  );
}
