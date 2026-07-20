import { defineMermaidSetup } from '@slidev/types'

// Dark mermaid tuned to the deck palette (navy bg, yellow accent) so diagrams
// read on the dark slides instead of dropping light boxes onto navy.
export default defineMermaidSetup(() => ({
  theme: 'dark',
  themeVariables: {
    background: '#050F2B',
    primaryColor: '#0A1740',
    primaryBorderColor: '#FFEA00',
    primaryTextColor: '#FFFFFF',
    secondaryColor: '#0D1F4A',
    tertiaryColor: '#01081B',
    lineColor: '#FFEA00',
    clusterBkg: 'rgba(255,255,255,0.04)',
    clusterBorder: 'rgba(255,234,0,0.45)',
  },
}))
