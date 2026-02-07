import React, {useState} from 'react';
import {View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView} from 'react-native';
import {TextInput, Button, Text, Surface, useTheme} from 'react-native-paper';
import {spacing, borderRadius} from '../../utils/theme';

const ForgotPasswordScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleReset = async () => {
    if (!email) {
      setMessage('Please enter your email');
      return;
    }

    setIsLoading(true);
    // TODO: Implement password reset API call
    setTimeout(() => {
      setIsLoading(false);
      setMessage('Password reset link sent to your email');
    }, 2000);
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
            Forgot Password?
          </Text>
          <Text variant="bodyMedium" style={styles.subtitle}>
            Enter your email and we'll send you a reset link
          </Text>
        </View>

        <Surface style={styles.formContainer} elevation={1}>
          {message ? (
            <Surface
              style={[
                styles.messageContainer,
                message.includes('sent') ? styles.successContainer : styles.errorContainer,
              ]}
              elevation={0}>
              <Text style={styles.messageText}>{message}</Text>
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

          <Button
            mode="contained"
            onPress={handleReset}
            style={styles.resetButton}
            loading={isLoading}
            disabled={isLoading}>
            Send Reset Link
          </Button>

          <Button
            mode="text"
            onPress={() => navigation.goBack()}
            style={styles.backButton}>
            Back to Login
          </Button>
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
    textAlign: 'center',
  },
  formContainer: {
    padding: spacing.lg,
    borderRadius: borderRadius.lg,
    backgroundColor: '#ffffff',
  },
  input: {
    marginBottom: spacing.md,
  },
  resetButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
  backButton: {
    marginTop: spacing.md,
  },
  messageContainer: {
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginBottom: spacing.md,
  },
  successContainer: {
    backgroundColor: '#d1fae5',
  },
  errorContainer: {
    backgroundColor: '#fee2e2',
  },
  messageText: {
    textAlign: 'center',
  },
});

export default ForgotPasswordScreen;
