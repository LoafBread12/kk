"""Builds arrange-room.html by inlining lib/arrange.js into the page template."""
from pathlib import Path

here = Path(__file__).parent
page = (here / "arrange-room.template.html").read_text()
lib = (here / "lib" / "arrange.js").read_text()
assert "/*ARRANGE_LIB*/" in page
(here / "arrange-room.html").write_text(page.replace("/*ARRANGE_LIB*/", lib))
