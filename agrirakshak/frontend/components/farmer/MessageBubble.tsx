"use client";

import React from "react";
import { User, Bot } from "lucide-react";
import { Advisory, PredictionResult, WeatherRisk } from "@/lib/types";
import { DiagnosisCard } from "./DiagnosisCard";
import { AdvisoryCard } from "./AdvisoryCard";
import { WeatherRiskCard } from "./WeatherRiskCard";

export interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text?: string;
  image_base64?: string;
  advisory?: Advisory;
  prediction_result?: PredictionResult;
  weather_risk?: WeatherRisk;
  timestamp: string;
}

interface MessageBubbleProps {
  message: ChatMessage;
  onEscalate?: () => void;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onEscalate }) => {
  const isUser = message.sender === "user";

  return (
    <div className={`flex gap-2.5 mb-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shadow-sm flex-shrink-0 ${
        isUser ? 'bg-agri-700 text-white' : 'bg-agri-100 text-agri-800 border border-agri-200'
      }`}>
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Bubble container */}
      <div className={`max-w-[88%] space-y-2 ${isUser ? 'items-end' : 'items-start'}`}>
        {/* User image attachment */}
        {message.image_base64 && (
          <img
            src={message.image_base64}
            alt="Uploaded Leaf"
            className="w-48 h-36 object-cover rounded-xl border border-gray-200 shadow-sm"
          />
        )}

        {/* Text bubble */}
        {message.text && (
          <div className={`px-4 py-3 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-sm ${
            isUser
              ? 'bg-agri-600 text-white rounded-tr-none'
              : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none'
          }`}>
            {message.text}
          </div>
        )}

        {/* AI Diagnosis Card */}
        {message.prediction_result && (
          <DiagnosisCard
            prediction={message.prediction_result}
            onEscalate={onEscalate}
          />
        )}

        {/* Weather Risk Card */}
        {message.weather_risk && (
          <WeatherRiskCard weatherRisk={message.weather_risk} />
        )}

        {/* Advisory Actions Card */}
        {message.advisory && (
          <AdvisoryCard advisory={message.advisory} />
        )}

        <span className="text-[10px] text-gray-400 block px-1">
          {message.timestamp}
        </span>
      </div>
    </div>
  );
};
