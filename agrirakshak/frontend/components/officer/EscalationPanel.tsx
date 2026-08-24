"use client";

import React, { useState } from "react";
import { AlertTriangle, CheckCircle2, ShieldAlert, Send, Loader2 } from "lucide-react";
import { resolveEscalation } from "@/lib/api";
import { EscalationCase } from "@/lib/types";

interface EscalationPanelProps {
  escalations: EscalationCase[];
  onResolved: () => void;
}

export const EscalationPanel: React.FC<EscalationPanelProps> = ({
  escalations,
  onResolved,
}) => {
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [diagnosis, setDiagnosis] = useState("");
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");

  const pendingList = escalations.filter((e) => e.status === "pending");

  const handleResolve = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedId || !diagnosis) return;

    setIsSubmitting(true);
    setSuccessMsg("");

    try {
      await resolveEscalation(selectedId, diagnosis, notes || "Confirmed by Agricultural Extension Officer.");
      setSuccessMsg("✓ Escalation resolved and confirmed diagnosis persisted to database.");
      setSelectedId(null);
      setDiagnosis("");
      setNotes("");
      onResolved();
    } catch (err) {
      console.error("Failed to resolve escalation:", err);
      alert("Failed to resolve escalation. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm space-y-4">
      <div className="flex justify-between items-center pb-3 border-b border-gray-200">
        <div>
          <span className="section-label">EXPERT ESCALATIONS QUEUE</span>
          <h3 className="font-bold text-lg text-[#163d2f]">Awaiting Review</h3>
        </div>
        <span className="bg-amber-100 text-amber-900 font-bold px-2.5 py-1 rounded-full text-xs">
          {pendingList.length} Pending
        </span>
      </div>

      {successMsg && (
        <div className="bg-green-50 text-green-800 border border-green-200 p-3 rounded-lg text-xs font-bold">
          {successMsg}
        </div>
      )}

      {pendingList.length === 0 ? (
        <div className="text-center py-8 space-y-2 text-gray-500">
          <CheckCircle2 size={32} className="mx-auto text-green-600" />
          <p className="text-xs font-semibold">Queue is clear! All low-confidence AI cases resolved.</p>
        </div>
      ) : (
        <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
          {pendingList.map((item) => {
            const isSelected = selectedId === item.id;
            return (
              <div
                key={item.id}
                className={`p-3.5 rounded-xl border transition ${
                  isSelected
                    ? "border-[#163d2f] bg-[#f8f6ef]"
                    : "border-gray-200 bg-gray-50 hover:bg-gray-100"
                }`}
              >
                <div className="flex justify-between items-start text-xs mb-1">
                  <span className="font-bold text-[#163d2f]">Case #{item.farmer_case_id}</span>
                  <span className="text-amber-800 bg-amber-100 px-2 py-0.5 rounded font-bold text-[10px]">
                    Low Confidence AI
                  </span>
                </div>

                <p className="text-xs text-gray-600 mb-2">
                  <strong>Crop:</strong> {item.farmer_case?.crop || "Rice"} | <strong>Reason:</strong> {item.reason}
                </p>

                {isSelected ? (
                  <form onSubmit={handleResolve} className="mt-3 pt-3 border-t border-gray-200 space-y-2.5">
                    <div>
                      <label className="block text-[11px] font-bold text-[#163d2f] mb-1">
                        Confirmed Diagnosis
                      </label>
                      <input
                        type="text"
                        value={diagnosis}
                        onChange={(e) => setDiagnosis(e.target.value)}
                        placeholder="e.g. Bacterial Leaf Blight"
                        required
                        className="w-full bg-white border border-gray-300 rounded px-2.5 py-1.5 text-xs text-gray-900 focus:outline-none focus:border-[#163d2f]"
                      />
                    </div>

                    <div>
                      <label className="block text-[11px] font-bold text-[#163d2f] mb-1">
                        Officer Advisory Notes
                      </label>
                      <textarea
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                        placeholder="Recommended treatment or field instructions..."
                        rows={2}
                        className="w-full bg-white border border-gray-300 rounded px-2.5 py-1.5 text-xs text-gray-900 focus:outline-none focus:border-[#163d2f]"
                      />
                    </div>

                    <div className="flex gap-2 justify-end pt-1">
                      <button
                        type="button"
                        onClick={() => setSelectedId(null)}
                        className="px-3 py-1.5 text-xs border border-gray-300 rounded text-gray-700 hover:bg-gray-100 font-semibold"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className="button button-ink !min-h-[32px] !px-3 !text-xs"
                      >
                        {isSubmitting ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />} Confirm Resolution
                      </button>
                    </div>
                  </form>
                ) : (
                  <button
                    onClick={() => {
                      setSelectedId(item.id);
                      setDiagnosis(item.farmer_case?.predicted_class?.replace(/_/g, " ") || "");
                    }}
                    className="button button-outline !min-h-[32px] !px-3 !text-xs !w-full"
                  >
                    Examine & Confirm Diagnosis
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
