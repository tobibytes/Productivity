"use client";
import { useParams, useRouter } from "next/navigation";
import React from "react";

export default function AssignmentsLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const params = useParams();
  const courseId = params?.course_id;

  return (
    <div className="bg-gray-50 min-h-screen">
      <header className="mb-6 pt-8 px-4">
        <h1
          className="text-3xl font-bold text-gray-800 cursor-pointer"
          onClick={() => router.push(`/courses/${courseId}/assignments`)}
        >
          Assignments
        </h1>
        <p className="text-sm text-gray-500">All your assignments for this course</p>
      </header>

      <main className="flex-grow p-4">{children}</main>
    </div>
  );
}