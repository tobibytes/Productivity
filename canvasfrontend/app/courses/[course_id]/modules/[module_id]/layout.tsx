"use client"
import React from "react";

export default function ModuleLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className=" bg-gray-50 min-h-screen overflow-x-hidden">
      <header className="mb-6 pt-8 px-4 max-w-7xl mx-auto w-full">
        <h1 className="text-2xl font-bold text-gray-800">Module Items</h1>
        <p className="text-sm text-gray-500">Resources and content for this module</p>
      </header>

      <main className="flex-1 w-full">
        {children}
      </main>
    </div>
  );
}
