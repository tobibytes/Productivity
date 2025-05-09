"use client";

import React from "react";

export default function AssignmentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="w-full max-w-4xl mx-auto px-6 py-10">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800">Assignment Details</h1>
        <p className="text-sm text-gray-500">
          View and interact with your assignment information
        </p>
      </header>

      <main>{children}</main>
    </div>
  );
}