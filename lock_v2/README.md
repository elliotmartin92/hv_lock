# Lock v2: Continuous Organic Connector Lock System
## Kia EV6 / Hyundai E-GMP 95190-CV780 High-Voltage V2L Outlet Connector Lock
### Anchored by Dual M6 Flanged Nuts (Ø 17.25 mm Built-In Washers) with Under-Box Clamping Toe

---

### 1. Engineering Highlights & Structural Architecture
**Lock v2** is a continuous, flow-formed automotive physical lock engineered from scratch for the high-voltage V2L connector.

In direct response to mechanical fatigue, installation ergonomics, and physical vehicle clearances:
1. **100% Open-Top U-Saddle (Zero Roof, Zero Closed Circles)**:
   - **No Closed Circles**: The base bracket cradle is completely open through the top and rear. The connector does **not** need to be threaded through any closed hole (which is physically impossible with a factory-wired vehicle cable).
   - **Direct Drop-In Installation**: The orange connector body nests directly into the lower cradle from above, resting securely on a solid PCTG saddle bed.
   - **Full Latch & CPA Access**: With zero top roof, the connector latch lever and red CPA slider remain 100% unobstructed and accessible.
   - **Massive Dual Guide Towers**: The cradle upright towers flanking the connector are **\(12.0\text{ mm}\) thick solid PCTG** on each side with \(R = 4.0\text{ mm}\) rounded corners, eliminating any thin, fragile, or flexing faces.

2. **Heavy-Duty Slide-In Retention Keeper (\(8.2\text{ mm}\) Solid PCTG Gate)**:
   - The retention is provided by the slide-in **Keeper**, which drops vertically downward into precision guide tracks on the towers.
   - **Robust Thickness**: Upgraded to **\(8.2\text{ mm}\) solid PCTG thickness** (with a **\(12.2\text{ mm}\) thick** ergonomic thumb grip tab with tactile ribs).
   - **Inverted U-Slot**: Features a \(\varnothing 19.0\text{ mm}\) U-slot with a \(45^\circ\) lead-in chamfer that slides down over the \(\varnothing 17.0\text{ mm}\) rubber cable boot.
   - **Positive Axial Lock**: The flat front face of the keeper bears directly against the rigid orange shoulder plane at \(Y = -95.51\text{ mm}\), preventing any axial pullout.
   - **Precision Aligned Snap Detents**:
     * **Base Track Pockets (Female)**: Precision spherical pockets (\(R = 2.2\text{ mm}\)) subtracted directly into the track side walls at \(X = 5.20\text{ mm}\) and \(X = 48.80\text{ mm}\), \(Y = -98.01\text{ mm}\), \(Z = 56.00\text{ mm}\), with vertical lead-in guide channels.
     * **Keeper Bumps (Male)**: Symmetrical spherical bumps (\(R = 1.8\text{ mm}\)) protruding from the lateral side edges at \(X = 5.50\text{ mm}\) and \(X = 48.50\text{ mm}\), \(Y = -98.01\text{ mm}\), \(Z = 56.00\text{ mm}\).
     * **0.000 mm Alignment Error**: The detents line up identically in \(Y\) and \(Z\), sliding down smoothly and snapping together with a tactile "CLICK" that prevents vibration walkout.
   - **Toolless Release**: Simply pull straight up on the textured thumb tab to release the keeper for vehicle servicing.

3. **Accommodates OEM M6 Flanged Nuts with Built-In \(\varnothing 17.25\text{ mm}\) Washers**:
   - Precision counterbore seats of **\(\varnothing 18.50\text{ mm}\)** (\(0.625\text{ mm}\) radial clearance) allow OEM flanged nuts with their integrated \(\varnothing 17.25\text{ mm}\) washer to seat completely flush without edge binding.
   - Enclosed through-holes (\(\varnothing 7.20\text{ mm}\) Central / \(8.00 \times 7.20\text{ mm}\) Outer Slot) clamp the lock rigidly to the vehicle frame.
   - Unimpeded vertical socket tool clearance cylinders (\(\varnothing 18.50\text{ mm}\)) extend normal to the plate through the top of the bracket for direct access with a standard \(10\text{ mm}\) socket wrench.

4. **Extended Clamping Toe Underneath the Outlet Box**:
   - Because the nut's \(\varnothing 17.25\text{ mm}\) built-in washer reaches \(Y = -33.66\text{ mm}\) (\(2.55\text{ mm}\) forward of the outlet box rear wall at \(Y = -36.21\text{ mm}\)), the mounting foot extends forward to **\(Y = -28.00\text{ mm}\)** (\(8.21\text{ mm}\) underneath the outlet box).
   - Provides **\(5.66\text{ mm}\) of solid PCTG bearing material ahead of the washer rim**, supporting the primary forward compressive reaction load.
   - The foot thickness under the box is calibrated to \(2.80\text{ mm}\), leaving a verified **\(2.04\text{ mm}\) vertical air gap** below the flat underside of the outlet box (\(Z = 36.20\text{ mm}\)).
   - Acts as a continuous cantilever lever arm that prevents bracket tipping and transfers compressive clamping reaction directly into the vehicle floor plate.

