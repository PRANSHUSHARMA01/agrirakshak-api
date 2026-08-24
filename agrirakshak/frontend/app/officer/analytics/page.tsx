"use client";

import React, { useState, useEffect } from "react";
import { OfficerLayout } from "@/components/officer/OfficerLayout";
import { AnalyticsCharts } from "@/components/officer/AnalyticsCharts";
import { getCases } from "@/lib/api";
import { FarmerCase } from "@/lib/types";

export default function OfficerAnalyticsPage() {
  const [cases, setCases] = useState<FarmerCase[]>([]);

  useEffect(() => {
    getCases().then(setCases).catch(console.error);
  }, []);

  return (
    <OfficerLayout>
      <div className="space-y-4">
        <div className="section-intro">
          <span className="section-label">District Analytics</span>
          <h2>National Disease Trends</h2>
        </div>
        <AnalyticsCharts cases={cases} />
      </div>
    </OfficerLayout>
  );
}
