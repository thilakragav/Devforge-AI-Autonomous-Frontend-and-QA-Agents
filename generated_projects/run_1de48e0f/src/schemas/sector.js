export default {
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
