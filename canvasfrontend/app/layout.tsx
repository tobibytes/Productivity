import type { Metadata } from "next";
import "./globals.css";


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
        <h1><a href="/">Home</a></h1>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" >
          {children}
        </div>
      </body>
    </html>
  );
}
