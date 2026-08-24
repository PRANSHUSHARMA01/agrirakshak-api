"use client";

import React, { useState } from "react";
import { Search, Filter, AlertCircle, CheckCircle } from "lucide-react";
import { FarmerCase } from "@/lib/types";

interface CaseTableProps {
  cases: FarmerCase[];
}

export const CaseTable: React.FC<CaseTableProps> = ({ cases }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const filtered = cases.filter((c) => {
    const matchesSearch =
      c.crop.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (c.predicted_class || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.session_id.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus =
      statusFilter === "all" ||
      (statusFilter === "escalated" && c.needs_expert_review) ||
      (statusFilter === "resolved" && !c.needs_expert_review);

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 space-y-4">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-gray-800">Recorded Cases Registry</h3>
          <p className="text-xs text-gray-500">Comprehensive log of crop disease scans across regions</p>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          {/* Search Box */}
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by crop, disease, session ID..."
              className="w-full bg-gray-50 border border-gray-200 text-xs text-gray-800 rounded-xl pl-9 pr-3 py-2 focus:outline-none focus:border-agri-500"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-gray-50 border border-gray-200 text-xs font-semibold text-gray-700 rounded-xl px-3 py-2 focus:outline-none"
          >
            <option value="all">All Status</option>
            <option value="escalated">Escalated</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto border border-gray-100 rounded-xl">
        <table className="w-full text-left text-xs">
          <thead className="bg-gray-50 border-b border-gray-100 text-gray-500 font-bold uppercase tracking-wider">
            <tr>
              <th className="p-3">Case ID</th>
              <th className="p-3">Date</th>
              <th className="p-3">Crop</th>
              <th className="p-3">AI Prediction</th>
              <th className="p-3">Confidence</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-6 text-gray-400">
                  No crop cases found matching search criteria.
                </td>
              </tr>
            ) : (
              filtered.map((c) => (
                <tr key={c.id} className="hover:bg-gray-50/80 transition">
                  <td className="p-3 font-semibold text-gray-900">#{c.id}</td>
                  <td className="p-3 text-gray-500">
                    {new Date(c.created_at).toLocaleDateString()}
                  </td>
                  <td className="p-3 font-semibold text-gray-800">{c.crop}</td>
                  <td className="p-3 font-bold text-agri-800">
                    {c.predicted_class?.replace(/_/g, " ")}
                  </td>
                  <td className="p-3">
                    <span className={`font-extrabold ${c.confidence < 0.6 ? 'text-amber-600' : 'text-green-600'}`}>
                      {Math.round(c.confidence * 100)}%
                    </span>
                  </td>
                  <td className="p-3">
                    {c.needs_expert_review ? (
                      <span className="inline-flex items-center gap-1 bg-amber-50 text-amber-800 border border-amber-200 px-2.5 py-0.5 rounded-full font-bold text-[10px]">
                        <AlertCircle className="w-3 h-3 text-amber-600" />
                        Pending Review
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 bg-green-50 text-green-800 border border-green-200 px-2.5 py-0.5 rounded-full font-bold text-[10px]">
                        <CheckCircle className="w-3 h-3 text-green-600" />
                        Confirmed / Diagnosed
                      </span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
