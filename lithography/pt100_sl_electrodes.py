import pya, os, sys, math

base_dir = os.path.dirname(os.path.abspath(__file__))
gds_elec = os.path.join(base_dir, "sulfilogger_electrodes_noleads.gds")
gds_rtd  = os.path.join(base_dir, "pt100_rtd.gds")
gds_out  = os.path.join(base_dir, "rtd_sulfilogger.gds")

if not os.path.isfile(gds_elec):
    raise FileNotFoundError("Electrodes GDS not found: " + gds_elec)
if not os.path.isfile(gds_rtd):
    raise FileNotFoundError("RTD GDS not found: " + gds_rtd)

ly = pya.Layout()

ly.read(gds_elec)
elec_top = ly.top_cell()
if elec_top is None:
    raise RuntimeError("Could not determine electrodes top cell after reading electrodes GDS.")

names_before = set([c.name for c in ly.each_cell()])

ly.read(gds_rtd)

names_after = set([c.name for c in ly.each_cell()])
new_names = list(names_after - names_before)
if not new_names:
    raise RuntimeError("No new cells found after reading RTD GDS.")

rtd_cell = None
if "PT100_RTD" in new_names:
    rtd_cell = ly.cell("PT100_RTD")
else:
    rtd_cell = ly.cell(new_names[0])

if rtd_cell is None:
    raise RuntimeError("Could not find RTD cell in layout.")

dbu = ly.dbu
if not dbu:
    dbu = 0.001   

scale = 1.0 / dbu  

def um_to_point(um_xy):
    return pya.Point(int(round(um_xy[0] * scale)), int(round(um_xy[1] * scale)))

rtd_center = um_to_point((750.0, 750.0))
targets = [um_to_point((-5400.0, 0.0)), um_to_point((-1000.0, 0.0))]

for i, tgt in enumerate(targets):
    dx = tgt.x - rtd_center.x
    dy = tgt.y - rtd_center.y

    trans = pya.Trans(pya.Point(dx, dy))
    inst = pya.CellInstArray(rtd_cell.cell_index(), trans)
    elec_top.insert(inst)

w_wide   = 200.0
w_narrow = 60.0   
l_trace  = ly.layer(3, 0)

def create_horizontal_taper(p_start, p_end, width_start, width_end):
    x1, y1 = p_start
    x2, y2 = p_end
    hw1 = width_start / 2.0
    hw2 = width_end / 2.0

    c1 = um_to_point((x1, y1 + hw1)) 
    c2 = um_to_point((x1, y1 - hw1)) 
    c3 = um_to_point((x2, y2 - hw2)) 
    c4 = um_to_point((x2, y2 + hw2)) 
    return pya.Polygon([c1, c2, c3, c4])

traces_wide = [
    # Sensor 1
    [(-6500, 260), (-5850, 260)],
    [(-6500, -260), (-5850, -260)],
    [(-6500, 700), (-5850, 700), (-5685,570), (-5685,340)],
    [(-6500, -700), (-5850, -700), (-5685,-570), (-5685,-340)],
    # Sensor 2
    [(-6500, 1260), (-4600, 1260),(-1685,315),(-1445,315)],
    [(-6500, -1260), (-4600, -1260), (-1685,-315), (-1445,-315)],
    [(-6500, 1700), (-4050, 1700), (-1283,500), (-1283,340)],
    [(-6500, -1700), (-4050, -1700), (-1283,-500), (-1283,-340)]
]

taper_defs = [
    # Sensor 1
    ((-5850, 260), (-5784, 315)),
    ((-5850, -260), (-5784, -315)),
    # Sensor 2
    ((-1445,315), (-1384, 315)),
    ((-1445,-315), (-1384, -315))
    
]

print(f"Generating Wide traces...")
for pts in traces_wide:
    path_pts = [um_to_point(p) for p in pts]
    path = pya.Path(path_pts, int(round(w_wide * scale)))
    elec_top.shapes(l_trace).insert(path)

print(f"Generating Horizontal Tapers...")
for p_start, p_end in taper_defs:
    poly = create_horizontal_taper(p_start, p_end, w_wide, w_narrow)
    elec_top.shapes(l_trace).insert(poly)

ly.write(gds_out)
print("Wrote merged GDS:", gds_out)

