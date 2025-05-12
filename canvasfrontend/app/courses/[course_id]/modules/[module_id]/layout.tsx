"use client"
import React from "react";
import { useParams, useRouter } from "next/navigation";

export default function ModuleLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { course_id, module_id } = useParams();
  return (
    <div className="min-w-screen min-h-screen overflow-x-hidden " >
      <header className="mb-6 pt-8 px-4 max-w-7xl mx-auto w-full cursor-pointer" onClick={() => router.push(`/courses/${course_id}/modules/${module_id}/moduleitems`)}>
        <h1 className="text-2xl font-bold text-gray-800">Module Items</h1>
        <p className="text-sm text-gray-500">Resources and content for this module</p>
      </header>

      <main className="flex-1 w-full">
        {children}
      </main>
    </div>
  );
}
