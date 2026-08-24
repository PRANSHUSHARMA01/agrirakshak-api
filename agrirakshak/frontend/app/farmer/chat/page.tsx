"use client";

import React, { useState } from "react";
import { FarmerLayout } from "@/components/farmer/FarmerLayout";
import { ChatWindow } from "@/components/farmer/ChatWindow";

export default function FarmerChatPage() {
  const [language, setLanguage] = useState("en");

  return (
    <FarmerLayout language={language} onLanguageChange={setLanguage}>
      <div className="content-wrap narrow">
        <ChatWindow />
      </div>
    </FarmerLayout>
  );
}
