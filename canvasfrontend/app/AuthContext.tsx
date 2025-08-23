"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

export type AuthState = {
  email: string | null;
  loading: boolean;
  error: string | null;
};

const AuthContext = createContext<AuthState>({ email: null, loading: true, error: null });

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({ email: null, loading: true, error: null });

  useEffect(() => {
    async function load() {
      try {
        const backend = process.env.NEXT_PUBLIC_BACKEND_URL || process.env.BACKEND_URL;
        const res = await fetch(`${backend}/auth/me`, { credentials: "include" });
        if (res.ok) {
          const data = await res.json();
          setState({ email: data.email, loading: false, error: null });
        } else {
          setState({ email: null, loading: false, error: null });
        }
      } catch (e: any) {
        setState({ email: null, loading: false, error: e?.message ?? "Failed to auth" });
      }
    }
    load();
  }, []);

  return <AuthContext.Provider value={state}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}

