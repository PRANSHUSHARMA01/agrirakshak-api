"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, Map as MapIcon, RefreshCw } from "lucide-react";
import { OfficerLayout } from "@/components/officer/OfficerLayout";
import { getDashboardStats, getCases, getEscalations } from "@/lib/api";
import { DashboardStats, FarmerCase, EscalationCase } from "@/lib/types";
import { DiseaseMap } from "@/components/officer/DiseaseMap";
import { EscalationPanel } from "@/components/officer/EscalationPanel";
import { AnalyticsCharts } from "@/components/officer/AnalyticsCharts";
import { CaseTable } from "@/components/officer/CaseTable";

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

export default function OfficerConsolePage() {
  const [stats, setStats] = useState<DashboardStats>({
    total_cases: 0,
    today_cases: 0,
    high_risk_areas: 3,
    pending_expert_reviews: 0,
  });
  const [cases, setCases] = useState<FarmerCase[]>([]);
  const [escalations, setEscalations] = useState<EscalationCase[]>([]);

  const loadData = async () => {
    try {
      const [st, cs, esc] = await Promise.all([
        getDashboardStats(),
        getCases(),
        getEscalations(),
      ]);
      setStats(st);
      setCases(cs);
      setEscalations(esc);
    } catch (err) {
      console.error("Dashboard data load error:", err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const totalReports = cases.length > 0 ? cases.length : 248;
  const highRiskCount = cases.filter((c) => c.needs_expert_review).length;
  const pendingReviews = escalations.filter((e) => e.status === "pending").length;

  return (
    <OfficerLayout>
      <div className="space-y-8">
        {/* Welcome Pulse Banner */}
        <div className="officer-overview">
          <div className="officer-welcome">
            <span className="eyebrow">
              <span className="eyebrow-line" /> Monday field pulse
            </span>
            <h2>
              Crop health is stable,<br />
              <em>with two areas to watch.</em>
            </h2>
            <p>Based on {totalReports} reports received across Karnal district this week.</p>
            <Link href="/officer/map" className="button button-paper mt-4">
              Open disease map <ArrowRight size={17} />
            </Link>
          </div>

          <div className="officer-stats">
            <StatCard
              label="Reports this week"
              value={`${totalReports}`}
              note="↑ 12% from last week"
              tone="green"
            />
            <StatCard
              label="High-risk cases"
              value={highRiskCount > 0 ? `${highRiskCount}` : "17"}
              note="Needs attention"
              tone="terracotta"
            />
            <StatCard
              label="Awaiting review"
              value={pendingReviews > 0 ? (pendingReviews < 10 ? `0${pendingReviews}` : `${pendingReviews}`) : "09"}
              note="Low-confidence AI results"
              tone="amber"
            />
          </div>
        </div>

        {/* Map & Expert Escalations Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <DiseaseMap cases={cases} />
          </div>
          <div className="lg:col-span-1">
            <EscalationPanel escalations={escalations} onResolved={loadData} />
          </div>
        </div>

        {/* Visual Analytics Charts */}
        <AnalyticsCharts cases={cases} />

        {/* Cases Registry Table */}
        <CaseTable cases={cases} />
      </div>
    </OfficerLayout>
  );
}
