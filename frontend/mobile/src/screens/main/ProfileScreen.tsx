import React from 'react';
import {View, StyleSheet, ScrollView, TouchableOpacity} from 'react-native';
import {
  Text,
  Avatar,
  Card,
  List,
  Divider,
  useTheme,
  Button,
} from 'react-native-paper';
import {useAuthStore} from '../../store/authStore';
import {spacing, borderRadius} from '../../utils/theme';

const ProfileScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const {user, logout} = useAuthStore();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.profileCard} mode="elevated">
        <Card.Content style={styles.profileContent}>
          <Avatar.Text
            size={80}
            label={user?.full_name?.[0]?.toUpperCase() || 'U'}
            style={styles.avatar}
          />
          <Text variant="headlineSmall" style={styles.name}>
            {user?.full_name || 'User'}
          </Text>
          <Text variant="bodyMedium" style={styles.username}>
            @{user?.username}
          </Text>
          {user?.bio ? (
            <Text variant="bodyMedium" style={styles.bio}>
              {user.bio}
            </Text>
          ) : null}

          <View style={styles.statsContainer}>
            <View style={styles.stat}>
              <Text variant="titleLarge">0</Text>
              <Text variant="bodySmall">Posts</Text>
            </View>
            <View style={styles.stat}>
              <Text variant="titleLarge">0</Text>
              <Text variant="bodySmall">Followers</Text>
            </View>
            <View style={styles.stat}>
              <Text variant="titleLarge">0</Text>
              <Text variant="bodySmall">Following</Text>
            </View>
          </View>

          <View style={styles.buttonContainer}>
            <Button
              mode="outlined"
              onPress={() => navigation.navigate('EditProfile')}
              style={styles.editButton}>
              Edit Profile
            </Button>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.menuCard} mode="elevated">
        <List.Item
          title="Settings"
          left={props => <List.Icon {...props} icon="cog" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => navigation.navigate('Settings')}
        />
        <Divider />
        <List.Item
          title="My Orders"
          left={props => <List.Icon {...props} icon="package-variant" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
          onPress={() => navigation.navigate('Cart')}
        />
        <Divider />
        <List.Item
          title="Help & Support"
          left={props => <List.Icon {...props} icon="help-circle" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
        <Divider />
        <List.Item
          title="About"
          left={props => <List.Icon {...props} icon="information" />}
          right={props => <List.Icon {...props} icon="chevron-right" />}
        />
      </Card>

      <Button
        mode="text"
        onPress={handleLogout}
        textColor={theme.colors.error}
        style={styles.logoutButton}>
        Logout
      </Button>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  profileCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
  },
  profileContent: {
    alignItems: 'center',
    paddingVertical: spacing.lg,
  },
  avatar: {
    marginBottom: spacing.md,
  },
  name: {
    fontWeight: 'bold',
    marginBottom: spacing.xs,
  },
  username: {
    color: '#6b7280',
    marginBottom: spacing.sm,
  },
  bio: {
    textAlign: 'center',
    marginTop: spacing.md,
    marginBottom: spacing.lg,
    paddingHorizontal: spacing.md,
  },
  statsContainer: {
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-around',
    marginTop: spacing.md,
    paddingTop: spacing.md,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  stat: {
    alignItems: 'center',
  },
  buttonContainer: {
    width: '100%',
    marginTop: spacing.md,
  },
  editButton: {
    marginHorizontal: spacing.md,
  },
  menuCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
  },
  logoutButton: {
    margin: spacing.md,
  },
});

export default ProfileScreen;
