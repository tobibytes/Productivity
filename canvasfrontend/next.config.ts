import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "http://localhost:8000",
  }
};

export default nextConfig;
