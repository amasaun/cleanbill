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
      const finishedWelcomeFlow =
        localStorage.getItem("finishedWelcomeFlow") === "true";
      router.push(finishedWelcomeFlow ? "/dashboard" : "/welcome");
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
      className="fixed inset-x-0 top-[64px] flex items-center justify-center bg-gray-50"
      style={{ height: "calc(100vh - 64px)" }}
    >
      <div className="w-[440px] p-8">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-semibold text-gray-900">
            Sign in / Sign up
          </h2>
        </div>

        <div className="bg-white shadow-sm rounded-2xl p-8">
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
                  borderRadii: {
                    inputButton: "12px",
                  },
                },
              },
              style: {
                button: {
                  padding: "8px 12px",
                  fontSize: "14px",
                  height: "42px",
                  borderRadius: "12px",
                },
                container: {
                  gap: "16px",
                  margin: "0",
                },
                divider: {
                  margin: "20px 0",
                },
                input: {
                  padding: "8px 12px",
                  fontSize: "14px",
                  height: "42px",
                  borderRadius: "12px",
                },
                label: {
                  fontSize: "14px",
                  marginBottom: "4px",
                },
                anchor: {
                  fontSize: "14px",
                  padding: "0",
                  height: "auto",
                },
                message: {
                  fontSize: "14px",
                  margin: "4px 0",
                  padding: "0",
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
