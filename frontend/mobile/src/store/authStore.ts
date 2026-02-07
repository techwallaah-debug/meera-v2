import {create} from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {apiService} from '../services/api';

interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  bio?: string;
  avatar_url?: string;
  is_creator: boolean;
  is_verified: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    email: string;
    username: string;
    full_name: string;
    password: string;
    is_creator?: boolean;
  }) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (user: User) => void;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email: string, password: string) => {
    try {
      const response = await apiService.login(email, password);
      const token = response.access_token;
      
      await AsyncStorage.setItem('access_token', token);
      
      const user = await apiService.getCurrentUser();
      await AsyncStorage.setItem('user', JSON.stringify(user));
      
      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error: any) {
      set({isLoading: false});
      throw error;
    }
  },

  register: async data => {
    try {
      const user = await apiService.register(data);
      // Auto login after registration
      await get().login(data.email, data.password);
    } catch (error: any) {
      throw error;
    }
  },

  logout: async () => {
    await AsyncStorage.removeItem('access_token');
    await AsyncStorage.removeItem('user');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },

  updateUser: (user: User) => {
    set({user});
    AsyncStorage.setItem('user', JSON.stringify(user));
  },

  loadUser: async () => {
    try {
      const token = await AsyncStorage.getItem('access_token');
      const userStr = await AsyncStorage.getItem('user');
      
      if (token && userStr) {
        const user = JSON.parse(userStr);
        set({
          user,
          token,
          isAuthenticated: true,
          isLoading: false,
        });
        // Refresh user data
        try {
          const freshUser = await apiService.getCurrentUser();
          set({user: freshUser});
          await AsyncStorage.setItem('user', JSON.stringify(freshUser));
        } catch (error) {
          // Token might be expired
          await get().logout();
        }
      } else {
        set({isLoading: false});
      }
    } catch (error) {
      set({isLoading: false});
    }
  },
}));
