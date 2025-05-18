import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "https://c0cc-2607-fb90-a82e-8763-203a-e0fe-6e87-8c68.ngrok-free.app",
    STRIPE_PUBLIC_KEY: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF",
    PAYMENT_URL: "https://bpc64v11-4242.use.devtunnels.ms"
  }
};

export default nextConfig;
