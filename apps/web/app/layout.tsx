import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "API Documentation Generator", description: "Generate, refine, organize, and share API documentation." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
