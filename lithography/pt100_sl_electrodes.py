# merge_electrodes_and_rtd_instances.py
import pya, os, sys

base_dir = os.path.dirname(os.path.abspath(__file__))
gds_elec = os.path.join(base_dir, "sulfilogger_electrodes_bak.gds")
gds_rtd  = os.path.join(base_dir, "pt100_rtd.gds")
gds_out  = os.path.join(base_dir, "rtd_sulfilogger.gds")

if not os.path.isfile(gds_elec):
    raise FileNotFoundError("Electrodes GDS not found: " + gds_elec)
if not os.path.isfile(gds_rtd):
    raise FileNotFoundError("RTD GDS not found: " + gds_rtd)

ly = pya.Layout()

# 1) Read electrodes file and get its top cell (destination)
ly.read(gds_elec)
elec_top = ly.top_cell()
if elec_top is None:
    raise RuntimeError("Could not determine electrodes top cell after reading electrodes GDS.")

# snapshot existing cell names before reading RTD
names_before = set([c.name for c in ly.each_cell()])

# 2) Read RTD file into same layout
ly.read(gds_rtd)

# find newly added cell names (from RTD file)
names_after = set([c.name for c in ly.each_cell()])
new_names = list(names_after - names_before)
if not new_names:
    raise RuntimeError("No new cells found after reading RTD GDS.")

# prefer PT100_RTD if present, otherwise take first new cell
rtd_cell = None
if "PT100_RTD" in new_names:
    rtd_cell = ly.cell("PT100_RTD")
else:
    rtd_cell = ly.cell(new_names[0])

if rtd_cell is None:
    raise RuntimeError("Could not find RTD cell in layout.")

# 3) Compute translations so RTD center (750,750) -> targets (-5500,0) and (-1000,0)
dbu = ly.dbu
if not dbu:
    dbu = 0.001   # µm per dbu fallback
scale = 1.0 / dbu  # µm -> dbu

def um_to_point(um_xy):
    return pya.Point(int(round(um_xy[0] * scale)), int(round(um_xy[1] * scale)))

rtd_center = um_to_point((750.0, 750.0))
targets = [um_to_point((-5400.0, 0.0)), um_to_point((-1000.0, 0.0))]

# 4) Insert instances into electrodes top cell
for i, tgt in enumerate(targets):
    dx = tgt.x - rtd_center.x
    dy = tgt.y - rtd_center.y

    # Mirror the second RTD horizontally
#    if i == 1:
#        trans = pya.Trans(pya.Trans.M0, pya.Point(dx, dy))
#    else:
#        trans = pya.Trans(pya.Trans.R0, pya.Point(dx, dy))
    trans = pya.Trans(pya.Point(dx, dy))
    inst = pya.CellInstArray(rtd_cell.cell_index(), trans)
    elec_top.insert(inst)


# 5) Write merged GDS (contains electrodes + two RTD instances)
ly.write(gds_out)
print("Wrote merged GDS:", gds_out)
