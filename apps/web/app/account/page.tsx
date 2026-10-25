"use client";
import { FormEvent, useEffect, useState } from "react";
import AppShell from "@/components/AppShell";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

type User = { email: string; display_name: string; created_at: string };
type GeminiSettings = { has_api_key: boolean; model: string; provider: string };
const MODELS = [
  { value: "gemini-3.8-flash", label: "Gemini 3.8 Flash — recommended, latest stable" },
  { value: "gemini-3.5-flash-lite", label: "Gemini 3.5 Flash-Lite — fast and cost-efficient" },
  { value: "gemini-3.6-flash", label: "Gemini 3.6 Flash — balanced performance" },
  { value: "gemini-3.1-flash-lite", label: "Gemini 3.1 Flash-Lite — lightweight" },
  { value: "gemini-3.1-pro-preview", label: "Gemini 3.1 Pro Preview — advanced reasoning (preview)" },
  { value: "gemini-3-flash-preview", label: "Gemini 3 Flash Preview (preview)" },
  { value: "gemini-2.5-flash", label: "Gemini 2.5 Flash — legacy model" },
  { value: "gemini-2.5-flash-lite", label: "Gemini 2.5 Flash-Lite — legacy lightweight model" },
  { value: "gemini-2.5-pro", label: "Gemini 2.5 Pro — legacy advanced reasoning" },
];

