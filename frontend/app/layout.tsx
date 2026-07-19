import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Product Scene Generator",
  description: "Generate AI marketing images from a single product image.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#f4f5f7] text-slate-900">
        {children}
      </body>
    </html>
  );
}
