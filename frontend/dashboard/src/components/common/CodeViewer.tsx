import React, { useState } from 'react';
import { Copy, Check, FileCode, FileText } from 'lucide-react';
import { AstroComponentCode } from '../../types';

interface Props {
  components: AstroComponentCode[];
  structuredData?: string;
  globalCss?: string;
  packageJson?: string;
}

export const CodeViewer: React.FC<Props> = ({
  components,
  structuredData = '',
  globalCss = '',
  packageJson = '',
}) => {
  // Aggregate all files
  const files: { name: string; path: string; content: string; type: string }[] = [
    ...components.map((c) => ({
      name: c.filename,
      path: c.path,
      content: c.content,
      type: 'astro',
    })),
    {
      name: 'homepage.js',
      path: 'src/data/homepage.js',
      content: structuredData,
      type: 'javascript',
    },
    {
      name: 'global.css',
      path: 'src/styles/global.css',
      content: globalCss,
      type: 'css',
    },
    {
      name: 'package.json',
      path: 'package.json',
      content: packageJson,
      type: 'json',
    },
  ];

  const [selectedPath, setSelectedPath] = useState<string>(files[0]?.path || 'src/components/Hero.astro');
  const [copied, setCopied] = useState(false);

  const activeFile = files.find((f) => f.path === selectedPath) || files[0];

  const handleCopy = () => {
    if (activeFile?.content) {
      navigator.clipboard.writeText(activeFile.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg flex flex-col md:flex-row h-[560px]">
      {/* File Tree Sidebar */}
      <div className="w-full md:w-64 bg-slate-950 border-r border-slate-800 p-3 overflow-y-auto shrink-0">
        <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 px-3 py-2">
          Generated Project Files
        </div>
        <div className="space-y-1">
          {files.map((f) => {
            const isSelected = selectedPath === f.path;
            return (
              <button
                key={f.path}
                onClick={() => setSelectedPath(f.path)}
                className={`w-full flex items-center space-x-2.5 px-3 py-1.5 rounded-md text-xs font-mono transition ${
                  isSelected
                    ? 'bg-amber-500/15 text-amber-300 font-semibold border border-amber-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                {f.type === 'astro' ? (
                  <FileCode className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                ) : (
                  <FileText className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                )}
                <span className="truncate">{f.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Editor Content Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-slate-900">
        {/* Editor Bar */}
        <div className="h-10 bg-slate-950/70 border-b border-slate-800 px-4 flex items-center justify-between">
          <span className="font-mono text-xs text-slate-300 font-medium truncate">
            {activeFile?.path}
          </span>
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] font-mono transition"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy File</span>
              </>
            )}
          </button>
        </div>

        {/* Code Block with Line Numbers */}
        <div className="flex-1 overflow-auto p-4 font-mono text-xs text-slate-200 leading-relaxed bg-[#0A192F]/60">
          <pre className="select-text whitespace-pre overflow-x-auto">
            {activeFile?.content || '// File is empty'}
          </pre>
        </div>
      </div>
    </div>
  );
};
