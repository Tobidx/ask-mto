import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable static export for better performance
  output: 'standalone',
  
  // Configure environment variables
  env: {
    // Railway backend URL
    NEXT_PUBLIC_API_URL: 'https://ask-mto-production.up.railway.app',
  },

  // CORS and security settings
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: '*' },
        ],
      },
    ];
  }
};

export default nextConfig; 