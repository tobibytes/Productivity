"use client";
import Link from "next/link";

const routes = [
  { href: "/courses", label: "Courses" },
  // { href: "/profile", label: "Profile" },
  { href: "/signin", label: "Sign In" },
  { href: "/register", label: "Register" },
  { href: "/pricing", label: "Pricing" },
];

export default function HomePage() {
  return (
    <div className="flex flex-wrap gap-6">
      <div className="flex flex-wrap gap-6">
      <h1 className="text-4xl font-bold text-gray-800 text-center">Welcome</h1>
      <p className="text-gray-600 text-center self-center">Navigate to key sections of the app.</p>
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