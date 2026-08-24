"use client";

import React from "react";
import { CheckCircle, ShieldCheck, PhoneCall } from "lucide-react";
import { Advisory } from "@/lib/types";

interface AdvisoryCardProps {
  advisory: Advisory;
}

export const AdvisoryCard: React.FC<AdvisoryCardProps> = ({ advisory }) => {
  return (
    <div className="w-full bg-white rounded-2xl border border-gray-100 shadow-sm p-4 space-y-4">
      {/* Overview Explanation */}
      <div className="bg-agri-50/60 p-3.5 rounded-xl border border-agri-100">
        <p className="text-sm text-agri-900 leading-relaxed font-medium">
          {advisory.diagnosis_or_answer}
        </p>
      </div>

      {/* Recommended Actions */}
      {advisory.recommended_actions.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-xs font-bold uppercase tracking-wider text-agri-800 flex items-center gap-1.5">
            <CheckCircle className="w-4 h-4 text-agri-600" />
            What You Should Do
          </h4>
          <ul className="space-y-2">
            {advisory.recommended_actions.map((act, i) => (
              <li key={i} className="flex items-start gap-2.5 text-xs text-gray-700 bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                <span className="w-4 h-4 rounded-full bg-agri-100 text-agri-700 text-[10px] font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                  ✓
                </span>
                <span className="leading-normal">{act}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Safety Notes */}
      {advisory.safety_notes.length > 0 && (
        <div className="space-y-2 pt-1 border-t border-gray-100">
          <h4 className="text-xs font-bold uppercase tracking-wider text-amber-800 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-amber-600" />
            Safety Information
          </h4>
          <ul className="space-y-1.5">
            {advisory.safety_notes.map((note, i) => (
              <li key={i} className="text-xs text-amber-900 bg-amber-50/70 p-2.5 rounded-lg border border-amber-100 leading-relaxed">
                • {note}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* KVK Helpline Note */}
      <div className="bg-gray-50 p-3 rounded-xl flex items-center justify-between text-xs text-gray-600">
        <span className="flex items-center gap-1.5 font-medium">
          <PhoneCall className="w-3.5 h-3.5 text-agri-600" />
          Kisan Call Center Helpline:
        </span>
        <a href="tel:18001801551" className="font-bold text-agri-700 hover:underline">
          1800-180-1551
        </a>
      </div>
    </div>
  );
};
