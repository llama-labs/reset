"""Inline every asset into one HTML file you can AirDrop, email or open offline.

    python3 site/build.py   ->   Embody-prototype.html (next to the site/ folder)
"""
import base64, mimetypes, pathlib, re

SITE = pathlib.Path(__file__).parent
OUT = SITE.parent / "Embody-prototype.html"
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("font/woff2", ".woff2")

def data_uri(rel):
    path = SITE / rel
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"

html = (SITE / "index.html").read_text()
html = re.sub(r'(?<=src=")(assets/[^"]+)', lambda m: data_uri(m.group(1)), html)
html = re.sub(r'(?<=url\()(assets/[^)]+)', lambda m: data_uri(m.group(1)), html)
assert not re.search(r'(src="|url\()assets/', html), "an asset reference was left behind"
OUT.write_text(html)
print(f"{OUT.name}: {OUT.stat().st_size / 1e6:.1f} MB")
