/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8001',
  },
  images: {
    domains: ['localhost', 'social-commerce-media.s3.amazonaws.com'],
  },
}

module.exports = nextConfig
