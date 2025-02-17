"use client";

import { useEffect } from "react";

export function DebugLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    console.log("DebugLayout mounted");
  }, []);

  return (
    <>
      <div className="fixed top-0 left-0 bg-red-500 text-white p-2 z-50">
        Layout Rendered
      </div>
      {children}
    </>
  );
}
