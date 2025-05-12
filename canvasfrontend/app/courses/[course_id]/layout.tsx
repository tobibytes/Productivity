
"use client";

export default function CourseLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="min-w-screen">
      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}
