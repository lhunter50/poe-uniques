import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PoE Uniques",
  description: "Browse Path of Exile unique items",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-black">{children}</body>
    </html>
  );
}
