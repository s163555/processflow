import pya, os, math

SRC_GDS = os.path.join(os.path.dirname(__file__), "rtd_sulfilogger.gds")
OUT_GDS = os.path.join(os.path.dirname(__file__), "rtd_sulfilogger_wafer.gds")

DIE_W_UM, DIE_H_UM = 7760.0, 4550.0
WAFER_DIA, EDGE_CLEAR = 100000.0, 0.0   # 4" wafer

ly = pya.Layout()
ly.read(SRC_GDS)
die = ly.top_cell()
wafer_top = ly.create_cell("WAFER_100MM")

L_OUT = ly.layer(90, 0)
L_TXT = ly.layer(91, 0)

def um(v): return int(round(v / ly.dbu))

# --- Wafer outline ---
R = WAFER_DIA / 2.0 - EDGE_CLEAR
pts = [pya.Point(um(R*math.cos(2*math.pi*i/512)),
                 um(R*math.sin(2*math.pi*i/512))) for i in range(512)]
wafer_top.shapes(L_OUT).insert(pya.Polygon(pts))

def fully_inside_circle(x, y, w, h, r):
    rr = r*r
    for (cx, cy) in ((x, y), (x+w, y), (x, y+h), (x+w, y+h)):
        if cx*cx + cy*cy > rr: return False
    return True

# --- Offsets due to die origin on right edge and Y-centered ---
x_offset = DIE_W_UM           # shift right so right edge = 0
y_offset = -DIE_H_UM / 2.0 + DIE_H_UM    # shift down to bottom alignment

dx, dy = DIE_W_UM, DIE_H_UM
placed = 0
y = math.floor((-R) / dy) * dy
while y <= R:
    x = math.floor((-R) / dx) * dx
    while x <= R:
        if fully_inside_circle(x, y, dx, dy, R):
            trans = pya.Trans(pya.Point(um(x + x_offset),
                                        um(y + y_offset)))
            wafer_top.insert(pya.CellInstArray(die.cell_index(), trans))
            placed += 1
        x += dx
    y += dy

t = pya.Text(f"{placed} dies", pya.Trans(pya.Point(um(-R+2000), um(R-2000))))
t.size = um(500)
wafer_top.shapes(L_TXT).insert(t)

ly.write(OUT_GDS)
print(f"Wrote {OUT_GDS} (placed {placed} dies)")
