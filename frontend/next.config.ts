import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standard Next.js config for local development
  // No static export or base path needed for localhost
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
