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
    // Check active sessions and sets the user
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);

      // Get finishedWelcomeFlow from localStorage when session exists
      if (session) {
        const finishedWelcomeFlow = localStorage.getItem("finishedWelcomeFlow");
        if (finishedWelcomeFlow) {
          document.cookie = "finishedWelcomeFlow=true; path=/";
        }
      }
    });

    // Listen for changes on auth state
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
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

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  return useContext(AuthContext);
};
