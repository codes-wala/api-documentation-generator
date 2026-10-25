"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { BookOpenText, FolderKanban, LayoutDashboard, Settings, LogOut, Plus } from "lucide-react";
import { api } from "@/lib/api";
export default function AppShell({ children }: { children: React.ReactNode }) {
  const path = usePathname(); const router = useRouter();
  async function logout() { try { await api("/api/v1/auth/logout", { method: "POST" }); } finally { router.push("/login"); } }
  const items = [{ href: "/dashboard", label: "Dashboard", icon: LayoutDashboard }, { href: "/dashboard?view=projects", label: "Projects", icon: FolderKanban }, { href: "/dashboard?view=documents", label: "Documentation", icon: BookOpenText }, { href: "/dashboard?view=settings", label: "Settings", icon: Settings }];
  return <div className="app-shell"><header className="topbar"><Link href="/dashboard" className="brand" style={{textDecoration:"none",color:"inherit"}}><span className="brand-mark">A</span><span>API Documentation Generator</span></Link><div className="top-actions"><Link href="/dashboard?new=project" className="button primary"><Plus size={15}/> New project</Link><button className="button" onClick={logout} aria-label="Log out"><LogOut size={15}/><span className="hide-mobile">Log out</span></button></div></header><div className="layout"><aside className="sidebar"><div className="side-label">Workspace</div>{items.map(item=>{const Icon=item.icon;return <a key={item.href} href={item.href} className={`nav-item ${path===item.href.split("?")[0]&&!path.includes("/projects/")&&!path.includes("/documents/")?"active":""}`} style={{textDecoration:"none"}}><Icon size={17}/>{item.label}</a>})}</aside><main className="main">{children}</main></div></div>;
}
