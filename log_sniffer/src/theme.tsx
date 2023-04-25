import { extendTheme } from '@mui/joy/styles';

declare module '@mui/joy/styles' {
  interface PaletteBackground {
    appBody: string;
    componentBg: string;
  }
}

export default extendTheme({
  colorSchemes: {
    light: {
      palette: {
        background: {
          appBody: 'var(--joy-palette-neutral-100)',
          componentBg: 'var(--joy-palette-neutral-50)',
        },
      },
    },
    dark: {
      palette: {
        background: {
          appBody: 'var(--joy-palette-common-black)',
          componentBg: 'var(--joy-palette-neutral-900)',
        },
      },
    },
  },
  fontFamily: {
    display: "'Roboto Flex', var(--joy-fontFamily-fallback)",
    body: "'Roboto Flex', var(--joy-fontFamily-fallback)",
  },
});
