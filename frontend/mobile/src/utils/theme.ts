import {MD3LightTheme} from 'react-native-paper';

export const theme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: '#6366f1', // Indigo
    secondary: '#ec4899', // Pink
    tertiary: '#10b981', // Green
    error: '#ef4444',
    background: '#ffffff',
    surface: '#f9fafb',
    text: '#111827',
    onPrimary: '#ffffff',
    onSecondary: '#ffffff',
    onSurface: '#111827',
    onBackground: '#111827',
    outline: '#e5e7eb',
    surfaceVariant: '#f3f4f6',
  },
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  round: 9999,
};
