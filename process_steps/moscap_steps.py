import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# --- Drawing helper ---
def draw_step(ax, step_id, step_desc,
              show_oxide=False, show_poly=False, patterned=False,
              poly_doped=False, show_top_pad=False,
              locos=False, show_back_oxide=False,
              show_back_ti=False, show_back_al=False, annealed=False):
    
    # --- Base wafer ---
    W = 8.0
    H_total = 1.0  # total height of substrate for proportional scaling

    # Proportional heights (scaled relative to substrate)
    H_sub = H_total
    H_ox = max(0.1, 0.2 * show_oxide)          # gate oxide
    H_poly = max(0.15, 0.4 * show_poly)        # poly-Si
    H_pad = 0.15 if show_top_pad else 0        # top pad
    H_back_oxide = 0.10 if show_back_oxide else 0
    H_ti = 0.10 if show_back_ti else 0
    H_al = 0.15 if show_back_al else 0

    # --- Substrate ---
    ax.add_patch(Rectangle((0, 0), W, H_sub,
                           facecolor="#ffcc99", edgecolor="black"))
    ax.text(W/2, H_sub/2, "p-type Si substrate",
            ha='center', va='center', fontsize=10)

    # --- LOCOS isolation ---
    if locos:
        locos_w = 1.0
        locos_h = 0.4
        ax.add_patch(Rectangle((0, H_sub), locos_w, locos_h,
                               facecolor="#ccccff", edgecolor="black"))
        ax.add_patch(Rectangle((W-locos_w, H_sub), locos_w, locos_h,
                               facecolor="#ccccff", edgecolor="black"))
        ax.text(W/2, H_sub + locos_h/2, "LOCOS field oxide", ha='center', va='center', fontsize=9)

    # --- Gate oxide ---
    y_ox = H_sub
    if show_oxide:
        ax.add_patch(Rectangle((0, y_ox), W, H_ox, facecolor="#ccccff", edgecolor="black"))
        ax.text(W/2, y_ox + H_ox/2, "Gate oxide (35 nm SiO₂)", ha='center', va='center', fontsize=10)

    # --- Poly-Si ---
    y_poly = y_ox + H_ox
    if show_poly:
        if patterned:
            gate_w = 4.0
            gate_x = (W - gate_w)/2
            ax.add_patch(Rectangle((gate_x, y_poly), gate_w, H_poly,
                                   facecolor="#777777" if poly_doped else "#999999",
                                   edgecolor="black"))
            ax.text(W/2, y_poly + H_poly/2,
                    "n⁺ polysilicon gate" if poly_doped else "Polysilicon gate",
                    ha='center', va='center', fontsize=10, color='white')
            if show_top_pad:
                pad_w = gate_w + 1.0
                pad_h = H_pad
                pad_x = (W - pad_w)/2
                ax.add_patch(Rectangle((pad_x, y_poly + H_poly), pad_w, pad_h,
                                       facecolor="#cccccc", edgecolor="black"))
                ax.text(W/2, y_poly + H_poly + pad_h/2,
                        "Top metal pad", ha='center', va='center', fontsize=9)
        else:
            ax.add_patch(Rectangle((0, y_poly), W, H_poly,
                                   facecolor="#777777" if poly_doped else "#999999",
                                   edgecolor="black"))
            ax.text(W/2, y_poly + H_poly/2,
                    "n⁺ polysilicon (blanket)" if poly_doped else "Polysilicon (blanket)",
                    ha='center', va='center', fontsize=10, color='white')

    # --- Backside layers ---
    y_back = 0  # wafer backside at y=0
    if show_back_oxide:
        ax.add_patch(Rectangle((0, y_back), W, H_back_oxide, facecolor="#e6e6ff", edgecolor="black"))
        ax.text(W/2, y_back + H_back_oxide/2, "Backside oxide (thin)", ha='center', va='center', fontsize=9)
        #y_back -= H_back_oxide

    if show_back_ti:
        ax.add_patch(Rectangle((0, y_back), W, H_ti, facecolor="#9999cc", edgecolor="black"))
        ax.text(W/2, y_back + H_ti/2, "Backside Ti (100 nm)", ha='center', va='center', fontsize=9)
        y_back -= 1.5*H_ti

    if show_back_al:
        if annealed:
            ax.add_patch(Rectangle((0, y_back), W, H_al, facecolor="#cccccc", edgecolor="black", hatch="////"))
            ax.text(W/2, y_back + H_al/2, "Backside Al (400 nm, annealed)", ha='center', va='center', fontsize=9)
            ax.text(W/2, y_back - 0.05, "Alloyed contact formed", ha='center', va='top', fontsize=9)
        else:
            ax.add_patch(Rectangle((0, y_back), W, H_al, facecolor="#cccccc", edgecolor="black"))
            ax.text(W/2, y_back + H_al/2, "Backside Al (400 nm)", ha='center', va='center', fontsize=9)

    # --- Figure limits ---
    top_y = H_sub + H_ox + H_poly + (H_pad if show_top_pad else 0)
    ax.set_xlim(-0.5, W + 0.5)
    ax.set_ylim(-0.5, top_y + 0.5)
    ax.axis('off')

    # --- Title ---
    ax.set_title(f"{step_id} — {step_desc}", fontsize=12, pad=8)


# --- Process steps ---
steps = [
    ("0.1", "LOCOS isolation (optional)", dict(locos=True)),
    ("1.1", "Pre-oxidation clean (HF-last)", dict()),
    ("2.1", "Gate oxide growth", dict(show_oxide=True)),
    ("3.1", "Poly-Si deposition (blanket)", dict(show_oxide=True, show_poly=True)),
    ("3.2", "Poly doping + anneal", dict(show_oxide=True, show_poly=True, poly_doped=True)),
    ("4.1", "Gate patterning", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, show_top_pad=False)),
    ("5.0", "Backside oxide strip", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, show_back_oxide=True, show_top_pad=True)),
    ("5.1", "Backside Ti deposition", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, show_back_ti=True, show_top_pad=True)),
    ("5.2", "Backside Al deposition", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, show_back_ti=True, show_back_al=True, show_top_pad=True)),
    ("5.3", "Contact anneal", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, show_back_ti=True, show_back_al=True, annealed=True, show_top_pad=True)),
]

# --- Output folder ---
out_dir = os.path.join("process_steps", "moscap")
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
