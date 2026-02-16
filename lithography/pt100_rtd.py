import pya
import os

die_w = 1500.0; die_h = 1500.0
w_line = 60.0; gap = 35.0; pitch = w_line + gap
runs = 8; run_len = 550.0
script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(script_dir, "pt100_rtd.gds")

ly = pya.Layout(); ly.dbu = 0.001
top = ly.create_cell("PT100_RTD")
L_PLATINUM = ly.layer(1,0)

def um(x_um): return int(round(x_um / ly.dbu))
def add_path(layer, pts, width):
    p = pya.Path([pya.Point(um(x),um(y)) for x,y in pts], um(width))
    top.shapes(layer).insert(p.polygon())

cx, cy = die_w/2.0, die_h/2.0
me_w = run_len
me_h = (runs-1)*pitch + w_line
left  = cx - me_w/2.0
right = cx + me_w/2.0
y0    = cy - me_h/2.0 + w_line/2.0

pts = []
y = y0
for i in range(runs):

    if i % 2 == 0: 
        pts += [(left, y), (right, y)]

    else:          
        pts += [(right, y), (left, y)]

    if i < runs-1: y += pitch

extension = w_line / 2.0 + 60

pts[0] = (pts[0][0] - extension, pts[0][1])

if runs % 2 == 0:

    pts[-1] = (pts[-1][0] - extension, pts[-1][1])
else:

    pts[-1] = (pts[-1][0] + extension, pts[-1][1])

add_path(L_PLATINUM, pts, w_line)

ly.write(OUTPUT_PATH)
print(f"Wrote {OUTPUT_PATH}")