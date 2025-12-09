'use client';

import { useState, useEffect, useRef } from 'react';
import Header from '@/components/Header';
import AgentPanel from '@/components/AgentPanel';
import ChatPanel from '@/components/ChatPanel';
import ActivityPanel from '@/components/ActivityPanel';
import StatusBar from '@/components/StatusBar';

export default function Dashboard() {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(true);
  const [agents] = useState([
    { id: 'ceo', name: 'CEO', role: 'Executive Director', status: 'online', icon: '👔' },
    { id: 'architect', name: 'Architect', role: 'System Designer', status: 'online', icon: '🏗️' },
    { id: 'developer', name: 'Developer', role: 'Code Engineer', status: 'online', icon: '💻' },
    { id: 'tester', name: 'Tester', role: 'QA Specialist', status: 'online', icon: '🧪' },
    { id: 'deployment', name: 'Deployment', role: 'DevOps Lead', status: 'online', icon: '🚀' },
  ]);
  const [selectedAgent, setSelectedAgent] = useState('ceo');
  const [messages, setMessages] = useState([]);
  const [activities, setActivities] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [threadId, setThreadId] = useState(null);
  const activityIdRef = useRef(0);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch('/api/agency/health', { method: 'GET', signal: AbortSignal.timeout(3000) });
        setConnected(response.ok);
        if (response.ok) addActivity('system', 'Connected to Agency Swarm backend');
      } catch {
        setConnected(false);
        addActivity('error', 'Backend offline - running in demo mode');
      } finally {
        setConnecting(false);
      }
    };
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const addActivity = (type, message, agent = null) => {
    setActivities(prev => [{ id: ++activityIdRef.current, type, message, agent, timestamp: new Date() }, ...prev].slice(0, 100));
  };

  const sendMessage = async (content) => {
    if (!content.trim()) return;
    setMessages(prev => [...prev, { id: Date.now(), role: 'user', content, timestamp: new Date() }]);
    addActivity('message', `User: ${content.slice(0, 50)}${content.length > 50 ? '...' : ''}`);
    setIsTyping(true);
    addActivity('thinking', 'CEO is processing request...', 'ceo');

    try {
      const response = await fetch('/api/agency/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, thread_id: threadId }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (data.thread_id && !threadId) setThreadId(data.thread_id);
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'agent', agent: 'CEO', content: data.output || data.response || 'No response', timestamp: new Date() }]);
      addActivity('action', 'CEO responded', 'ceo');
    } catch (error) {
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'agent', agent: 'CEO', content: `[DEMO] Backend offline. Message: "${content}"`, timestamp: new Date() }]);
      addActivity('error', 'Demo response');
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      <Header connected={connected} connecting={connecting} threadId={threadId} />
      <div className="flex-1 flex overflow-hidden">
        <AgentPanel agents={agents} selectedAgent={selectedAgent} onSelectAgent={setSelectedAgent} />
        <ChatPanel messages={messages} isTyping={isTyping} onSendMessage={sendMessage} onClearChat={() => { setMessages([]); setThreadId(null); }} onExportChat={() => {}} connected={connected} />
        <ActivityPanel activities={activities} onClearActivities={() => setActivities([])} />
      </div>
      <StatusBar connected={connected} messageCount={messages.length} threadId={threadId} />
    </div>
  );
}
