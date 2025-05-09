"use client";
import React from "react";

export default function ModulesLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className=" bg-gray-50 min-h-screen">
      <header className="mb-6 pt-8 px-4">
        <h1 className="text-3xl font-bold text-gray-800">Modules</h1>
        <p className="text-sm text-gray-500">View all modules for this course</p>
      </header>

      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}
