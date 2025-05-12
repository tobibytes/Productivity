"use client";
import React from "react";
import { useParams, useRouter } from "next/navigation";

export default function ModulesLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const {course_id} = useParams()
  return (
    <div className="min-w-screen min-h-screen">
      <header className="cursor-pointer mb-6 pt-8 px-4"  onClick={() => router.push(`/courses/${course_id}/modules`)}>
        <h1 className="text-3xl font-bold text-gray-800">Modules</h1>
        <p className="text-sm text-gray-500">View all modules for this course</p>
      </header>

      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}
