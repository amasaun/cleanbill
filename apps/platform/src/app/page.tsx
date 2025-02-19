"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function HomePage() {
  console.log("Home page rendering");

  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    console.log("Home page effect", { user, loading });

    // Add a delay to allow for development
    const timer = setTimeout(() => {
      if (!loading) {
        router.push(user ? "/dashboard" : "/auth");
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [user, loading, router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="fixed top-10 left-0 bg-green-500 text-white p-2 z-50">
        Home Page Mounted
      </div>
      <div className="text-lg">{loading ? "Loading..." : "Redirecting..."}</div>
    </div>
  );
}
