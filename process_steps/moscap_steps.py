import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# Drawing helper
def draw_step(ax, step_id, step_desc, show_oxide=False, show_poly=False, patterned=False, show_back_al=False, annealed=False):
    # Geometry constants
    W = 8.0
    H_sub = 1.0
    H_ox = 0.2 if show_oxide else 0   # Thicker oxide so label fits
    H_poly = 0.4
    H_al = 0.1
    
    # Substrate
    ax.add_patch(Rectangle((0, 0), W, H_sub, facecolor="#ffcc99", edgecolor="black"))
    
    # Oxide
    if show_oxide:
        ax.add_patch(Rectangle((0, H_sub), W, H_ox, facecolor="#ccccff", edgecolor="black"))
    
    # Poly-Si (blanket or patterned)
    if show_poly:
        if patterned:
            gate_w = 4.0
            gate_x = (W - gate_w) / 2
            ax.add_patch(Rectangle((gate_x, H_sub + H_ox), gate_w, H_poly, facecolor="#999999", edgecolor="black"))
        else:
            ax.add_patch(Rectangle((0, H_sub + H_ox), W, H_poly, facecolor="#999999", edgecolor="black"))
    
    # Backside Al
    if show_back_al:
        ax.add_patch(Rectangle((0, -0.2), W, H_al, facecolor="#cccccc", edgecolor="black"))
    
    # Labels
    ax.text(W/2, -0.5, "p-type Si substrate", ha='center', va='center', fontsize=10)
    if show_oxide:
        ax.text(W/2, H_sub + H_ox/2, "Gate oxide (35 nm SiO₂)", ha='center', va='center', fontsize=10)
    if show_poly and patterned:
        ax.text(W/2, H_sub + H_ox + H_poly/2, "n⁺ polysilicon gate (patterned)", 
                ha='center', va='center', fontsize=10, color='white')
    elif show_poly:
        ax.text(W/2, H_sub + H_ox + H_poly/2, "n⁺ polysilicon (blanket)", 
                ha='center', va='center', fontsize=10, color='white')
    if show_back_al:
        ax.text(W/2, -0.35, "Backside Al contact (400 nm)", ha='center', va='center', fontsize=9)
    
    # Top surface line
    #top_y = H_sub + H_ox + (H_poly if show_poly else 0)
    #ax.plot([0, W], [top_y, top_y], color='black', linewidth=0.5)
    
    # Formatting
    ax.set_xlim(-0.5, W + 0.5)
    ax.set_ylim(-0.6, 2.0)
    ax.axis('off')
    
    # Title
    title = f"{step_id} — {step_desc}"
    if annealed:
        title += " (RTP 450 °C, 30 min)"
    ax.set_title(title, fontsize=12, pad=8)

# Define process steps
steps = [
    ("1.1", "RCA clean", dict(show_oxide=False, show_poly=False, patterned=False, show_back_al=False, annealed=False)),
    ("2.1", "SiO₂ growth", dict(show_oxide=True, show_poly=False, patterned=False, show_back_al=False, annealed=False)),
    ("3.1", "Poly-Si deposition (blanket)", dict(show_oxide=True, show_poly=True, patterned=False, show_back_al=False, annealed=False)),
    ("4.1", "Gate patterning", dict(show_oxide=True, show_poly=True, patterned=True, show_back_al=False, annealed=False)),
    ("5.1", "Back Al deposition", dict(show_oxide=True, show_poly=True, patterned=True, show_back_al=True, annealed=False)),
    ("5.2", "Contact anneal", dict(show_oxide=True, show_poly=True, patterned=True, show_back_al=True, annealed=True)),
]

# Output folder
out_dir = "moscap"
os.makedirs(out_dir, exist_ok=True)

# Generate figures
for sid, desc, params in steps:
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_alpha(0.0)  # transparent background
    draw_step(ax, sid, desc, **params)

    # Filenames
    base_filename = os.path.join(out_dir, f"moscap_step_{sid.replace('.', '-')}")
    png_path = f"{base_filename}.png"
    pdf_path = f"{base_filename}.pdf"
    
    # Save files
    fig.savefig(png_path, dpi=200, bbox_inches="tight", transparent=True)
    fig.savefig(pdf_path, bbox_inches="tight", transparent=True)
    plt.close(fig)

print(f"Saved all figures in '{out_dir}'")
