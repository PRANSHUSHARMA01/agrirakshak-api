"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  BarChart3,
  Bell,
  FileText,
  HeartHandshake,
  LogOut,
  Map,
  Search,
  Sprout,
  Users,
} from "lucide-react";
import { getAuthToken, removeAuthToken } from "@/lib/auth";

function Brand() {
  return (
    <Link href="/" className="brand">
      <img src="/agrirakshak-logo.png" alt="AgriRakshak Logo" />
      <span>
        Agri<span>Rakshak</span>
      </span>
    </Link>
  );
}

export const OfficerLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const pathname = usePathname();
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.push("/login");
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  const handleLogout = () => {
    removeAuthToken();
    router.push("/login");
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-[#f4f5ee] flex items-center justify-center p-4">
        <div className="text-center space-y-3">
          <Brand />
          <p className="text-xs text-gray-500 font-semibold">Redirecting to Officer Authentication...</p>
        </div>
      </div>
    );
  }

  const navLinks = [
    { href: "/officer", icon: BarChart3, label: "Overview" },
    { href: "/officer/map", icon: Map, label: "Disease map" },
    { href: "/officer/cases", icon: FileText, label: "All cases" },
    { href: "/officer/analytics", icon: BarChart3, label: "Analytics" },
    { href: "/officer/escalations", icon: HeartHandshake, label: "Escalations" },
  ];

  return (
    <div className="officer-shell">
      {/* Officer Sidebar */}
      <aside className="officer-side">
        <Brand />
        <span className="officer-badge">OFFICER CONSOLE</span>

        <nav>
          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={isActive ? "active" : ""}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="officer-side-foot">
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-xs font-bold text-red-700 hover:text-red-900 transition"
          >
            <LogOut size={16} /> Logout
          </button>
          <Link href="/farmer">
            <Sprout size={17} />
            Switch to farmer view
          </Link>
          <span>
            District Agriculture Office<br />
            <strong>Karnal, Haryana</strong>
          </span>
        </div>
      </aside>

      {/* Main Content */}
      <main className="officer-main">
        <header className="officer-header">
          <div>
            <span className="section-label">District overview</span>
            <h1>Good morning, Meera.</h1>
          </div>
          <div className="officer-head-actions">
            <button className="icon-button" title="Search">
              <Search size={18} />
            </button>
            <button className="icon-button" title="Notifications">
              <Bell size={18} />
            </button>
            <div className="avatar">MK</div>
          </div>
        </header>

        {children}
      </main>
    </div>
  );
};
