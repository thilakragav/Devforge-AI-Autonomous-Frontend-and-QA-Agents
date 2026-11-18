export type TestSeverity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
export type TestCategory = 'VISUAL' | 'RESPONSIVE' | 'FUNCTIONAL';

export interface ColorToken {
  name: string;
  hex: string;
  usage: string;
}

export interface TypographyToken {
  element: string;
  font_family: string;
  size: string;
  weight: string;
  line_height: string;
}

export interface SectionSpec {
  id: string;
  name: string;
  component_name: string;
  description: string;
  estimated_height_ratio: number;
  data_keys: string[];
}

export interface DesignAnalysisResult {
  project_name: string;
  brand_identity: string;
  layout_type: string;
  colors: ColorToken[];
  typography: TypographyToken[];
  sections: SectionSpec[];
  assumptions_and_limitations: string[];
}

export interface AstroComponentCode {
  filename: string;
  path: string;
  content: string;
  is_layout: boolean;
  description?: string;
}

export interface AstroProjectManifest {
  project_id: string;
  version: number;
  project_name: string;
  output_directory: string;
  components: AstroComponentCode[];
  structured_content_file: string;
  global_css: string;
  package_json: string;
  astro_config: string;
  build_valid: boolean;
  validation_errors: string[];
  assumptions: string[];
}

export interface TestCaseResult {
  test_id: string;
  category: TestCategory;
  description: string;
  expected_result: string;
  actual_result: string;
  passed: boolean;
  severity: TestSeverity;
  issue_description?: string;
  recommendation?: string;
  affected_component?: string;
  screenshot_path?: string;
}

export interface VisualDiffMetrics {
  ssim_score: number;
  pixel_diff_percentage: number;
  mismatched_pixel_count: number;
  diff_image_path: string;
  reference_image_path: string;
  generated_image_path: string;
  llm_visual_critique: string;
}

export interface ViewportAudit {
  device: string;
  viewport: string;
  screenshot_path: string;
  horizontal_overflow: boolean;
  text_overflow_detected: boolean;
  navigation_broken: boolean;
  issues: string[];
}

export interface QAReport {
  project_id: string;
  iteration: number;
  timestamp: string;
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  critical_issues_count: number;
  high_issues_count: number;
  overall_status: string;
  test_cases: TestCaseResult[];
  visual_metrics?: VisualDiffMetrics;
  responsive_audits: ViewportAudit[];
  html_report_path?: string;
  pdf_report_path?: string;
  recommendations_summary: string[];
}

export interface RunStepLog {
  timestamp: string;
  stage: string;
  agent: string;
  message: string;
  level: string;
}

export interface CorrectionDirective {
  iteration: number;
  target_components: string[];
  specific_issues: string[];
  actionable_instructions: string[];
}

export interface OrchestratorRunState {
  run_id: string;
  project_name: string;
  status: string;
  current_iteration: number;
  max_iterations: number;
  design_input_path: string;
  figma_url?: string;
  design_analysis?: DesignAnalysisResult;
  manifest_history: AstroProjectManifest[];
  qa_history: QAReport[];
  correction_history: CorrectionDirective[];
  logs: RunStepLog[];
  preview_url?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface HealthCheckResponse {
  status: string;
  service: string;
  ai_engine: {
    mode: string;
    provider: string;
    notice?: string;
  };
  active_agents: string[];
  orchestrator_state: string;
}
