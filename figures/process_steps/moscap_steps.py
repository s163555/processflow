import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# --- Drawing helper ---
def draw_step(ax, step_id, step_desc,
              show_oxide=False, show_poly=False, patterned=False,
              poly_doped=False, backside_poly_etched=False,
              backside_oxide_etched=False,
              show_ti=False, show_al=False, patterned_backside=False, annealed=False):

    # Geometry constants
    W = 8.0
    H_sub = 1.0
    H_ox = 0.2 if show_oxide else 0
    H_poly = 0.4 if show_poly else 0
    H_ti = 0.15 if show_ti else 0
    H_al = 0.25 if show_al else 0
    
    # Backside layer thicknesses (thinner than frontside)
    H_ox_back = 0.1 if show_oxide else 0
    H_poly_back = 0.2 if show_poly else 0

    # --- Substrate ---
    ax.add_patch(Rectangle((0, 0), W, H_sub,
                           facecolor="#ffcc99", edgecolor="black"))
    ax.text(W/2, H_sub/2, "p-type Si substrate",
            ha='center', va='center', fontsize=10)

    # --- Backside oxide (if not etched) ---
    y_back = 0
    if show_oxide and not backside_oxide_etched:
        ax.add_patch(Rectangle((0, y_back - H_ox_back), W, H_ox_back,
                               facecolor="#e6e6ff", edgecolor="black"))
        #ax.text(W/2, y_back - H_ox_back/2, "Backside oxide\n(35 nm)",
                #ha='center', va='center', fontsize=8)

    # --- Backside poly-Si (if not etched) ---
    y_poly_back = y_back - H_ox_back if show_oxide and not backside_oxide_etched else y_back
    if show_poly and not backside_poly_etched:
        ax.add_patch(Rectangle((0, y_poly_back - H_poly_back), W, H_poly_back,
                               facecolor="#999999", edgecolor="black"))
        #ax.text(W/2, y_poly_back - H_poly_back/2, "Backside poly-Si",
                #ha='center', va='center', fontsize=8, color='white')

    # --- Gate oxide ---
    y_ox_top = H_sub
    if show_oxide:
        ax.add_patch(Rectangle((0, y_ox_top), W, H_ox,
                               facecolor="#ccccff", edgecolor="black"))
        ax.text(W/2, y_ox_top + H_ox/2, "Gate oxide (35 nm SiO₂)",
                ha='center', va='center', fontsize=10)

    # --- Poly-Si ---
    y_poly_top = y_ox_top + H_ox
    if show_poly:
        if patterned:
            gate_w = 4.0
            gate_x = (W - gate_w)/2
            ax.add_patch(Rectangle((gate_x, y_poly_top), gate_w, H_poly,
                                   facecolor="#777777" if poly_doped else "#999999",
                                   edgecolor="black"))
            label = "n⁺ polysilicon gate" if poly_doped else "Polysilicon gate"
            ax.text(W/2, y_poly_top + H_poly/2, label,
                    ha='center', va='center', fontsize=10, color='white')
        else:
            ax.add_patch(Rectangle((0, y_poly_top), W, H_poly,
                                   facecolor="#777777" if poly_doped else "#999999",
                                   edgecolor="black"))
            label = "n⁺ polysilicon (blanket)" if poly_doped else "Polysilicon (blanket)"
            ax.text(W/2, y_poly_top + H_poly/2, label,
                    ha='center', va='center', fontsize=10, color='white')

