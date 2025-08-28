import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# --- Drawing helper ---
def draw_step(ax, step_id, step_desc,
              show_oxide=False, show_poly=False, patterned=False,
              poly_doped=False,
              substrate_thinned=False,
              show_ti=False, show_al=False,
              annealed=False):

    # Geometry constants
    W = 8.0
    H_sub = 1.0 if not substrate_thinned else 0.5
    H_ox = 0.2 if show_oxide else 0
    H_poly = 0.4 if show_poly else 0
    H_ti = 0.15 if show_ti else 0
    H_al = 0.25 if show_al else 0

    # --- Substrate ---
    ax.add_patch(Rectangle((0, 0), W, H_sub,
                           facecolor="#ffcc99", edgecolor="black"))
    ax.text(W/2, H_sub/2, "p-type Si substrate",
            ha='center', va='center', fontsize=10)

    # --- Gate oxide ---
    y_ox = H_sub
    if show_oxide:
        ax.add_patch(Rectangle((0, y_ox), W, H_ox,
                               facecolor="#ccccff", edgecolor="black"))
        ax.text(W/2, y_ox + H_ox/2, "Gate oxide (35 nm SiO₂)",
                ha='center', va='center', fontsize=10)

    # --- Poly-Si ---
    y_poly = y_ox + H_ox
    if show_poly:
        if patterned:
            gate_w = 4.0
            gate_x = (W - gate_w)/2
            ax.add_patch(Rectangle((gate_x, y_poly), gate_w, H_poly,
                                   facecolor="#777777" if poly_doped else "#999999",
                                   edgecolor="black"))
            label = "n⁺ polysilicon gate" if poly_doped else "Polysilicon gate"
            ax.text(W/2, y_poly + H_poly/2, label,
                    ha='center', va='center', fontsize=10, color='white')
        else:
            ax.add_patch(Rectangle((0, y_poly), W, H_poly,
                                   facecolor="#777777" if poly_doped else "#999999",
                                   edgecolor="black"))
            label = "n⁺ polysilicon (blanket)" if poly_doped else "Polysilicon (blanket)"
            ax.text(W/2, y_poly + H_poly/2, label,
                    ha='center', va='center', fontsize=10, color='white')

    # --- Backside Ti ---
    y_back = 0
    if show_ti:
        ax.add_patch(Rectangle((0, y_back - H_ti), W, H_ti,
                               facecolor="#9999cc", edgecolor="black"))
        ax.text(W/2, y_back - H_ti/2, "Backside Ti (100 nm)",
                ha='center', va='center', fontsize=9)
        y_back += H_ti

    # --- Backside Al ---
    y_al = y_back - H_ti
    if show_al:
        if annealed:
            ax.add_patch(Rectangle((0, y_al - H_al - H_ti), W, H_al,
            facecolor="#cccccc", edgecolor="black", hatch="////"))
            ax.text(W/2, y_al - H_ti - H_al/2, "Backside Al (400 nm, annealed)",
                ha='center', va='center', fontsize=9, fontweight='bold',
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.7))
            #ax.text(W/2, -0.15, "Ohmic contact formed",
                #ha='center', va='top', fontsize=9, fontweight='bold')
        else:
            ax.add_patch(Rectangle((0, y_al - H_al - H_ti), W, H_al,
                                   facecolor="#cccccc", edgecolor="black"))
            ax.text(W/2, y_al - H_ti - H_al/2, "Backside Al (400 nm)",
                    ha='center', va='center', fontsize=9)

    # --- Figure limits ---
    top_y = H_sub + H_ox + H_poly
    ax.set_xlim(-0.5, W + 0.5)
    ax.set_ylim(-0.5, top_y + 1.0)
    ax.axis('off')

    # --- Title ---
    #ax.set_title(f"{step_id} — {step_desc}", fontsize=12, pad=8)


# --- Key process steps ---
steps = [
    ("1.3", "Gate oxide growth", dict(show_oxide=True)),
    ("2.2", "Poly-Si deposition (blanket)", dict(show_oxide=True, show_poly=True)),
    ("3.2", "Poly-Si anneal (doped)", dict(show_oxide=True, show_poly=True, poly_doped=True)),
    ("4.6", "Gate poly etch", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True)),
    ("5.1", "Backside oxide strip", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, substrate_thinned=True)),
    ("6.5", "Backside Ti deposition", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, substrate_thinned=True, show_ti=True)),
    ("6.6", "Backside Al deposition", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, substrate_thinned=True, show_ti=True, show_al=True)),
    ("6.9", "Contact anneal", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, substrate_thinned=True, show_ti=True, show_al=True, annealed=True)),
]

# --- Output folder ---
out_dir = "moscap_steps"
os.makedirs(out_dir, exist_ok=True)

# --- Generate figures ---
for sid, desc, params in steps:
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_alpha(0.0)  # transparent background
    draw_step(ax, sid, desc, **params)

    base_filename = os.path.join(out_dir, f"moscap_step_{sid.replace('.', '-')}")
    fig.savefig(f"{base_filename}.png", dpi=200, bbox_inches="tight", transparent=True)
    fig.savefig(f"{base_filename}.pdf", bbox_inches="tight", transparent=True)
    plt.close(fig)

print(f"Saved all figures in '{out_dir}'")
