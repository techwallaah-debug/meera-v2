import React from 'react';
import {View, StyleSheet, ActivityIndicator} from 'react-native';
import {useTheme} from 'react-native-paper';

interface LoadingSpinnerProps {
  size?: 'small' | 'large';
  fullScreen?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'large',
  fullScreen = false,
}) => {
  const theme = useTheme();

  return (
    <View style={fullScreen ? styles.fullScreen : styles.container}>
      <ActivityIndicator size={size} color={theme.colors.primary} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  fullScreen: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ffffff',
  },
});

export default LoadingSpinner;
