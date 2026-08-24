"use client";

import React, { useState, useEffect } from "react";
import { OfficerLayout } from "@/components/officer/OfficerLayout";
import { CaseTable } from "@/components/officer/CaseTable";
import { getCases } from "@/lib/api";
import { FarmerCase } from "@/lib/types";

export default function OfficerCasesPage() {
  const [cases, setCases] = useState<FarmerCase[]>([]);

  useEffect(() => {
    getCases().then(setCases).catch(console.error);
  }, []);

  return (
    <OfficerLayout>
      <div className="space-y-4">
        <div className="section-intro">
          <span className="section-label">Cases Registry</span>
          <h2>All Diagnostic Reports</h2>
        </div>
        <CaseTable cases={cases} />
      </div>
    </OfficerLayout>
  );
}
