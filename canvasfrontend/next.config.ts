import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    BACKEND_URL: "https://6047-2607-fb90-a82e-8763-1dc5-2ee-967c-809b.ngrok-free.app",
    STRIPE_PUBLIC_KEY: "pk_live_51MEwjTLpjISvJMPETOabPmJimxlDll0j9WY1ZL5YnSXhCzjeN5wRwLlplfndf9QlGxPc8RD9QMeRGRZdpe1dy7EX00SyyBwjYF"
  }
};

export default nextConfig;
