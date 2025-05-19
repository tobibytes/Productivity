import "./globals.css";
import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/react";

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
        <header className="p-4">
          <h1 className="text-lg font-bold"><a href="/">Home</a></h1>
        </header>
        <main className="flex flex-wrap justify-center items-center min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}