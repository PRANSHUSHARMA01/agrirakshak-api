"use client";

import React from "react";
import { CloudRain, Sun, Wind, Thermometer, Droplets, AlertTriangle, ShieldCheck } from "lucide-react";
import { WeatherRisk } from "@/lib/types";

interface WeatherRiskCardProps {
  weatherRisk: WeatherRisk;
  crop?: string;
}

export const WeatherRiskCard: React.FC<WeatherRiskCardProps> = ({
  weatherRisk,
  crop = "Rice",
}) => {
  const isHigh = weatherRisk.risk_level === "HIGH";
  const isMed = weatherRisk.risk_level === "MEDIUM";

  const badgeColor = isHigh
    ? "bg-red-500 text-white"
    : isMed
    ? "bg-amber-500 text-white"
    : "bg-green-600 text-white";

  return (
    <div className="w-full bg-white rounded-2xl border border-gray-100 shadow-sm p-4 space-y-3">
      {/* Title & Badge */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <CloudRain className="w-5 h-5 text-sky-600" />
          <h3 className="text-sm font-bold text-gray-800">
            Weather Disease Risk ({crop})
          </h3>
        </div>
        <span className={`text-xs px-2.5 py-1 rounded-full font-extrabold uppercase tracking-wide ${badgeColor}`}>
          {weatherRisk.risk_level} RISK
        </span>
      </div>

      {/* Temp / Humidity Grid */}
      <div className="grid grid-cols-2 gap-2 bg-sky-50/50 p-3 rounded-xl border border-sky-100">
        <div className="flex items-center gap-2">
          <Thermometer className="w-4 h-4 text-orange-500" />
          <div>
            <span className="text-[10px] uppercase font-semibold text-gray-400 block">Temperature</span>
            <span className="text-sm font-extrabold text-gray-800">
              {weatherRisk.temperature_celsius ?? 28.5}°C
            </span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Droplets className="w-4 h-4 text-sky-500" />
          <div>
            <span className="text-[10px] uppercase font-semibold text-gray-400 block">Humidity</span>
            <span className="text-sm font-extrabold text-gray-800">
              {weatherRisk.humidity_percent ?? 82}%
            </span>
          </div>
        </div>
      </div>

      {/* Explanation */}
      <p className="text-xs text-gray-700 leading-relaxed bg-gray-50 p-3 rounded-xl border border-gray-100">
        {weatherRisk.reason}
      </p>

      {/* Recommended Actions */}
      {weatherRisk.recommended_actions.length > 0 && (
        <div className="space-y-1.5 pt-1">
          <h4 className="text-[11px] font-bold text-gray-600 uppercase tracking-wider">
            Preventive Actions
          </h4>
          <ul className="space-y-1 text-xs text-gray-700">
            {weatherRisk.recommended_actions.map((act, i) => (
              <li key={i} className="flex items-start gap-1.5">
                <span className="text-agri-600 font-bold">•</span>
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