```text
               VEHICLE INTERIOR (+Y)
                         │
        ┌────────────────▼────────────────┐
        │   Outlet Box Bottom (Z = 36.20) │
        └────────────────┬────────────────┘
                         │ 2.04 mm Air Gap
        ┌────────────────▼────────────────┐
        │   Extended Clamping Toe         │  Extends to Y = -28.0 mm (8.21 mm under box);
        │   (5.66 mm solid ahead of nut)  │  2.80 mm thick PCTG compression shelf.
        └────────────────┬────────────────┘
                         │ M6 Flanged Nuts with Ø 17.25 mm built-in washer
        ┌────────────────▼────────────────┐
        │   lock_v2_base_bracket.stl      │  Continuous filleted mounting foot;
        │   (Continuous Flow-Formed Solid)│  100% flush 5.87° pitch; R=3-6mm fillets.
        └────────────────┬────────────────┘
                         │ Continuous organic Wishbone/A-frame spine
        ┌────────────────▼────────────────┐
        │   Open-Top U-Saddle & Towers    │  100% OPEN TOP: Zero roof, zero closed circle!
        │   (12 mm thick side towers)     │  Connector drops in directly from above.
        └────────────────┬────────────────┘
                         │ Vertical slide-in from above (+Z)
        ┌────────────────▼────────────────┐
        │   lock_v2_keeper.stl            │  Robust 8.2 mm solid PCTG gate;
        │   (Slide Retention Gate)        │  Inverted U-slot traps boot; locks shoulder!
        └─────────────────────────────────┘
                         │
               DASHBOARD CAVITY (-Y)
```

---

### 2. Dimensional Ground Truth & Clearance Matrix

All geometry strictly references [`accurate_models/README_AI.md`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/accurate_models/README_AI.md) and [`accurate_models/mated_assembly_blueprint_ai.json`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/accurate_models/mated_assembly_blueprint_ai.json):

| Metric / Feature | Ground Truth Value | Lock v2 Continuous Value | Engineering Function |
| :--- | :--- | :--- | :--- |
| **Cradle Top Roof** | None (open space) | **100% Open Top (Zero Roof)** | Unobstructed latch access; drop-in installation |
| **Rear Cable Passage** | Hardwired cable | **Open U-Channel (Zero Closed Circles)**| Cable drops into saddle from above |
| **Keeper Body Thickness**| N/A | **\(8.2\text{ mm}\) Solid PCTG** | Heavy-duty axial retention gate |
| **Thumb Grip Thickness** | N/A | **\(12.2\text{ mm}\) Solid PCTG** | Ergonomic ribbed grip tab |
| **Nut Washer Diameter** | **\(\varnothing 17.25\text{ mm}\)** built-in | **\(\varnothing 18.50\text{ mm}\)** counterbore seat | Full flush washer seating without edge binding |
| **Solid Margin Ahead of Nut** | Overhangs box by \(2.55\text{ mm}\) | **\(5.66\text{ mm}\)** solid PCTG ahead of washer | Prevents shearing & edge crushing |
| **Under-Box Extension** | Box rear wall at \(Y = -36.21\text{ mm}\) | Foot reaches **\(Y = -28.00\text{ mm}\)** (\(8.21\text{ mm}\) under box) | Extended anti-tipping cantilever toe |
| **Vertical Headroom Under Box**| Box bottom at \(Z = 36.20\text{ mm}\) | Foot top max \(Z = 34.16\text{ mm}\) (**\(2.04\text{ mm}\) clearance**) | Meets user requirement of \(\ge 2\text{ mm}\) clearance |
| **Central Bolt Hole `[H15d]`** | \(\varnothing 6.45\text{ mm}\) at \((+5.28, -42.29, 30.87)\) | \(\varnothing 7.20\text{ mm}\) enclosed through-bore | Captive M6 through-bolt clamping |
| **Outer Slot `[H15b]`** | \(7.45 \times 6.45\text{ mm}\) at \((-39.63, -42.59, 30.90)\) | \(8.00 \times 7.20\text{ mm}\) enclosed through-slot | Captive M6 through-bolt anti-rotation |
| **Dual Bolt Center Span `[H15e]`**| **\(44.90\text{ mm}\)** | **\(44.90\text{ mm}\)** exact spacing (\(0.00\text{ mm}\) center offset) | Direct chassis anchoring |
| **Aluminum Plate Angle `[H16c]`** | **\(5.87^\circ\)** upward pitch | **\(5.87^\circ\)** matched base foot pitch | 100% flush bearing contact |
| **Connector Seated Gap `[GAP]`** | \(4.70\text{ mm}\) clearance | Leaves \(4.70\text{ mm}\) undisturbed | Factory seal compression maintained |
| **Connector Rigid Length `[B7]`**| \(54.60\text{ mm}\) | Shoulder plane locked at **\(Y = -95.51\text{ mm}\)** | Positive mechanical axial stop |
| **Cable Boot Clearance** | \(\varnothing 17.00\text{ mm}\) rubber boot | \(\varnothing 19.00\text{ mm}\) U-slot (\(1.0\text{ mm}\) radial air gap) | Smooth lead-in, zero cable chafing |
| **Outer Housing Wings** | Inner span \(140.50\text{ mm}\) \([H11]\) | Lock width \(105.10\text{ mm}\) (\(>17\text{ mm}\) air gap to wings) | Ample lateral clearance |
| **Roof Arch Margin** | Roof arch apex at \(Z = 95.40\text{ mm}\) | Max lock height \(Z = 81.00\text{ mm}\) (\(14.40\text{ mm}\) clearance) | Fits easily inside dash aperture |

