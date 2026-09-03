# Kia EV6 / Hyundai E-GMP 95190-CV780 V2L Complete CAD System & Connector Lock

Comprehensive engineering repository containing high-fidelity, caliper-calibrated 3D CAD models of the vehicle outlet assembly, physical measurements ground truth, multimodal AI blueprints, and retention lock prototypes.

---

## 📂 Repository Structure

```text
hv_lock/
├── accurate_models/               # Master Caliper-Calibrated 3D CAD Models & AI Blueprints
│   ├── mated_assembly.stl         # Complete 3-part watertight mated assembly (8,708 faces)
│   ├── mated_assembly.obj         # 3-part assembly with materials & vertex colors
│   ├── mated_outer_housing.stl    # Outer cowl bezel & stamped aluminum bracket
│   ├── mated_outlet_box.stl       # Calibrated outlet box module
│   ├── mated_connector.stl        # Orange HV connector plug seated in receptacle collar
│   ├── mated_assembly_blueprint_ai.png # 5K Multimodal AI technical blueprint
│   ├── mated_assembly_blueprint_ai.json# Machine-readable metadata & coordinate anchors
│   ├── generate_ai_blueprint.py   # AI blueprint & JSON generator script
│   ├── build_accurate_models.py   # Master CAD synthesis script
│   ├── render_accurate_blueprints.py # Standard orthographic blueprint renderer
│   ├── outer_housing_measurements.json # Outer housing dimensional parameters
│   └── README_AI.md               # Detailed AI agent topology manual
│
├── caliper_measurements.csv       # Master physical caliper ground truth table
├── caliper_measurements.xlsx      # Formatted Excel workbook with calculations
├── README.md                      # Primary project overview (this file)
├── README_AI.md                   # AI topology atlas & datum reference guide
├── .gitignore                     # Git ignore rules
│
└── testing/                       # All Testing Scripts, Early Prototypes & Concept Iterations
    ├── chassis_bolt_lock.*        # Direct chassis bolt lock prototypes & prints
    ├── c_bracket.*                # 2-piece monolithic C-bracket prototypes & prints
    ├── exact_chassis_bolt_lock.*  # Calibrated chassis lock variations
    ├── concept1_notch_deadbolt.stl# Early concept 1 deadbolt
    ├── concept2_c_bracket_cage.stl# Early concept 2 cage
    ├── concept3_chassis_bracket_retainer.stl # Early concept 3 bracket
    ├── print_plate_all_parts.stl  # Combined print plates for prototype testing
    ├── build_*.py                 # Historical build scripts
    ├── illustrate_*.py            # Historical diagram generators
    ├── render_*.py                # Historical rendering scripts
    └── *.png                      # Historical test diagrams and blue prints
```

---

## 📐 Primary Production Deliverables (`accurate_models/`)

| File | Format | Description |
| :--- | :---: | :--- |
| **`mated_assembly.stl`** | STL (Binary) | Complete 3-part solid watertight assembly ($142.30 \times 166.71 \times 95.40\text{ mm}$) |
| **`mated_assembly.obj`** | OBJ | Multi-component assembly with materials, vertex colors, and normals |
| **`mated_outer_housing.stl`** | STL | Outer cowl bezel with smooth curved roof, $5.6^\circ$ wings, stamped aluminum plate |
| **`mated_outlet_box.stl`** | STL | Box enclosure seated $16.79\text{ mm}$ ahead of plate back ($3.04\text{ mm}$ hole clearance) |
| **`mated_connector.stl`** | STL | Orange HV connector plug seated in collar with confirmed $4.70\text{ mm}$ gap |
| **`mated_assembly_blueprint_ai.png`** | Image (5K) | Multimodal AI blueprint with all 35+ physical caliper measurement ties |
| **`mated_assembly_blueprint_ai.json`**| JSON | Machine-readable bounding boxes, datum reference frames, and tolerances |

---

## 🤖 AI & Multimodal System Reference

For AI agents, vision-language models, and automated CAD pipelines:
- Refer to [**`README_AI.md`**](README_AI.md) or [`accurate_models/README_AI.md`](accurate_models/README_AI.md) for full coordinate system specifications, topological constraints, and design rules for lock mechanisms.
