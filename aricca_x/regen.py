import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

body_match = re.search(r'<body>(.*?)<script>', content, re.DOTALL)
body_html = body_match.group(1) if body_match else ''
body_html = body_html.replace('`', '\\`').replace('$', '\\$')

# Fix form onsubmit
body_html = body_html.replace('<form class="auth-form" id="login-form">', '<form class="auth-form" id="login-form" onsubmit="window.handleLogin(event)">')

page_tsx = '''"use client";
import { useEffect, useRef } from 'react';

export default function Home() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = '/aricca_logic.js';
    document.body.appendChild(script);
    
    // Simulate initial tab click to setup active state
    setTimeout(() => {
        if(window.document.getElementById('tabVenue')) {
            window.document.getElementById('tabVenue')?.click();
        }
    }, 200);

    return () => {
      if (document.body.contains(script)) {
          document.body.removeChild(script);
      }
    };
  }, []);

  return (
    <div ref={containerRef} dangerouslySetInnerHTML={{ __html: `''' + body_html + '''` }} />
  );
}
'''

with open('portal/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(page_tsx)

print('Regenerated page.tsx')
