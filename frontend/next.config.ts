import type { NextConfig } from "next";

// @ts-ignore
const nextConfig: NextConfig = {
  output: 'export',
  // GitHub Pages repository name
  basePath: '/Python-Debugger',
  assetPrefix: '/Python-Debugger/',
  images: {
    unoptimized: true,
  },
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
  },
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
