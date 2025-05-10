import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "http://api.talvra.us:8000",
  }
};

export default nextConfig;
