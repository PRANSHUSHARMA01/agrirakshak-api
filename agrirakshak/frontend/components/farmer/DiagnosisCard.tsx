"use client";

import React from "react";
import { AlertTriangle, CheckCircle2, ShieldAlert, ArrowUpRight } from "lucide-react";
import { PredictionResult } from "@/lib/types";

interface DiagnosisCardProps {
  prediction: PredictionResult;
  crop?: string;
  onEscalate?: () => void;
}

export const DiagnosisCard: React.FC<DiagnosisCardProps> = ({
  prediction,
  crop = "Rice",
  onEscalate,
}) => {
  const confPct = Math.round(prediction.confidence * 100);
  const isLowConf = prediction.needs_expert_review;

  return (
    <div className="w-full bg-white rounded-2xl border border-gray-100 shadow-md overflow-hidden">
      {/* Header Banner */}
      <div className={`p-4 ${isLowConf ? 'bg-amber-500' : 'bg-agri-600'} text-white flex items-center justify-between`}>
        <div className="flex items-center gap-2">
          {isLowConf ? (
            <AlertTriangle className="w-6 h-6 text-amber-100" />
          ) : (
            <CheckCircle2 className="w-6 h-6 text-green-100" />
          )}
          <div>
            <h4 className="text-xs uppercase tracking-wider font-semibold opacity-90">
              AI Diagnosis Result
            </h4>
            <h3 className="text-lg font-bold">
              {prediction.predicted_class.replace(/_/g, " ")}
            </h3>
          </div>
        </div>
        <div className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-right">
          <span className="text-xs block font-medium opacity-80">Confidence</span>
          <span className="text-base font-extrabold">{confPct}%</span>
        </div>
      </div>

      {/* Content body */}
      <div className="p-4 space-y-3">
        <div className="flex justify-between items-center text-sm py-1 border-b border-gray-100">
          <span className="text-gray-500 font-medium">Target Crop:</span>
          <span className="font-semibold text-gray-800">{crop}</span>
        </div>

        {isLowConf && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-3.5 space-y-2">
            <div className="flex items-start gap-2 text-amber-800 text-xs font-semibold">
              <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
              <span>Low-confidence diagnosis ({confPct}% &lt; 60%)</span>
            </div>
            <p className="text-xs text-amber-700 leading-relaxed">
              This detection result may not be fully reliable. We recommend escalating this case to an agricultural expert officer.
            </p>
            {onEscalate && (
              <button
                onClick={onEscalate}
                className="w-full mt-1 bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs py-2 px-3 rounded-lg flex items-center justify-center gap-1 shadow-sm transition"
              >
                Send to Agricultural Expert
                <ArrowUpRight className="w-4 h-4" />
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
