
"use client";

export default function CourseLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className=" bg-gray-50 min-h-screen">
      <main className="flex-1">
        {children}
      </main>
    </div>
  );
}
