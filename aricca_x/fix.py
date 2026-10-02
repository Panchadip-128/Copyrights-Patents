import re

with open('portal/src/app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the giant script.innerHTML block
new_content = re.sub(
    r"script\.innerHTML = `.*?`;",
    "script.src = '/aricca_logic.js';",
    content,
    flags=re.DOTALL
)

with open('portal/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated page.tsx')
