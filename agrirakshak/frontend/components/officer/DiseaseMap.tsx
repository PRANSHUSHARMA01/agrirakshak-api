"use client";

import React, { useState, useEffect } from "react";
import { FarmerCase } from "@/lib/types";

// Dynamic client component wrapper for Leaflet
interface DiseaseMapProps {
  cases: FarmerCase[];
}

// Sample fallback coordinates across northern/central Indian regions
const SAMPLE_LOCATIONS = [
  { name: "Delhi NCR", lat: 28.6139, lng: 77.2090 },
  { name: "Meerut", lat: 28.9845, lng: 77.7064 },
  { name: "Ghaziabad", lat: 28.6692, lng: 77.4538 },
  { name: "Lucknow", lat: 26.8467, lng: 80.9462 },
  { name: "Kanpur", lat: 26.4499, lng: 80.3319 },
  { name: "Agra", lat: 27.1767, lng: 78.0081 },
  { name: "Varanasi", lat: 25.3176, lng: 82.9739 },
];

export const DiseaseMap: React.FC<DiseaseMapProps> = ({ cases }) => {
  const [filter, setFilter] = useState("All");
  const [viewMode, setViewMode] = useState<"markers" | "heatmap">("markers");
  const [LeafletMap, setLeafletMap] = useState<any>(null);

  useEffect(() => {
    // Dynamically import leaflet and react-leaflet on client
    Promise.all([
      import("react-leaflet"),
      import("leaflet")
    ]).then(([ReactLeaflet, L]) => {
      // Fix default marker icon paths in Leaflet
      delete (L.Icon.Default.prototype as any)._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
        iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
      });
      setLeafletMap({ ReactLeaflet, L });
    });
  }, []);

  // Filter cases based on category dropdown
  const filteredCases = cases.filter((c) => {
    if (filter === "All") return true;
    if (filter === "Rice") return c.crop.toLowerCase() === "rice";
    if (filter === "Maize") return c.crop.toLowerCase() === "maize";
    if (filter === "Disease") return !c.predicted_class?.toLowerCase().includes("borer") && !c.predicted_class?.toLowerCase().includes("skipper");
    if (filter === "Pest") return c.predicted_class?.toLowerCase().includes("borer") || c.predicted_class?.toLowerCase().includes("skipper");
    if (filter === "High Risk") return c.needs_expert_review;
    return true;
  });

  if (!LeafletMap) {
    return (
      <div className="w-full h-96 bg-gray-100 rounded-2xl border border-gray-200 flex items-center justify-center text-sm font-semibold text-gray-500 animate-pulse">
        Loading Outbreak Map (Leaflet)...
      </div>
    );
  }

  const { MapContainer, TileLayer, Marker, Popup, CircleMarker } = LeafletMap.ReactLeaflet;

  return (
    <div className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm space-y-4">
      {/* Controls & Filter Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-gray-100 pb-3">
        <div>
          <h3 className="text-base font-bold text-gray-800">Disease Outbreak Map</h3>
          <p className="text-xs text-gray-500">Real-time geographic distribution of crop infection cases</p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Mode Toggle */}
          <div className="bg-gray-100 p-1 rounded-xl flex items-center text-xs font-bold text-gray-600">
            <button
              onClick={() => setViewMode("markers")}
              className={`px-3 py-1 rounded-lg transition ${
                viewMode === "markers" ? "bg-white text-agri-700 shadow-sm" : "hover:text-gray-900"
              }`}
            >
              📍 Markers
            </button>
            <button
              onClick={() => setViewMode("heatmap")}
              className={`px-3 py-1 rounded-lg transition ${
                viewMode === "heatmap" ? "bg-white text-agri-700 shadow-sm" : "hover:text-gray-900"
              }`}
            >
              🔥 Heatmap
            </button>
          </div>

          {/* Category Filter */}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-gray-50 border border-gray-200 text-xs font-bold text-gray-700 rounded-xl px-3 py-1.5 focus:outline-none cursor-pointer"
          >
            <option value="All">All Categories</option>
            <option value="Rice">Rice Crops</option>
            <option value="Maize">Maize Crops</option>
            <option value="Disease">Fungal/Bacterial Diseases</option>
            <option value="Pest">Insect Pests</option>
            <option value="High Risk">High Risk Cases</option>
          </select>
        </div>
      </div>

      {/* Map View */}
      <div className="w-full h-96 rounded-xl overflow-hidden border border-gray-200 z-0">
        <MapContainer
          center={[27.5, 78.5]}
          zoom={6}
          style={{ width: "100%", height: "100%" }}
          scrollWheelZoom={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {filteredCases.map((c, idx) => {
            const loc = SAMPLE_LOCATIONS[idx % SAMPLE_LOCATIONS.length];
            const lat = c.latitude || loc.lat;
            const lng = c.longitude || loc.lng;
            const isEscalated = c.needs_expert_review;

            if (viewMode === "heatmap") {
              return (
                <CircleMarker
                  key={`heat-${c.id || idx}`}
                  center={[lat, lng]}
                  radius={isEscalated ? 24 : 16}
                  pathOptions={{
                    color: isEscalated ? "red" : "#22c55e",
                    fillColor: isEscalated ? "#ef4444" : "#4ade80",
                    fillOpacity: 0.45,
                    stroke: false,
                  }}
                />
              );
            }

            return (
              <Marker key={`marker-${c.id || idx}`} position={[lat, lng]}>
                <Popup>
                  <div className="text-xs space-y-1 p-1">
                    <strong className="block text-sm text-gray-900 font-bold">
                      {c.predicted_class?.replace(/_/g, " ")}
                    </strong>
                    <span className="block text-gray-600">Crop: {c.crop}</span>
                    <span className="block text-gray-600">
                      Confidence: {Math.round(c.confidence * 100)}%
                    </span>
                    <span className="block text-gray-500">Location: {loc.name}</span>
                    {isEscalated && (
                      <span className="inline-block bg-red-100 text-red-800 text-[10px] font-bold px-2 py-0.5 rounded-full mt-1">
                        ⚠ Low Confidence / Escalated
                      </span>
                    )}
                  </div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
};
