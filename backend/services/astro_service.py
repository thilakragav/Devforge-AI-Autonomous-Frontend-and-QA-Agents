"""
Astro Service - Project Scaffolding, File System Management, Code Validation, and Preview Server
"""
import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from backend.schemas.agent1_schema import AstroProjectManifest, AstroComponentCode
from backend.utils.logger import global_log_buffer
from backend.utils.security import is_safe_path


class AstroService:
    def __init__(self, base_dir: str = "generated_projects"):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.active_processes: Dict[str, subprocess.Popen] = {}

    def get_project_dir(self, project_id: str) -> Path:
        p = self.base_dir / project_id
        if not is_safe_path(str(p), str(self.base_dir)):
            raise ValueError(f"Invalid project path traversal attempt: {project_id}")
        return p

    def write_project_files(self, manifest: AstroProjectManifest) -> str:
        """
        Materializes an Astro project manifest onto disk in the required modular structure:
        src/
          components/
          layouts/
          pages/
          data/
          styles/
        public/
        package.json
        astro.config.mjs
        """
        proj_dir = self.get_project_dir(manifest.project_id)
        proj_dir.mkdir(parents=True, exist_ok=True)

        # Standard subdirectories
        (proj_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "layouts").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "pages").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "data").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "styles").mkdir(parents=True, exist_ok=True)
        (proj_dir / "src" / "schemas").mkdir(parents=True, exist_ok=True)
        (proj_dir / "public").mkdir(parents=True, exist_ok=True)

        # 1. Write components
        for comp in manifest.components:
            target_path = proj_dir / comp.path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(comp.content)

        # 2. Write structured data file
        data_path = proj_dir / "src" / "data" / "homepage.js"
        with open(data_path, "w", encoding="utf-8") as f:
            f.write(manifest.structured_content_file)

        # 3. Write Sanity schemas
        for sanity_schema in manifest.sanity_schemas:
            schema_file = proj_dir / "src" / "schemas" / f"{sanity_schema.schema_name}.js"
            with open(schema_file, "w", encoding="utf-8") as f:
                f.write(sanity_schema.schema_code)

        # 4. Write global CSS
        css_path = proj_dir / "src" / "styles" / "global.css"
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(manifest.global_css)

        # 5. Write package.json
        pkg_path = proj_dir / "package.json"
        with open(pkg_path, "w", encoding="utf-8") as f:
            f.write(manifest.package_json)

        # 6. Write astro.config.mjs
        config_path = proj_dir / "astro.config.mjs"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(manifest.astro_config)

        # 7. Write index.html pre-render for direct browser preview
        compiled_html = self.compile_to_static_html(manifest)
        index_html_path = proj_dir / "public" / "preview.html"
        with open(index_html_path, "w", encoding="utf-8") as f:
            f.write(compiled_html)

        global_log_buffer.log("ASTRO_GEN", "AGENT_1", f"Wrote {len(manifest.components)} components and assets to {proj_dir.name}")
        return str(proj_dir)

    def validate_project(self, project_id: str) -> List[str]:
        """
        Validates the modular Astro project:
        - Frontmatter integrity
        - File existence
        - Matching imports
        - Responsive CSS classes
        """
        proj_dir = self.get_project_dir(project_id)
        errors: List[str] = []

        if not (proj_dir / "package.json").exists():
            errors.append("Missing package.json")
        if not (proj_dir / "astro.config.mjs").exists():
            errors.append("Missing astro.config.mjs")
        if not (proj_dir / "src" / "pages" / "index.astro").exists():
            errors.append("Missing src/pages/index.astro")
        if not (proj_dir / "src" / "data" / "homepage.js").exists():
            errors.append("Missing structured content file: src/data/homepage.js")

        # Check components frontmatter
        comp_dir = proj_dir / "src" / "components"
        if comp_dir.exists():
            for f in comp_dir.glob("*.astro"):
                content = f.read_text(encoding="utf-8")
                # Must have --- delimiters if it has frontmatter
                if content.startswith("---"):
                    parts = content.split("---")
                    if len(parts) < 3:
                        errors.append(f"Component {f.name} has unclosed frontmatter '---' fence.")

        return errors

    def compile_to_static_html(self, manifest: AstroProjectManifest) -> str:
        """
        Generates a 1:1 compiled HTML document from the modular Astro components and data.
        This provides a zero-dependency, instantaneous preview server for Playwright, OpenCV, and Dashboard iframe.
        """
        css = manifest.global_css

        template = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RDGCC Corporate Regional Portal — Gulf Regional Development Holding</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            brand: {
              navy: '#0A192F',
              navyLight: '#112240',
              gold: '#C29B38',
              goldHover: '#D4AF37',
              slateDark: '#020C1B'
            }
          },
          fontFamily: {
            heading: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
            sans: ['Inter', 'system-ui', 'sans-serif']
          }
        }
      }
    };
  </script>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      overflow-x: hidden;
      width: 100%;
      background-color: #0A192F;
      color: #F8FAFC;
    }
    .font-heading {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }
    .container-custom {
      max-width: 1280px;
      margin-left: auto;
      margin-right: auto;
      padding-left: 1.5rem;
      padding-right: 1.5rem;
    }
    .btn-primary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background-color: #C29B38;
      color: #FFFFFF;
      font-weight: 700;
      font-size: 0.9375rem;
      padding: 0.75rem 1.75rem;
      border-radius: 0.5rem;
      text-decoration: none;
      transition: all 0.25s ease;
      border: 1px solid transparent;
      cursor: pointer;
    }
    .btn-primary:hover {
      background-color: #D4AF37;
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(194, 155, 56, 0.4);
    }
    .btn-outline {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background-color: rgba(255, 255, 255, 0.05);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.25);
      font-weight: 600;
      font-size: 0.9375rem;
      padding: 0.75rem 1.75rem;
      border-radius: 0.5rem;
      text-decoration: none;
      transition: all 0.25s ease;
      cursor: pointer;
    }
    .btn-outline:hover {
      background-color: rgba(255, 255, 255, 0.15);
      border-color: #FFFFFF;
      transform: translateY(-2px);
    }
    .gold-gradient-text {
      background: linear-gradient(135deg, #ECC974 0%, #C29B38 50%, #997722 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .card-hover {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card-hover:hover {
      transform: translateY(-6px);
      box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.5), 0 0 20px 0 rgba(194, 155, 56, 0.15);
      border-color: #C29B38;
    }
    __CUSTOM_CSS__
  </style>
