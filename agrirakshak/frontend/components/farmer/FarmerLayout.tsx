"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bell,
  Camera,
  CloudSun,
  HeartHandshake,
  History,
  Menu,
  MessageCircle,
  MoreHorizontal,
  ShieldCheck,
  Sprout,
  Users,
  X,
} from "lucide-react";
import { LanguageSelector } from "./LanguageSelector";

const navItems = [
  { href: "/farmer", label: "My field", icon: Sprout },
  { href: "/farmer/diagnose", label: "Scan a crop", icon: Camera },
  { href: "/farmer/chat", label: "Ask AgriRakshak", icon: MessageCircle },
  { href: "/farmer/history", label: "My reports", icon: History },
  { href: "/farmer/weather", label: "Weather risk", icon: CloudSun },
  { href: "/farmer/expert", label: "Expert help", icon: HeartHandshake },
];

function Brand({ light = false }: { light?: boolean }) {
  return (
    <Link href="/" className={`brand ${light ? "brand-light" : ""}`}>
      <img src="/agrirakshak-logo.png" alt="AgriRakshak Logo" />
      <span>
        Agri<span>Rakshak</span>
      </span>
    </Link>
  );
}

export const FarmerLayout: React.FC<{ children: React.ReactNode; language?: string; onLanguageChange?: (lang: string) => void }> = ({
  children,
  language = "en",
  onLanguageChange,
}) => {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="sidebar-top flex items-center justify-between">
          <Brand light />
          <button
            className="icon-button mobile-only text-white"
            onClick={() => setOpen(false)}
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        </div>

        <div className="profile-mini">
          <div className="avatar">RS</div>
          <div>
            <strong>Ravi Singh</strong>
            <span>Farmer account</span>
          </div>
          <MoreHorizontal size={17} />
        </div>

        <p className="nav-caption">Your field companion</p>

        <nav className="side-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={isActive ? "active" : ""}
                onClick={() => setOpen(false)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
                {isActive && <span className="nav-dot" />}
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-note">
          <ShieldCheck size={19} />
          <div>
            <strong>Your data is private</strong>
            <span>Photos are used only to help with your crop.</span>
          </div>
        </div>

        <div className="sidebar-bottom">
          <Link href="/officer">
            <Users size={18} />
            Officer view
          </Link>
          {onLanguageChange && (
            <div className="mt-2 px-1">
              <LanguageSelector language={language} onLanguageChange={onLanguageChange} />
            </div>
          )}
        </div>
      </aside>

      {/* Scrim Overlay on Mobile */}
      {open && (
        <button
          className="scrim mobile-only"
          onClick={() => setOpen(false)}
          aria-label="Close navigation"
        />
      )}

      {/* Main Content View */}
      <main className="app-main">
        <div className="mobile-toolbar mobile-only">
          <button
            className="icon-button"
            onClick={() => setOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={21} />
          </button>
          <Brand />
          <Bell size={19} />
        </div>
        {children}
      </main>
    </div>
  );
};
