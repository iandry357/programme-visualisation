import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/api/concerts/**',
      },
      {
        protocol: 'https',
        hostname: '*.railway.app',
        pathname: '/api/concerts/**',
      },
    ],
  },
};

export default nextConfig;