import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "https://76c1-2607-fb90-a82e-8763-bd66-3e9-b33c-c9bf.ngrok-free.app",
    STRIPE_PUBLIC_KEY: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF",
    PAYMENT_URL: "https://bpc64v11-4242.use.devtunnels.ms"
  }
};

export default nextConfig;