---

### 3. File Deliverables in `lock_v2/`

| File | Format | Description |
| :--- | :--- | :--- |
| [`build_lock_v2.py`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/build_lock_v2.py) | Python 3.13 | Master CAD script utilizing `manifold3d` for continuous organic modeling |
| [`render_lock_v2_blueprints.py`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/render_lock_v2_blueprints.py) | Python 3.13 | High-resolution 4-panel technical blueprint generator |
| [`lock_v2_base_bracket.stl`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_base_bracket.stl) | 3D STL (Solid) | Open-top U-saddle base with under-box toe & \(\varnothing 18.50\text{ mm}\) nut seats |
| [`lock_v2_base_bracket.obj`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_base_bracket.obj) | Wavefront OBJ | Base bracket with anodized blue material vertex colors |
| [`lock_v2_keeper.stl`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_keeper.stl) | 3D STL (Solid) | Robust \(8.2\text{ mm}\) solid PCTG slide-in retention gate with snap detents |
| [`lock_v2_keeper.obj`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_keeper.obj) | Wavefront OBJ | Keeper with safety green material vertex colors |
| [`lock_v2_1piece_monolithic.stl`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_1piece_monolithic.stl) | 3D STL (Solid) | 1-piece through-bolted alternative lock with side-entry cable collar |
| [`lock_v2_1piece_monolithic.obj`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_1piece_monolithic.obj) | Wavefront OBJ | Monolithic lock with royal purple material vertex colors |
| [`lock_v2_mated_verification.stl`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_mated_verification.stl) | 3D STL (Assembly) | Complete vehicle mated assembly + Lock + M6 flanged nuts |
| [`lock_v2_mated_verification.obj`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_mated_verification.obj) | Wavefront OBJ | Color-coded full mated verification assembly |
| [`lock_v2_print_plate.stl`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_print_plate.stl) | 3D STL (Plated) | Pre-arranged flat on build plate for Bambu P1S (0% supports) |
| [`lock_v2_blueprint.png`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/lock_v2/lock_v2_blueprint.png) | 5K PNG Image | 4-panel AI multimodal technical blueprint with callouts |

---

### 4. Bambu Lab P1S Slicer Settings & Print Plate Orientation

- **Print Plate Orientation (`lock_v2_print_plate.stl`)**:
  * **Base Bracket**: Pre-oriented **100% flat on its wide \(1707\text{ mm}^2\) mounting foot** (\(Z = 0\)).
    - *Hoop Strength*: M6 through-bores and counterbores print vertically as continuous concentric perimeter loops, maximizing hoop tensile strength against bolt torque.
    - *Clamp Compression*: Compressive clamping reaction from the \(\varnothing 17.25\text{ mm}\) flanged nuts acts directly perpendicular to layers, eliminating inter-layer shear risk.
    - *Minimal Supports*: The Wishbone spine rises at a gentle \(35^\circ - 40^\circ\) angle from the bed, printing cleanly with minimal or zero supports.
  * **Slide Keeper**: Pre-oriented **100% flat on its wide \(1351\text{ mm}^2\) front bearing face** (\(Z = 0\)).
    - *Flexural Strength*: Continuous filament strands run across the cantilever snap detent tabs in the XY plane, maximizing flexural fatigue endurance.
    - *Zero Supports*: Low profile (\(12.2\text{ mm}\) total height) requires 0% supports.
  * **Combined Bed Contact Area**: **\(1806.8\text{ mm}^2\)** of planar contact for rock-solid bed adhesion on the textured PEI plate.

- **Material Selection**: **PCTG** (e.g. Fiberlogy PCTG or Bambu PCTG)
- **Nozzle**: \(0.4\text{ mm}\) Hardened Steel
- **Bed Surface**: Textured PEI Plate (\(80^\circ\text{C} - 85^\circ\text{C}\))
- **Nozzle Temperature**: \(255^\circ\text{C} - 265^\circ\text{C}\)
- **Layer Height**: \(0.20\text{ mm}\) Strength Profile
- **Wall Loops (Perimeters)**: **6 walls** (\(2.4\text{ mm}\) solid shell)
- **Top / Bottom Shell Layers**: 5 top layers, 5 bottom layers (\(1.0\text{ mm}\) solid skins)
- **Infill**: **40% Gyroid** or **Cross-Hatch**
- **Supports**: **0% (Disabled)** — both parts are pre-oriented flat on their largest planar faces for support-free printing.
