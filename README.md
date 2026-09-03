# Heavy-Duty V2L Cable Connector Lock (Kia EV6 / E-GMP 95190-CV780)

This project contains the complete 3D-printable external locking bracket system engineered to physically lock the orange V2L cable connector into the vehicle's black outlet box.

---

## 📂 Production Deliverables (Root Folder)

| File | Format | Description |
| :--- | :---: | :--- |
| **`print_plate_all_parts.stl`** | **STL (Binary)** | **Recommended: Both parts pre-arranged flat on build plate for 1-click support-free printing** |
| `print_plate_all_parts.obj` | OBJ | 3D mesh format with vertex normals |
| `c_bracket_spine.stl` | STL | Part 1: Monolithic structural C-Spine alone |
| `c_bracket_keeper.stl` | STL | Part 2: Toolless slide-in locking keeper alone |
| `c_bracket.scad` | OpenSCAD | Full parametric source code for adjusting dimensions |
| `how_it_works_explained.png` | Image | 4-step engineering storyboard explaining the mechanical trap |
| `c_bracket_blueprint.png` | Image | Dimensioned orthographic blueprint and cross-section |
| `caliper_measurements.xlsx` | Excel | Styled measurement spreadsheet with confirmed caliper data |
| `caliper_measurements.csv` | CSV | Raw caliper measurements |

All testing scripts, intermediate iterations, and reference models have been archived into the `testing/` subdirectory.

---

## 🖨️ Recommended Slicer Settings

- **File to Open**: `print_plate_all_parts.stl`
- **Material**: **PETG** (Recommended for automotive heat/creep resistance) or ABS / ASA
- **Layer Height**: `0.20 mm`
- **Perimeters / Walls**: **4 walls** (Critical for maximum tensile strength of the spine)
- **Top / Bottom Layers**: `5 top` / `5 bottom`
- **Infill**: `40% Gyroid or Grid`
- **Supports**: **0% (NONE)** — 100% support-free design
- **Print Time**: ~65–70 minutes total on standard FDM printers (Bambu Lab, Prusa, Creality)

---

## 🔒 3-Step Operation Flow

1. **Plug In**: Push the orange connector into the car's outlet receptacle until seated ($4.7\text{ mm}$ gap).
2. **Drop C-Spine**: Hook the top lip of the blue C-Spine over the top edge of the black outlet box lid.
3. **Slide Keeper**: Slide the green keeper into the bottom track with your thumb until it clicks into the snap detents.
   - *Result*: The orange connector's rigid shoulder is trapped against the keeper. Pulling on the cable is directly resisted by the rigid box lid with $>40\text{ kg}$ ($90\text{ lbs}$) of pullout strength!
   - *To Unplug*: Push the green thumb tab and slide the keeper out.
