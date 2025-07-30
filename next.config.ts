import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configure environment variables
  env: {
    // Railway backend URL - updated to new custom domain
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://ask-mto.up.railway.app',
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