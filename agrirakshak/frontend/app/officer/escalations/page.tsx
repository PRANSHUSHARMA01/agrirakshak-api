"use client";

import React, { useState, useEffect } from "react";
import { OfficerLayout } from "@/components/officer/OfficerLayout";
import { EscalationPanel } from "@/components/officer/EscalationPanel";
import { getEscalations } from "@/lib/api";
import { EscalationCase } from "@/lib/types";

export default function OfficerEscalationsPage() {
  const [escalations, setEscalations] = useState<EscalationCase[]>([]);

  const loadEscalations = async () => {
    try {
      const data = await getEscalations();
      setEscalations(data);
    } catch (err) {
      console.error("Error loading escalations:", err);
    }
  };

  useEffect(() => {
    loadEscalations();
  }, []);

  return (
    <OfficerLayout>
      <div className="space-y-4">
        <div className="section-intro">
          <span className="section-label">Expert Review Queue</span>
          <h2>Awaiting Officer Confirmation</h2>
        </div>
        <EscalationPanel escalations={escalations} onResolved={loadEscalations} />
      </div>
    </OfficerLayout>
  );
}
