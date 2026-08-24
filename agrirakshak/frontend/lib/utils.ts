import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function generateSessionId(): string {
  if (typeof window !== "undefined") {
    let sid = localStorage.getItem("agri_session_id");
    if (!sid) {
      sid = "session-" + Math.random().toString(36).substring(2, 9);
      localStorage.setItem("agri_session_id", sid);
    }
    return sid;
  }
  return "demo-session-123";
}
