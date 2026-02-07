import React, {useState} from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Surface,
  Checkbox,
  useTheme,
} from 'react-native-paper';
import {useAuthStore} from '../../store/authStore';
import {spacing, borderRadius} from '../../utils/theme';

const RegisterScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const {register, isLoading} = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    password: '',
    confirmPassword: '',
    is_creator: false,
  });
  const [error, setError] = useState('');

  const handleRegister = async () => {
    if (
      !formData.email ||
      !formData.username ||
      !formData.full_name ||
      !formData.password
    ) {
      setError('Please fill in all fields');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    try {
      setError('');
      await register({
        email: formData.email,
        username: formData.username,
        full_name: formData.full_name,
        password: formData.password,
        is_creator: formData.is_creator,
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
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
            Create Account
          </Text>
          <Text variant="bodyMedium" style={styles.subtitle}>
            Join our community
          </Text>
        </View>

        <Surface style={styles.formContainer} elevation={1}>
          {error ? (
            <Surface style={styles.errorContainer} elevation={0}>
              <Text style={styles.errorText}>{error}</Text>
            </Surface>
          ) : null}

          <TextInput
            label="Full Name"
            value={formData.full_name}
            onChangeText={text => setFormData({...formData, full_name: text})}
            mode="outlined"
            style={styles.input}
            left={<TextInput.Icon icon="account" />}
          />

          <TextInput
            label="Username"
            value={formData.username}
            onChangeText={text => setFormData({...formData, username: text})}
            mode="outlined"
            autoCapitalize="none"
            style={styles.input}
            left={<TextInput.Icon icon="account-circle" />}
          />

          <TextInput
            label="Email"
            value={formData.email}
            onChangeText={text => setFormData({...formData, email: text})}
            mode="outlined"
            keyboardType="email-address"
            autoCapitalize="none"
            style={styles.input}
            left={<TextInput.Icon icon="email" />}
          />

          <TextInput
            label="Password"
            value={formData.password}
            onChangeText={text => setFormData({...formData, password: text})}
            mode="outlined"
            secureTextEntry
            style={styles.input}
            left={<TextInput.Icon icon="lock" />}
          />

          <TextInput
            label="Confirm Password"
            value={formData.confirmPassword}
            onChangeText={text =>
              setFormData({...formData, confirmPassword: text})
            }
            mode="outlined"
            secureTextEntry
            style={styles.input}
            left={<TextInput.Icon icon="lock-check" />}
          />

          <View style={styles.checkboxContainer}>
            <Checkbox
              status={formData.is_creator ? 'checked' : 'unchecked'}
              onPress={() =>
                setFormData({...formData, is_creator: !formData.is_creator})
              }
            />
            <Text
              variant="bodyMedium"
              onPress={() =>
                setFormData({...formData, is_creator: !formData.is_creator})
              }
              style={styles.checkboxLabel}>
              I want to be a creator/seller
            </Text>
          </View>

          <Button
            mode="contained"
            onPress={handleRegister}
            style={styles.registerButton}
            loading={isLoading}
            disabled={isLoading}>
            Sign Up
          </Button>

          <View style={styles.loginContainer}>
            <Text variant="bodyMedium">Already have an account? </Text>
            <Button
              mode="text"
              onPress={() => navigation.navigate('Login')}
              compact>
              Sign In
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
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  checkboxLabel: {
    flex: 1,
    marginLeft: spacing.sm,
  },
  registerButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
  loginContainer: {
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

export default RegisterScreen;
