"use client";

import React from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { FarmerCase } from "@/lib/types";

interface AnalyticsChartsProps {
  cases: FarmerCase[];
}

const COLORS = ["#16a34a", "#0284c7", "#d97706", "#dc2626", "#8b5cf6", "#059669"];

// Demo Data fallback if database records are empty
const DEMO_CASES_OVER_TIME = [
  { day: "Mon", cases: 12, escalated: 2 },
  { day: "Tue", cases: 19, escalated: 4 },
  { day: "Wed", cases: 15, escalated: 1 },
  { day: "Thu", cases: 27, escalated: 5 },
  { day: "Fri", cases: 32, escalated: 6 },
  { day: "Sat", cases: 22, escalated: 3 },
  { day: "Sun", cases: 18, escalated: 2 },
];

const DEMO_TOP_DISEASES = [
  { disease: "Bacterial Leaf Blight", count: 42 },
  { disease: "Rice Blast", count: 35 },
  { disease: "Rice Skipper", count: 28 },
  { disease: "White Stem Borer", count: 21 },
  { disease: "Turcicum Blight", count: 16 },
  { disease: "Brown Spot", count: 12 },
];

const DEMO_CROP_DISTRIBUTION = [
  { name: "Rice", value: 65 },
  { name: "Maize", value: 25 },
  { name: "Wheat/Other", value: 10 },
];

const DEMO_REGIONAL_CASES = [
  { region: "Meerut", cases: 45 },
  { region: "Ghaziabad", cases: 38 },
  { region: "Lucknow", cases: 32 },
  { region: "Kanpur", cases: 24 },
  { region: "Varanasi", cases: 18 },
];

export const AnalyticsCharts: React.FC<AnalyticsChartsProps> = ({ cases }) => {
  const isDemo = cases.length === 0;

  return (
    <div className="space-y-6">
      {isDemo && (
        <div className="bg-blue-50 border border-blue-200 p-3 rounded-xl text-xs font-semibold text-blue-800 flex items-center justify-between">
          <span>ℹ Showing demo analytics data for Smart India Hackathon preview.</span>
          <span className="bg-blue-200 text-blue-900 px-2 py-0.5 rounded font-extrabold text-[10px]">
            DEMO MODE
          </span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Cases Over Time */}
        <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-gray-800">Infection Cases Over Time</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={DEMO_CASES_OVER_TIME}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="day" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Line type="monotone" dataKey="cases" stroke="#16a34a" strokeWidth={3} name="Total Scans" />
                <Line type="monotone" dataKey="escalated" stroke="#dc2626" strokeWidth={2} name="Escalations" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Top Diseases */}
        <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-gray-800">Top Identified Diseases & Pests</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={DEMO_TOP_DISEASES}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="disease" tick={{ fontSize: 10 }} interval={0} angle={-15} textAnchor="end" />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#0284c7" radius={[6, 6, 0, 0]} name="Cases Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Crop Distribution */}
        <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-gray-800">Crop Type Breakdown</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={DEMO_CROP_DISTRIBUTION}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {DEMO_CROP_DISTRIBUTION.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend wrapperStyle={{ fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Regional Outbreak Distribution */}
        <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-gray-800">Regional Outbreak Density</h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={DEMO_REGIONAL_CASES} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" tick={{ fontSize: 11 }} />
                <YAxis type="category" dataKey="region" tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="cases" fill="#16a34a" radius={[0, 6, 6, 0]} name="Reported Cases" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
