import React from 'react';
import {View, StyleSheet, FlatList, TouchableOpacity} from 'react-native';
import {Card, Text, useTheme} from 'react-native-paper';
import {useQuery} from '@tanstack/react-query';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';

const ProductListScreen: React.FC = ({navigation, route}: any) => {
  const theme = useTheme();
  const {category, searchQuery} = route.params || {};

  const {
    data: products,
    isLoading,
  } = useQuery({
    queryKey: ['products', category, searchQuery],
    queryFn: () =>
      apiService.getProducts({
        category: category,
        q: searchQuery,
        limit: 20,
      }),
  });

  return (
    <View style={styles.container}>
      <FlatList
        data={products || []}
        numColumns={2}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={styles.productsList}
        renderItem={({item}) => (
          <TouchableOpacity
            style={styles.productCard}
            onPress={() => navigation.navigate('ProductDetail', {productId: item.id})}>
            <Card style={styles.card}>
              <Card.Cover
                source={
                  item.image_urls?.[0]
                    ? {uri: item.image_urls[0]}
                    : require('../../assets/placeholder.png')
                }
                style={styles.productImage}
              />
              <Card.Content style={styles.cardContent}>
                <Text variant="bodyMedium" numberOfLines={2} style={styles.productTitle}>
                  {item.title}
                </Text>
                <View style={styles.priceContainer}>
                  <Text variant="titleMedium" style={styles.price}>
                    ₹{item.price}
                  </Text>
                  {item.discount_price ? (
                    <Text variant="bodySmall" style={styles.originalPrice}>
                      ₹{item.discount_price}
                    </Text>
                  ) : null}
                </View>
                {item.rating > 0 ? (
                  <View style={styles.ratingContainer}>
                    <Text variant="bodySmall">⭐ {item.rating.toFixed(1)}</Text>
                    <Text variant="bodySmall" style={styles.reviewCount}>
                      ({item.review_count})
                    </Text>
                  </View>
                ) : null}
              </Card.Content>
            </Card>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text variant="bodyLarge" style={styles.emptyText}>
              No products found
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
    backgroundColor: '#ffffff',
  },
  productsList: {
    padding: spacing.md,
  },
  productCard: {
    flex: 1,
    margin: spacing.xs,
    maxWidth: '48%',
  },
  card: {
    borderRadius: borderRadius.md,
  },
  productImage: {
    height: 200,
  },
  cardContent: {
    padding: spacing.sm,
  },
  productTitle: {
    marginBottom: spacing.xs,
    fontWeight: '500',
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  price: {
    fontWeight: 'bold',
    color: '#10b981',
  },
  originalPrice: {
    textDecorationLine: 'line-through',
    color: '#6b7280',
    marginLeft: spacing.xs,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  reviewCount: {
    color: '#6b7280',
    marginLeft: spacing.xs,
  },
  emptyContainer: {
    padding: spacing.xl,
    alignItems: 'center',
  },
  emptyText: {
    color: '#6b7280',
  },
});

export default ProductListScreen;
