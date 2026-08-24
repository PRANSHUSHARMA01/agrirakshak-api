"use client";

import React from "react";
import { Globe } from "lucide-react";

interface LanguageSelectorProps {
  language: string;
  onLanguageChange: (lang: string) => void;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  language,
  onLanguageChange,
}) => {
  return (
    <div className="flex items-center space-x-2 bg-agri-50 px-3 py-1.5 rounded-full border border-agri-200">
      <Globe className="w-4 h-4 text-agri-700" />
      <select
        value={language}
        onChange={(e) => onLanguageChange(e.target.value)}
        className="bg-transparent text-sm font-semibold text-agri-800 outline-none cursor-pointer"
      >
        <option value="en">English (English)</option>
        <option value="hi">हिंदी (Hindi)</option>
      </select>
    </div>
  );
};