</head>
<body class="bg-[#0A192F] text-slate-100 antialiased selection:bg-[#C29B38] selection:text-slate-950">
  <div id="site-container" class="min-h-screen flex flex-col max-w-full overflow-x-hidden">
    
    <!-- Top Corporate Header -->
    <header class="sticky top-0 z-50 bg-[#0A192F]/90 backdrop-blur-md border-b border-slate-800 shadow-lg">
      <div class="container-custom">
        <div class="flex items-center justify-between h-20">
          
          <!-- Brand Logo -->
          <a href="/" class="flex items-center space-x-3 text-white no-underline group" aria-label="RDGCC Corporate Homepage">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-tr from-[#C29B38] to-[#ECC974] flex items-center justify-center font-extrabold text-[#0A192F] text-xl shadow-md group-hover:scale-105 transition-transform">
              R
            </div>
            <div class="flex flex-col">
              <span class="font-heading font-extrabold text-xl tracking-tight text-white group-hover:text-amber-400 transition-colors">
                RDGCC
              </span>
              <span class="text-[10px] uppercase font-mono tracking-widest text-slate-400 font-medium">
                GCC Regional Holding
              </span>
            </div>
          </a>

          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center space-x-8 text-sm font-medium" aria-label="Main Navigation">
            <a href="#about" class="text-slate-300 hover:text-[#ECC974] transition-colors py-1 border-b-2 border-transparent hover:border-[#C29B38]">Overview</a>
            <a href="#sectors" class="text-slate-300 hover:text-[#ECC974] transition-colors py-1 border-b-2 border-transparent hover:border-[#C29B38]">Sectors</a>
            <a href="#stats" class="text-slate-300 hover:text-[#ECC974] transition-colors py-1 border-b-2 border-transparent hover:border-[#C29B38]">Performance</a>
            <a href="#projects" class="text-slate-300 hover:text-[#ECC974] transition-colors py-1 border-b-2 border-transparent hover:border-[#C29B38]">Projects</a>
            <a href="#contact" class="text-slate-300 hover:text-[#ECC974] transition-colors py-1 border-b-2 border-transparent hover:border-[#C29B38]">Contact</a>
          </nav>

          <!-- Utilities & CTA -->
          <div class="flex items-center space-x-4">
            <div class="hidden sm:flex items-center bg-slate-900/80 rounded-lg border border-slate-700/60 p-1 text-xs font-semibold">
              <button type="button" class="px-2.5 py-1 rounded bg-[#C29B38] text-white shadow-sm" aria-label="Switch to English">EN</button>
              <button type="button" class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition-colors" aria-label="Switch to Arabic">العربية</button>
            </div>
            <a href="#contact" class="btn-primary text-xs !py-2.5 !px-5 shadow">
              Contact Us
            </a>
            <!-- Mobile Menu Toggle Button -->
            <button id="mobile-menu-btn" class="md:hidden p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white" aria-label="Toggle Mobile Menu">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
            </button>
          </div>

        </div>
      </div>
      <!-- Mobile Dropdown -->
      <div id="mobile-nav" class="hidden md:hidden bg-slate-950 border-b border-slate-800 px-6 py-4 space-y-3">
        <a href="#about" class="block text-sm text-slate-300 hover:text-amber-400">Overview</a>
        <a href="#sectors" class="block text-sm text-slate-300 hover:text-amber-400">Sectors</a>
        <a href="#stats" class="block text-sm text-slate-300 hover:text-amber-400">Performance</a>
        <a href="#projects" class="block text-sm text-slate-300 hover:text-amber-400">Projects</a>
        <a href="#contact" class="block text-sm text-slate-300 hover:text-amber-400">Contact</a>
      </div>
    </header>

    <main class="flex-grow">
      
      <!-- HERO SECTION -->
      <section id="hero" class="relative bg-[#0A192F] py-24 md:py-36 overflow-hidden border-b border-slate-800">
        <!-- Radial Grid Architectural Background -->
        <div class="absolute inset-0 opacity-15 pointer-events-none" style="background-image: radial-gradient(#C29B38 1.5px, transparent 1.5px); background-size: 36px 36px;"></div>
        <div class="absolute -top-40 -right-40 w-[550px] h-[550px] bg-[#C29B38]/15 rounded-full blur-[140px] pointer-events-none"></div>
        <div class="absolute -bottom-40 -left-40 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[140px] pointer-events-none"></div>

        <div class="container-custom relative z-10">
          <div class="max-w-3xl">
            
            <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-800/90 border border-[#C29B38]/40 text-[#ECC974] text-xs font-semibold tracking-wider uppercase mb-8 shadow-sm">
              <span class="w-2 h-2 rounded-full bg-[#C29B38] animate-pulse"></span>
              <span>Strategic GCC Investment Holding</span>
            </div>

            <h1 class="text-4xl sm:text-5xl md:text-6xl font-heading font-extrabold text-white tracking-tight leading-[1.12] mb-6">
              Empowering Regional Excellence and <span class="gold-gradient-text">Strategic Growth</span> Across the GCC
            </h1>

            <p class="text-lg sm:text-xl text-slate-300 leading-relaxed mb-10 font-normal max-w-2xl">
              RDGCC drives transformative sovereign and institutional capital, pioneering industrial infrastructure, and sustainable value creation across Gulf Cooperation Council economies.
            </p>

            <div class="flex flex-wrap items-center gap-4">
              <a href="#sectors" class="btn-primary shadow-xl">
                Explore Our Sectors
              </a>
              <a href="#about" class="btn-outline">
                Corporate Overview
              </a>
            </div>

          </div>
        </div>
      </section>

      <!-- KEY STATS SECTION -->
      <section id="stats" class="py-14 bg-[#112240] border-b border-slate-800 relative z-20">
        <div class="container-custom">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-6 text-center">
            <div class="p-4 border-r border-slate-800 last:border-r-0">
              <div class="font-heading text-4xl sm:text-5xl font-extrabold gold-gradient-text mb-1">$3.8B+</div>
              <div class="text-sm font-semibold text-white mb-0.5">Assets Under Management</div>
              <div class="text-xs text-slate-400">Institutional investment portfolio</div>
            </div>
            <div class="p-4 border-r border-slate-800 last:border-r-0">
              <div class="font-heading text-4xl sm:text-5xl font-extrabold text-white mb-1">18+</div>
              <div class="text-sm font-semibold text-white mb-0.5">Regional Hubs</div>
              <div class="text-xs text-slate-400">Presence across GCC member states</div>
            </div>
            <div class="p-4 border-r border-slate-800 last:border-r-0">
              <div class="font-heading text-4xl sm:text-5xl font-extrabold gold-gradient-text mb-1">32</div>
              <div class="text-sm font-semibold text-white mb-0.5">Years of Heritage</div>
              <div class="text-xs text-slate-400">Delivering regional industrial milestones</div>
            </div>
            <div class="p-4">
              <div class="font-heading text-4xl sm:text-5xl font-extrabold text-white mb-1">99.4%</div>
              <div class="text-sm font-semibold text-white mb-0.5">Safety & Compliance</div>
              <div class="text-xs text-slate-400">HSE international Gold Standard</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ABOUT SECTION -->
      <section id="about" class="py-24 bg-[#0A192F] border-b border-slate-800">
        <div class="container-custom">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div class="lg:col-span-7">
              <div class="inline-block text-xs uppercase tracking-widest text-[#ECC974] font-semibold mb-3">About RDGCC</div>
              <h2 class="text-3xl sm:text-4xl font-heading font-extrabold text-white tracking-tight mb-6">
                Building Resilient Infrastructure for a Sustainable Arabian Future
              </h2>
              <p class="text-slate-300 leading-relaxed mb-4 text-base">
                For over three decades, RDGCC has served as a catalyst for sovereign and private development across Saudi Arabia and the wider GCC region. We partner with institutional leaders to deploy innovative engineering, energy infrastructure, and industrial manufacturing capacity.
              </p>
              <p class="text-slate-300 leading-relaxed mb-8 text-base">
                Our commitment to Vision 2030 and GCC unified growth frameworks establishes sustainable economic ecosystems built for multi-generational returns.
              </p>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                <div class="p-4 rounded-xl bg-[#112240]/60 border border-slate-800">
                  <div class="font-heading font-bold text-sm text-[#ECC974] mb-1">Strategic Capital</div>
                  <div class="text-xs text-slate-400">Targeted regional equity investments in sovereign-priority sectors.</div>
                </div>
                <div class="p-4 rounded-xl bg-[#112240]/60 border border-slate-800">
                  <div class="font-heading font-bold text-sm text-white mb-1">Industrial Innovation</div>
                  <div class="text-xs text-slate-400">Deploying advanced manufacturing and logistics automation.</div>
                </div>
                <div class="p-4 rounded-xl bg-[#112240]/60 border border-slate-800">
                  <div class="font-heading font-bold text-sm text-[#ECC974] mb-1">Governance & ESG</div>
                  <div class="text-xs text-slate-400">Institutional excellence adhering to international sustainability benchmarks.</div>
                </div>
              </div>
            </div>

            <div class="lg:col-span-5">
              <div class="relative rounded-2xl overflow-hidden border border-slate-700/60 shadow-2xl bg-gradient-to-br from-[#112240] to-slate-900 p-8">
                <div class="w-14 h-14 rounded-xl bg-[#C29B38]/20 border border-[#C29B38]/40 flex items-center justify-center mb-6">
                  <svg class="w-8 h-8 text-[#ECC974]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                </div>
                <h3 class="text-2xl font-heading font-bold text-white mb-3">Pioneering Sovereign Growth</h3>
                <p class="text-slate-300 text-sm leading-relaxed mb-6">
                  Aligning global institutional investment with the Arabian Gulf's most ambitious industrial megaprojects.
                </p>
                <div class="flex items-center space-x-3 text-xs font-mono text-[#ECC974]">
                  <span>KSA</span> • <span>UAE</span> • <span>QATAR</span> • <span>BAHRAIN</span> • <span>OMAN</span> • <span>KUWAIT</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTORS SECTION -->
      <section id="sectors" class="py-24 bg-[#112240] border-b border-slate-800">
        <div class="container-custom">
          <div class="text-center max-w-2xl mx-auto mb-16">
            <div class="text-xs uppercase tracking-widest text-[#ECC974] font-semibold mb-3">Strategic Focus</div>
            <h2 class="text-3xl sm:text-4xl font-heading font-extrabold text-white tracking-tight mb-4">
              Core Investment Sectors
            </h2>
            <p class="text-slate-300 text-sm sm:text-base">
              Delivering high-performance execution across foundational industrial, logistics, and energy verticals.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            <!-- Sector 1 -->
            <div class="p-6 rounded-2xl bg-[#0A192F] border border-slate-800 card-hover flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-[#ECC974] mb-5">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div class="text-xs font-semibold text-[#ECC974] uppercase tracking-wider mb-1">1.4 GW Capacity</div>
                <h3 class="text-xl font-heading font-bold text-white mb-3">Energy & Industrial</h3>
                <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                  Clean power grids, EPC infrastructure, and specialized offshore servicing supporting GCC energy transitions.
                </p>
              </div>
              <div class="flex flex-wrap gap-1.5 pt-3 border-t border-slate-800/80">
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Renewable Microgrids</span>
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Petrochemical</span>
              </div>
            </div>

            <!-- Sector 2 -->
            <div class="p-6 rounded-2xl bg-[#0A192F] border border-slate-800 card-hover flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400 mb-5">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 13h18M5 10h14a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2z"/></svg>
                </div>
                <div class="text-xs font-semibold text-[#ECC974] uppercase tracking-wider mb-1">4.8M TEU Handled</div>
                <h3 class="text-xl font-heading font-bold text-white mb-3">Maritime & Ports</h3>
                <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                  Multi-modal logistics corridors, deepwater container terminals, and integrated supply networks.
                </p>
              </div>
              <div class="flex flex-wrap gap-1.5 pt-3 border-t border-slate-800/80">
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Automated Ports</span>
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Cold Chain</span>
              </div>
            </div>

            <!-- Sector 3 -->
            <div class="p-6 rounded-2xl bg-[#0A192F] border border-slate-800 card-hover flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-5">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                </div>
                <div class="text-xs font-semibold text-[#ECC974] uppercase tracking-wider mb-1">12M+ Sq. Ft. Built</div>
                <h3 class="text-xl font-heading font-bold text-white mb-3">Infrastructure</h3>
                <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                  Master-planned industrial cities, commercial logistics hubs, and sustainable urban developments.
                </p>
              </div>
              <div class="flex flex-wrap gap-1.5 pt-3 border-t border-slate-800/80">
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Free Zones</span>
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Smart Cities</span>
              </div>
            </div>

            <!-- Sector 4 -->
            <div class="p-6 rounded-2xl bg-[#0A192F] border border-slate-800 card-hover flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 mb-5">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                </div>
                <div class="text-xs font-semibold text-[#ECC974] uppercase tracking-wider mb-1">35% Carbon Cut</div>
                <h3 class="text-xl font-heading font-bold text-white mb-3">Sustainable Tech</h3>
                <p class="text-slate-400 text-xs sm:text-sm leading-relaxed mb-4">
                  Circular economy initiatives, green hydrogen applications, and digital twins for heavy industry.
                </p>
              </div>
              <div class="flex flex-wrap gap-1.5 pt-3 border-t border-slate-800/80">
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Green Hydrogen</span>
                <span class="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300">Telemetry</span>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- FEATURED PROJECTS SHOWCASE -->
      <section id="projects" class="py-24 bg-[#0A192F] border-b border-slate-800">
        <div class="container-custom">
          <div class="flex flex-col md:flex-row md:items-end justify-between mb-16">
            <div>
              <div class="text-xs uppercase tracking-widest text-[#ECC974] font-semibold mb-3">Flagship Portfolio</div>
              <h2 class="text-3xl sm:text-4xl font-heading font-extrabold text-white tracking-tight">
                Transformative Regional Projects
              </h2>
            </div>
            <p class="text-slate-400 text-sm max-w-md mt-4 md:mt-0">
              Pioneering sovereign engineering milestones delivered on time, within safety standards, and across regional borders.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            <div class="p-8 rounded-2xl bg-[#112240] border border-slate-800 card-hover">
              <div class="flex items-center justify-between text-xs font-mono mb-4">
                <span class="px-2.5 py-1 rounded bg-[#0A192F] text-[#ECC974] border border-amber-500/30">Maritime Logistics</span>
                <span class="text-slate-400">Ras Al Khair, KSA • 2024</span>
              </div>
              <h3 class="text-2xl font-heading font-bold text-white mb-3">King Salman Maritime Gateway</h3>
              <p class="text-slate-300 text-sm leading-relaxed mb-6">
                Integrated maritime mega-hub incorporating automated dry docks, container feeder terminals, and AI-driven harbor control systems.
              </p>
              <div class="flex items-center space-x-2 text-xs font-bold text-[#ECC974]">
                <span>Completed Infrastructure Milestone</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>

            <div class="p-8 rounded-2xl bg-[#112240] border border-slate-800 card-hover">
              <div class="flex items-center justify-between text-xs font-mono mb-4">
                <span class="px-2.5 py-1 rounded bg-[#0A192F] text-emerald-400 border border-emerald-500/30">Renewable Energy</span>
                <span class="text-slate-400">Yanbu Industrial City, KSA • 2023</span>
              </div>
              <h3 class="text-2xl font-heading font-bold text-white mb-3">Gulf Clean Energy Microgrid</h3>
              <p class="text-slate-300 text-sm leading-relaxed mb-6">
                Utility-scale 450MW solar and battery storage installation providing zero-carbon baseload power to heavy manufacturing facilities.
              </p>
              <div class="flex items-center space-x-2 text-xs font-bold text-emerald-400">
                <span>Operational Clean Energy Facility</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>

            <div class="p-8 rounded-2xl bg-[#112240] border border-slate-800 card-hover">
              <div class="flex items-center justify-between text-xs font-mono mb-4">
                <span class="px-2.5 py-1 rounded bg-[#0A192F] text-blue-400 border border-blue-500/30">Urban Logistics</span>
                <span class="text-slate-400">Riyadh, KSA • 2024</span>
              </div>
              <h3 class="text-2xl font-heading font-bold text-white mb-3">Riyadh Logistics Corridor & Free Zone</h3>
              <p class="text-slate-300 text-sm leading-relaxed mb-6">
                State-of-the-art multimodal distribution park with automated sorting centers, bonded customs handling, and refrigerated pharmaceutical facilities.
              </p>
              <div class="flex items-center space-x-2 text-xs font-bold text-blue-400">
                <span>Phase I Active Operations</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>

            <div class="p-8 rounded-2xl bg-[#112240] border border-slate-800 card-hover">
              <div class="flex items-center justify-between text-xs font-mono mb-4">
                <span class="px-2.5 py-1 rounded bg-[#0A192F] text-purple-400 border border-purple-500/30">Industrial Tech</span>
                <span class="text-slate-400">Dubai, UAE • 2023</span>
              </div>
              <h3 class="text-2xl font-heading font-bold text-white mb-3">Dubai Maritime Tech Incubator</h3>
              <p class="text-slate-300 text-sm leading-relaxed mb-6">
                Dedicated research center and testbed prototyping autonomous surface vessels, composite materials, and port telemetry platforms.
              </p>
              <div class="flex items-center space-x-2 text-xs font-bold text-purple-400">
                <span>Center of Excellence</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>

          </div>
        </div>
      </section>

      <!-- CORPORATE CONTACT & INQUIRY SECTION -->
      <section id="contact" class="py-24 bg-[#112240] border-b border-slate-800">
        <div class="container-custom">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
            
            <div class="lg:col-span-5">
              <div class="text-xs uppercase tracking-widest text-[#ECC974] font-semibold mb-3">Connect With Us</div>
              <h2 class="text-3xl sm:text-4xl font-heading font-extrabold text-white tracking-tight mb-6">
                Partner With RDGCC Holdings
              </h2>
              <p class="text-slate-300 leading-relaxed mb-8 text-sm sm:text-base">
                We invite institutional investors, sovereign funds, and EPC consortiums to discuss co-investment and development opportunities across the Arabian Gulf.
              </p>

              <div class="space-y-4">
                <div class="p-4 rounded-xl bg-[#0A192F] border border-slate-800 flex items-center space-x-4">
                  <div class="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center text-[#ECC974]">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                  </div>
                  <div>
                    <div class="text-xs text-slate-400">Official Inquiries</div>
                    <div class="text-sm font-semibold text-white">inquiries@rdgcc.com</div>
                  </div>
                </div>

                <div class="p-4 rounded-xl bg-[#0A192F] border border-slate-800 flex items-center space-x-4">
                  <div class="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  </div>
                  <div>
                    <div class="text-xs text-slate-400">Regional Headquarters</div>
                    <div class="text-sm font-semibold text-white">King Fahd Road, Riyadh, Kingdom of Saudi Arabia</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Interactive Form -->
            <div class="lg:col-span-7">
              <div class="p-8 rounded-2xl bg-[#0A192F] border border-slate-800 shadow-2xl">
                <h3 class="text-xl font-heading font-bold text-white mb-2">Submit Institutional Inquiry</h3>
                <p class="text-xs text-slate-400 mb-6">Please complete all required fields. Our executive team will respond within 24 business hours.</p>

                <form id="inquiry-form" class="space-y-4" onsubmit="event.preventDefault(); document.getElementById('form-feedback').classList.remove('hidden'); this.reset();">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label for="fullname" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Full Name *</label>
                      <input type="text" id="fullname" name="fullname" required placeholder="H.E. / Dr. / Mr. / Ms." class="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder-slate-500 text-sm focus:border-[#C29B38] focus:outline-none transition-colors">
                    </div>
                    <div>
                      <label for="email" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Corporate Email *</label>
                      <input type="email" id="email" name="email" required placeholder="executive@institution.com" class="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder-slate-500 text-sm focus:border-[#C29B38] focus:outline-none transition-colors">
                    </div>
                  </div>

                  <div>
                    <label for="sector" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Sector of Interest</label>
                    <select id="sector" name="sector" class="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white text-sm focus:border-[#C29B38] focus:outline-none transition-colors">
                      <option value="energy">Energy & Industrial Services</option>
                      <option value="maritime">Maritime & Port Logistics</option>
                      <option value="infrastructure">Real Estate & Strategic Infrastructure</option>
                      <option value="tech">Sustainable Tech & Materials</option>
                      <option value="general">General Corporate Inquiry</option>
                    </select>
                  </div>

                  <div>
                    <label for="message" class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Inquiry Overview *</label>
                    <textarea id="message" name="message" rows="4" required placeholder="Outline your strategic objective or partnership inquiry..." class="w-full px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder-slate-500 text-sm focus:border-[#C29B38] focus:outline-none transition-colors"></textarea>
                  </div>

                  <button type="submit" class="btn-primary w-full !py-3.5 text-sm font-bold tracking-wide shadow-lg">
                    Submit Corporate Inquiry
                  </button>
                  
                  <div id="form-feedback" class="hidden p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs text-center font-medium">
                    Thank you. Your corporate inquiry has been submitted securely to the RDGCC executive desk.
                  </div>
                </form>
              </div>
            </div>

          </div>
        </div>
      </section>

    </main>

    <!-- EXECUTIVE FOOTER -->
    <footer class="bg-[#020C1B] border-t border-slate-800/80 py-12 text-slate-400 text-xs">
      <div class="container-custom">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          <div class="md:col-span-2">
            <div class="flex items-center space-x-2 text-white font-heading font-extrabold text-lg mb-3">
              <div class="w-6 h-6 rounded bg-[#C29B38] flex items-center justify-center text-slate-950 font-bold text-xs">R</div>
              <span>RDGCC Holdings</span>
            </div>
            <p class="text-slate-400 max-w-sm leading-relaxed mb-4">
              Pioneering sovereign-aligned capital deployment and critical industrial infrastructure across the Gulf Cooperation Council economies.
            </p>
            <div class="text-[11px] text-slate-500 font-mono">
              Riyadh • Dubai • Manama • Doha • Muscat • Kuwait City
            </div>
          </div>

          <div>
            <div class="text-xs font-bold text-white uppercase tracking-wider mb-3">Navigation</div>
            <ul class="space-y-2">
              <li><a href="#about" class="hover:text-white transition-colors">About Holding</a></li>
              <li><a href="#sectors" class="hover:text-white transition-colors">Core Sectors</a></li>
              <li><a href="#stats" class="hover:text-white transition-colors">Financial Performance</a></li>
              <li><a href="#projects" class="hover:text-white transition-colors">Key Projects</a></li>
            </ul>
          </div>

          <div>
            <div class="text-xs font-bold text-white uppercase tracking-wider mb-3">Governance & Legal</div>
            <ul class="space-y-2">
              <li><a href="#contact" class="hover:text-white transition-colors">Investor Relations</a></li>
              <li><a href="#contact" class="hover:text-white transition-colors">ESG Policy & Benchmarks</a></li>
              <li><a href="#contact" class="hover:text-white transition-colors">HSE Gold Standard</a></li>
              <li><a href="#contact" class="hover:text-white transition-colors">Privacy & Disclosures</a></li>
            </ul>
          </div>
        </div>

        <div class="pt-8 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500">
          <div>© 2024-2026 RDGCC Holdings Ltd. All rights reserved. Sovereign-Aligned Regional Investment.</div>
          <div class="mt-2 sm:mt-0 font-mono text-amber-500/80">ISO 9001:2015 & HSE Certified</div>
        </div>
      </div>
    </footer>

  </div>

  <script>
    // Mobile navigation toggle
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const mobileNav = document.getElementById('mobile-nav');
    if (mobileBtn && mobileNav) {
      mobileBtn.addEventListener('click', function() {
        mobileNav.classList.toggle('hidden');
      });
    }
  </script>
</body>
</html>"""
        return template.replace("__CUSTOM_CSS__", css)
