"""Builds ../basma.html from basma.template.html and the generated fingerprint SVGs."""
from pathlib import Path
from fingerprints import OUT

here = Path(__file__).parent
html = (here / "basma.template.html").read_text()
for key, svg in OUT.items():
    html = html.replace("{{" + key + "}}", svg)
assert "{{" not in html
(here.parent / "basma.html").write_text(html)
