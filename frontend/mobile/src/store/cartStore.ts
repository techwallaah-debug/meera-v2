import {create} from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {apiService} from '../services/api';

export interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  product_title?: string;
  product_price?: number;
  product_image?: string;
}

interface CartState {
  items: CartItem[];
  isLoading: boolean;
  error: string | null;
  loadCart: () => Promise<void>;
  addToCart: (productId: number, quantity?: number) => Promise<void>;
  updateQuantity: (itemId: number, quantity: number) => Promise<void>;
  removeFromCart: (itemId: number) => Promise<void>;
  clearCart: () => Promise<void>;
  getTotal: () => number;
  getItemCount: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  isLoading: false,
  error: null,

  loadCart: async () => {
    set({isLoading: true, error: null});
    try {
      const items = await apiService.getCart();
      set({items, isLoading: false});
    } catch (error: any) {
      set({
        error: error.message || 'Failed to load cart',
        isLoading: false,
      });
    }
  },

  addToCart: async (productId: number, quantity = 1) => {
    try {
      set({error: null});
      const item = await apiService.addToCart(productId, quantity);
      
      // Update local state
      const currentItems = get().items;
      const existingItem = currentItems.find(i => i.product_id === productId);
      
      if (existingItem) {
        set({
          items: currentItems.map(i =>
            i.product_id === productId
              ? {...i, quantity: i.quantity + quantity}
              : i
          ),
        });
      } else {
        set({items: [...currentItems, item]});
      }
    } catch (error: any) {
      set({error: error.message || 'Failed to add to cart'});
      throw error;
    }
  },

  updateQuantity: async (itemId: number, quantity: number) => {
    if (quantity <= 0) {
      await get().removeFromCart(itemId);
      return;
    }

    try {
      set({error: null});
      await apiService.updateCartItem(itemId, quantity);
      
      set({
        items: get().items.map(item =>
          item.id === itemId ? {...item, quantity} : item
        ),
      });
    } catch (error: any) {
      set({error: error.message || 'Failed to update cart'});
      throw error;
    }
  },

  removeFromCart: async (itemId: number) => {
    try {
      set({error: null});
      await apiService.removeFromCart(itemId);
      
      set({
        items: get().items.filter(item => item.id !== itemId),
      });
    } catch (error: any) {
      set({error: error.message || 'Failed to remove from cart'});
      throw error;
    }
  },

  clearCart: async () => {
    try {
      set({error: null});
      await apiService.clearCart();
      set({items: []});
    } catch (error: any) {
      set({error: error.message || 'Failed to clear cart'});
      throw error;
    }
  },

  getTotal: () => {
    const items = get().items;
    return items.reduce(
      (total, item) => total + (item.product_price || 0) * item.quantity,
      0
    );
  },

  getItemCount: () => {
    return get().items.reduce((count, item) => count + item.quantity, 0);
  },
}));
