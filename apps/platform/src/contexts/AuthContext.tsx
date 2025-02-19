"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { User } from "@supabase/supabase-js";
import { supabase } from "@/lib/supabase";

type AuthContextType = {
  user: User | null;
  loading: boolean;
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log("AuthProvider mounted"); // Debug log

    // Check active sessions and sets the user
    supabase.auth
      .getSession()
      .then(({ data: { session } }) => {
        console.log("Initial session check:", session); // Debug log
        setUser(session?.user ?? null);
        setLoading(false);

        // Get finishedWelcomeFlow from localStorage when session exists
        if (session) {
          const finishedWelcomeFlow = localStorage.getItem(
            "finishedWelcomeFlow"
          );
          if (finishedWelcomeFlow) {
            document.cookie = "finishedWelcomeFlow=true; path=/";
          }
        }
      })
      .catch((error) => {
        console.error("Session check error:", error); // Debug error
        setLoading(false);
      });

    // Listen for changes on auth state
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      console.log("Auth state changed:", _event, session); // Debug log
      setUser(session?.user ?? null);

      // Set cookie when auth state changes
      if (session) {
        const finishedWelcomeFlow = localStorage.getItem("finishedWelcomeFlow");
        if (finishedWelcomeFlow) {
          document.cookie = "finishedWelcomeFlow=true; path=/";
        }
      } else {
        // Clear cookie on logout
        document.cookie =
          "finishedWelcomeFlow=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  console.log("AuthProvider rendering", { user, loading }); // Debug log

  return (
    <AuthContext.Provider value={{ user, loading }}>
      <div className="fixed top-20 left-0 bg-purple-500 text-white p-2 z-50">
        Auth Provider Mounted (Loading: {loading.toString()})
      </div>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
