// Use same-origin requests. Next.js proxies /api/v1/* to the API container, avoiding browser CORS and localhost hostname mismatches.
export const API = "";
let csrfToken = "";
export async function bootstrapCsrf() {
  const res = await fetch(`${API}/api/v1/auth/csrf`, { credentials: "include", cache: "no-store" });
  if (!res.ok) throw new Error("Could not initialize a secure session. Please refresh the page.");
  const data = await res.json(); csrfToken = data.csrf_token; return csrfToken;
}
export async function api<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
  const method = (options.method || "GET").toUpperCase();
  const headers = new Headers(options.headers || {});
  if (options.body && !(options.body instanceof FormData) && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
    if (!csrfToken) await bootstrapCsrf();
    headers.set("X-CSRF-Token", csrfToken);
  }
  const res = await fetch(`${API}${path}`, { ...options, method, headers, credentials: "include", cache: "no-store" });
  if (res.status === 204) return undefined as T;
  const type = res.headers.get("content-type") || "";
  const payload = type.includes("application/json") ? await res.json() : await res.text();
  if (!res.ok) {
    if (res.status === 401 && typeof window !== "undefined" && !window.location.pathname.startsWith("/login") && !window.location.pathname.startsWith("/register")) window.location.href = "/login";
    const detail = typeof payload === "object" && payload !== null && "detail" in payload ? (payload as { detail?: unknown }).detail : undefined;
    const message = typeof detail === "string" ? detail : typeof payload === "string" && payload ? payload : "Request failed.";
    throw new Error(message);
  }
  return payload as T;
}
export async function download(path: string, filename: string) {
  const res = await fetch(`${API}${path}`, { credentials: "include", cache: "no-store" });
  if (!res.ok) { const p = await res.json().catch(() => ({})); throw new Error(p.detail || "Download failed."); }
  const blob = await res.blob(); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = filename; a.click(); URL.revokeObjectURL(url);
}
