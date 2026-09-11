import { ChatResponse, WeatherRisk, FarmerCase, EscalationCase, DashboardStats } from "./types";
import { getAuthToken } from "./auth";

const BACKEND_URL = (process.env.NEXT_PUBLIC_BACKEND_URL || "https://agrirakshak-backend.onrender.com").replace(/\/$/, "");

async function fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(`${BACKEND_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API Error (${response.status}): ${errorText}`);
  }

  return response.json();
}

export async function sendChatMessage(payload: {
  session_id: string;
  message?: string;
  language?: string;
  image_base64?: string;
  crop?: string;
  latitude?: number;
  longitude?: number;
}): Promise<ChatResponse> {
  return fetchAPI<ChatResponse>("/chat/message", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function uploadDiagnosis(formData: FormData): Promise<any> {
  return fetchAPI("/prediction/analyze", {
    method: "POST",
    body: formData,
  });
}

export async function getWeatherRisk(lat: number = 28.6139, lon: number = 77.2090, crop: string = "Rice"): Promise<WeatherRisk> {
  return fetchAPI<WeatherRisk>(`/weather/risk?latitude=${lat}&longitude=${lon}&crop=${encodeURIComponent(crop)}`);
}

export async function getDashboardStats(): Promise<DashboardStats> {
  return fetchAPI<DashboardStats>("/dashboard/stats");
}

export async function getCases(): Promise<FarmerCase[]> {
  return fetchAPI<FarmerCase[]>("/dashboard/cases");
}

export async function getEscalations(status?: string): Promise<EscalationCase[]> {
  const q = status ? `?status=${status}` : "";
  return fetchAPI<EscalationCase[]>(`/reports/escalations${q}`);
}

export async function resolveEscalation(id: number, diagnosis: string, notes: string): Promise<EscalationCase> {
  return fetchAPI<EscalationCase>(`/reports/escalations/${id}/resolve`, {
    method: "POST",
    body: JSON.stringify({
      expert_confirmed_diagnosis: diagnosis,
      expert_notes: notes,
    }),
  });
}

export async function loginOfficer(username: string, password: string): Promise<{ access_token: string }> {
  return fetchAPI<{ access_token: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}
