"use client";

import { useRouter } from "next/navigation";

export default function CoursesLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter()
  return (
    <div className="bg-gray-50">
      <header className="mb-6 pt-8 px-4">
        <h1 className="text-3xl font-bold text-gray-800" onClick={() => router.push(`/courses`)}>Your Courses</h1>
        <p className="text-sm text-gray-500">Browse all enrolled or available courses</p>
      </header>

      <main className="flex-1 min-h-screen">
        {children}
      </main>
    </div>
  );
}