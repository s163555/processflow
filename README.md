# Nanolab fabrication process workflows

This repository contains documentation, cross-section illustrations, and LaTeX source files for the fabrication of various devices. It is intended as a reference for fabrication support staff and research engineers. The file `template.tex` can be used for developing further process flows.

---

## Repository Structure

```
moscap/
├── figures/process_steps/
│ ├── moscap_steps.py # Script that generates PDF/PNG cross-section illustrations per process step
│ ├── moscap/moscap_step_0-1.pdf
│ ├── moscap/moscap_step_1-1.pdf
│ └── ...
├── figures/
│ ├── moscap_mwe_flow.tikz # TikZ diagram of the full process flow
├── .gitignore # Revision control template
├── moscap_mwe.tex # Minimal MOS Capacitor Process
├── template.tex # Document template with styling and macros
└── README.md # This file
```

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