export default function AccountPage() {
  const [user, setUser] = useState<User | null>(null);
  const [gemini, setGemini] = useState<GeminiSettings | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("gemini-3.5-flash-lite");
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [connection, setConnection] = useState<"unknown" | "ready" | "failed">("unknown");
  const router = useRouter();

  async function loadGemini() {
    const data = await api<GeminiSettings>("/api/v1/account/gemini");
    setGemini(data); setModel(data.model); setConnection("unknown");
  }
  useEffect(() => {
    api<User>("/api/v1/auth/me").then(setUser).catch(e => setError(e instanceof Error ? e.message : "Could not load account."));
    loadGemini().catch(e => setError(e instanceof Error ? e.message : "Could not load Gemini settings."));
  }, []);

  async function saveGemini(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(""); setNotice("");
    try {
      const data = await api<GeminiSettings>("/api/v1/account/gemini", { method: "PUT", body: JSON.stringify({ api_key: apiKey, model }) });
      setGemini(data); setApiKey(""); setConnection("unknown"); setNotice("Gemini API key saved securely. Test the connection to confirm it is ready.");
    } catch (e) { setError(e instanceof TypeError ? "Could not reach the application API. Refresh the page; if the problem continues, check that the API and web containers are healthy." : e instanceof Error ? e.message : "Could not save Gemini settings."); }
    finally { setBusy(false); }
  }
  async function saveModel(value: string) {
    setModel(value); setError(""); setNotice(""); setBusy(true);
    try { const data = await api<GeminiSettings>("/api/v1/account/gemini/model", { method: "PATCH", body: JSON.stringify({ model: value }) }); setGemini(data); setNotice("Model preference saved."); setConnection("unknown"); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not save model."); }
    finally { setBusy(false); }
  }
  async function testConnection() {
    setBusy(true); setError(""); setNotice(""); setConnection("unknown");
    try { const result = await api<{ connected: boolean; message: string }>("/api/v1/account/gemini/test", { method: "POST", body: JSON.stringify({}) }); setConnection("ready"); setNotice(result.message); }
    catch (e) { setConnection("failed"); setError(e instanceof Error ? e.message : "Gemini connection test failed."); }
    finally { setBusy(false); }
  }
  async function deleteGemini() {
    if (!window.confirm("Remove the Gemini API key from your account? Documentation generation will stop until you add a key again.")) return;
    setBusy(true); setError(""); setNotice("");
    try { await api("/api/v1/account/gemini", { method: "DELETE" }); setGemini({ has_api_key: false, model, provider: "Google Gemini" }); setApiKey(""); setConnection("unknown"); setNotice("Gemini API key removed from your account."); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not remove Gemini key."); }
    finally { setBusy(false); }
  }
  async function deleteAccount() {
    const first = window.confirm("Permanently delete your account? This will also delete all your projects, source files, documentation, version history, share links, and saved Gemini settings. This cannot be undone.");
    if (!first) return;
    const typed = window.prompt('Type DELETE to permanently remove your account and all its data.');
    if (typed !== "DELETE") return;
    setBusy(true); setError(""); setNotice("");
    try {
      await api("/api/v1/account", { method: "DELETE" });
      router.replace("/register");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not delete your account.");
      setBusy(false);
    }
  }

  async function change(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(""); setNotice("");
    try { await api("/api/v1/auth/change-password", { method: "POST", body: JSON.stringify({ current_password: current, new_password: next }) }); setNotice("Password updated. Please sign in again."); setCurrent(""); setNext(""); setTimeout(() => router.push("/login"), 1200); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not update password."); }
    finally { setBusy(false); }
  }

  return <AppShell>
    <div className="page-head"><div><div className="eyebrow">Settings / Account</div><h1>Account settings</h1><p>Manage your account, Gemini connection, and model without editing server configuration files.</p></div></div>
    {error && <div className="notice error" role="alert">{error}</div>}{notice && <div className="notice success" role="status">{notice}</div>}
    <section className="form-card" style={{ maxWidth: "none", marginBottom: 24 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}><div><h2 style={{ marginTop: 0, marginBottom: 6 }}>Gemini AI configuration</h2><p className="muted" style={{ marginTop: 0 }}>Used only when you generate API documentation. Your key is encrypted before it is stored and is never displayed again after saving.</p></div>
        <span className={`status-pill ${connection === "ready" ? "success" : connection === "failed" ? "error" : ""}`} style={{ padding: "8px 12px", borderRadius: 999, border: "1px solid var(--border, #dbe1ea)", fontWeight: 600 }}>{connection === "ready" ? "● Connected and ready" : connection === "failed" ? "● Connection failed" : gemini?.has_api_key ? "● Key saved — test connection" : "● Not configured"}</span></div>
      <form onSubmit={saveGemini}>
        <div className="field"><label htmlFor="gemini-key">Gemini API key</label><input id="gemini-key" className="input" type="password" autoComplete="new-password" value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder={gemini?.has_api_key ? "Key saved; enter a new key to replace it" : "Paste your Gemini API key"} minLength={10} maxLength={500} required /><span className="small muted">Create or manage your key in Google AI Studio. The key is stored encrypted and cannot be retrieved from this page.</span></div>
        <div className="field"><label htmlFor="gemini-model">Model for documentation generation</label><select id="gemini-model" className="input" value={model} onChange={e => saveModel(e.target.value)} disabled={busy}>{MODELS.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}</select><span className="small muted">The selected model is saved to your account and used for future generations.</span></div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}><button className="button primary" disabled={busy || !apiKey.trim()}>{busy ? "Please wait…" : gemini?.has_api_key ? "Save new API key" : "Save API key"}</button><button type="button" className="button" disabled={busy || !gemini?.has_api_key} onClick={testConnection}>Test connection</button><button type="button" className="button danger" disabled={busy || !gemini?.has_api_key} onClick={deleteGemini}>Remove API key</button></div>
      </form>
      <p className="small muted" style={{ marginBottom: 0, marginTop: 16 }}>If the connection test succeeds, the interface will show “Connected and ready.” If the key is removed, AI generation is disabled for your account until another key is saved.</p>
    </section>
    <section className="form-card"><h2 style={{ marginTop: 0 }}>Account</h2><div className="field"><label>Email address</label><input className="input" readOnly value={user?.email || "Loading…"}/></div><div className="field"><label>Display name</label><input className="input" readOnly value={user?.display_name || "Not set"}/></div><div className="field"><label>Member since</label><input className="input" readOnly value={user ? new Date(user.created_at).toLocaleDateString() : "Loading…"}/></div><div className="divider"/><h2>Change password</h2><form onSubmit={change}><div className="field"><label htmlFor="current">Current password</label><input id="current" type="password" autoComplete="current-password" className="input" required value={current} onChange={e => setCurrent(e.target.value)}/></div><div className="field"><label htmlFor="new">New password</label><input id="new" type="password" autoComplete="new-password" minLength={10} maxLength={128} className="input" required value={next} onChange={e => setNext(e.target.value)}/><span className="small muted">At least 10 characters. Changing your password signs out existing sessions.</span></div><button className="button primary" disabled={busy}>{busy ? "Updating…" : "Update password"}</button></form><div className="divider"/><h2 style={{color:"var(--danger)"}}>Delete account</h2><p className="muted">Permanently delete your account and all associated workspace data, including projects, source files, documentation, version history, share links, and Gemini settings. This action cannot be undone.</p><button type="button" className="button danger" disabled={busy} onClick={deleteAccount}>Permanently delete my account</button></section>
  </AppShell>;
}
