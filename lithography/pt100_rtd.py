# KLayout Python macro — Pt100 RTD, rectangular sense traces + align marks
import pya
import os

# ---- Parameters ----
die_w = 1500.0; die_h = 1500.0
w_line = 22.0; gap = 15.0; pitch = w_line + gap
runs = 7; run_len = 178.0
route_w = 20.0; pad_size = 150.0; pad_clear = 80.0
keepout = 35.0
label_h = 120.0
script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(script_dir, "pt100_rtd.gds")

# ---- Setup ----
ly = pya.Layout(); ly.dbu = 0.001
top = ly.create_cell("PT100_RTD")
L_METAL = ly.layer(1,0); L_DICE = ly.layer(10,0); L_ALIGN = ly.layer(20,0); L_TEXT = ly.layer(100,0)
um = lambda x: int(round(x/(ly.dbu*1000.0)))
def box(x,y,w,h): return pya.Box(um(x),um(y),um(x+w),um(y+h))
def rect(layer,x,y,w,h): top.shapes(layer).insert(box(x,y,w,h))
def cross(layer,x,y,arm=100.0,w=10.0):
    rect(L_ALIGN,x-arm,y-w/2,2*arm,w); rect(L_ALIGN,x-w/2,y-arm,w,2*arm)
def add_path(layer, pts, width):
    p = pya.Path([pya.Point(um(x),um(y)) for x,y in pts], um(width))
    top.shapes(layer).insert(p.polygon())
def add_text(layer, s, x, y, h):
    t = pya.Text(s, pya.Trans(pya.Point(um(x), um(y)))); t.size = um(h); top.shapes(layer).insert(t)

# ---- Frame & alignment (layers 10/0 and 20/0) ----
rect(L_DICE,0,0,die_w,5); rect(L_DICE,0,die_h-5,die_w,5)
rect(L_DICE,0,0,5,die_h); rect(L_DICE,die_w-5,0,5,die_h)
for x,y in [(150,150),(die_w-150,150),(150,die_h-150),(die_w-150,die_h-150)]:
    cross(L_ALIGN,x,y)

# ---- Meander (centered) ----
cx, cy = die_w/2.0, die_h/2.0
me_w = run_len
me_h = (runs-1)*pitch + w_line
left  = cx - me_w/2.0
right = cx + me_w/2.0
y0    = cy - me_h/2.0 + w_line/2.0

pts = []
y = y0
for i in range(runs):
    if i % 2 == 0: pts += [(left,y),(right,y)]
    else:          pts += [(right,y),(left,y)]
    if i < runs-1: y += pitch
add_path(L_METAL, pts, w_line)

# Endpoints
start = (left,  y0)                    # − node
end   = (right, y0 + (runs-1)*pitch)   # + node

# ---- Symmetric pad rows (sense near node) ----
padL_x = left  - pad_clear - pad_size
padR_x = right + pad_clear
pad_y_low  = cy - pad_size - 40.0      # lower row
pad_y_high = cy + 40.0                 # upper row

# Left: lower=S−, upper=F− ; Right: lower=F+, upper=S+
for (px,py) in [(padL_x,pad_y_low),(padL_x,pad_y_high),
                (padR_x,pad_y_low),(padR_x,pad_y_high)]:
    rect(L_METAL, px, py, pad_size, pad_size)

L_SENSE = (padL_x, pad_y_low ); L_FORCE = (padL_x, pad_y_high)
R_FORCE = (padR_x, pad_y_low ); R_SENSE = (padR_x, pad_y_high)

# Pad-edge Xs
L_edge = L_SENSE[0] + pad_size         # right edge of left pads
R_edge = R_SENSE[0]                    # left edge of right pads

# Keepout rails outside meander
rail_L = left  - keepout
rail_R = right + keepout

# ---- Force + Sense routing with exact programmatic sense rectangles ----
# Parameters: target sense length and minimum clearance to meander edge
sense_len_target = 45.0   # µm  -> gives 0.04500 mm length
min_clear        = 10.0    # µm  -> safety gap to meander edge
y_offset         = 4.0

# Pad-center Y for each sense pad
ySm = L_SENSE[1] + pad_size/2.0   # S− center Y
ySp = R_SENSE[1] + pad_size/2.0   # S+ center Y

# Max allowed sense lengths so the vertical force rails stay outside the meander
max_len_left  = max(0.0, (left  - min_clear) - L_edge)  # rail_L must be < left - min_clear
max_len_right = max(0.0,  R_edge - (right + min_clear)) # rail_R must be > right + min_clear

# Final sense length used on both sides (keeps symmetry)
sense_len = min(sense_len_target, max_len_left, max_len_right)

# Place vertical force rails exactly at the sense rectangle far edges
rail_L = L_edge + sense_len
rail_R = R_edge - sense_len

# ---- Force traces (paths) ----
# F−: node -> left rail -> up to F− pad center -> into pad edge
add_path(L_METAL, [
    (start[0], start[1]),
    (rail_L,   start[1]),
    (rail_L,   L_FORCE[1] + pad_size/2.0),
    (L_edge,   L_FORCE[1] + pad_size/2.0)
], route_w)

# F+: node -> right rail -> down to F+ pad center -> into pad edge
add_path(L_METAL, [
    (end[0], end[1]),
    (rail_R, end[1]),
    (rail_R, R_FORCE[1] + pad_size/2.0),
    (R_edge, R_FORCE[1] + pad_size/2.0)
], route_w)

pad_gap = 0.0        # µm space between pad and trace
L_edge = L_SENSE[0] + pad_size + pad_gap
R_edge = R_SENSE[0]  - pad_gap
L_edge = L_SENSE[0] + pad_size + pad_gap
R_edge = R_SENSE[0]  - pad_gap

ySm = L_SENSE[1] + pad_size/2.0 + y_offset
ySp = R_SENSE[1] + pad_size/2.0 - y_offset

rail_L = L_edge + sense_len_target
rail_R = R_edge - sense_len_target

rect(L_METAL, L_edge, ySm - route_w/2.0, sense_len_target, route_w)
rect(L_METAL, R_edge - sense_len_target, ySp - route_w/2.0, sense_len_target, route_w)

# ---- (Optional) print the actual rectangle corners in mm for verification ----
def um_to_mm(v): return v/1000.0
def rpt(name, x1, y1, x2, y2):
    print(f"{name} LL=({um_to_mm(x1):.5f}, {um_to_mm(y1):.5f})  "
          f"UR=({um_to_mm(x2):.5f}, {um_to_mm(y2):.5f})")

# ---- Labels ----
add_text(L_TEXT, "Sm", L_SENSE[0]+pad_size/2, L_SENSE[1]+pad_size/2, label_h)
add_text(L_TEXT, "Fm", L_FORCE[0]+pad_size/2, L_FORCE[1]+pad_size/2, label_h)
add_text(L_TEXT, "Fp", R_FORCE[0]+pad_size/2, R_FORCE[1]+pad_size/2, label_h)
add_text(L_TEXT, "Sp", R_SENSE[0]+pad_size/2, R_SENSE[1]+pad_size/2, label_h)

# ---- Save ----
ly.write(OUTPUT_PATH)
print(f"Wrote {OUTPUT_PATH}")
