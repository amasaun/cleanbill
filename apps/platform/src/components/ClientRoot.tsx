"use client";

import { useEffect } from "react";
import { AuthProvider } from "@/contexts/AuthContext";

export function ClientRoot({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    console.log("ClientRoot mounted");
  }, []);

  return (
    <div className="min-h-screen">
      <div className="fixed top-0 left-0 bg-red-500 text-white p-2 z-50">
        Client Root Mounted
      </div>
      <AuthProvider>{children}</AuthProvider>
    </div>
  );
}
