import re
with open("prd_dump.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

with open("output.txt", "w", encoding="utf-8") as out:
    out.write("Topology occurrences:\n")
    matches = re.finditer(r'.{0,100}topology.{0,100}', text, re.IGNORECASE)
    for m in matches:
        out.write(m.group(0).strip() + "\n")

