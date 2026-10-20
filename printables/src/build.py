"""Builds the fingerprint worksheets in .. from their templates and the generated SVGs."""
from pathlib import Path
from fingerprints import OUT

here = Path(__file__).parent
for name in ("basma", "basma-2"):
    html = (here / f"{name}.template.html").read_text()
    for key, svg in OUT.items():
        html = html.replace("{{" + key + "}}", svg)
    assert "{{" not in html, name
    (here.parent / f"{name}.html").write_text(html)
