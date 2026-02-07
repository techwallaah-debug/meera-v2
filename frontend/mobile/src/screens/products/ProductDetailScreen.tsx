import React, {useState} from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Image,
  Dimensions,
  TouchableOpacity,
} from 'react-native';
import {
  Text,
  Button,
  Card,
  Chip,
  Divider,
  useTheme,
  ActivityIndicator,
  IconButton,
} from 'react-native-paper';
import {useQuery} from '@tanstack/react-query';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';

const {width} = Dimensions.get('window');

const ProductDetailScreen: React.FC = ({navigation, route}: any) => {
  const theme = useTheme();
  const {productId} = route.params;
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);

  const {
    data: product,
    isLoading,
  } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => apiService.getProduct(productId),
  });

  const {
    data: reviews,
  } = useQuery({
    queryKey: ['reviews', productId],
    queryFn: () => apiService.getReviews(productId),
  });

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  if (!product) {
    return (
      <View style={styles.emptyContainer}>
        <Text>Product not found</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Image Gallery */}
      <View style={styles.imageContainer}>
        <Image
          source={{
            uri: product.image_urls?.[selectedImageIndex] || 'https://via.placeholder.com/400',
          }}
          style={styles.mainImage}
          resizeMode="cover"
        />
        {product.image_urls?.length > 1 && (
          <ScrollView
            horizontal
            style={styles.thumbnailContainer}
            showsHorizontalScrollIndicator={false}>
            {product.image_urls.map((url: string, index: number) => (
              <TouchableOpacity
                key={index}
                onPress={() => setSelectedImageIndex(index)}>
                <Image
                  source={{uri: url}}
                  style={[
                    styles.thumbnail,
                    selectedImageIndex === index && styles.selectedThumbnail,
                  ]}
                />
              </TouchableOpacity>
            ))}
          </ScrollView>
        )}
      </View>

      {/* Product Info */}
      <Card style={styles.infoCard} mode="elevated">
        <Card.Content>
          <Text variant="headlineSmall" style={styles.title}>
            {product.title}
          </Text>

          <View style={styles.priceRow}>
            <Text variant="displaySmall" style={styles.price}>
              ₹{product.price}
            </Text>
            {product.discount_price && (
              <Text variant="titleMedium" style={styles.originalPrice}>
                ₹{product.discount_price}
              </Text>
            )}
          </View>

          {product.rating > 0 && (
            <View style={styles.ratingRow}>
              <Text variant="titleMedium">⭐ {product.rating.toFixed(1)}</Text>
              <Text variant="bodyMedium" style={styles.reviewCount}>
                ({product.review_count} reviews)
              </Text>
            </View>
          )}

          <Chip style={styles.categoryChip} mode="outlined">
            {product.category}
          </Chip>

          <Divider style={styles.divider} />

          <Text variant="titleMedium" style={styles.sectionTitle}>
            Description
          </Text>
          <Text variant="bodyMedium" style={styles.description}>
            {product.description || 'No description available'}
          </Text>

          <View style={styles.stockContainer}>
            <Text variant="bodyMedium">
              Stock: {product.stock_quantity > 0 ? 'In Stock' : 'Out of Stock'}
            </Text>
          </View>
        </Card.Content>
      </Card>

      {/* Reviews */}
      {reviews && reviews.length > 0 && (
        <Card style={styles.reviewsCard} mode="elevated">
          <Card.Content>
            <Text variant="titleMedium" style={styles.sectionTitle}>
              Reviews ({reviews.length})
            </Text>
            {reviews.slice(0, 3).map((review: any) => (
              <View key={review.id} style={styles.reviewItem}>
                <View style={styles.reviewHeader}>
                  <Text variant="bodyLarge" style={styles.reviewerName}>
                    User {review.user_id}
                  </Text>
                  <Text variant="bodySmall">⭐ {review.rating}/5</Text>
                </View>
                {review.title && (
                  <Text variant="bodyMedium" style={styles.reviewTitle}>
                    {review.title}
                  </Text>
                )}
                {review.content && (
                  <Text variant="bodySmall" style={styles.reviewContent}>
                    {review.content}
                  </Text>
                )}
                <Divider style={styles.reviewDivider} />
              </View>
            ))}
          </Card.Content>
        </Card>
      )}

      {/* Add to Cart Button */}
      <View style={styles.buttonContainer}>
        <Button
          mode="contained"
          onPress={async () => {
            try {
              const {useCartStore} = await import('../../store/cartStore');
              const cartStore = useCartStore.getState();
              await cartStore.addToCart(product.id, 1);
              navigation.navigate('Cart');
            } catch (error) {
              console.error('Failed to add to cart:', error);
            }
          }}
          style={styles.addToCartButton}
          disabled={product.stock_quantity === 0}>
          {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
        </Button>
      </View>
    </ScrollView>
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
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageContainer: {
    backgroundColor: '#ffffff',
  },
  mainImage: {
    width: width,
    height: width,
    backgroundColor: '#e5e7eb',
  },
  thumbnailContainer: {
    padding: spacing.md,
  },
  thumbnail: {
    width: 60,
    height: 60,
    borderRadius: borderRadius.sm,
    marginRight: spacing.sm,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedThumbnail: {
    borderColor: '#6366f1',
  },
  infoCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: spacing.sm,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  price: {
    fontWeight: 'bold',
    color: '#10b981',
    marginRight: spacing.md,
  },
  originalPrice: {
    textDecorationLine: 'line-through',
    color: '#6b7280',
  },
  ratingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  reviewCount: {
    color: '#6b7280',
    marginLeft: spacing.sm,
  },
  categoryChip: {
    alignSelf: 'flex-start',
    marginBottom: spacing.md,
  },
  divider: {
    marginVertical: spacing.md,
  },
  sectionTitle: {
    fontWeight: '600',
    marginBottom: spacing.sm,
  },
  description: {
    color: '#4b5563',
    lineHeight: 22,
  },
  stockContainer: {
    marginTop: spacing.md,
  },
  reviewsCard: {
    margin: spacing.md,
    borderRadius: borderRadius.lg,
  },
  reviewItem: {
    marginBottom: spacing.md,
  },
  reviewHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.xs,
  },
  reviewerName: {
    fontWeight: '600',
  },
  reviewTitle: {
    fontWeight: '500',
    marginBottom: spacing.xs,
  },
  reviewContent: {
    color: '#4b5563',
  },
  reviewDivider: {
    marginTop: spacing.md,
  },
  buttonContainer: {
    padding: spacing.md,
  },
  addToCartButton: {
    paddingVertical: spacing.xs,
  },
});

export default ProductDetailScreen;
