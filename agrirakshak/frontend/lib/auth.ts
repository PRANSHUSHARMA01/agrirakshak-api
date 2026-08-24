export const AUTH_TOKEN_KEY = "agri_officer_token";

export function setAuthToken(token: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(AUTH_TOKEN_KEY, token);
  }
}

export function getAuthToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  }
  return null;
}

export function removeAuthToken() {
  if (typeof window !== "undefined") {
    localStorage.removeItem(AUTH_TOKEN_KEY);
  }
}

export function isAuthenticated(): boolean {
  return !!getAuthToken();
}
