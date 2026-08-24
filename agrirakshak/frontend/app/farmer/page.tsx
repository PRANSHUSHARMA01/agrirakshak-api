"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  ArrowRight,
  Bell,
  Bot,
  Camera,
  Check,
  ChevronRight,
  CloudSun,
  ShieldCheck,
  Sprout,
} from "lucide-react";
import { FarmerLayout } from "@/components/farmer/FarmerLayout";
import { getWeatherRisk, getCases, getEscalations } from "@/lib/api";
import { WeatherRisk, FarmerCase, EscalationCase } from "@/lib/types";

function PageHeader({
  title,
  eyebrow,
  action,
}: {
  title: React.ReactNode;
  eyebrow?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="page-header">
      <div>
        {eyebrow && <span className="section-label">{eyebrow}</span>}
        <h1>{title}</h1>
      </div>
      {action}
    </div>
  );
}

function StatCard({
  label,
  value,
  note,
  tone = "green",
}: {
  label: string;
  value: string;
  note: string;
  tone?: string;
}) {
  return (
    <div className={`stat-card tone-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{note}</small>
    </div>
  );
}

export default function FarmerHomePage() {
  const [weatherRisk, setWeatherRisk] = useState<WeatherRisk | null>(null);
  const [cases, setCases] = useState<FarmerCase[]>([]);
  const [escalations, setEscalations] = useState<EscalationCase[]>([]);

  useEffect(() => {
    getWeatherRisk().then(setWeatherRisk).catch(console.error);
    getCases().then(setCases).catch(console.error);
    getEscalations("pending").then(setEscalations).catch(console.error);
  }, []);

  const latestCase = cases[0];
  const pendingCount = escalations.length;

  return (
    <FarmerLayout>
      <div className="content-wrap">
        <PageHeader
          eyebrow="Tuesday, 24 August 2026"
          title={
            <>
              Namaste, Ravi <span className="wave">✦</span>
            </>
          }
          action={
            <button className="button button-outline">
              <Bell size={17} /> Notifications
            </button>
          }
        />
        <p className="lead-copy">How can AgriRakshak help you today?</p>

        {/* Field note strip */}
        <div className="field-note-strip">
          <img src="/agrirakshak-logo.png" alt="AgriRakshak logo" />
          <span>
            <strong>Field note / 024</strong> Your crop care starts with one clear observation.
          </span>
          <span className="strip-place">Karnal · Haryana</span>
        </div>

        {/* Primary Dashboard Grid */}
        <div className="dashboard-grid">
          <Link href="/farmer/diagnose" className="scan-panel">
            <div className="scan-panel-copy">
              <span className="panel-kicker">Most useful right now</span>
              <h2>Scan your crop.</h2>
              <p>Take a photo of an affected leaf and get a clearer next step.</p>
              <span className="button button-paper">
                Take a photo <Camera size={17} />
              </span>
            </div>
            <div className="scan-orbit">
              <div className="orbit-ring" />
              <div className="orbit-center">
                <Camera size={31} />
              </div>
              <span className="orbit-leaf">⌁</span>
            </div>
          </Link>

          <Link href="/farmer/chat" className="ask-panel">
            <div className="ask-icon">
              <Bot size={23} />
            </div>
            <div>
              <span className="panel-kicker">Ask anything</span>
              <h3>Talk to AgriRakshak</h3>
              <p>“Why are the leaves on my rice turning yellow?”</p>
            </div>
            <ArrowRight size={18} />
          </Link>
        </div>

        {/* Section Heading Row */}
        <div className="section-heading-row compact">
          <div>
            <span className="section-label">Your field at a glance</span>
            <h2>Small signals, useful context.</h2>
          </div>
          <Link href="/farmer/history" className="text-link">
            View all reports <ArrowRight size={16} />
          </Link>
        </div>

        {/* Live Stats Grid */}
        <div className="stats-grid">
          <StatCard
            label="Weather risk"
            value={weatherRisk?.risk_level || "Low"}
            note={weatherRisk?.reason ? weatherRisk.reason.substring(0, 30) + "..." : "Rain likely in 2 days"}
            tone={weatherRisk?.risk_level === "HIGH" ? "terracotta" : "blue"}
          />
          <StatCard
            label="Last scan"
            value={latestCase ? `${Math.round(latestCase.confidence * 100)}%` : "94%"}
            note={latestCase ? (latestCase.predicted_class?.replace(/_/g, " ") || "Bacterial Leaf Blight") : "Bacterial Leaf Blight"}
            tone="green"
          />
          <StatCard
            label="Expert cases"
            value={pendingCount > 0 ? (pendingCount < 10 ? `0${pendingCount}` : `${pendingCount}`) : "01"}
            note="Awaiting review"
            tone="amber"
          />
        </div>

        {/* Dashboard Lower */}
        <div className="dashboard-lower">
          <div className="recent-card">
            <div className="card-heading">
              <div>
                <span className="section-label">Recent report</span>
                <h3>
                  {latestCase ? `${latestCase.crop} · ${latestCase.predicted_class?.replace(/_/g, " ")}` : "Rice · Bacterial Leaf Blight"}
                </h3>
              </div>
              <span className={`status-pill ${latestCase?.needs_expert_review ? "muted-pill" : "success"}`}>
                <Check size={13} /> {latestCase?.needs_expert_review ? "Needs Review" : "High confidence"}
              </span>
            </div>
            <div className="report-row">
              <img src="/agrirakshak-rice-detail.jpg" alt="Rice leaf report" />
              <div>
                <p>Scanned {latestCase ? new Date(latestCase.created_at).toLocaleDateString() : "22 Aug 2026"}</p>
                <strong>{latestCase ? `${Math.round(latestCase.confidence * 100)}% confidence` : "94% confidence"}</strong>
                <span>Inspect nearby plants and maintain field drainage.</span>
              </div>
              <ChevronRight size={19} />
            </div>
          </div>

          <div className="tip-card">
            <div className="tip-mark">✳</div>
            <span className="section-label">A note for today</span>
            <h3>
              Good drainage helps<br />your rice breathe.
            </h3>
            <p>Standing water can make some leaf problems harder to manage.</p>
            <a href="https://icar.gov.in" target="_blank" rel="noreferrer">
              Read field guidance ↗
            </a>
          </div>
        </div>
      </div>
    </FarmerLayout>
  );
}
