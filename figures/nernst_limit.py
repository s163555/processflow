import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(10,4))

# Define realistic pH range
pH_values = [4, 6, 8, 10]

# --- (a) Nernst-limited ISFET ---
nernst_output = [(ph-4)*59 for ph in pH_values]  # 59 mV per pH unit relative to pH 4 baseline
axs[0].plot(pH_values, nernst_output, marker='o', color='tab:blue')
axs[0].set_title("(a) Nernst-limited ISFET")
axs[0].set_xlabel("pH value")
axs[0].set_ylabel("Output voltage (mV)")
axs[0].set_xticks(pH_values)
axs[0].set_ylim(0,260)
axs[0].grid(True, linestyle="--", alpha=0.6)
axs[0].text(6.2, 200, "≈59 mV/pH\n(Nernst limit)", fontsize=9, color="tab:blue")

# --- (b) CCD with accumulation cycles ---
out_1cycle = [(ph-4)*59 for ph in pH_values]
out_100cycles = [(ph-4)*240 for ph in pH_values]  # ~240 mV/pH from paper
axs[1].plot(pH_values, out_1cycle, marker='o', color='tab:blue', label="Single cycle")
axs[1].plot(pH_values, out_100cycles, marker='o', color='tab:red', label="100 cycles (CCD)")
axs[1].set_title("(b) CCD with accumulation cycles")
axs[1].set_xlabel("pH value")
axs[1].set_ylabel("Output voltage (mV)")
axs[1].legend()
axs[1].grid(True, linestyle="--", alpha=0.6)
#axs[1].set_ylim(0,1000)

plt.suptitle("Comparison: Nernst-limited ISFET vs CCD-based pH Sensor", fontsize=12)
plt.tight_layout(rect=[0,0,1,0.95])

# Save
file_path = "Nernst_vs_CCD_realistic.png"
plt.savefig(file_path, dpi=300)
plt.close()

file_path
