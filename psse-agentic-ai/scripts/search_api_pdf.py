import sys
import re
from pathlib import Path
import PyPDF2

def search_pdf(pdf_path, keywords, context_lines=5):
    print(f"Searching {pdf_path} for {len(keywords)} keywords...")
    results = {k: [] for k in keywords}
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            print(f"Total pages: {num_pages}")
            
            for page_num in range(num_pages):
                if page_num % 500 == 0:
                    print(f"Scanning page {page_num}...")
                
                page = reader.pages[page_num]
                text = page.extract_text()
                if not text: continue
                
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    line_lower = line.lower()
                    for kw in keywords:
                        if kw.lower() in line_lower:
                            # get context
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)
                            context = "\n".join(lines[start:end])
                            results[kw].append(f"--- PAGE {page_num + 1} ---\n{context}\n")
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return
        
    print("Writing results...")
    with open("pdf_search_results.txt", "w", encoding="utf-8") as out:
        for kw, matches in results.items():
            if matches:
                out.write(f"==================================================\n")
                out.write(f"KEYWORD: {kw} ({len(matches)} matches)\n")
                out.write(f"==================================================\n")
                # write first 15 matches to avoid huge files
                for match in matches[:15]:
                    out.write(match + "\n")
                if len(matches) > 15:
                    out.write(f"... and {len(matches) - 15} more matches for {kw}.\n")
                    
    print("Done. Results saved to pdf_search_results.txt")

if __name__ == "__main__":
    pdf_path = r"C:\Program Files\PTI\PSSE36\36.0\DOCS\API.pdf"
    keywords = [
        "slider", "diagram refresh", "refresh diagram", "diagram rebuild",
        "viewport", "fit to", "zoom", "center diagram", "active document",
        "growdiagram", "savediagfile", "newdiagfile",
        "graphics", "map string", "bus symbol"
    ]
    search_pdf(pdf_path, keywords)
