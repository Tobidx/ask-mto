import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Remove static export for Vercel - we want SSR capabilities
  trailingSlash: false,
  images: {
    unoptimized: true,
  },
  // Remove basePath and assetPrefix for Vercel deployment
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '/api',
  },
  // Optimize for Vercel
  poweredByHeader: false,
  generateEtags: false,
  compress: true,
};

export default nextConfig;
