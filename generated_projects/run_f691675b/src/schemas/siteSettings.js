export default {
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
