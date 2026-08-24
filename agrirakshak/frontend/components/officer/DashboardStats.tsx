"use client";

import React from "react";
import { Activity, Calendar, ShieldAlert, Clock } from "lucide-react";
import { DashboardStats } from "@/lib/types";

interface DashboardStatsProps {
  stats: DashboardStats;
}

export const DashboardStatsCards: React.FC<DashboardStatsProps> = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Total Cases */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider block">
            Total Cases
          </span>
          <span className="text-2xl font-black text-gray-900 mt-1 block">
            {stats.total_cases}
          </span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-agri-50 text-agri-600 flex items-center justify-center">
          <Activity className="w-6 h-6" />
        </div>
      </div>

      {/* Today's Cases */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider block">
            Today's Cases
          </span>
          <span className="text-2xl font-black text-gray-900 mt-1 block">
            {stats.today_cases}
          </span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
          <Calendar className="w-6 h-6" />
        </div>
      </div>

      {/* High Risk Outbreak Areas */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider block">
            High Risk Areas
          </span>
          <span className="text-2xl font-black text-red-600 mt-1 block">
            {stats.high_risk_areas}
          </span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-red-50 text-red-600 flex items-center justify-center">
          <ShieldAlert className="w-6 h-6" />
        </div>
      </div>

      {/* Pending Expert Reviews */}
      <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider block">
            Pending Reviews
          </span>
          <span className="text-2xl font-black text-amber-600 mt-1 block">
            {stats.pending_expert_reviews}
          </span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
          <Clock className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
};
