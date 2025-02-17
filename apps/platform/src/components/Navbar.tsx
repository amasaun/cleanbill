"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useState, useRef, useEffect } from "react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { Menu } from "@headlessui/react";
import Link from "next/link";

export default function Navbar() {
  const { user } = useAuth();
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowMenu(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    router.push("/");
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white px-4 py-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <a href="/" className="flex items-center space-x-3">
              <Image
                src="/images/icon-blue.svg"
                alt="Cleanbill Icon"
                width={48}
                height={48}
                className="md:hidden"
                priority
              />
              <Image
                src="/images/logo-blue.svg"
                alt="Cleanbill"
                width={120}
                height={40}
                className="hidden md:block"
                priority
              />
            </a>
          </div>

          {user && (
            <Menu as="div" className="relative">
              <Menu.Button className="flex items-center space-x-3 rounded-full p-2 hover:bg-gray-100">
                <div className="h-8 w-8 rounded-full bg-gray-300 p-1">
                  <svg
                    className="h-6 w-6 text-gray-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                </div>
                <span className="text-sm text-gray-700">{user.email}</span>
                <svg
                  className={`h-5 w-5 text-gray-400 transition-transform ${
                    showMenu ? "rotate-180" : ""
                  }`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </Menu.Button>

              <Menu.Items className="absolute right-0 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <Menu.Item>
                  {({ active }) => (
                    <Link
                      href="/dashboard"
                      className={`${
                        active ? "bg-gray-100" : ""
                      } block px-4 py-2 text-sm text-gray-700`}
                    >
                      Dashboard
                    </Link>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <Link
                      href="/welcome"
                      className={`${
                        active ? "bg-gray-100" : ""
                      } block px-4 py-2 text-sm text-gray-700`}
                    >
                      Connect Insurance
                    </Link>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <button
                      onClick={handleSignOut}
                      className={`${
                        active ? "bg-gray-100" : ""
                      } block w-full px-4 py-2 text-left text-sm text-gray-700`}
                    >
                      Sign out
                    </button>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Menu>
          )}
        </div>
      </div>
    </nav>
  );
}
