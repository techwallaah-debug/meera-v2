import React, {useState} from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Image,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Surface,
  useTheme,
  ActivityIndicator,
} from 'react-native-paper';
import {useAuthStore} from '../../store/authStore';
import {spacing, borderRadius} from '../../utils/theme';

const LoginScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const {login, isLoading} = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    try {
      setError('');
      await login(email, password);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled">
        <View style={styles.header}>
          <Text variant="displaySmall" style={styles.title}>
            Welcome Back
          </Text>
          <Text variant="bodyMedium" style={styles.subtitle}>
            Sign in to continue
          </Text>
        </View>

        <Surface style={styles.formContainer} elevation={1}>
          {error ? (
            <Surface style={styles.errorContainer} elevation={0}>
              <Text style={styles.errorText}>{error}</Text>
            </Surface>
          ) : null}

          <TextInput
            label="Email"
            value={email}
            onChangeText={setEmail}
            mode="outlined"
            keyboardType="email-address"
            autoCapitalize="none"
            style={styles.input}
            left={<TextInput.Icon icon="email" />}
          />

          <TextInput
            label="Password"
            value={password}
            onChangeText={setPassword}
            mode="outlined"
            secureTextEntry
            style={styles.input}
            left={<TextInput.Icon icon="lock" />}
          />

          <Button
            mode="text"
            onPress={() => navigation.navigate('ForgotPassword')}
            style={styles.forgotButton}>
            Forgot Password?
          </Button>

          <Button
            mode="contained"
            onPress={handleLogin}
            style={styles.loginButton}
            loading={isLoading}
            disabled={isLoading}>
            Sign In
          </Button>

          <View style={styles.registerContainer}>
            <Text variant="bodyMedium">Don't have an account? </Text>
            <Button
              mode="text"
              onPress={() => navigation.navigate('Register')}
              compact>
              Sign Up
            </Button>
          </View>
        </Surface>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xl,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: spacing.sm,
  },
  subtitle: {
    color: '#6b7280',
  },
  formContainer: {
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    backgroundColor: '#ffffff',
  },
  input: {
    marginBottom: spacing.md,
  },
  forgotButton: {
    alignSelf: 'flex-end',
    marginBottom: spacing.md,
  },
  loginButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: spacing.lg,
  },
  errorContainer: {
    backgroundColor: '#fee2e2',
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.md,
  },
  errorText: {
    color: '#dc2626',
    textAlign: 'center',
  },
});

export default LoginScreen;
