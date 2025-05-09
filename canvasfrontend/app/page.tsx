"use client";
import Link from "next/link";

const routes = [
  { href: "/courses", label: "Courses" },
  { href: "/profile", label: "Profile" },
  { href: "/signin", label: "Sign In" },
  { href: "/register", label: "Register" },
];

export default function HomePage() {
  return (
    <div className="min-h-screen flex gap-20 justify-center items-center bg-gray-50 px-6 py-12">
      <div className="">
      <h1 className="text-4xl font-bold text-gray-800 mb-4 text-center">Welcome</h1>
      <p className="text-gray-600 mb-8 text-center">Navigate to key sections of the app.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-md">
        {routes.map((route) => (
          <Link
            key={route.href}
            href={route.href}
            className="bg-white rounded-xl shadow p-6 text-center text-lg font-medium text-blue-700 hover:text-blue-900 border border-gray-200 hover:shadow-md transition"
          >
            {route.label}
          </Link>
        ))}
      </div>
    </div>
  );
}