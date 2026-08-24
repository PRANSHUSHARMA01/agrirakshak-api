"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, CloudSun } from "lucide-react";
import { FarmerLayout } from "@/components/farmer/FarmerLayout";
import { WeatherRiskCard } from "@/components/farmer/WeatherRiskCard";
import { getWeatherRisk } from "@/lib/api";
import { WeatherRisk } from "@/lib/types";

export default function FarmerWeatherPage() {
  const [weatherRisk, setWeatherRisk] = useState<WeatherRisk | null>(null);

  useEffect(() => {
    getWeatherRisk().then(setWeatherRisk).catch(console.error);
  }, []);

  return (
    <FarmerLayout>
      <div className="content-wrap">
        <div className="page-header">
          <div>
            <span className="section-label">Weather risk</span>
            <h1>Know what the sky may bring.</h1>
          </div>
          <Link href="/farmer/diagnose" className="button button-ink">
            Scan a crop <ArrowRight size={17} />
          </Link>
        </div>
        <p className="lead-copy">Real-time humidity, temperature, and 3-day forecast disease outbreak risk alerts.</p>

        {weatherRisk && <WeatherRiskCard weatherRisk={weatherRisk} crop="Rice" />}
      </div>
    </FarmerLayout>
  );
}
