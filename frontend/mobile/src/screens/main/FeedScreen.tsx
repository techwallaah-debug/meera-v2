import React, {useEffect, useState} from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  RefreshControl,
  Image,
  TouchableOpacity,
} from 'react-native';
import {Text, Card, Avatar, IconButton, useTheme, ActivityIndicator} from 'react-native-paper';
import {useQuery} from '@tanstack/react-query';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';
import {formatDistanceToNow} from 'date-fns';

interface Post {
  id: number;
  user_id: number;
  caption?: string;
  media_urls: string[];
  like_count: number;
  comment_count: number;
  created_at: string;
}

const FeedScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const [refreshing, setRefreshing] = useState(false);

  const {
    data: posts,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ['feed'],
    queryFn: () => apiService.getFeed(0, 20),
  });

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  const handleLike = async (postId: number) => {
    try {
      await apiService.likePost(postId);
      refetch();
    } catch (error) {
      console.error('Like error:', error);
    }
  };

  const renderPost = ({item}: {item: Post}) => (
    <Card style={styles.postCard} mode="elevated">
      <Card.Content>
        <View style={styles.postHeader}>
          <Avatar.Text size={40} label="U" />
          <View style={styles.postHeaderText}>
            <Text variant="titleMedium" style={styles.username}>
              User {item.user_id}
            </Text>
            <Text variant="bodySmall" style={styles.timestamp}>
              {formatDistanceToNow(new Date(item.created_at), {addSuffix: true})}
            </Text>
          </View>
        </View>

        {item.caption ? (
          <Text variant="bodyMedium" style={styles.caption}>
            {item.caption}
          </Text>
        ) : null}

        {item.media_urls.length > 0 ? (
          <View style={styles.mediaContainer}>
            <Image
              source={{uri: item.media_urls[0]}}
              style={styles.mediaImage}
              resizeMode="cover"
            />
          </View>
        ) : null}

        <View style={styles.postActions}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => handleLike(item.id)}>
            <IconButton icon="heart-outline" size={24} />
            <Text variant="bodySmall">{item.like_count}</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionButton}>
            <IconButton icon="comment-outline" size={24} />
            <Text variant="bodySmall">{item.comment_count}</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionButton}>
            <IconButton icon="share-outline" size={24} />
          </TouchableOpacity>
        </View>
      </Card.Content>
    </Card>
  );

  if (isLoading && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={posts || []}
        renderItem={renderPost}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text variant="bodyLarge" style={styles.emptyText}>
              No posts yet. Start following people to see their posts!
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContent: {
    padding: spacing.md,
  },
  postCard: {
    marginBottom: spacing.md,
    borderRadius: borderRadius.lg,
  },
  postHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  postHeaderText: {
    marginLeft: spacing.md,
    flex: 1,
  },
  username: {
    fontWeight: '600',
  },
  timestamp: {
    color: '#6b7280',
  },
  caption: {
    marginBottom: spacing.md,
  },
  mediaContainer: {
    marginBottom: spacing.md,
    borderRadius: borderRadius.md,
    overflow: 'hidden',
  },
  mediaImage: {
    width: '100%',
    height: 300,
    backgroundColor: '#e5e7eb',
  },
  postActions: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: spacing.sm,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: spacing.lg,
  },
  emptyContainer: {
    padding: spacing.xl,
    alignItems: 'center',
  },
  emptyText: {
    color: '#6b7280',
    textAlign: 'center',
  },
});

export default FeedScreen;
