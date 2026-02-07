export const API_BASE_URL = __DEV__
  ? 'http://localhost:8001'
  : 'https://api.socialcommerce.com';

export const CONTENT_SERVICE_URL = __DEV__
  ? 'http://localhost:8002'
  : 'https://api.socialcommerce.com';

export const PRODUCT_SERVICE_URL = __DEV__
  ? 'http://localhost:8003'
  : 'https://api.socialcommerce.com';

export const ORDER_SERVICE_URL = __DEV__
  ? 'http://localhost:8004'
  : 'https://api.socialcommerce.com';

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  USER: 'user',
  CART: 'cart',
  SETTINGS: 'settings',
};

export const PRODUCT_CATEGORIES = [
  'Fashion',
  'Beauty',
  'Home',
  'Electronics',
  'Sports',
  'Books',
  'Food',
  'Health',
] as const;

export const PAYMENT_METHODS = {
  RAZORPAY: 'razorpay',
  COD: 'cod',
} as const;
