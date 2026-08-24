"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, HeartHandshake, PhoneCall } from "lucide-react";
import { FarmerLayout } from "@/components/farmer/FarmerLayout";
import { getEscalations } from "@/lib/api";
import { EscalationCase } from "@/lib/types";

export default function FarmerExpertPage() {
  const [escalations, setEscalations] = useState<EscalationCase[]>([]);

  useEffect(() => {
    getEscalations().then(setEscalations).catch(console.error);
  }, []);

  return (
    <FarmerLayout>
      <div className="content-wrap">
        <div className="page-header">
          <div>
            <span className="section-label">Expert help</span>
            <h1>When you need another pair of eyes.</h1>
          </div>
          <Link href="/farmer/diagnose" className="button button-ink">
            Scan a crop <ArrowRight size={17} />
          </Link>
        </div>
        <p className="lead-copy">Direct referral and escalation connection to Block Agricultural Officers and KVK experts.</p>

        <div className="space-y-4 max-w-2xl">
          <div className="tip-card">
            <div className="tip-mark">📞</div>
            <span className="section-label">Kisan Call Center</span>
            <h3>Toll-Free Agricultural Support</h3>
            <p>Speak directly with certified extension scientists and officers in Hindi or English.</p>
            <a href="tel:18001801551" className="text-lg font-bold text-agri-900 block mt-2">
              1800-180-1551
            </a>
          </div>

          <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-3">
            <h3 className="text-sm font-bold text-gray-800">Your Escalated Cases Status</h3>
            {escalations.length === 0 ? (
              <p className="text-xs text-gray-500">No active escalations. When AI confidence is under 60%, your scan is sent here automatically.</p>
            ) : (
              <div className="space-y-2">
                {escalations.map((e) => (
                  <div key={e.id} className="p-3 bg-gray-50 rounded-lg border border-gray-200 text-xs flex justify-between items-center">
                    <div>
                      <strong className="block text-gray-900">Case #{e.farmer_case_id} — {e.farmer_case?.crop || "Crop"}</strong>
                      <span className="text-gray-500">Reason: {e.reason}</span>
                      {e.expert_diagnosis && (
                        <span className="block font-bold text-agri-800 mt-1">Confirmed: {e.expert_diagnosis}</span>
                      )}
                    </div>
                    <span className={`px-2.5 py-1 rounded-full font-bold uppercase text-[10px] ${
                      e.status === "resolved" ? "bg-green-100 text-green-800" : "bg-amber-100 text-amber-800"
                    }`}>
                      {e.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </FarmerLayout>
  );
}
