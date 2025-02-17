"use client";

import { useEffect, useState } from "react";

export default function TestPage() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    console.log("Test page mounted");
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-2xl">
        {mounted ? "Test Page Mounted!" : "Mounting..."}
      </div>
    </div>
  );
}
