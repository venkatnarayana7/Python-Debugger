import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  // GitHub Pages repository name
  basePath: '/Python-Debugger',
  assetPrefix: '/Python-Debugger/',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
