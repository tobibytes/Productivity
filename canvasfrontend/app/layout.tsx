import type { Metadata } from "next";
import "./globals.css";
import { Analytics } from "@vercel/analytics/next"

export const metadata: Metadata = {
  title: "Canvas",
  description: "Complete your Homeworks",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
<html lang="en">
      <body className="min-h-screen bg-white text-gray-800">
        <Analytics />
        <h1><a href="/">Home</a></h1>
        <div className="flex flex-wrap justify-center items-center min-h-svh" >
          {children}
        </div>
      </body>
      <script async src="https://js.stripe.com/v3/pricing-table.js"></script>
    </html>
  );
}
