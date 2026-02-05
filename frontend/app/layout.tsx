import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Truth Engine - Zero-Trust Python Debugger",
  description: "AI-powered code repair with verified fixes",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-900 text-white">
        {children}
      </body>
    </html>
  );
}
