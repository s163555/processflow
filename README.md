# Nanolab fabrication process workflows

This repository contains documentation, cross-section illustrations, and LaTeX source files for the fabrication of various devices. It is intended as a reference for fabrication support staff and research engineers. The file `template.tex` can be used for developing further process flows.

---

## Quick Start

To generate the documentation:

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/s163555/processflow
   cd processflow
   ```
2. **Install dependencies** (assuming python is installed):
   ```bash
   pip install matplotlib numpy
   ```
3. **Generate figures**:
   ```bash
	python figures/process_steps/moscap_steps.py
   ```
4. **Compile LaTeX document** (assuming texlive is installed):
   ```bash
   lualatex moscap.tex
	```

---

## Repository Structure

```
processflow/
├── figures/
│ ├── process_steps/
│ │ ├── moscap/
│ │ │ ├── moscap_step_0-1.pdf
│ │ │ ├── moscap_step_1-1.pdf
│ │ │ └── ...
│ │ └── moscap_steps.py # Script that generates PDF/PNG cross-section illustrations per process step
│ └── moscap_mwe_flow.tikz # TikZ diagram of the full process flow
├── .gitignore # Revision control template
├── moscap_mwe.tex # Minimal MOS Capacitor Process
├── template.tex # Document template with styling and macros
└── README.md # This file
```

---

## Scripts

- `figures/process_steps/moscap_steps.py`: generates proportional cross-section figures (`.png` and `.pdf`) in `figures/process_steps/moscap`.  
- Ensure `matplotlib` and `numpy` are installed to run the script.

---

## License

This repository is for internal research and fabrication documentation. Redistribution or use outside DTU Nanolab requires permission.

---

## Contact

**Jeppe Hinrichs**  
Email: jephin@dtu.dk  
Phone: Not applicable