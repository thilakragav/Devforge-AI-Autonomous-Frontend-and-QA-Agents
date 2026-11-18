export default {
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
