import re

with open("diagram_help.txt", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()
    
# find context around two_winding_data_6
matches = re.finditer(r'two_winding_data_6', content, re.IGNORECASE)
for m in matches:
    start = max(0, m.start() - 1000)
    end = min(len(content), m.end() + 1000)
    print(content[start:end])
    print("="*80)
