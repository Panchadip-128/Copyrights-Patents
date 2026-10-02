import os

with open('portal/src/app/page.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('<div id="app-container">')
login_part = parts[0].strip() + '\n    `}} />\n  );\n}\n'
app_part = '<div id="app-container">' + parts[1].split('`}} />')[0]

# Now, we should also remove display:none from app_part so it shows immediately on the dashboard page
app_part = app_part.replace('<div id="app-container" style="display: none;">', '<div id="app-container">')

with open('portal/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(login_part)

dashboard = """\"use client\";
import { useEffect, useRef } from 'react';

export default function Dashboard() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!document.querySelector('script[src="/aricca_logic.js"]')) {
        const script = document.createElement('script');
        script.src = '/aricca_logic.js';
        document.body.appendChild(script);
    }
    setTimeout(() => {
        if(window.document.getElementById('tabVenue')) {
            window.document.getElementById('tabVenue')?.click();
        }
        const appContainer = document.getElementById('app-container');
        if (appContainer) appContainer.style.display = 'block';
    }, 200);
  }, []);

  return (
    <div ref={containerRef} dangerouslySetInnerHTML={{ __html: `
""" + app_part + """
    `}} />
  );
}
"""

os.makedirs('portal/src/app/dashboard', exist_ok=True)
with open('portal/src/app/dashboard/page.tsx', 'w', encoding='utf-8') as f:
    f.write(dashboard)

# Update aricca_logic.js to use routing instead of DOM display toggles
with open('portal/public/aricca_logic.js', 'r', encoding='utf-8') as f:
    logic = f.read()

logic = logic.replace("document.getElementById('auth-container').style.display = 'none';", "window.location.href = '/dashboard';")
logic = logic.replace("document.getElementById('app-container').style.display = 'block';", "")

with open('portal/public/aricca_logic.js', 'w', encoding='utf-8') as f:
    f.write(logic)

print("Pages refactored!")
