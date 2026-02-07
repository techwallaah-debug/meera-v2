import React from 'react';
import {View, StyleSheet, FlatList} from 'react-native';
import {Text, Card, Avatar, useTheme} from 'react-native-paper';
import {spacing, borderRadius} from '../../utils/theme';

const NotificationsScreen: React.FC = () => {
  const theme = useTheme();
  // TODO: Implement notifications API
  const notifications: any[] = [];

  const renderNotification = ({item}: {item: any}) => (
    <Card style={styles.notificationCard} mode="elevated">
      <Card.Content style={styles.notificationContent}>
        <Avatar.Text size={40} label="U" />
        <View style={styles.notificationText}>
          <Text variant="bodyMedium">{item.message || 'New notification'}</Text>
          <Text variant="bodySmall" style={styles.timestamp}>
            {item.time || 'Just now'}
          </Text>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={notifications}
        renderItem={renderNotification}
        keyExtractor={(item, index) => index.toString()}
        contentContainerStyle={styles.listContent}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text variant="bodyLarge" style={styles.emptyText}>
              No notifications yet
            </Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  listContent: {
    padding: spacing.md,
  },
  notificationCard: {
    marginBottom: spacing.md,
    borderRadius: borderRadius.lg,
  },
  notificationContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  notificationText: {
    marginLeft: spacing.md,
    flex: 1,
  },
  timestamp: {
    color: '#6b7280',
    marginTop: spacing.xs,
  },
  emptyContainer: {
    padding: spacing.xl,
    alignItems: 'center',
  },
  emptyText: {
    color: '#6b7280',
  },
});

export default NotificationsScreen;
