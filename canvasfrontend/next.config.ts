import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "https://1650-2601-601-1700-b030-1c8a-fb07-18a9-2073.ngrok-free.app",
    STRIPE_PUBLIC_KEY: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF",
    PAYMENT_URL: "https://bpc64v11-4242.use.devtunnels.ms/"
  }
};

export default nextConfig;
