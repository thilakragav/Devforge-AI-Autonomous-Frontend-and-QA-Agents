import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { Dashboard } from './pages/Dashboard';
import { DesignInput } from './pages/DesignInput';
import { Agent1Workspace } from './pages/Agent1Workspace';
import { Agent2Workspace } from './pages/Agent2Workspace';
import { QAReports } from './pages/QAReports';
import { AgentActivity } from './pages/AgentActivity';
import { api } from './services/api';
import { 
  QAReport, 
  OrchestratorRunState, 
  AstroProjectManifest, 
  RunStepLog, 
  HealthCheckResponse 
} from './types';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [health, setHealth] = useState<HealthCheckResponse | null>(null);
  const [latestReport, setLatestReport] = useState<QAReport | null>(null);
  const [latestRun, setLatestRun] = useState<OrchestratorRunState | null>(null);
  const [manifest, setManifest] = useState<AstroProjectManifest | null>(null);
  const [logs, setLogs] = useState<RunStepLog[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Initial Load: Fetch health, initial project manifest, logs, and report
  const loadData = async () => {
    try {
      const healthData = await api.getHealth();
      setHealth(healthData);

      const logsData = await api.getLogs();
      setLogs(logsData);

      // Try loading project_001 report
      try {
        const rep = await api.getReport('project_001', 1);
        setLatestReport(rep);
      } catch (e) {
        // Report not ready yet
      }

      // Try loading runs
      try {
        const runs = await api.getRuns();
        if (runs.length > 0) {
          setLatestRun(runs[runs.length - 1]);
        }
      } catch (e) {}
    } catch (err) {
      console.error('Initial data load error:', err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleTriggerRun = async () => {
    setIsLoading(true);
    try {
      const run = await api.triggerOrchestrator('uploads/rdgcc_reference.png', undefined, 3);
      setLatestRun(run);
      setActiveTab('activity');

      // Poll until completed
      const pollInterval = setInterval(async () => {
        try {
          const status = await api.getOrchestratorStatus(run.run_id);
          setLatestRun(status);
          const currentLogs = await api.getLogs();
          setLogs(currentLogs);

          if (status.status === 'COMPLETED' || status.status === 'FAILED') {
            clearInterval(pollInterval);
            setIsLoading(false);
            if (status.qa_history.length > 0) {
              setLatestReport(status.qa_history[status.qa_history.length - 1]);
            }
          }
        } catch (e) {
          clearInterval(pollInterval);
          setIsLoading(false);
        }
      }, 2000);
    } catch (err: any) {
      alert(`Error triggering run: ${err.message}`);
      setIsLoading(false);
    }
  };

  const getPageTitle = () => {
    switch (activeTab) {
      case 'dashboard':
        return { title: 'Executive Overview', subtitle: 'Autonomous frontend development & quality assurance pipeline' };
      case 'input':
        return { title: 'Design Reference Ingestion', subtitle: 'Submit screenshots, PDFs, or Figma URLs for analysis' };
      case 'agent1':
        return { title: 'Agent 1: Design-to-Astro Code Generator', subtitle: 'Modular components, typography tokens, and Sanity schemas' };
      case 'agent2':
        return { title: 'Agent 2: UI & QA Testing Agent', subtitle: 'Measurable OpenCV SSIM diffing, viewports, and Playwright DOM tests' };
      case 'reports':
        return { title: 'Quality Assurance Reports', subtitle: 'Downloadable PDF and interactive HTML compliance audit ledger' };
      case 'activity':
        return { title: 'Agent Activity & Telemetry', subtitle: 'Live streaming event logs and multi-iteration feedback history' };
      default:
        return { title: 'Multi-Agent AI PoC', subtitle: 'Automated Frontend & QA System' };
    }
  };

  const { title, subtitle } = getPageTitle();

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        systemMode={health?.ai_engine.mode}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Header
          title={title}
          subtitle={subtitle}
          currentRunStatus={latestRun?.status || (isLoading ? 'RUNNING' : 'ONLINE')}
          iteration={latestRun?.current_iteration || latestReport?.iteration || 1}
          onTriggerRun={handleTriggerRun}
          onRefresh={loadData}
          isLoading={isLoading}
        />

        <main className="flex-1 p-8 overflow-y-auto max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && (
            <Dashboard
              latestReport={latestReport}
              latestRun={latestRun}
              onNavigate={setActiveTab}
              onTriggerRun={handleTriggerRun}
            />
          )}

          {activeTab === 'input' && (
            <DesignInput
              onSuccess={(runId) => {
                setActiveTab('activity');
                loadData();
              }}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          )}

          {activeTab === 'agent1' && (
            <Agent1Workspace
              manifest={latestRun?.manifest_history[latestRun.manifest_history.length - 1] || manifest}
              analysis={latestRun?.design_analysis}
            />
          )}

          {activeTab === 'agent2' && (
            <Agent2Workspace
              report={latestReport}
              referenceImage="/uploads/rdgcc_reference.png"
              generatedImage="/reports/screenshots/project_001_v1_Desktop_1440x900.png"
            />
          )}

          {activeTab === 'reports' && (
            <QAReports report={latestReport} />
          )}

          {activeTab === 'activity' && (
            <AgentActivity
              logs={logs}
              runState={latestRun}
              onRefresh={loadData}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
