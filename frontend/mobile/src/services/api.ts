import axios, {AxiosInstance, AxiosError} from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = __DEV__
  ? 'http://localhost:8001' // Change to your backend URL
  : 'https://api.socialcommerce.com';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      async config => {
        const token = await AsyncStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      },
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      response => response,
      async error => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          await AsyncStorage.removeItem('access_token');
          await AsyncStorage.removeItem('user');
          // Navigate to login (handled in navigation)
        }
        return Promise.reject(error);
      },
    );
  }

  // User Service
  async register(data: {
    email: string;
    username: string;
    full_name: string;
    password: string;
    is_creator?: boolean;
  }) {
    const response = await this.client.post('/register', data);
    return response.data;
  }

  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    const response = await this.client.post('/token', formData, {
      headers: {'Content-Type': 'multipart/form-data'},
    });
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/users/me');
    return response.data;
  }

  async updateProfile(data: {full_name?: string; bio?: string; avatar_url?: string}) {
    const response = await this.client.put('/users/me', data);
    return response.data;
  }

  async getUser(userId: number) {
    const response = await this.client.get(`/users/${userId}`);
    return response.data;
  }

  async followUser(userId: number) {
    const response = await this.client.post(`/users/${userId}/follow`);
    return response.data;
  }

  // Content Service (change base URL for content service)
  async getFeed(skip = 0, limit = 20) {
    const client = this.getServiceClient('8002');
    const response = await client.get('/posts', {params: {skip, limit}});
    return response.data;
  }

  async getPost(postId: number) {
    const client = this.getServiceClient('8002');
    const response = await client.get(`/posts/${postId}`);
    return response.data;
  }

  async createPost(data: {
    caption?: string;
    media_urls: string[];
    product_tags: number[];
  }) {
    const client = this.getServiceClient('8002');
    const response = await client.post('/posts', data);
    return response.data;
  }

  async likePost(postId: number) {
    const client = this.getServiceClient('8002');
    const response = await client.post(`/posts/${postId}/like`);
    return response.data;
  }

  async createComment(postId: number, content: string, parentId?: number) {
    const client = this.getServiceClient('8002');
    const response = await client.post(`/posts/${postId}/comments`, {
      content,
      parent_id: parentId,
    });
    return response.data;
  }

  async getComments(postId: number, skip = 0, limit = 20) {
    const client = this.getServiceClient('8002');
    const response = await client.get(`/posts/${postId}/comments`, {
      params: {skip, limit},
    });
    return response.data;
  }

  async uploadMedia(file: any) {
    const client = this.getServiceClient('8002');
    const formData = new FormData();
    formData.append('file', file);
    const response = await client.post('/upload-media', formData, {
      headers: {'Content-Type': 'multipart/form-data'},
    });
    return response.data;
  }

  // Product Service
  async getProducts(params: {
    q?: string;
    category?: string;
    min_price?: number;
    max_price?: number;
    skip?: number;
    limit?: number;
  }) {
    const client = this.getServiceClient('8003');
    const response = await client.get('/products', {params});
    return response.data;
  }

  async getProduct(productId: number) {
    const client = this.getServiceClient('8003');
    const response = await client.get(`/products/${productId}`);
    return response.data;
  }

  async createReview(productId: number, data: {
    rating: number;
    title?: string;
    content?: string;
    images?: string[];
  }) {
    const client = this.getServiceClient('8003');
    const response = await client.post(`/products/${productId}/reviews`, data);
    return response.data;
  }

  async getReviews(productId: number, skip = 0, limit = 20) {
    const client = this.getServiceClient('8003');
    const response = await client.get(`/products/${productId}/reviews`, {
      params: {skip, limit},
    });
    return response.data;
  }

  // Order Service (Cart & Orders)
  async getCart() {
    const client = this.getServiceClient('8004');
    const response = await client.get('/cart');
    return response.data;
  }

  async addToCart(productId: number, quantity = 1) {
    const client = this.getServiceClient('8004');
    const response = await client.post('/cart', {
      product_id: productId,
      quantity,
    });
    return response.data;
  }

  async updateCartItem(itemId: number, quantity: number) {
    const client = this.getServiceClient('8004');
    const response = await client.put(`/cart/${itemId}`, null, {
      params: {quantity},
    });
    return response.data;
  }

  async removeFromCart(itemId: number) {
    const client = this.getServiceClient('8004');
    const response = await client.delete(`/cart/${itemId}`);
    return response.data;
  }

  async clearCart() {
    const client = this.getServiceClient('8004');
    const response = await client.delete('/cart');
    return response.data;
  }

  async createOrder(data: {
    address: {
      name: string;
      phone: string;
      street: string;
      city: string;
      state: string;
      pincode: string;
    };
    payment_method: 'razorpay' | 'cod';
  }) {
    const client = this.getServiceClient('8004');
    const response = await client.post('/orders', data);
    return response.data;
  }

  async getOrders(skip = 0, limit = 20) {
    const client = this.getServiceClient('8004');
    const response = await client.get('/orders', {
      params: {skip, limit},
    });
    return response.data;
  }

  async getOrder(orderId: number) {
    const client = this.getServiceClient('8004');
    const response = await client.get(`/orders/${orderId}`);
    return response.data;
  }

  async verifyPayment(orderId: number, paymentId: string, signature: string) {
    const client = this.getServiceClient('8004');
    const response = await client.post(`/orders/${orderId}/payment/verify`, {
      payment_id: paymentId,
      signature: signature,
    });
    return response.data;
  }

  async cancelOrder(orderId: number) {
    const client = this.getServiceClient('8004');
    const response = await client.post(`/orders/${orderId}/cancel`);
    return response.data;
  }

  // Helper to get service-specific client
  private getServiceClient(port: string): AxiosInstance {
    const baseURL = __DEV__
      ? `http://localhost:${port}`
      : `https://api.socialcommerce.com`;
    
    const client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token
    client.interceptors.request.use(async config => {
      const token = await AsyncStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    return client;
  }
}

export const apiService = new ApiService();
