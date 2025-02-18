"use client";

import { Auth } from "@supabase/auth-ui-react";
import { ThemeSupa } from "@supabase/auth-ui-shared";
import { supabase } from "@/lib/supabase";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AuthPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.push("/welcome");
    }
  }, [user, loading, router]);

  // Add effect to handle viewport height
  useEffect(() => {
    const setVH = () => {
      // Subtract navbar height (64px) from viewport height
      const vh = (window.innerHeight - 64) * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`);
    };

    setVH();
    window.addEventListener("resize", setVH);

    return () => window.removeEventListener("resize", setVH);
  }, []);

  if (loading) {
    return (
      <div
        className="fixed inset-x-0 top-[64px] flex items-center justify-center bg-gray-50"
        style={{ height: "calc(var(--vh, 1vh) * 100)" }}
      >
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (user) {
    return null;
  }

  return (
    <div
      className="fixed inset-x-0 top-[64px] flex justify-center bg-gray-50"
      style={{ height: "calc(100vh - 64px)" }}
    >
      <div className="w-[300px] pt-8">
        <div className="text-center mb-4">
          <h2 className="text-lg font-bold">Welcome to cleanbill</h2>
          <p className="text-xs text-gray-600">
            Sign in or create an account to continue
          </p>
        </div>

        <div className="bg-white shadow rounded-lg">
          <Auth
            supabaseClient={supabase}
            appearance={{
              theme: ThemeSupa,
              variables: {
                default: {
                  colors: {
                    brand: "#404040",
                    brandAccent: "#262626",
                  },
                },
              },
              style: {
                button: {
                  padding: "4px 8px",
                  fontSize: "13px",
                  minHeight: "28px",
                  height: "28px",
                },
                container: {
                  gap: "4px",
                  minHeight: "0",
                  margin: "0",
                  padding: "10px",
                },
                divider: {
                  margin: "4px 0",
                },
                input: {
                  padding: "4px 6px",
                  fontSize: "13px",
                  minHeight: "28px",
                  height: "28px",
                },
                label: {
                  fontSize: "13px",
                  marginBottom: "1px",
                },
                anchor: {
                  fontSize: "11px",
                  padding: "0",
                  height: "auto",
                  minHeight: "0",
                },
                message: {
                  fontSize: "11px",
                  margin: "2px 0",
                  padding: "0",
                  height: "auto",
                  minHeight: "0",
                },
              },
            }}
            providers={["google", "twitter"]}
            redirectTo={`${window.location.origin}/auth/callback`}
            onlyThirdPartyProviders={false}
          />
        </div>
      </div>
    </div>
  );
}
