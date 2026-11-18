import React, { useState } from 'react';
import { 
  Code2, 
  Palette, 
  Type, 
  Layers, 
  FileCode, 
  CheckCircle2, 
  ExternalLink,
  ShieldCheck,
  FileText
} from 'lucide-react';
import { CodeViewer } from '../components/common/CodeViewer';
import { StatusBadge } from '../components/common/StatusBadge';
import { DesignAnalysisResult, AstroProjectManifest } from '../types';

interface Props {
  manifest?: AstroProjectManifest | null;
  analysis?: DesignAnalysisResult | null;
}

export const Agent1Workspace: React.FC<Props> = ({ manifest, analysis }) => {
  const [activeTab, setActiveTab] = useState<'components' | 'tokens' | 'sections' | 'schemas'>('components');

  const defaultAnalysis = analysis || {
    project_name: 'RDGCC Corporate Regional Portal',
    brand_identity: 'Prestigious GCC industrial development and regional investment holding. Dark navy contrast with warm bronze/gold accents.',
    layout_type: 'corporate-holding-portal',
    colors: [
      { name: 'primary-dark', hex: '#0A192F', usage: 'Header, Hero backdrop, Footer, Headings' },
      { name: 'accent-gold', hex: '#C29B38', usage: 'CTAs, highlights, active nav' },
      { name: 'surface-light', hex: '#F8FAFC', usage: 'Section alternation, card backgrounds' },
      { name: 'surface-white', hex: '#FFFFFF', usage: 'Card surfaces, content modules' },
      { name: 'text-muted', hex: '#64748B', usage: 'Secondary body text, descriptors' },
    ],
    typography: [
      { element: 'h1', font_family: 'Plus Jakarta Sans', size: '3.75rem', weight: '800', line_height: '1.12' },
      { element: 'h2', font_family: 'Plus Jakarta Sans', size: '2.25rem', weight: '700', line_height: '1.2' },
      { element: 'body', font_family: 'Inter', size: '1rem', weight: '400', line_height: '1.6' },
      { element: 'metric', font_family: 'Plus Jakarta Sans', size: '3rem', weight: '800', line_height: '1.0' },
    ],
    sections: [
      { id: 'header', name: 'Header & Navigation', component_name: 'Header.astro', description: 'Sticky logo, language switcher, nav links, and contact CTA', estimated_height_ratio: 0.08, data_keys: ['navigation'] },
      { id: 'hero', name: 'Strategic Vision Hero', component_name: 'Hero.astro', description: 'Impactful headline, regional development thesis, primary & secondary CTAs', estimated_height_ratio: 0.25, data_keys: ['hero'] },
      { id: 'about', name: 'About RDGCC', component_name: 'About.astro', description: 'Two-column narrative with three structured strategic pillars', estimated_height_ratio: 0.18, data_keys: ['about'] },
      { id: 'sectors', name: 'Strategic Business Sectors', component_name: 'Sectors.astro', description: '4-card responsive grid: Energy, Maritime, Infrastructure, Sustainable Tech', estimated_height_ratio: 0.22, data_keys: ['sectors'] },
      { id: 'stats', name: 'Key Performance Indicators', component_name: 'Stats.astro', description: '4-column KPI counters: AUM, Regional Hubs, Heritage Years, Compliance', estimated_height_ratio: 0.10, data_keys: ['stats'] },
      { id: 'projects', name: 'Flagship GCC Developments', component_name: 'Projects.astro', description: 'Featured industrial and infrastructure project portfolio showcase', estimated_height_ratio: 0.20, data_keys: ['projects'] },
      { id: 'contact', name: 'Regional Inquiries Form', component_name: 'Contact.astro', description: 'Corporate inquiry form with validation inputs and regional contact details', estimated_height_ratio: 0.15, data_keys: ['contact'] },
      { id: 'footer', name: 'Corporate Footer', component_name: 'Footer.astro', description: 'Multi-column directory with legal disclaimers and governance disclosures', estimated_height_ratio: 0.12, data_keys: ['footer'] },
    ],
    assumptions_and_limitations: [
      'Content decoupled into src/data/homepage.js for direct Sanity Studio binding.',
      'Responsive clamp applied on all headings for mobile viewport protection.'
    ]
  };

  return (
    <div className="space-y-8">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div>
          <div className="flex items-center space-x-2 text-xs text-amber-400 font-bold mb-1">
            <Code2 className="w-4 h-4" />
            <span>AGENT 1: DESIGN-TO-ASTRO GENERATOR</span>
          </div>
          <h2 className="text-2xl font-heading font-extrabold text-white tracking-tight">
            {defaultAnalysis.project_name}
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
            {defaultAnalysis.brand_identity}
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <StatusBadge status={manifest?.build_valid ? 'BUILD VALID' : 'GENERATED'} size="sm" />
          <a
            href="/api/preview/project_001"
            target="_blank"
            rel="noreferrer"
            className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow flex items-center space-x-1.5 transition"
          >
            <span>Preview Astro App</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* Tabs Row */}
      <div className="flex border-b border-slate-800 space-x-6 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('components')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            activeTab === 'components'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileCode className="w-4 h-4" />
          <span>Astro Components & Code ({manifest?.components.length || 11})</span>
        </button>

        <button
          onClick={() => setActiveTab('tokens')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            activeTab === 'tokens'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Palette className="w-4 h-4" />
          <span>Design Tokens ({defaultAnalysis.colors.length + defaultAnalysis.typography.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('sections')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            activeTab === 'sections'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Detected Sections ({defaultAnalysis.sections.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('schemas')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            activeTab === 'schemas'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Sanity CMS Schemas (4)</span>
        </button>
      </div>

      {/* Tab 1: Code Viewer */}
      {activeTab === 'components' && (
        <div className="space-y-4">
          <CodeViewer
            components={manifest?.components || []}
            structuredData={manifest?.structured_content_file || ''}
            globalCss={manifest?.global_css || ''}
            packageJson={manifest?.package_json || ''}
          />
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
            <span className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Modular Architecture: No monolithic files. Fully decomposed into clean Astro components.</span>
            </span>
            <span className="font-mono text-slate-500">Astro v4.x</span>
          </div>
        </div>
      )}

      {/* Tab 2: Design Tokens */}
      {activeTab === 'tokens' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Colors Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Palette className="w-4 h-4 text-amber-400" />
              <span>Extracted Brand Colors</span>
            </h3>
            <div className="space-y-3">
              {defaultAnalysis.colors.map((c) => (
                <div key={c.name} className="flex items-center justify-between p-3 rounded-lg bg-slate-950 border border-slate-800">
                  <div className="flex items-center space-x-3">
                    <div
                      className="w-7 h-7 rounded-md border border-slate-700 shadow-sm"
                      style={{ backgroundColor: c.hex }}
                    ></div>
                    <div>
                      <div className="text-xs font-bold text-white font-mono">{c.name}</div>
                      <div className="text-[11px] text-slate-400">{c.usage}</div>
                    </div>
                  </div>
                  <span className="text-xs font-mono font-semibold text-slate-300 px-2 py-1 rounded bg-slate-900 border border-slate-800">
                    {c.hex}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Typography Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Type className="w-4 h-4 text-amber-400" />
              <span>Typography Scale & Hierarchy</span>
            </h3>
            <div className="space-y-3">
              {defaultAnalysis.typography.map((t) => (
                <div key={t.element} className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div>
                    <div className="text-xs font-bold text-white font-mono uppercase">{t.element}</div>
                    <div className="text-[11px] text-slate-400">{t.font_family} • Weight: {t.weight}</div>
                  </div>
                  <span className="text-xs font-mono font-semibold text-amber-400">
                    {t.size}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Detected Sections */}
      {activeTab === 'sections' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-950 border-b border-slate-800 text-slate-500 uppercase text-[11px] font-bold">
                <th className="py-3 px-4">Section Slug</th>
                <th className="py-3 px-4">Component File</th>
                <th className="py-3 px-4">Description</th>
                <th className="py-3 px-4">Height Ratio</th>
                <th className="py-3 px-4">Structured Data Keys</th>
              </tr>
            </thead>
            <tbody>
              {defaultAnalysis.sections.map((sec) => (
                <tr key={sec.id} className="border-b border-slate-800/60 hover:bg-slate-800/30 transition">
                  <td className="py-3 px-4 font-mono text-xs font-bold text-white">{sec.id}</td>
                  <td className="py-3 px-4 font-mono text-xs text-amber-400">{sec.component_name}</td>
                  <td className="py-3 px-4 text-xs text-slate-300">{sec.description}</td>
                  <td className="py-3 px-4 font-mono text-xs text-slate-400">{(sec.estimated_height_ratio * 100).toFixed(0)}%</td>
                  <td className="py-3 px-4 text-xs">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">
                      {sec.data_keys.join(', ')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 4: Sanity CMS Schemas */}
      {activeTab === 'schemas' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-heading font-bold text-white">
                Sanity-Compatible Schema Architecture
              </h3>
              <p className="text-xs text-slate-400">
                Ready for editorial CMS decoupling in Sanity Studio v3
              </p>
            </div>
            <span className="px-2.5 py-1 rounded bg-amber-500/15 border border-amber-500/30 text-amber-400 text-xs font-mono font-semibold">
              Sanity v3 Ready
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
              <h4 className="text-xs font-bold text-white font-mono mb-1">homepage.js</h4>
              <p className="text-[11px] text-slate-400">Document schema backing hero banner, strategic about narrative, and stats metrics.</p>
            </div>
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
              <h4 className="text-xs font-bold text-white font-mono mb-1">sector.js</h4>
              <p className="text-[11px] text-slate-400">Document schema backing Energy, Maritime, Real Estate, and Sustainable Tech verticals.</p>
            </div>
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
              <h4 className="text-xs font-bold text-white font-mono mb-1">featuredProject.js</h4>
              <p className="text-[11px] text-slate-400">Project schema with year, sector tags, executive summary, and regional hub.</p>
            </div>
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
              <h4 className="text-xs font-bold text-white font-mono mb-1">siteSettings.js</h4>
              <p className="text-[11px] text-slate-400">Global site settings, regional office directory, legal disclaimers, and multilingual links.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
