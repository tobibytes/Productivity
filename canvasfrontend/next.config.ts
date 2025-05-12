import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "https://2bdc-2607-fb90-a82e-8763-c873-81ed-f658-6c93.ngrok-free.app",
    STRIPE_PUBLIC_KEY: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF"
  }
};

export default nextConfig;
