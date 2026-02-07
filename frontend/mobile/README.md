# Social Commerce Mobile App

React Native mobile application for the Social Commerce Platform.

## Setup

### Prerequisites
- Node.js 20 LTS
- React Native CLI
- iOS: Xcode (for Mac)
- Android: Android Studio

### Installation

```bash
# Install dependencies
npm install

# iOS (Mac only)
cd ios && pod install && cd ..

# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

## Project Structure

```
src/
├── screens/          # All screen components
│   ├── auth/        # Login, Register, ForgotPassword
│   ├── main/        # Feed, Search, CreatePost, Notifications, Profile
│   ├── products/    # ProductList, ProductDetail
│   ├── cart/        # Cart, Checkout
│   └── settings/    # Settings, EditProfile
├── components/      # Reusable components
├── navigation/      # Navigation configuration
├── store/           # Zustand state management
├── services/        # API service layer
└── utils/           # Utilities and helpers
```

## Features

- ✅ User authentication (Login, Register)
- ✅ Social feed with posts
- ✅ Product browsing and search
- ✅ Shopping cart and checkout
- ✅ User profiles
- ✅ Post creation with media upload
- ✅ Settings and profile editing

## Environment Configuration

Update API URLs in `src/services/api.ts` or use environment variables.

## Development

The app uses:
- **React Native Paper** for UI components
- **React Navigation** for navigation
- **Zustand** for state management
- **React Query** for data fetching
- **TypeScript** for type safety

## Building for Production

```bash
# Android
cd android && ./gradlew assembleRelease

# iOS
cd ios && xcodebuild -workspace SocialCommerce.xcworkspace -scheme SocialCommerce -configuration Release
```
