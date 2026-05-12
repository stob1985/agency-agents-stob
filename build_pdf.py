#!/usr/bin/env python3
"""Convert SaaS niche research markdown reports to PDFs."""
import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

ROOT = Path(__file__).parent

CSS_STYLE = """
@page {
  size: A4;
  margin: 2cm 1.8cm;
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-size: 9pt;
    color: #888;
  }
  @bottom-left {
    content: string(doctitle);
    font-size: 9pt;
    color: #888;
  }
}
body {
  font-family: "DejaVu Sans", "Liberation Sans", sans-serif;
  font-size: 10.5pt;
  line-height: 1.5;
  color: #222;
}
h1 {
  string-set: doctitle content();
  color: #1a365d;
  font-size: 22pt;
  border-bottom: 3px solid #2b6cb0;
  padding-bottom: 8px;
  margin-top: 0;
  page-break-after: avoid;
}
h2 {
  color: #2b6cb0;
  font-size: 16pt;
  margin-top: 24px;
  border-bottom: 1px solid #cbd5e0;
  padding-bottom: 4px;
  page-break-after: avoid;
}
h3 {
  color: #2c5282;
  font-size: 13pt;
  margin-top: 18px;
  page-break-after: avoid;
}
h4 {
  color: #2d3748;
  font-size: 11.5pt;
  margin-top: 14px;
  page-break-after: avoid;
}
p { margin: 6px 0; }
ul, ol { margin: 6px 0; padding-left: 24px; }
li { margin: 3px 0; }
code {
  background: #edf2f7;
  padding: 1px 5px;
  border-radius: 3px;
  font-family: "DejaVu Sans Mono", monospace;
  font-size: 9.5pt;
  color: #c53030;
}
pre {
  background: #1a202c;
  color: #e2e8f0;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 9pt;
  page-break-inside: avoid;
}
pre code { background: transparent; color: inherit; padding: 0; }
blockquote {
  border-left: 4px solid #2b6cb0;
  background: #ebf4ff;
  padding: 8px 14px;
  margin: 10px 0;
  color: #2d3748;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 9.5pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #cbd5e0;
  padding: 6px 8px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #2b6cb0;
  color: white;
  font-weight: 600;
}
tr:nth-child(even) td { background: #f7fafc; }
a { color: #2b6cb0; text-decoration: none; word-break: break-all; }
hr { border: 0; border-top: 1px solid #cbd5e0; margin: 20px 0; }
strong { color: #1a365d; }
"""

def convert(md_path: Path, pdf_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="hu">
<head><meta charset="utf-8"><title>{md_path.stem}</title></head>
<body>{html_body}</body>
</html>"""
    HTML(string=html_doc).write_pdf(str(pdf_path), stylesheets=[CSS(string=CSS_STYLE)])
    print(f"  -> {pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)")

def main() -> int:
    reports = [
        "saas-niches-research.md",
        "niche-1-2-voice-compliance.md",
        "niche-3-4-ecom-internal-ai.md",
        "niche-5-practice-management.md",
        "mvp-product-opportunities.md",
    ]
    out_dir = ROOT / "pdf"
    out_dir.mkdir(exist_ok=True)
    for name in reports:
        md_path = ROOT / name
        if not md_path.exists():
            print(f"SKIP {name} (not found)")
            continue
        pdf_path = out_dir / (md_path.stem + ".pdf")
        print(f"Converting {name}...")
        convert(md_path, pdf_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
