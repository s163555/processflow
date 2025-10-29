import pya
import os

# ---- Parameters ----
die_w = 1500.0; die_h = 1500.0
w_line = 60.0; gap = 35.0; pitch = w_line + gap
runs = 8; run_len = 550.0
route_w = 22.0; pad_size = 150.0; pad_clear = 80.0
keepout = 35.0
label_h = 120.0
script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(script_dir, "pt100_rtd.gds")

# ---- Setup ----
ly = pya.Layout(); ly.dbu = 0.001

top = ly.create_cell("PT100_RTD")
L_PLATINUM = ly.layer(1,0); L_METAL = ly.layer(2,0); L_DICE = ly.layer(10,0); L_ALIGN = ly.layer(20,0); L_TEXT = ly.layer(100,0);
def um(x_um): return int(round(x_um / ly.dbu))
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
#rect(L_DICE,0,0,die_w,5); rect(L_DICE,0,die_h-5,die_w,5)
#rect(L_DICE,0,0,5,die_h); rect(L_DICE,die_w-5,0,5,die_h)
#for x,y in [(150,150),(die_w-150,150),(150,die_h-150),(die_w-150,die_h-150)]:
#    cross(L_ALIGN,x,y)

# ---- Orientation chamfer moved to UPPER-LEFT corner (Pin 1 = S-)
chamfer = 300.0   # µm

# Upper-left triangle points: (0,die_h), (chamfer,die_h), (0,die_h-chamfer)
pts = [
    pya.Point(um(0),         um(die_h)),
    pya.Point(um(chamfer),   um(die_h)),
    pya.Point(um(0),         um(die_h - chamfer))
]
#top.shapes(L_DICE).insert(pya.Polygon(pts))

# small human-readable "1" next to chamfer on text layer
#add_text(L_TEXT, "1", chamfer - 60, die_h - chamfer + 80.0, 120.0)

# ---- Meander (centered) ----
cx, cy = die_w/2.0, die_h/2.0
me_w = run_len
me_h = (runs-1)*pitch + w_line
left  = cx - me_w/2.0
right = cx + me_w/2.0
y0    = cy - me_h/2.0 + w_line/2.0
y_offset         = 4.0

pts = []
y = y0
for i in range(runs):
    if i % 2 == 0: pts += [(left,y),(right,y)]
    else:          pts += [(right,y),(left,y)]
    if i < runs-1: y += pitch
add_path(L_PLATINUM, pts, w_line)

# Endpoints
start = (left,  y0)                    # − node
end   = (right, y0 + (runs-1)*pitch)   # + node

# ---- Symmetric pad rows (force near node) ----
padL_x = left  - pad_clear - pad_size
padR_x = right + pad_clear
pad_y_low  = cy - pad_size - 40.0 + y_offset      # lower row
pad_y_high = cy + 40.0 - y_offset               # upper row

# Pads on platinum deposition
#for (px,py) in [(padL_x,pad_y_low),(padL_x,pad_y_high),
#                (padR_x,pad_y_low),(padR_x,pad_y_high)]:
#    rect(L_PLATINUM, px, py, pad_size, pad_size)

# Optional metallization of contacts (Ti, Au)
#for (px,py) in [(padL_x,pad_y_low),(padL_x,pad_y_high),
#                (padR_x,pad_y_low),(padR_x,pad_y_high)]:
#    rect(L_METAL, px, py, pad_size, pad_size)

L_FORCE = (padL_x, pad_y_low )   # Fm (lower-left)
L_SENSE = (padL_x, pad_y_high)   # Sm (upper-left)
R_SENSE = (padR_x, pad_y_low )   # Sp (lower-right)
R_FORCE = (padR_x, pad_y_high)   # Fp (upper-right)

# Pad-edge Xs
L_edge = L_SENSE[0] + pad_size         # right edge of left pads (same calc as before)
R_edge = R_SENSE[0]                    # left edge of right pads

# Keepout rails outside meander
rail_L = left  - keepout
rail_R = right + keepout

# ---- Force + Sense routing with exact programmatic sense rectangles ----
# Parameters: target sense length and minimum clearance to meander edge
sense_len_target = 45.0   # µm  -> gives 0.04500 mm length
min_clear        = 10.0    # µm  -> safety gap to meander edge


# Pad-center Y for each sense pad
ySm = L_SENSE[1] + pad_size/2.0  # Sm center Y (upper-left)
ySp = R_SENSE[1] + pad_size/2.0  # Sp center Y (lower-right)

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
#add_path(L_PLATINUM, [
#    (start[0], start[1]),
#    (rail_L,   start[1]),
#    (rail_L,   L_FORCE[1] + pad_size/2.0),
#    (L_edge,   L_FORCE[1] + pad_size/2.0)
#], route_w)

# F+: node -> right rail -> down to F+ pad center -> into pad edge
#add_path(L_PLATINUM, [
#    (end[0], end[1]),
#    (rail_R, end[1]),
#    (rail_R, R_FORCE[1] + pad_size/2.0),
#    (R_edge, R_FORCE[1] + pad_size/2.0)
#], route_w)

L_edge = L_SENSE[0] + pad_size
R_edge = R_SENSE[0]
L_edge = L_SENSE[0] + pad_size
R_edge = R_SENSE[0]

ySm = L_SENSE[1] + pad_size/2.0 - y_offset
ySp = R_SENSE[1] + pad_size/2.0 + y_offset

rail_L = L_edge + sense_len_target
rail_R = R_edge - sense_len_target

#rect(L_PLATINUM, L_edge, ySm - route_w/2.0, sense_len_target, route_w)
#rect(L_PLATINUM, R_edge - sense_len_target, ySp - route_w/2.0, sense_len_target, route_w)

sense_padL_x = L_SENSE[0] + pad_size/2.0   # center X of left sense pad (Sm)
sense_padR_x = R_SENSE[0] + pad_size/2.0   # center X of right sense pad (Sp)

# left pad right-edge (outside pad)
left_pad_edge_x = L_SENSE[0] + pad_size

#add_path(L_PLATINUM, [
#    (start[0], start[1]),       # meander start
#    (rail_L,   start[1]),       # horizontal out to left rail (outside pad)
#    (rail_L,   ySm),            # vertical up to sense Y
#    (left_pad_edge_x, ySm),     # horizontal to just outside pad edge
#    (sense_padL_x, ySm)         # short horizontal into pad center
#], route_w)

# right pad left-edge (outside pad)
right_pad_edge_x = R_SENSE[0]

#add_path(L_PLATINUM, [
#    (end[0],   end[1]),         # meander end
#    (rail_R,   end[1]),         # horizontal out to right rail
#    (rail_R,   ySp),            # vertical to sense Y
#    (right_pad_edge_x, ySp),    # horizontal to just outside right pad edge
#    (sense_padR_x, ySp)         # short horizontal into pad center
#], route_w)

# ---- Labels ----
#add_text(L_TEXT, "Sm", L_SENSE[0]+pad_size/2, L_SENSE[1]+pad_size/2, label_h)
#add_text(L_TEXT, "Fm", L_FORCE[0]+pad_size/2, L_FORCE[1]+pad_size/2, label_h)
#add_text(L_TEXT, "Fp", R_FORCE[0]+pad_size/2, R_FORCE[1]+pad_size/2, label_h)
#add_text(L_TEXT, "Sp", R_SENSE[0]+pad_size/2, R_SENSE[1]+pad_size/2, label_h)

# ---- Save ----
ly.write(OUTPUT_PATH)
print(f"Wrote {OUTPUT_PATH}")
