"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, ShieldCheck, Lock, User, Loader2 } from "lucide-react";
import { loginOfficer } from "@/lib/api";
import { setAuthToken } from "@/lib/auth";

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

export default function OfficerLoginPage() {
  const [username, setUsername] = useState("officer");
  const [password, setPassword] = useState("officer123");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMsg("");

    try {
      const res = await loginOfficer(username, password);
      setAuthToken(res.access_token);
      router.push("/officer");
    } catch (err: any) {
      console.error("Login failed:", err);
      setErrorMsg("Invalid credentials. Please use demo credentials: officer / officer123");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Brand />

      <div className="login-card">
        <span className="section-label">Agricultural Officer Portal</span>
        <h1>
          Good things grow<br />
          <em>with a little care.</em>
        </h1>
        <p>Sign in to review field reports, examine low-confidence AI cases, and confirm crop diagnoses.</p>

        {/* Demo Credentials Banner */}
        <div className="bg-[#f0ede3] border border-[#dce2d4] p-3 rounded-lg text-xs text-[#163d2f] mb-4 space-y-0.5">
          <strong className="block text-[10px] uppercase tracking-wider text-[#69806c]">
            DEMO OFFICER CREDENTIALS
          </strong>
          <span>Username: <strong>officer</strong> | Password: <strong>officer123</strong></span>
        </div>

        {errorMsg && (
          <div className="bg-amber-50 text-amber-900 border border-amber-200 p-2.5 rounded-lg text-xs font-semibold mb-4">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-3.5">
          <div>
            <label className="block text-xs font-bold text-[#163d2f] mb-1">
              Officer Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full bg-[#f8f6ef] border border-[#d9ddcf] rounded-lg px-3.5 py-2.5 text-xs sm:text-sm font-semibold text-gray-800 focus:outline-none focus:border-[#163d2f]"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#163d2f] mb-1">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full bg-[#f8f6ef] border border-[#d9ddcf] rounded-lg px-3.5 py-2.5 text-xs sm:text-sm font-semibold text-gray-800 focus:outline-none focus:border-[#163d2f]"
            />
          </div>

          <button type="submit" disabled={isLoading} className="button button-ink w-full">
            {isLoading ? (
              <>
                <Loader2 size={18} className="animate-spin" /> Authenticating...
              </>
            ) : (
              <>
                Sign in to Officer Console <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>

        <span className="login-note">
          <ShieldCheck size={15} /> Authorized District Officer Authentication
        </span>
      </div>

      <span className="login-footer">
        Built for farmers and agricultural officers in India · 2026
      </span>
    </div>
  );
}
