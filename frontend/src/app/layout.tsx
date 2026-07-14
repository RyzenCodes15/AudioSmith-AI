import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AudioSmith AI | Premium Speech Enhancement",
  description: "Remove background noise from human speech recordings using state-of-the-art deep learning.",
};

import { AuthProvider } from "@/lib/auth/AuthContext";
import { ToastProvider } from "@/lib/ToastContext";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <ToastProvider>
            <main>{children}</main>
          </ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
