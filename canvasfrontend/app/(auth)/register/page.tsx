"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import CanvasTokenGuide from "@/components/CanvasTokenGuide";

const Register = () => {
  const [showHowTo, setShowHowTo] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    api_key: ""
  });
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const res = await fetch(`${process.env.BACKEND_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      const data = await res.json();
      if (data.success) {
        console.log("Registration successful:", data);
        router.push("/signin");
      }
    } else {
      console.error("Registration failed:", res.statusText);
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-50 min-w-80" id="register">
    <div className="flex justify-center items-center bg-gray-100">
      <div className="bg-white p-8 rounded-2xl shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              name="email"
              id="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label htmlFor="api_key" className="block text-sm font-medium text-gray-700 mb-1">
              Canvas API Key
            </label>
            <input
              type="password"
              name="api_key"
              id="api_key"
              value={formData.api_key}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your Canvas API Key"
              required
            />
            <p className="text-sm text-blue-600 mt-2" onClick={() => setShowHowTo(!showHowTo)}>
              <Link href="#howto" className="hover:underline">
                How do I get my Canvas access token?
              </Link>
            </p>
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          >
            Register
          </button>
          <p className="text-sm text-gray-500 text-center">
            Already have an account?{" "}
            <Link href="/signin" className="text-blue-600 hover:underline">
              Sign in here
            </Link>
          </p>
        </form>
      </div>
    </div>
      { showHowTo && <CanvasTokenGuide />}
      </div>
  );
};

export default Register;