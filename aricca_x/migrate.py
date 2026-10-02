import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
css = css_match.group(1) if css_match else ''

body_match = re.search(r'<body>(.*?)<script>', content, re.DOTALL)
body_html = body_match.group(1) if body_match else ''

script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
script_js = script_match.group(1) if script_match else ''

# Write globals.css
with open('portal/src/app/globals.css', 'w', encoding='utf-8') as f:
    f.write('@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' + css)

# Write page.tsx
page_tsx = '''"use client";
import { useEffect, useRef } from 'react';

export default function Home() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Inject the raw JS logic into window scope so inline onclick handlers work
    const script = document.createElement('script');
    script.innerHTML = `''' + script_js.replace('`', '\\`').replace('$', '\\$') + '''`;
    document.body.appendChild(script);
    
    // Simulate initial tab click to setup active state
    setTimeout(() => {
        if(window.document.getElementById('tabVenue')) {
            window.document.getElementById('tabVenue').click();
        }
    }, 100);

    return () => {
      if (document.body.contains(script)) {
          document.body.removeChild(script);
      }
    };
  }, []);

  return (
    <div ref={containerRef} dangerouslySetInnerHTML={{ __html: `''' + body_html.replace('`', '\\`').replace('$', '\\$') + '''` }} />
  );
}
'''

with open('portal/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(page_tsx)

# Create layout.tsx with correct fonts
layout_tsx = '''import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains" });

export const metadata: Metadata = {
  title: "ARICCA-X | Patent-Pending Academic Venue Credibility Analyzer",
  description: "Automated Research Integrity, Credibility & Compliance Analyzer",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${jetbrains.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
'''

with open('portal/src/app/layout.tsx', 'w', encoding='utf-8') as f:
    f.write(layout_tsx)

print('Migration successful!')
