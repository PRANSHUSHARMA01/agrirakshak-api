"use client";

import React, { useState, useEffect } from "react";
import { OfficerLayout } from "@/components/officer/OfficerLayout";
import { DiseaseMap } from "@/components/officer/DiseaseMap";
import { getCases } from "@/lib/api";
import { FarmerCase } from "@/lib/types";

export default function OfficerMapPage() {
  const [cases, setCases] = useState<FarmerCase[]>([]);

  useEffect(() => {
    getCases().then(setCases).catch(console.error);
  }, []);

  return (
    <OfficerLayout>
      <div className="space-y-4">
        <div className="section-intro">
          <span className="section-label">District Map</span>
          <h2>Geographic Disease Distribution</h2>
        </div>
        <DiseaseMap cases={cases} />
      </div>
    </OfficerLayout>
  );
}
