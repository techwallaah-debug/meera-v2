import React, {useEffect, useState} from 'react';
import {View, StyleSheet, ScrollView, TouchableOpacity, Image, ActivityIndicator} from 'react-native';
import {
  Text,
  Card,
  Button,
  IconButton,
  useTheme,
  Divider,
} from 'react-native-paper';
import {useQuery} from '@tanstack/react-query';
import {useCartStore, CartItem} from '../../store/cartStore';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';

const CartScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const {
    items,
    isLoading,
    loadCart,
    updateQuantity,
    removeFromCart,
    getTotal,
  } = useCartStore();

  useEffect(() => {
    loadCart();
  }, []);

  // Fetch product details for cart items
  const {data: productsData} = useQuery({
    queryKey: ['cart-products', items.map(i => i.product_id)],
    queryFn: async () => {
      const productPromises = items.map(item =>
        apiService.getProduct(item.product_id).catch(() => null)
      );
      return Promise.all(productPromises);
    },
    enabled: items.length > 0,
  });

  // Merge cart items with product data
  const cartItemsWithDetails: (CartItem & {title?: string; price?: number; image?: string})[] =
    items.map(item => {
      const product = productsData?.find(p => p?.id === item.product_id);
      return {
        ...item,
        title: product?.title,
        price: product?.price,
        image: product?.image_urls?.[0],
      };
    });

  const subtotal = getTotal();
  const shipping = 50;
  const total = subtotal + shipping;

  const handleUpdateQuantity = async (itemId: number, newQuantity: number) => {
    try {
      await updateQuantity(itemId, newQuantity);
    } catch (error) {
      console.error('Failed to update quantity:', error);
    }
  };

  const handleRemove = async (itemId: number) => {
    try {
      await removeFromCart(itemId);
    } catch (error) {
      console.error('Failed to remove item:', error);
    }
  };

  const renderCartItem = (item: typeof cartItemsWithDetails[0]) => (
    <Card key={item.id} style={styles.cartItem} mode="elevated">
      <Card.Content style={styles.cartItemContent}>
        <View style={styles.cartItemImage}>
          {item.image ? (
            <Image source={{uri: item.image}} style={styles.productImage} />
          ) : (
            <View style={styles.imagePlaceholder} />
          )}
        </View>
        <View style={styles.cartItemInfo}>
          <Text variant="titleMedium" numberOfLines={2}>
            {item.title || `Product ${item.product_id}`}
          </Text>
          <Text variant="titleMedium" style={styles.itemPrice}>
            ₹{item.price || 0}
          </Text>
          <View style={styles.quantityContainer}>
            <IconButton
              icon="minus"
              size={20}
              onPress={() => handleUpdateQuantity(item.id, item.quantity - 1)}
            />
            <Text variant="bodyLarge">{item.quantity}</Text>
            <IconButton
              icon="plus"
              size={20}
              onPress={() => handleUpdateQuantity(item.id, item.quantity + 1)}
            />
          </View>
        </View>
        <IconButton
          icon="delete-outline"
          size={24}
          onPress={() => handleRemove(item.id)}
        />
      </Card.Content>
    </Card>
  );

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {cartItemsWithDetails.length === 0 ? (
          <View style={styles.emptyContainer}>
            <IconButton icon="cart-off" size={64} />
            <Text variant="headlineSmall" style={styles.emptyText}>
              Your cart is empty
            </Text>
            <Text variant="bodyMedium" style={styles.emptySubtext}>
              Add items to your cart to get started
            </Text>
            <Button
              mode="contained"
              onPress={() => navigation.navigate('Search')}
              style={styles.shopButton}>
              Start Shopping
            </Button>
          </View>
        ) : (
          <>
            {cartItemsWithDetails.map(renderCartItem)}

            <Card style={styles.summaryCard} mode="elevated">
              <Card.Content>
                <View style={styles.summaryRow}>
                  <Text variant="bodyLarge">Subtotal</Text>
                  <Text variant="bodyLarge">₹{subtotal.toFixed(2)}</Text>
                </View>
                <View style={styles.summaryRow}>
                  <Text variant="bodyLarge">Shipping</Text>
                  <Text variant="bodyLarge">₹{shipping.toFixed(2)}</Text>
                </View>
                <Divider style={styles.summaryDivider} />
                <View style={styles.summaryRow}>
                  <Text variant="titleLarge" style={styles.totalLabel}>
                    Total
                  </Text>
                  <Text variant="titleLarge" style={styles.totalAmount}>
                    ₹{total.toFixed(2)}
                  </Text>
                </View>
              </Card.Content>
            </Card>
          </>
        )}
      </ScrollView>

      {cartItemsWithDetails.length > 0 && (
        <View style={styles.checkoutContainer}>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('Checkout')}
            style={styles.checkoutButton}>
            Proceed to Checkout
          </Button>
        </View>
      )}
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
  scrollContent: {
    padding: spacing.md,
    paddingBottom: 100,
  },
  productImage: {
    width: '100%',
    height: '100%',
    borderRadius: borderRadius.md,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xl,
  },
  emptyText: {
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  emptySubtext: {
    color: '#6b7280',
    marginBottom: spacing.lg,
    textAlign: 'center',
  },
  shopButton: {
    marginTop: spacing.md,
  },
  cartItem: {
    marginBottom: spacing.md,
    borderRadius: borderRadius.lg,
  },
  cartItemContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  cartItemImage: {
    width: 80,
    height: 80,
    marginRight: spacing.md,
  },
  imagePlaceholder: {
    width: '100%',
    height: '100%',
    backgroundColor: '#e5e7eb',
    borderRadius: borderRadius.md,
  },
  cartItemInfo: {
    flex: 1,
  },
  itemPrice: {
    color: '#10b981',
    fontWeight: 'bold',
    marginVertical: spacing.xs,
  },
  quantityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: spacing.xs,
  },
  summaryCard: {
    marginTop: spacing.md,
    borderRadius: borderRadius.lg,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  summaryDivider: {
    marginVertical: spacing.md,
  },
  totalLabel: {
    fontWeight: 'bold',
  },
  totalAmount: {
    fontWeight: 'bold',
    color: '#10b981',
  },
  checkoutContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#ffffff',
    padding: spacing.md,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
    elevation: 8,
  },
  checkoutButton: {
    paddingVertical: spacing.xs,
  },
});

export default CartScreen;
