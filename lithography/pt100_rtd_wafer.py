import pya, os, math

SRC_GDS = os.path.join(os.path.dirname(__file__), "pt100_rtd.gds")
OUT_GDS = os.path.join(os.path.dirname(__file__), "pt100_rtd_wafer.gds")
DIE_W_UM, DIE_H_UM = 1500.0, 1500.0
WAFER_DIA, EDGE_CLEAR = 100000.0, 0.0   # 4" wafer, no edge exclusion

# --- Read your single-die GDS into a layout ---
ly = pya.Layout()
ly.read(SRC_GDS)                # <- keeps dbu from your die file
die = ly.top_cell()             # your die’s top cell
wafer_top = ly.create_cell("WAFER_100MM")  # new wafer-level top

# Layers for outline/labels
L_OUT = ly.layer(90, 0)
L_TXT = ly.layer(91, 0)

def um(v): return int(round(v / ly.dbu))  # µm -> dbu

# --- Wafer outline (circle) ---
R = WAFER_DIA / 2.0 - EDGE_CLEAR
num_pts = 512  # smoothness
pts = []
for i in range(num_pts):
    theta = 2 * math.pi * i / num_pts
    x = R * math.cos(theta)
    y = R * math.sin(theta)
    pts.append(pya.Point(um(x), um(y)))
wafer_top.shapes(L_OUT).insert(pya.Polygon(pts))

# --- Helper: is a die fully inside the wafer? (check 4 corners) ---
def fully_inside_circle(x, y, w, h, r):
    rr = r*r
    for (cx, cy) in ((x, y), (x+w, y), (x, y+h), (x+w, y+h)):
        if cx*cx + cy*cy > rr: return False
    return True

# --- Tile dies touching (no scribe gap). Assumes die origin at lower-left (0,0) ---
dx, dy = DIE_W_UM, DIE_H_UM
placed = 0
y = math.floor((-R) / dy) * dy
while y <= R:
    x = math.floor((-R) / dx) * dx
    while x <= R:
        if fully_inside_circle(x, y, dx, dy, R):
            wafer_top.insert(pya.CellInstArray(die.cell_index(), pya.Trans(pya.Point(um(x), um(y)))))
            placed += 1
        x += dx
    y += dy

# Optional: label die count
t = pya.Text(f"{placed} dies", pya.Trans(pya.Point(um(-R+2000), um(R-2000))))
t.size = um(500); wafer_top.shapes(L_TXT).insert(t)

ly.write(OUT_GDS)
print(f"Wrote {OUT_GDS} (placed {placed} dies)")
