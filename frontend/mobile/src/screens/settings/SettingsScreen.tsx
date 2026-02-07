import React from 'react';
import {View, StyleSheet, ScrollView} from 'react-native';
import {List, Divider, Switch, Card, useTheme} from 'react-native-paper';
import {useAuthStore} from '../../store/authStore';
import {spacing, borderRadius} from '../../utils/theme';

const SettingsScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const [notificationsEnabled, setNotificationsEnabled] = React.useState(true);
  const [emailNotifications, setEmailNotifications] = React.useState(true);

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card} mode="elevated">
        <List.Item
          title="Edit Profile"
          description="Update your personal information"
          left={props => <List.Icon {...props} icon="account-edit" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => navigation.navigate('EditProfile')}
        />
        <Divider />
        <List.Item
          title="Account Settings"
          description="Manage your account"
          left={props => <List.Icon {...props} icon="account-cog" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
      </Card>

      <Card style={styles.card} mode="elevated">
        <List.Item
          title="Notifications"
          description="Push notifications"
          left={props => <List.Icon {...props} icon="bell" />}
          right={() => (
            <Switch
              value={notificationsEnabled}
              onValueChange={setNotificationsEnabled}
            />
          )}
        />
        <Divider />
        <List.Item
          title="Email Notifications"
          description="Receive updates via email"
          left={props => <List.Icon {...props} icon="email" />}
          right={() => (
            <Switch
              value={emailNotifications}
              onValueChange={setEmailNotifications}
            />
          )}
        />
      </Card>

      <Card style={styles.card} mode="elevated">
        <List.Item
          title="Privacy"
          description="Manage your privacy settings"
          left={props => <List.Icon {...props} icon="lock" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
        <Divider />
        <List.Item
          title="Security"
          description="Password and security"
          left={props => <List.Icon {...props} icon="shield-check" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
      </Card>

      <Card style={styles.card} mode="elevated">
        <List.Item
          title="Help & Support"
          description="Get help and contact support"
          left={props => <List.Icon {...props} icon="help-circle" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
        <Divider />
        <List.Item
          title="About"
          description="App version and information"
          left={props => <List.Icon {...props} icon="information" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
        <Divider />
        <List.Item
          title="Terms & Conditions"
          left={props => <List.Icon {...props} icon="file-document" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
        <Divider />
        <List.Item
          title="Privacy Policy"
          left={props => <List.Icon {...props} icon="shield-lock" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  card: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
  },
});

export default SettingsScreen;