# --- Backside Ti ---
    if show_ti:
        y_ti = y_poly_back - H_poly_back if show_poly and not backside_poly_etched else y_back
        y_ti = y_ti - H_ox_back if show_oxide and not backside_oxide_etched else y_ti
        
        if patterned_backside:
            elec_w = 4.0
            elec_x = (W - elec_w)/2
            ax.add_patch(Rectangle((elec_x, y_ti - H_ti), elec_w, H_ti,
                                facecolor="#9999cc", edgecolor="black"))
        else:
            ax.add_patch(Rectangle((0, y_ti - H_ti), W, H_ti,
                                facecolor="#9999cc", edgecolor="black"))
        ax.text(W/2, y_ti - H_ti/2, "Backside Ti (100 nm)",
                ha='center', va='center', fontsize=9)

    # --- Backside Al ---
    if show_al:
        y_al = y_ti - H_ti if show_ti else y_back_metal
        if patterned_backside:
            elec_w = 4.0
            elec_x = (W - elec_w)/2
            ax.add_patch(Rectangle((elec_x, y_al - H_al), elec_w, H_al,
                                facecolor="#cccccc", edgecolor="black",
                                hatch="////" if annealed else None))
        else:
            ax.add_patch(Rectangle((0, y_al - H_al), W, H_al,
                                facecolor="#cccccc", edgecolor="black",
                                hatch="////" if annealed else None))
        label = "Backside Al (400 nm, annealed)" if annealed else "Backside Al (400 nm)"
        ax.text(W/2, y_al - H_al/2, label,
                ha='center', va='center', fontsize=9,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.7) if annealed else None)

    # --- Figure limits ---
    top_y = H_sub + H_ox + H_poly
    bottom_y = -0.5  # Fixed bottom limit
    
    # Adjust bottom limit if backside layers extend below
    if show_oxide and not backside_oxide_etched:
        bottom_y = min(bottom_y, -H_ox_back - 0.1)
    if show_poly and not backside_poly_etched:
        bottom_y = min(bottom_y, -H_ox_back - H_poly_back - 0.1)
    if show_ti:
        bottom_y = min(bottom_y, -H_ti - 0.1)
    if show_al:
        bottom_y = min(bottom_y, -H_ti - H_al - 0.1)
    
    ax.set_xlim(-0.5, W + 0.5)
    ax.set_ylim(bottom_y, top_y + 0.5)
    ax.axis('off')

# --- Key process steps ---
steps = [
    ("1.1", "Start: Clean Si wafer", dict()),
    ("1.3", "Gate oxide growth", dict(show_oxide=True)),
    ("2.2", "Poly-Si deposition (blanket)", dict(show_oxide=True, show_poly=True)),
    ("3.2", "Poly-Si anneal (doped)", dict(show_oxide=True, show_poly=True, poly_doped=True)),
    ("4.2", "Backside poly-Si etch", dict(show_oxide=True, show_poly=True, poly_doped=True, 
                                         backside_poly_etched=True)),
    ("5.1", "Backside oxide etch", dict(show_oxide=True, show_poly=True, poly_doped=True, 
                                       backside_poly_etched=True, backside_oxide_etched=True)),
    ("6.6", "Gate poly etch", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, 
                                  backside_poly_etched=True, backside_oxide_etched=True)),
    ("7.5", "Backside Ti deposition", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, 
                                         backside_poly_etched=True, backside_oxide_etched=True, show_ti=True, patterned_backside=True)),
    ("7.6", "Backside Al deposition", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, 
                                         backside_poly_etched=True, backside_oxide_etched=True, 
                                         show_ti=True, show_al=True, patterned_backside=True)),
    ("7.9", "Contact anneal", dict(show_oxide=True, show_poly=True, patterned=True, poly_doped=True, 
                                  backside_poly_etched=True, backside_oxide_etched=True,
                                  show_ti=True, show_al=True, patterned_backside=True, annealed=True)),
]

# --- Output folder ---
out_dir = "moscap_steps"
os.makedirs(out_dir, exist_ok=True)

# --- Generate figures ---
for sid, desc, params in steps:
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0.0)  # transparent background
    draw_step(ax, sid, desc, **params)
    
    # Add step title
    #ax.set_title(f"{sid} — {desc}", fontsize=12, pad=10)

    base_filename = os.path.join(out_dir, f"moscap_step_{sid.replace('.', '-')}")
    fig.savefig(f"{base_filename}.png", dpi=200, bbox_inches="tight", transparent=True)
    fig.savefig(f"{base_filename}.pdf", bbox_inches="tight", transparent=True)
    plt.close(fig)

print(f"Saved all figures in '{out_dir}'")