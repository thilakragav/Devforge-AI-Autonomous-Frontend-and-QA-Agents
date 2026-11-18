"""
Sanity Schemas Generator - Content and Presentation Separation
Generates Sanity-ready schema definitions for CMS readiness.
"""
from typing import List
from backend.schemas.agent1_schema import SanitySchemaDefinition


def generate_sanity_schemas() -> List[SanitySchemaDefinition]:
    """
    Returns Sanity Studio-compatible schema definitions.
    Enables instant decoupling of editorial content from Astro frontend presentation.
    """
    homepage_schema = """export default {
  name: 'homepage',
  title: 'Homepage Content',
  type: 'document',
  fields: [
    {
      name: 'hero',
      title: 'Hero Section',
      type: 'object',
      fields: [
        { name: 'tagline', title: 'Badge Tagline', type: 'string' },
        { name: 'headline', title: 'Main Headline', type: 'string' },
        { name: 'subheadline', title: 'Subheadline', type: 'text' },
        { name: 'primaryCta', title: 'Primary CTA Label', type: 'string' },
        { name: 'secondaryCta', title: 'Secondary CTA Label', type: 'string' }
      ]
    },
    {
      name: 'about',
      title: 'About Section',
      type: 'object',
      fields: [
        { name: 'badge', title: 'Section Badge', type: 'string' },
        { name: 'title', title: 'Section Title', type: 'string' },
        { name: 'paragraphOne', title: 'Strategic Narrative', type: 'text' },
        { name: 'paragraphTwo', title: 'Operational Overview', type: 'text' },
        { name: 'keyPillars', title: 'Strategic Pillars', type: 'array', of: [{ type: 'string' }] }
      ]
    },
    {
      name: 'stats',
      title: 'Key Performance Indicators',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'value', title: 'Metric Value', type: 'string' },
            { name: 'label', title: 'Metric Label', type: 'string' },
            { name: 'description', title: 'Brief Detail', type: 'string' }
          ]
        }
      ]
    }
  ]
};
"""

    sector_schema = """export default {
  name: 'sector',
  title: 'Strategic Business Sector',
  type: 'document',
  fields: [
    { name: 'id', title: 'Sector ID', type: 'string' },
    { name: 'title', title: 'Sector Title', type: 'string' },
    { name: 'description', title: 'Overview', type: 'text' },
    { name: 'icon', title: 'Icon Identifier', type: 'string' },
    { name: 'statsHighlight', title: 'Key Metric', type: 'string' },
    { name: 'capabilities', title: 'Core Capabilities', type: 'array', of: [{ type: 'string' }] }
  ]
};
"""

    project_schema = """export default {
  name: 'featuredProject',
  title: 'Strategic Project',
  type: 'document',
  fields: [
    { name: 'title', title: 'Project Name', type: 'string' },
    { name: 'sector', title: 'Sector Category', type: 'string' },
    { name: 'location', title: 'Regional Hub', type: 'string' },
    { name: 'year', title: 'Completion Year', type: 'string' },
    { name: 'summary', title: 'Executive Summary', type: 'text' }
  ]
};
"""

    settings_schema = """export default {
  name: 'siteSettings',
  title: 'Global Corporate Settings',
  type: 'document',
  fields: [
    { name: 'companyName', title: 'Company Name', type: 'string' },
    { name: 'logoText', title: 'Logo Text / Brand', type: 'string' },
    { name: 'languageDefault', title: 'Default Language', type: 'string' },
    {
      name: 'navigation',
      title: 'Main Navigation Menu',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'label', title: 'Menu Label', type: 'string' },
            { name: 'href', title: 'Target Anchor / URL', type: 'string' }
          ]
        }
      ]
    },
    { name: 'contactEmail', title: 'Inquiries Email', type: 'string' },
    { name: 'headquarters', title: 'Regional Headquarters', type: 'string' }
  ]
};
"""

    return [
        SanitySchemaDefinition(
            schema_name="homepage",
            title="Homepage Document Schema",
            fields=[],
            schema_code=homepage_schema
        ),
        SanitySchemaDefinition(
            schema_name="sector",
            title="Strategic Business Sector Schema",
            fields=[],
            schema_code=sector_schema
        ),
        SanitySchemaDefinition(
            schema_name="featuredProject",
            title="Featured Strategic Project Schema",
            fields=[],
            schema_code=project_schema
        ),
        SanitySchemaDefinition(
            schema_name="siteSettings",
            title="Site Settings & Global Navigation Schema",
            fields=[],
            schema_code=settings_schema
        ),
    ]
