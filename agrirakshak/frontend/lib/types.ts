export interface Advisory {
  diagnosis_or_answer: string;
  recommended_actions: string[];
  safety_notes: string[];
  escalation_flag: boolean;
}

export interface PredictionResult {
  success: boolean;
  predicted_class: string;
  confidence: number;
  needs_expert_review: boolean;
  raw_response?: Record<string, any>;
  fallback_message?: string;
}

export interface WeatherRisk {
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  reason: string;
  recommended_actions: string[];
  temperature_celsius?: number;
  humidity_percent?: number;
  weather_condition?: string;
  forecast_3day_summary?: string;
}

export interface ChatResponse {
  intent: 'image_diagnosis' | 'knowledge_query' | 'weather_risk' | 'general';
  session_id: string;
  advisory: Advisory;
  prediction_result?: PredictionResult;
  weather_risk?: WeatherRisk;
  farmer_case_id?: number;
}

export interface FarmerCase {
  id: number;
  session_id: string;
  image_url?: string;
  crop: string;
  predicted_class?: string;
  confidence: number;
  latitude?: number;
  longitude?: number;
  location_name?: string;
  status: string;
  needs_expert_review: boolean;
  created_at: string;
}

export interface EscalationCase {
  id: number;
  farmer_case_id: number;
  reason?: string;
  status: 'pending' | 'resolved';
  expert_id?: number;
  expert_diagnosis?: string;
  expert_notes?: string;
  created_at: string;
  resolved_at?: string;
  farmer_case?: FarmerCase;
}

export interface DashboardStats {
  total_cases: number;
  today_cases: number;
  high_risk_areas: number;
  pending_expert_reviews: number;
}
