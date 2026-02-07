import React, {useState} from 'react';
import {View, StyleSheet, ScrollView, Alert, ActivityIndicator} from 'react-native';
import {
  Text,
  TextInput,
  Button,
  Card,
  RadioButton,
  useTheme,
  Divider,
} from 'react-native-paper';
import {useCartStore} from '../../store/cartStore';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';

const CheckoutScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const {getTotal, clearCart, items} = useCartStore();
  const [paymentMethod, setPaymentMethod] = useState<'razorpay' | 'cod'>('razorpay');
  const [isPlacingOrder, setIsPlacingOrder] = useState(false);
  const [address, setAddress] = useState({
    name: '',
    phone: '',
    street: '',
    city: '',
    state: '',
    pincode: '',
  });

  const subtotal = getTotal();
  const shipping = 50;
  const total = subtotal + shipping;

  const handlePlaceOrder = async () => {
    // Validate address
    if (!address.name || !address.phone || !address.street || !address.city || !address.pincode) {
      Alert.alert('Error', 'Please fill in all address fields');
      return;
    }

    if (items.length === 0) {
      Alert.alert('Error', 'Your cart is empty');
      return;
    }

    setIsPlacingOrder(true);
    try {
      const order = await apiService.createOrder({
        address: {
          name: address.name,
          phone: address.phone,
          street: address.street,
          city: address.city,
          state: address.state,
          pincode: address.pincode,
        },
        payment_method: paymentMethod,
      });

      // Clear cart after successful order
      await clearCart();

      if (paymentMethod === 'razorpay' && order.razorpay_order_id) {
        // TODO: Integrate Razorpay SDK for payment
        // For now, show success message
        Alert.alert('Order Created', `Order #${order.order_number} created successfully!`, [
          {
            text: 'OK',
            onPress: () => navigation.navigate('Feed'),
          },
        ]);
      } else {
        // COD order
        Alert.alert('Order Placed', `Order #${order.order_number} placed successfully!`, [
          {
            text: 'OK',
            onPress: () => navigation.navigate('Feed'),
          },
        ]);
      }
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to place order');
    } finally {
      setIsPlacingOrder(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      {/* Delivery Address */}
      <Card style={styles.card} mode="elevated">
        <Card.Content>
          <Text variant="titleLarge" style={styles.sectionTitle}>
            Delivery Address
          </Text>

          <TextInput
            label="Full Name"
            value={address.name}
            onChangeText={text => setAddress({...address, name: text})}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Phone Number"
            value={address.phone}
            onChangeText={text => setAddress({...address, phone: text})}
            mode="outlined"
            keyboardType="phone-pad"
            style={styles.input}
          />

          <TextInput
            label="Street Address"
            value={address.street}
            onChangeText={text => setAddress({...address, street: text})}
            mode="outlined"
            multiline
            style={styles.input}
          />

          <View style={styles.row}>
            <TextInput
              label="City"
              value={address.city}
              onChangeText={text => setAddress({...address, city: text})}
              mode="outlined"
              style={[styles.input, styles.halfInput]}
            />

            <TextInput
              label="State"
              value={address.state}
              onChangeText={text => setAddress({...address, state: text})}
              mode="outlined"
              style={[styles.input, styles.halfInput]}
            />
          </View>

          <TextInput
            label="Pincode"
            value={address.pincode}
            onChangeText={text => setAddress({...address, pincode: text})}
            mode="outlined"
            keyboardType="number-pad"
            style={styles.input}
          />
        </Card.Content>
      </Card>

      {/* Payment Method */}
      <Card style={styles.card} mode="elevated">
        <Card.Content>
          <Text variant="titleLarge" style={styles.sectionTitle}>
            Payment Method
          </Text>

          <RadioButton.Group
            onValueChange={value => setPaymentMethod(value)}
            value={paymentMethod}>
            <View style={styles.radioOption}>
              <RadioButton value="razorpay" />
              <Text variant="bodyLarge" style={styles.radioLabel}>
                Razorpay (UPI/Card/Net Banking)
              </Text>
            </View>
            <View style={styles.radioOption}>
              <RadioButton value="cod" />
              <Text variant="bodyLarge" style={styles.radioLabel}>
                Cash on Delivery
              </Text>
            </View>
          </RadioButton.Group>
        </Card.Content>
      </Card>

      {/* Order Summary */}
      <Card style={styles.card} mode="elevated">
        <Card.Content>
          <Text variant="titleLarge" style={styles.sectionTitle}>
            Order Summary
          </Text>

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

      <Button
        mode="contained"
        onPress={handlePlaceOrder}
        style={styles.placeOrderButton}
        loading={isPlacingOrder}
        disabled={isPlacingOrder || items.length === 0}>
        {isPlacingOrder ? 'Placing Order...' : 'Place Order'}
      </Button>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  scrollContent: {
    padding: spacing.md,
  },
  card: {
    marginBottom: spacing.md,
    borderRadius: borderRadius.lg,
  },
  sectionTitle: {
    fontWeight: 'bold',
    marginBottom: spacing.md,
  },
  input: {
    marginBottom: spacing.md,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  halfInput: {
    width: '48%',
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  radioLabel: {
    marginLeft: spacing.sm,
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
  placeOrderButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
});

export default CheckoutScreen;
