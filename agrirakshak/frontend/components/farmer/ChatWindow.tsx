"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, Camera, Upload, Bot, User, Sparkles, Loader2, LifeBuoy, Check, AlertTriangle } from "lucide-react";
import { sendChatMessage } from "@/lib/api";
import { generateSessionId } from "@/lib/utils";
import { ChatResponse, Advisory, PredictionResult, WeatherRisk } from "@/lib/types";

interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text?: string;
  image_base64?: string;
  advisory?: Advisory;
  prediction_result?: PredictionResult;
  weather_risk?: WeatherRisk;
  timestamp: string;
}

export const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome-1",
      sender: "bot",
      text: "Namaste! I am AgriRakshak, your AI field companion. You can ask agricultural questions in English or Hindi, or attach a photo of an affected leaf.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [language, setLanguage] = useState("en");
  const [showImageModal, setShowImageModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendText = async (textToSend?: string) => {
    const query = textToSend || inputText;
    if (!query.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: "user-" + Date.now(),
      sender: "user",
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputText("");
    setIsLoading(true);

    try {
      const sessionId = generateSessionId();
      const res = await sendChatMessage({
        session_id: sessionId,
        message: query,
        language: language,
      });

      const botMsg: ChatMessage = {
        id: "bot-" + Date.now(),
        sender: "bot",
        advisory: res.advisory,
        weather_risk: res.weather_risk,
        prediction_result: res.prediction_result,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      const errorMsg: ChatMessage = {
        id: "err-" + Date.now(),
        sender: "bot",
        text: "I couldn't process that request right now. Please try again or describe the symptoms.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please select a valid crop leaf image.");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64 = reader.result as string;
      setShowImageModal(false);

      const userMsg: ChatMessage = {
        id: "user-img-" + Date.now(),
        sender: "user",
        image_base64: base64,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        const sessionId = generateSessionId();
        const res = await sendChatMessage({
          session_id: sessionId,
          image_base64: base64,
          language: language,
          crop: "Rice",
        });

        const botMsg: ChatMessage = {
          id: "bot-img-" + Date.now(),
          sender: "bot",
          advisory: res.advisory,
          prediction_result: res.prediction_result,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };

        setMessages((prev) => [...prev, botMsg]);
      } catch (err) {
        console.error("Image diagnosis error:", err);
        const errorMsg: ChatMessage = {
          id: "err-img-" + Date.now(),
          sender: "bot",
          text: "I couldn't process that image right now. Please try again or describe the symptoms.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
      }
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="space-y-4">
      {/* Page Header */}
      <div className="page-header">
        <div>
          <span className="section-label">Ask AgriRakshak</span>
          <h1>A question is a good place to start.</h1>
        </div>
      </div>
      <p className="lead-copy">Get plain-language guidance based on official agricultural knowledge.</p>

      {/* Field Note Strip */}
      <div className="field-note-strip">
        <img src="/agrirakshak-logo.png" alt="AgriRakshak logo" />
        <span>
          <strong>Field note / 032</strong> Ask in plain Hindi or English. Type symptoms or attach a photo.
        </span>
        <span className="strip-place">AI Assistant</span>
      </div>

      {/* Main Chat Box Container */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden flex flex-col h-[560px]">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#fbfaf5]">
          {messages.map((msg) => {
            const isUser = msg.sender === "user";
            return (
              <div
                key={msg.id}
                className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
              >
                {/* Avatar */}
                <div
                  className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs shadow-sm flex-shrink-0 ${
                    isUser
                      ? "bg-[#163d2f] text-white"
                      : "bg-[#e2ecdf] text-[#163d2f]"
                  }`}
                >
                  {isUser ? <User size={16} /> : <Bot size={18} />}
                </div>

                {/* Message Content */}
                <div
                  className={`max-w-[85%] space-y-3 ${
                    isUser ? "items-end" : "items-start"
                  }`}
                >
                  {msg.image_base64 && (
                    <img
                      src={msg.image_base64}
                      alt="Uploaded Crop Leaf"
                      className="w-48 h-36 object-cover rounded-xl border border-gray-200 shadow-sm"
                    />
                  )}

                  {msg.text && (
                    <div
                      className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                        isUser
                          ? "bg-[#163d2f] text-white rounded-tr-none"
                          : "bg-white text-gray-900 border border-gray-200 shadow-xs rounded-tl-none"
                      }`}
                    >
                      {msg.text}
                    </div>
                  )}

                  {/* Prediction Result Card */}
                  {msg.prediction_result && (
                    <div className="bg-[#163d2f] text-white p-4 rounded-xl space-y-2 shadow-sm">
                      <div className="flex justify-between items-center text-xs">
                        <span className="text-[#a6c2a8] font-bold uppercase tracking-wider">
                          AI Crop Diagnosis
                        </span>
                        <span className="bg-[#91c184] text-[#163d2f] px-2 py-0.5 rounded-full font-bold">
                          {Math.round(msg.prediction_result.confidence * 100)}% Conf
                        </span>
                      </div>
                      <h4 className="text-base font-bold">
                        {msg.prediction_result.predicted_class?.replace(/_/g, " ")}
                      </h4>
                      {msg.prediction_result.needs_expert_review && (
                        <div className="text-[11px] bg-amber-500/20 text-amber-200 p-2 rounded border border-amber-500/40 flex items-center gap-1.5">
                          <AlertTriangle size={14} /> Low confidence detection: Escalated to expert queue.
                        </div>
                      )}
                    </div>
                  )}

                  {/* Advisory Actions Card */}
                  {msg.advisory && (
                    <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-3">
                      <p className="text-xs sm:text-sm font-semibold text-gray-800 bg-[#f0f4ef] p-3 rounded-lg border border-[#d2e0cf]">
                        {msg.advisory.diagnosis_or_answer}
                      </p>

                      {msg.advisory.recommended_actions.length > 0 && (
                        <div className="space-y-1.5">
                          <strong className="text-xs uppercase tracking-wider text-[#163d2f] block font-bold">
                            What you should do:
                          </strong>
                          <ul className="space-y-1 text-xs text-gray-700">
                            {msg.advisory.recommended_actions.map((act, i) => (
                              <li key={i} className="flex items-start gap-2 bg-[#f8f6ef] p-2 rounded border border-[#e2e6d8]">
                                <span className="font-bold text-[#69a56d]">✓</span>
                                <span>{act}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {msg.advisory.safety_notes.length > 0 && (
                        <div className="text-xs text-amber-900 bg-[#fbf5e8] p-2.5 rounded border border-[#eeddb8] flex items-start gap-2">
                          <LifeBuoy size={16} className="text-amber-700 flex-shrink-0 mt-0.5" />
                          <span>{msg.advisory.safety_notes[0]}</span>
                        </div>
                      )}
                    </div>
                  )}

                  <span className="text-[10px] text-gray-400 block px-1">
                    {msg.timestamp}
                  </span>
                </div>
              </div>
            );
          })}

          {isLoading && (
            <div className="flex items-center gap-2 text-[#163d2f] bg-[#e2ecdf] p-3 rounded-2xl w-fit text-xs font-semibold animate-pulse">
              <Loader2 size={16} className="animate-spin" />
              AgriRakshak is analyzing knowledge base context...
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Quick Prompts Bar */}
        <div className="p-2.5 bg-[#f0ede3] border-t border-gray-200 flex gap-2 overflow-x-auto no-scrollbar">
          <button
            onClick={() => handleSendText("Meri fasal mein daag hain")}
            className="bg-white hover:bg-gray-50 text-[#163d2f] text-xs font-bold px-3 py-1.5 rounded-full border border-gray-300 whitespace-nowrap shadow-xs transition"
          >
            ✦ Meri fasal mein daag hain
          </button>
          <button
            onClick={() => handleSendText("Rice blast disease symptoms and treatment")}
            className="bg-white hover:bg-gray-50 text-[#163d2f] text-xs font-bold px-3 py-1.5 rounded-full border border-gray-300 whitespace-nowrap shadow-xs transition"
          >
            🌾 Rice blast guidance
          </button>
          <button
            onClick={() => handleSendText("How to manage fall armyworm in maize")}
            className="bg-white hover:bg-gray-50 text-[#163d2f] text-xs font-bold px-3 py-1.5 rounded-full border border-gray-300 whitespace-nowrap shadow-xs transition"
          >
            🌽 Fall armyworm control
          </button>
        </div>

        {/* Input Bar */}
        <div className="p-3 bg-white border-t border-gray-200 flex items-center gap-2">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="button button-outline !min-h-[42px] !px-3"
            title="Attach Leaf Image"
          >
            <Camera size={18} />
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            className="hidden"
          />

          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSendText()}
            placeholder="Type your question in English or Hindi..."
            className="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-3.5 py-2.5 text-xs sm:text-sm text-gray-800 focus:outline-none focus:border-[#163d2f]"
          />

          <button
            onClick={() => handleSendText()}
            disabled={!inputText.trim() || isLoading}
            className="button button-ink !min-h-[42px] !px-4"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};
