"use client";

import React from "react";

export default function ModuleItemLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-50 px-6 py-8">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Module Item</h1>
        <p className="text-sm text-gray-500">Detailed view of a specific module item</p>
      </header>

      <main className="w-full max-w-5xl mx-auto">
        {children}
      </main>
    </div>
  );
}
