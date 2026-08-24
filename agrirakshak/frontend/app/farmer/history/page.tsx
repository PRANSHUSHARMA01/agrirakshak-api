"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, Leaf, History } from "lucide-react";
import { FarmerLayout } from "@/components/farmer/FarmerLayout";
import { getCases } from "@/lib/api";
import { FarmerCase } from "@/lib/types";

export default function FarmerHistoryPage() {
  const [cases, setCases] = useState<FarmerCase[]>([]);

  useEffect(() => {
    getCases().then(setCases).catch(console.error);
  }, []);

  return (
    <FarmerLayout>
      <div className="content-wrap">
        <div className="page-header">
          <div>
            <span className="section-label">Your reports</span>
            <h1>A clear record of your field.</h1>
          </div>
          <Link href="/farmer/diagnose" className="button button-ink">
            Scan a crop <ArrowRight size={17} />
          </Link>
        </div>
        <p className="lead-copy">Every leaf photo and advisory saved for seasonal reference.</p>

        {cases.length === 0 ? (
          <div className="empty-state">
            <div className="upload-mark">
              <Leaf size={25} />
            </div>
            <h2>No reports saved yet.</h2>
            <p>Take a clear photo of an affected crop leaf to generate your first field report.</p>
            <Link href="/farmer/diagnose" className="button button-ink">
              Scan your crop <ArrowRight size={17} />
            </Link>
          </div>
        ) : (
          <div className="space-y-3 mt-6">
            {cases.map((c) => (
              <div key={c.id} className="recent-card">
                <div className="card-heading">
                  <div>
                    <span className="section-label">Report #{c.id}</span>
                    <h3>{c.crop} · {c.predicted_class?.replace(/_/g, " ")}</h3>
                  </div>
                  <span className={`status-pill ${c.needs_expert_review ? "muted-pill" : "success"}`}>
                    {c.needs_expert_review ? "Awaiting Expert Review" : "Diagnosed"}
                  </span>
                </div>
                <div className="report-row">
                  <img src="/agrirakshak-rice-detail.jpg" alt="Report leaf thumbnail" />
                  <div>
                    <p>Scanned {new Date(c.created_at).toLocaleDateString()}</p>
                    <strong>{Math.round(c.confidence * 100)}% AI confidence</strong>
                    <span>Location: {c.location_name || "Karnal, Haryana"}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </FarmerLayout>
  );
}
