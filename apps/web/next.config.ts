import type { NextConfig } from "next";

const apiOrigin = (process.env.API_INTERNAL_URL || "http://api:8000").replace(/\/$/, "");
const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  async rewrites() {
    return [{ source: "/api/v1/:path*", destination: `${apiOrigin}/api/v1/:path*` }];
  },
};

export default nextConfig;
