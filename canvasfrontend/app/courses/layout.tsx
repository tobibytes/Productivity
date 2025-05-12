"use client";

import { useRouter } from "next/navigation";

export default function CoursesLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter()
  return (
    <div className="min-w-screen">
      <header className="cursor-pointer" onClick={() => router.push(`/courses`)}>
        <h1 className="text-3xl font-bold text-gray-800">Your Courses</h1>
        <p className="text-sm text-gray-500">Browse all enrolled or available courses</p>
      </header>

      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}