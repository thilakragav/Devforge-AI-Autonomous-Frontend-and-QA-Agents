"""
Agent 1 - Astro Code Generator
Generates modular, responsive Astro components, decoupled data, and Sanity schemas from DesignAnalysisResult.
"""
from typing import List, Optional
from datetime import datetime

from backend.schemas.agent1_schema import (
    DesignAnalysisResult,
    AstroProjectManifest,
    AstroComponentCode,
)
from backend.agents.agent1.sanity_schemas import generate_sanity_schemas
from backend.utils.logger import global_log_buffer


class AstroCodeGenerator:
    def __init__(self):
        pass

    def generate_project(
        self,
        analysis: DesignAnalysisResult,
        project_id: str = "project_001",
        version: int = 1,
        output_directory: str = "generated_projects/project_001"
    ) -> AstroProjectManifest:
        """
        Synthesizes complete, modular Astro application from design analysis.
        Separates content, presentation, and layout into distinct files.
        """
        global_log_buffer.log("GENERATOR", "AGENT_1", f"Generating modular Astro project: {project_id} (v{version})")

        components: List[AstroComponentCode] = []

        # 1. Structured Data (src/data/homepage.js)
        structured_data = self._generate_structured_data(analysis)

        # 2. Global CSS (src/styles/global.css)
        global_css = self._generate_global_css(analysis)

        # 3. Main Layout (src/layouts/MainLayout.astro)
        components.append(self._generate_main_layout(analysis))

        # 4. Header & Navigation (src/components/Header.astro & Navigation.astro)
        components.append(self._generate_navigation_component())
        components.append(self._generate_header_component())

        # 5. Core Content Sections
        components.append(self._generate_hero_component())
        components.append(self._generate_about_component())
        components.append(self._generate_sectors_component())
        components.append(self._generate_stats_component())
        components.append(self._generate_projects_component())
        components.append(self._generate_contact_component())
        components.append(self._generate_footer_component())

        # 6. Main Page (src/pages/index.astro)
        components.append(self._generate_index_page())

        # 7. Configs
        pkg_json = self._generate_package_json()
        astro_cfg = self._generate_astro_config()

        # 8. Sanity CMS Schemas
        sanity_schemas = generate_sanity_schemas()

        manifest = AstroProjectManifest(
            project_id=project_id,
            version=version,
            project_name=analysis.project_name,
            output_directory=output_directory,
            components=components,
            structured_content_file=structured_data,
            sanity_schemas=sanity_schemas,
            global_css=global_css,
            package_json=pkg_json,
            astro_config=astro_cfg,
            build_valid=True,
            assumptions=analysis.assumptions_and_limitations
        )

        global_log_buffer.log(
            "GENERATOR",
            "AGENT_1",
            f"Successfully assembled manifest with {len(components)} Astro files, structured data, and Sanity schemas."
        )

        return manifest

    def _generate_package_json(self) -> str:
        return """{
  "name": "rdgcc-corporate-astro",
  "type": "module",
  "version": "1.0.0",
  "scripts": {
    "dev": "astro dev --port 4321",
    "start": "astro dev --port 4321",
    "build": "astro build",
    "preview": "astro preview"
  },
  "dependencies": {
    "astro": "^4.15.0"
  }
}
"""

    def _generate_astro_config(self) -> str:
        return """import { defineConfig } from 'astro/config';

export default defineConfig({
  server: {
    port: 4321,
    host: true
  }
});
"""

    def _generate_global_css(self, analysis: DesignAnalysisResult) -> str:
        return """/* Reset and Modern Typography */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --color-primary: #0A192F;
  --color-primary-light: #112240;
  --color-accent: #C29B38;
  --color-accent-hover: #D4AF37;
  --color-surface: #F8FAFC;
  --color-surface-white: #FFFFFF;
  --color-text-main: #1E293B;
  --color-text-muted: #64748B;
  --color-border: #E2E8F0;
  --font-heading: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;
}

html {
  font-family: var(--font-body);
  color: var(--color-text-main);
  background-color: var(--color-surface);
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
}

body {
  line-height: 1.6;
  overflow-x: hidden;
  width: 100%;
}

h1, h2, h3, h4, .font-heading {
  font-family: var(--font-heading);
  letter-spacing: -0.02em;
}

/* Container Utility */
.container-custom {
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

/* Button Utilities */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-accent);
  color: #FFFFFF;
  font-weight: 600;
  font-size: 0.9375rem;
  padding: 0.75rem 1.75rem;
  border-radius: 0.375rem;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: var(--color-accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(194, 155, 56, 0.25);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  color: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.4);
  font-weight: 600;
  font-size: 0.9375rem;
  padding: 0.75rem 1.75rem;
  border-radius: 0.375rem;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

.btn-outline:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: #FFFFFF;
}

/* Card Hover Effects */
.sector-card {
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.sector-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -4px rgba(10, 25, 47, 0.08);
  border-color: var(--color-accent);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hero-headline {
    font-size: 2.25rem !important;
  }
}
"""

    def _generate_structured_data(self, analysis: DesignAnalysisResult) -> str:
        return """// src/data/homepage.js
// Structured Content Architecture (Sanity CMS Ready)
// Decouples editorial data from frontend layout and components.

export const siteSettings = {
  companyName: "RDGCC Holdings",
  logoText: "RDGCC",
  tagline: "Regional Development & Strategic Growth",
  contactEmail: "inquiries@rdgcc.com",
  regionalOffices: ["Riyadh, KSA", "Dubai, UAE", "Manama, Bahrain", "Doha, Qatar"],
  languages: [
    { code: "en", label: "EN", active: true },
    { code: "ar", label: "العربية", active: false }
  ]
};

export const navigationMenu = [
  { label: "Overview", href: "#about" },
  { label: "Sectors", href: "#sectors" },
  { label: "Performance", href: "#stats" },
  { label: "Projects", href: "#projects" },
  { label: "Contact", href: "#contact" }
];

export const heroContent = {
  badge: "Strategic GCC Investment Holding",
  headline: "Empowering Regional Excellence and Strategic Growth Across the GCC",
  subheadline: "RDGCC drives transformative capital, pioneering industrial infrastructure, and sustainable value creation across Gulf Cooperation Council economies.",
  primaryCta: { label: "Explore Our Sectors", href: "#sectors" },
  secondaryCta: { label: "Corporate Overview", href: "#about" }
};

export const aboutContent = {
  badge: "About RDGCC",
  title: "Building Resilient Infrastructure for a Sustainable Arabian Future",
  paragraphOne: "For over three decades, RDGCC has served as a catalyst for sovereign and private development across Saudi Arabia and the wider GCC region. We partner with institutional leaders to deploy innovative engineering, energy infrastructure, and industrial manufacturing capacity.",
  paragraphTwo: "Our commitment to Vision 2030 and GCC unified growth frameworks establishes sustainable economic ecosystems built for multi-generational returns.",
  pillars: [
    { title: "Strategic Capital", description: "Targeted regional equity investments in sovereign-priority sectors." },
    { title: "Industrial Innovation", description: "Deploying advanced manufacturing, logistics automation, and clean technologies." },
    { title: "Governance & ESG", description: "Institutional excellence adhering to international sustainability benchmarks." }
  ]
};

export const sectorsData = [
  {
    id: "energy",
    title: "Energy & Industrial Services",
    icon: "bolt",
    statsHighlight: "1.4 GW Capacity",
    description: "Developing clean power grids, EPC infrastructure, and specialized offshore servicing supporting GCC energy transitions.",
    capabilities: ["Renewable Microgrids", "Petrochemical Processing", "Offshore Support Vessels"]
  },
  {
    id: "maritime",
    title: "Maritime & Port Logistics",
    icon: "ship",
    statsHighlight: "4.8M TEU Handled",
    description: "Operating multi-modal logistics corridors, deepwater container terminals, and integrated supply networks connecting East and West.",
    capabilities: ["Automated Port Operations", "Cold Chain Logistics", "Bunkering Facilities"]
  },
  {
    id: "infrastructure",
    title: "Real Estate & Strategic Infrastructure",
    icon: "building",
    statsHighlight: "12M+ Sq. Ft. Built",
    description: "Master-planned industrial cities, commercial logistics hubs, and sustainable urban developments across major GCC trade hubs.",
    capabilities: ["Industrial Free Zones", "Specialized Tech Parks", "Smart City Utilities"]
  },
  {
    id: "technology",
    title: "Sustainable Tech & Materials",
    icon: "cpu",
    statsHighlight: "35% Carbon Reduction",
    description: "Pioneering circular economy initiatives, green hydrogen applications, and digital twin technology for heavy industry.",
    capabilities: ["Green Hydrogen", "Advanced Composites", "Autonomous Fleet Telemetry"]
  }
];

export const statsMetrics = [
  { value: "$3.8B+", label: "Assets Under Management", description: "Institutional investment portfolio" },
  { value: "18+", label: "Regional Hubs", description: "Presence across GCC member states" },
  { value: "32", label: "Years of Heritage", description: "Delivering regional industrial milestones" },
  { value: "99.4%", label: "Safety & Compliance", description: "HSE international Gold Standard" }
];

export const featuredProjects = [
  {
    title: "King Salman Maritime Gateway",
    sector: "Maritime Logistics",
    location: "Ras Al Khair, KSA",
    year: "2024",
    summary: "Integrated mega-hub incorporating automated dry docks, container feeder terminals, and AI-driven harbor control."
  },
  {
    title: "Gulf Clean Energy Microgrid",
    sector: "Renewable Energy",
    location: "Yanbu Industrial City, KSA",
    year: "2023",
    summary: "Utility-scale 450MW solar and battery storage installation powering heavy manufacturing facilities."
  },
  {
    title: "Al-Sharq Trade & Logistics Freezone",
    sector: "Infrastructure",
    location: "Dammam, KSA",
    year: "2024",
    summary: "2.4M square meter master-planned bonded logistics facility with multimodal rail and sea access."
  }
];

export const contactDetails = {
  headquarters: "RDGCC Tower, King Fahd Road, Riyadh, Kingdom of Saudi Arabia",
  phone: "+966 11 400 9200",
  email: "contact@rdgcc.com",
  inquiryTypes: ["General Corporate", "Investment & Partnerships", "Supply Chain & Procurement", "Media Inquiries"]
};
"""

    def _generate_main_layout(self, analysis: DesignAnalysisResult) -> AstroComponentCode:
        content = """---
// src/layouts/MainLayout.astro
import '../styles/global.css';

interface Props {
  title?: string;
  description?: string;
}

const { 
  title = "RDGCC | Regional Development & Strategic GCC Investment Holding",
  description = "RDGCC drives strategic regional investment, infrastructure development, and industrial transformation across the GCC."
} = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content={description} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <title>{title}</title>
  </head>
  <body class="bg-surface text-slate-800 antialiased min-h-screen flex flex-col">
    <slot />
  </body>
</html>
"""
        return AstroComponentCode(
            filename="MainLayout.astro",
            path="src/layouts/MainLayout.astro",
            content=content,
            is_layout=True,
            description="Main responsive HTML boilerplate layout with Google fonts and metadata."
        )

    def _generate_navigation_component(self) -> AstroComponentCode:
        content = """---
// src/components/Navigation.astro
import { navigationMenu } from '../data/homepage.js';
---

<nav class="hidden md:flex items-center space-x-8" aria-label="Main Navigation">
  {navigationMenu.map((item) => (
    <a 
      href={item.href}
      class="text-sm font-medium text-slate-200 hover:text-amber-400 transition-colors duration-200 py-1"
    >
      {item.label}
    </a>
  ))}
</nav>
"""
        return AstroComponentCode(
            filename="Navigation.astro",
            path="src/components/Navigation.astro",
            content=content,
            description="Navigation bar with semantic anchor links."
        )

    def _generate_header_component(self) -> AstroComponentCode:
        content = """---
// src/components/Header.astro
import Navigation from './Navigation.astro';
import { siteSettings } from '../data/homepage.js';
---

<header class="sticky top-0 z-50 bg-[#0A192F] border-b border-slate-800/80 backdrop-blur-md shadow-md">
  <div class="container-custom">
    <div class="flex items-center justify-between h-20">
      
      <!-- Brand Logo -->
      <a href="/" class="flex items-center space-x-3 text-white no-underline group" aria-label="RDGCC Homepage">
        <div class="w-10 h-10 rounded bg-gradient-to-br from-[#C29B38] to-[#997722] flex items-center justify-center font-bold text-white text-lg tracking-wider shadow">
          R
        </div>
        <div class="flex flex-col">
          <span class="font-heading font-extrabold text-xl tracking-tight text-white group-hover:text-amber-400 transition-colors">
            {siteSettings.logoText}
          </span>
          <span class="text-[10px] uppercase tracking-widest text-slate-400 font-medium">
            GCC Holdings
          </span>
        </div>
      </a>

      <!-- Desktop Navigation -->
      <Navigation />

      <!-- Utility: Language & CTA -->
      <div class="flex items-center space-x-4">
        <div class="hidden sm:flex items-center bg-slate-900/60 rounded border border-slate-700/60 p-1 text-xs font-semibold">
          {siteSettings.languages.map((lang) => (
            <button 
              type="button"
              class={`px-2 py-0.5 rounded transition-colors ${lang.active ? 'bg-[#C29B38] text-white' : 'text-slate-400 hover:text-white'}`}
              aria-label={`Switch to ${lang.label}`}
            >
              {lang.label}
            </button>
          ))}
        </div>

        <a href="#contact" class="btn-primary text-xs !py-2 !px-4">
          Contact Us
        </a>
      </div>

    </div>
  </div>
</header>
"""
        return AstroComponentCode(
            filename="Header.astro",
            path="src/components/Header.astro",
            content=content,
            description="Sticky corporate header with logo, language selector, and navigation."
        )

    def _generate_hero_component(self) -> AstroComponentCode:
        content = """---
// src/components/Hero.astro
import { heroContent } from '../data/homepage.js';
---

<section id="hero" class="relative bg-[#0A192F] text-white py-24 md:py-32 overflow-hidden border-b border-slate-800">
  <!-- Subtle Architectural Grid Background -->
  <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(#C29B38 1px, transparent 1px); background-size: 32px 32px;"></div>
  <div class="absolute -top-40 -right-40 w-96 h-96 bg-[#C29B38]/10 rounded-full blur-3xl pointer-events-none"></div>

  <div class="container-custom relative z-10">
    <div class="max-w-3xl">
      
      <!-- Badge -->
      <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800/80 border border-amber-500/30 text-amber-400 text-xs font-semibold tracking-wider uppercase mb-6">
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
        <span>{heroContent.badge}</span>
      </div>

      <!-- Headline -->
      <h1 class="hero-headline text-4xl sm:text-5xl md:text-6xl font-extrabold text-white tracking-tight leading-[1.12] mb-6 font-heading">
        {heroContent.headline}
      </h1>

      <!-- Subheadline -->
      <p class="text-lg md:text-xl text-slate-300 font-normal leading-relaxed mb-10 max-w-2xl">
        {heroContent.subheadline}
      </p>

      <!-- Action Buttons -->
      <div class="flex flex-wrap items-center gap-4">
        <a href={heroContent.primaryCta.href} class="btn-primary" id="hero-primary-cta">
          {heroContent.primaryCta.label}
          <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
          </svg>
        </a>
        <a href={heroContent.secondaryCta.href} class="btn-outline" id="hero-secondary-cta">
          {heroContent.secondaryCta.label}
        </a>
      </div>

    </div>
  </div>
</section>
"""
        return AstroComponentCode(
            filename="Hero.astro",
            path="src/components/Hero.astro",
            content=content,
            description="Hero section with primary & secondary CTAs and architectural badge."
        )

    def _generate_about_component(self) -> AstroComponentCode:
        content = """---
// src/components/About.astro
import { aboutContent } from '../data/homepage.js';
---

<section id="about" class="py-20 md:py-28 bg-[#FFFFFF] border-b border-slate-200">
  <div class="container-custom">
    
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
      
      <!-- Narrative Column -->
      <div class="lg:col-span-6">
        <span class="text-xs font-bold uppercase tracking-widest text-[#C29B38] block mb-2">
          {aboutContent.badge}
        </span>
        <h2 class="text-3xl md:text-4xl font-extrabold text-[#0A192F] tracking-tight mb-6 font-heading">
          {aboutContent.title}
        </h2>
        <p class="text-slate-600 text-base md:text-lg mb-6 leading-relaxed">
          {aboutContent.paragraphOne}
        </p>
        <p class="text-slate-600 text-base md:text-lg leading-relaxed">
          {aboutContent.paragraphTwo}
        </p>
      </div>

      <!-- Strategic Pillars Column -->
      <div class="lg:col-span-6 space-y-4">
        {aboutContent.pillars.map((pillar, idx) => (
          <div class="p-6 rounded-lg bg-slate-50 border border-slate-200/80 hover:border-amber-400/60 transition-all duration-200 shadow-sm">
            <div class="flex items-center space-x-3 mb-2">
              <span class="w-7 h-7 rounded-full bg-[#0A192F] text-[#C29B38] text-xs font-bold flex items-center justify-center">
                0{idx + 1}
              </span>
              <h3 class="text-lg font-bold text-[#0A192F] font-heading">
                {pillar.title}
              </h3>
            </div>
            <p class="text-sm text-slate-600 pl-10">
              {pillar.description}
            </p>
          </div>
        ))}
      </div>

    </div>

  </div>
</section>
"""
        return AstroComponentCode(
            filename="About.astro",
            path="src/components/About.astro",
            content=content,
            description="About RDGCC narrative section with structured strategic pillars."
        )

    def _generate_sectors_component(self) -> AstroComponentCode:
        content = """---
// src/components/Sectors.astro
import { sectorsData } from '../data/homepage.js';
---

<section id="sectors" class="py-20 md:py-28 bg-[#F8FAFC] border-b border-slate-200">
  <div class="container-custom">
    
    <div class="text-center max-w-2xl mx-auto mb-16">
      <span class="text-xs font-bold uppercase tracking-widest text-[#C29B38] block mb-2">
        Core Competencies
      </span>
      <h2 class="text-3xl md:text-4xl font-extrabold text-[#0A192F] tracking-tight font-heading">
        Strategic Business Sectors
      </h2>
      <p class="text-slate-600 mt-4 text-base">
        Deploying patient capital and engineering mastery across resilient foundational industries.
      </p>
    </div>

    <!-- 4-Column Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {sectorsData.map((sec) => (
        <article class="sector-card bg-white p-7 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-10 h-10 rounded-lg bg-amber-500/10 text-[#C29B38] flex items-center justify-center font-bold">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span class="text-xs font-semibold px-2.5 py-1 rounded bg-slate-100 text-slate-700">
                {sec.statsHighlight}
              </span>
            </div>

            <h3 class="text-xl font-bold text-[#0A192F] mb-3 font-heading">
              {sec.title}
            </h3>

            <p class="text-sm text-slate-600 leading-relaxed mb-6">
              {sec.description}
            </p>
          </div>

          <div>
            <div class="border-t border-slate-100 pt-4">
              <ul class="space-y-1.5">
                {sec.capabilities.map((cap) => (
                  <li class="text-xs text-slate-500 flex items-center space-x-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#C29B38]"></span>
                    <span>{cap}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </article>
      ))}
    </div>

  </div>
</section>
"""
        return AstroComponentCode(
            filename="Sectors.astro",
            path="src/components/Sectors.astro",
            content=content,
            description="4-column responsive business sector grid."
        )

    def _generate_stats_component(self) -> AstroComponentCode:
        content = """---
// src/components/Stats.astro
import { statsMetrics } from '../data/homepage.js';
---

<section id="stats" class="py-16 bg-[#0A192F] text-white border-b border-slate-800">
  <div class="container-custom">
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-slate-800">
      {statsMetrics.map((item, idx) => (
        <div class={`px-4 ${idx > 0 ? 'pt-6 md:pt-0' : ''}`}>
          <div class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#C29B38] font-heading tracking-tight mb-2">
            {item.value}
          </div>
          <div class="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-1">
            {item.label}
          </div>
          <p class="text-xs text-slate-400">
            {item.description}
          </p>
        </div>
      ))}
    </div>

  </div>
</section>
"""
        return AstroComponentCode(
            filename="Stats.astro",
            path="src/components/Stats.astro",
            content=content,
            description="4-column KPI metrics counter with gold highlights."
        )

    def _generate_projects_component(self) -> AstroComponentCode:
        content = """---
// src/components/Projects.astro
import { featuredProjects } from '../data/homepage.js';
---

<section id="projects" class="py-20 md:py-28 bg-white border-b border-slate-200">
  <div class="container-custom">
    
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-12">
      <div>
        <span class="text-xs font-bold uppercase tracking-widest text-[#C29B38] block mb-2">
          Track Record
        </span>
        <h2 class="text-3xl md:text-4xl font-extrabold text-[#0A192F] tracking-tight font-heading">
          Flagship GCC Developments
        </h2>
      </div>
      <p class="text-sm text-slate-500 max-w-md mt-4 md:mt-0">
        Pioneering infrastructure projects delivered on schedule with sovereign-grade operational benchmarks.
      </p>
    </div>

    <!-- 3-Column Project Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {featuredProjects.map((proj) => (
        <div class="bg-slate-50 rounded-xl overflow-hidden border border-slate-200/90 hover:shadow-lg transition-all duration-300 flex flex-col justify-between">
          <!-- Placeholder Graphic / Header Bar -->
          <div class="h-44 bg-gradient-to-tr from-[#0A192F] to-[#1E293B] relative p-6 flex flex-col justify-between">
            <span class="inline-block px-3 py-1 rounded bg-[#C29B38] text-white text-xs font-bold self-start">
              {proj.sector}
            </span>
            <div class="text-slate-300 text-xs font-medium">
              Location: <span class="text-white font-semibold">{proj.location}</span>
            </div>
          </div>

          <div class="p-6 flex-grow flex flex-col justify-between">
            <div>
              <div class="text-xs text-[#C29B38] font-bold mb-1">Delivered: {proj.year}</div>
              <h3 class="text-xl font-bold text-[#0A192F] mb-3 font-heading">
                {proj.title}
              </h3>
              <p class="text-sm text-slate-600 leading-relaxed mb-6">
                {proj.summary}
              </p>
            </div>

            <a href="#contact" class="text-xs font-bold text-[#0A192F] hover:text-[#C29B38] inline-flex items-center space-x-1.5 transition-colors">
              <span>View Strategic Brief</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        </div>
      ))}
    </div>

  </div>
</section>
"""
        return AstroComponentCode(
            filename="Projects.astro",
            path="src/components/Projects.astro",
            content=content,
            description="3-card flagship projects showcase with details and location tags."
        )

    def _generate_contact_component(self) -> AstroComponentCode:
        content = """---
// src/components/Contact.astro
import { contactDetails } from '../data/homepage.js';
---

<section id="contact" class="py-20 md:py-28 bg-[#F8FAFC] border-b border-slate-200">
  <div class="container-custom">
    
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="grid grid-cols-1 md:grid-cols-12">
        
        <!-- Info Column -->
        <div class="bg-[#0A192F] text-white p-8 md:p-12 md:col-span-5 flex flex-col justify-between">
          <div>
            <span class="text-xs font-bold uppercase tracking-widest text-[#C29B38] block mb-2">
              Regional Presence
            </span>
            <h2 class="text-2xl md:text-3xl font-extrabold text-white mb-6 font-heading">
              Initiate Inquiries
            </h2>
            <p class="text-slate-300 text-sm leading-relaxed mb-8">
              Connect directly with our institutional investment and project development leadership.
            </p>

            <div class="space-y-4 text-xs text-slate-300">
              <div>
                <strong class="text-white block mb-0.5">Headquarters:</strong>
                {contactDetails.headquarters}
              </div>
              <div>
                <strong class="text-white block mb-0.5">Telephone:</strong>
                {contactDetails.phone}
              </div>
              <div>
                <strong class="text-white block mb-0.5">Direct Correspondence:</strong>
                {contactDetails.email}
              </div>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-slate-800 text-[11px] text-slate-400">
            Confidentiality assured under standard institutional covenants.
          </div>
        </div>

        <!-- Interactive Form Column (For Functional QA Testing) -->
        <div class="p-8 md:p-12 md:col-span-7">
          <form id="contact-form" class="space-y-5" onsubmit="event.preventDefault(); alert('Inquiry submitted successfully.');">
            <div>
              <label for="contact-name" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Full Name *
              </label>
              <input 
                type="text" 
                id="contact-name" 
                name="name" 
                required 
                placeholder="Sheikh / Executive Name"
                class="w-full px-3.5 py-2.5 text-sm rounded border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#C29B38] focus:border-transparent transition"
              />
            </div>

            <div>
              <label for="contact-email" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Corporate Email *
              </label>
              <input 
                type="email" 
                id="contact-email" 
                name="email" 
                required 
                placeholder="executive@institution.com"
                class="w-full px-3.5 py-2.5 text-sm rounded border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#C29B38] focus:border-transparent transition"
              />
            </div>

            <div>
              <label for="contact-sector" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Area of Interest *
              </label>
              <select 
                id="contact-sector" 
                name="sector" 
                class="w-full px-3.5 py-2.5 text-sm rounded border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#C29B38] focus:border-transparent transition bg-white"
              >
                {contactDetails.inquiryTypes.map((t) => (
                  <option value={t}>{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label for="contact-message" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Brief Proposal / Inquiries
              </label>
              <textarea 
                id="contact-message" 
                name="message" 
                rows="3" 
                placeholder="Summary of strategic inquiry..."
                class="w-full px-3.5 py-2.5 text-sm rounded border border-slate-300 focus:outline-none focus:ring-2 focus:ring-[#C29B38] focus:border-transparent transition"
              ></textarea>
            </div>

            <button 
              type="submit" 
              id="submit-inquiry-btn" 
              class="btn-primary w-full text-center"
            >
              Submit Strategic Inquiry
            </button>
          </form>
        </div>

      </div>
    </div>

  </div>
</section>
"""
        return AstroComponentCode(
            filename="Contact.astro",
            path="src/components/Contact.astro",
            content=content,
            description="Functional corporate inquiry form with inputs and contact information."
        )

    def _generate_footer_component(self) -> AstroComponentCode:
        content = """---
// src/components/Footer.astro
import { siteSettings, navigationMenu } from '../data/homepage.js';
---

<footer class="bg-[#050C1A] text-slate-400 py-16 border-t border-slate-800">
  <div class="container-custom">
    
    <div class="grid grid-cols-1 md:grid-cols-12 gap-8 mb-12">
      
      <!-- Brand Summary -->
      <div class="md:col-span-5">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-8 h-8 rounded bg-[#C29B38] text-white font-bold flex items-center justify-center text-sm">
            R
          </div>
          <span class="text-white font-heading font-extrabold text-lg tracking-tight">
            {siteSettings.companyName}
          </span>
        </div>
        <p class="text-xs text-slate-400 leading-relaxed max-w-sm mb-6">
          Regional holding corporation advancing sustainable prosperity, industrial independence, and institutional excellence across the Gulf Cooperation Council.
        </p>
        <div class="text-xs text-slate-500">
          Regional Offices: {siteSettings.regionalOffices.join(" • ")}
        </div>
      </div>

      <!-- Quick Links -->
      <div class="md:col-span-3">
        <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-4 font-heading">
          Navigation
        </h4>
        <ul class="space-y-2 text-xs">
          {navigationMenu.map((item) => (
            <li>
              <a href={item.href} class="hover:text-amber-400 transition-colors">
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>

      <!-- Compliance & Governance -->
      <div class="md:col-span-4">
        <h4 class="text-xs font-bold text-white uppercase tracking-wider mb-4 font-heading">
          Governance & Standards
        </h4>
        <p class="text-xs text-slate-400 leading-relaxed mb-4">
          All investments and operational mandates adhere to strict sovereign regulatory compliances, CMA guidelines, and ESG disclosure standards.
        </p>
        <div class="inline-flex items-center px-3 py-1.5 rounded bg-slate-900 border border-slate-800 text-[11px] text-amber-400">
          ISO 9001:2015 & ISO 14001 Certified
        </div>
      </div>

    </div>

    <div class="pt-8 border-t border-slate-900 text-xs text-slate-600 flex flex-col sm:flex-row items-center justify-between">
      <div>
        &copy; {new Date().getFullYear()} {siteSettings.companyName}. All Rights Reserved.
      </div>
      <div class="flex space-x-6 mt-4 sm:mt-0">
        <a href="#about" class="hover:text-slate-400 transition-colors">Privacy Charter</a>
        <a href="#about" class="hover:text-slate-400 transition-colors">Terms of Investment</a>
        <a href="#contact" class="hover:text-slate-400 transition-colors">Security Disclosures</a>
      </div>
    </div>

  </div>
</footer>
"""
        return AstroComponentCode(
            filename="Footer.astro",
            path="src/components/Footer.astro",
            content=content,
            description="Comprehensive corporate footer with quick links and governance disclaimers."
        )

    def _generate_index_page(self) -> AstroComponentCode:
        content = """---
// src/pages/index.astro
// Main Composition Page - Assembles all modular components cleanly into MainLayout.
import MainLayout from '../layouts/MainLayout.astro';
import Header from '../components/Header.astro';
import Hero from '../components/Hero.astro';
import About from '../components/About.astro';
import Sectors from '../components/Sectors.astro';
import Stats from '../components/Stats.astro';
import Projects from '../components/Projects.astro';
import Contact from '../components/Contact.astro';
import Footer from '../components/Footer.astro';
---

<MainLayout title="RDGCC | Regional Development & Strategic GCC Investment Holding">
  <Header />
  <main id="main-content">
    <Hero />
    <About />
    <Sectors />
    <Stats />
    <Projects />
    <Contact />
  </main>
  <Footer />
</MainLayout>
"""
        return AstroComponentCode(
            filename="index.astro",
            path="src/pages/index.astro",
            content=content,
            description="Master index page importing and assembling modular sections."
        )
