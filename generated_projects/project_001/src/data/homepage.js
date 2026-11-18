// src/data/homepage.js
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
