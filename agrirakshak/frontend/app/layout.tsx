import type { Metadata } from "next";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgriRakshak — AI Crop Disease & Pest Protection Platform",
  description: "AI-powered agricultural assistant for crop health detection, weather alerts, and expert escalation.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
      </head>
      <body className="bg-gray-100 min-h-screen text-gray-900 font-sans antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
