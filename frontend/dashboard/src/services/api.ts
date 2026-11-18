import {
  HealthCheckResponse,
  DesignAnalysisResult,
  AstroProjectManifest,
  QAReport,
  OrchestratorRunState,
  RunStepLog,
} from '../types';

const API_BASE = '/api';

export const api = {
  async getHealth(): Promise<HealthCheckResponse> {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to fetch health check');
    return res.json();
  },

  async uploadBase64(filename: string, contentB64: string): Promise<{ status: string; saved_path: string; preview_image: string }> {
    const res = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename, content_b64: contentB64 }),
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },

  async analyzeDesign(filePath?: string, figmaUrl?: string): Promise<DesignAnalysisResult> {
    const res = await fetch(`${API_BASE}/agent1/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file_path: filePath, figma_url: figmaUrl }),
    });
    if (!res.ok) throw new Error('Analysis failed');
    return res.json();
  },

  async generateAstro(analysis: DesignAnalysisResult, projectId = 'project_001', version = 1): Promise<AstroProjectManifest> {
    const res = await fetch(`${API_BASE}/agent1/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ analysis, project_id: projectId, version }),
    });
    if (!res.ok) throw new Error('Generation failed');
    return res.json();
  },

  async getProject(projectId = 'project_001'): Promise<any> {
    const res = await fetch(`${API_BASE}/agent1/projects/${projectId}`);
    if (!res.ok) throw new Error('Project retrieval failed');
    return res.json();
  },

  async runAgent2Tests(projectId = 'project_001', previewUrl: string, refImagePath: string, iteration = 1): Promise<QAReport> {
    const res = await fetch(`${API_BASE}/agent2/test`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: projectId,
        preview_url: previewUrl,
        reference_image_path: refImagePath,
        iteration,
      }),
    });
    if (!res.ok) throw new Error('Agent 2 testing failed');
    return res.json();
  },

  async triggerOrchestrator(filePath?: string, figmaUrl?: string, maxIterations = 3): Promise<OrchestratorRunState> {
    const res = await fetch(`${API_BASE}/orchestrator/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file_path: filePath,
        figma_url: figmaUrl,
        max_iterations: maxIterations,
      }),
    });
    if (!res.ok) throw new Error('Orchestrator launch failed');
    return res.json();
  },

  async getOrchestratorStatus(runId: string): Promise<OrchestratorRunState> {
    const res = await fetch(`${API_BASE}/orchestrator/status/${runId}`);
    if (!res.ok) throw new Error('Failed to get run status');
    return res.json();
  },

  async getRuns(): Promise<OrchestratorRunState[]> {
    const res = await fetch(`${API_BASE}/orchestrator/runs`);
    if (!res.ok) throw new Error('Failed to list runs');
    return res.json();
  },

  async getLogs(): Promise<RunStepLog[]> {
    const res = await fetch(`${API_BASE}/orchestrator/logs`);
    if (!res.ok) throw new Error('Failed to get logs');
    return res.json();
  },

  async getReport(projectId = 'project_001', iteration = 1): Promise<QAReport> {
    const res = await fetch(`${API_BASE}/reports/${projectId}?iteration=${iteration}`);
    if (!res.ok) throw new Error('Failed to load report');
    return res.json();
  },

  getReportDownloadUrl(projectId = 'project_001', format: 'pdf' | 'html' = 'pdf', iteration = 1): string {
    return `${API_BASE}/reports/${projectId}/download?format=${format}&iteration=${iteration}`;
  },

  getPreviewUrl(projectId = 'project_001'): string {
    return `${API_BASE}/preview/${projectId}`;
  }
};
