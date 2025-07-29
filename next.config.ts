import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configure for static deployment to Vercel (frontend only)
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  env: {
    // Railway backend URL will be set as environment variable
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  // Optimize for production
  poweredByHeader: false,
  generateEtags: false,
  compress: true,
};

export default nextConfig;
