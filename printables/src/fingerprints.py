"""Generates the fingerprint SVGs used in basma.html (run: python3 fingerprints.py > ../basma-fp.txt)."""
import math

INK = "#22282b"

def arch_line(y, h, x0=-5, x1=105):
    pts = []
    for i in range(23):
        x = x0 + (x1 - x0) * i / 22
        pts.append((x, y - h * math.exp(-((x - 50) / 24) ** 2)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)

def ridges(kind):
    d = []
    if kind == "arch":
        for k in range(22):
            y = 10 + k * 5.6
            h = max(0, 16 - abs(y - 78) * 0.28)
            d.append(arch_line(y, h))
        return d
    cx, cy = 46, 66
    if kind == "loop":
        for r in range(4, 30, 5):
            d.append(f"M105 {cy-r} L{cx} {cy-r} A{r} {r} 0 0 0 {cx} {cy+r} L105 {cy+r}")
        d.append(f"M{cx+2} {cy} L105 {cy}")
        top, bottom = cy - 31, cy + 31
    else:  # whorl
        for r in range(3, 28, 5):
            d.append(f"M{cx+4} {cy} m{-r} 0 a{r} {r*1.15:.1f} 0 1 0 {2*r} 0 a{r} {r*1.15:.1f} 0 1 0 {-2*r} 0")
        top, bottom = cy - 33, cy + 33
    y = top
    while y > 2:
        d.append(arch_line(y, 4)); y -= 5.6
    y = bottom
    while y < 135:
        d.append(arch_line(y, -3)); y += 5.6
    return d

def body(kind, mirror=False, dot=None, fork=None):
    g = "".join(f'<path d="{p}"/>' for p in ridges(kind))
    if dot:
        x, y = dot
        g += f'<circle cx="{x}" cy="{y}" r="3.1" fill="#fff" stroke="none"/><circle cx="{x}" cy="{y}" r="2.1" fill="{INK}" stroke="none"/>'
    if fork:
        x, y, s = fork
        g += f'<path d="M{x} {y} q6 {s*1.2} 12 {s*2.5}"/>'
    t = ' transform="translate(100 0) scale(-1 1)"' if mirror else ""
    return f'<g{t}>{g}</g>'

def fp(kind, mirror=False, dot=None, fork=None, uid="x"):
    return (f'<svg viewBox="0 0 100 132" class="fp"><defs><clipPath id="c{uid}"><ellipse cx="50" cy="66" rx="45" ry="60"/></clipPath></defs>'
            f'<g clip-path="url(#c{uid})" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round">{body(kind, mirror, dot, fork)}</g>'
            f'<ellipse cx="50" cy="66" rx="45" ry="60" fill="none" stroke="#c9d0ce" stroke-width="1"/></svg>')

def fragment(kind, dot=None, fork=None, x0=40, y0=38, size=60, uid="frag"):
    """A torn-looking piece of a print, cropped at (x0, y0) and turned upside down."""
    k = size / 60
    edge = " ".join(f"{float(a)*k:.1f},{float(b)*k:.1f}" for a, b in (pt.split(",") for pt in
        "4,6 18,2 31,5 45,1 57,7 55,21 59,34 54,47 57,58 42,55 29,59 16,54 3,57 6,42 1,29 5,16".split()))
    return (f'<svg viewBox="0 0 {size} {size}" class="fp"><defs><clipPath id="c{uid}"><polygon points="{edge}"/></clipPath></defs>'
            f'<g clip-path="url(#c{uid})"><rect width="{size}" height="{size}" fill="#fff"/>'
            f'<g fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round" '
            f'transform="rotate(180 {size/2} {size/2}) translate({-x0} {-y0})">{body(kind, False, dot, fork)}</g></g>'
            f'<polygon points="{edge}" fill="none" stroke="#9aa5a2" stroke-width=".8" stroke-dasharray="2 1.5"/></svg>')

DOT, FORK = (78, 54.5), (66, 85, 1)
OUT = {
    "type_arch": fp("arch", uid="ta"),
    "type_loop": fp("loop", uid="tl"),
    "type_whorl": fp("whorl", uid="tw"),
    "p1": fp("loop", fork=FORK, uid="p1"),
    "p2": fp("loop", dot=DOT, fork=FORK, uid="p2"),
    "p3": fp("whorl", dot=DOT, fork=FORK, uid="p3"),
    "p4": fp("loop", mirror=True, dot=DOT, fork=FORK, uid="p4"),
    "p5": fp("arch", dot=DOT, fork=FORK, uid="p5"),
    "p6": fp("loop", dot=(78, 77.5), fork=(66, 47, -1), uid="p6"),
    "p7": fp("loop", dot=DOT, fork=FORK, uid="p7"),
    "p8": fp("loop", dot=DOT, uid="p8"),
    # harder task: which print is the upside-down piece taken from? (answer: h3)
    "piece": fragment("loop", dot=DOT, fork=FORK, x0=24, y0=32, size=66),
    "h1": fp("loop", dot=(78, 59.5), fork=FORK, uid="h1"),
    "h2": fp("loop", mirror=True, dot=DOT, fork=FORK, uid="h2"),
    "h3": fp("loop", dot=DOT, fork=FORK, uid="h3"),
    "h4": fp("loop", dot=DOT, fork=(66, 85, -1), uid="h4"),
    "h5": fp("loop", dot=DOT, uid="h5"),
    "h6": fp("loop", dot=(78, 77.5), fork=(66, 47, -1), uid="h6"),
}

if __name__ == "__main__":
    import json, sys
    json.dump(OUT, sys.stdout)
