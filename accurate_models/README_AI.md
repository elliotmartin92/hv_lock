# AI AGENT & MULTIMODAL SYSTEM DIRECTIVE: SYSTEM TOPOLOGY & CAD ASSET ATLAS
## Kia EV6 / Hyundai E-GMP 95190-CV780 V2L Vehicle Outlet & Mated Assembly

This document is the authoritative machine-readable and cognitive guide for AI agents, vision-language models, and automated engineering pipelines interacting with this repository.

---

### 1. DATUM REFERENCE FRAME & COORDINATE SYSTEM

All CAD models (`.stl`, `.obj`), blueprint projections, and mathematical constraints adhere strictly to this right-handed Cartesian coordinate system:

| Axis | Orientation & Sign | Origin ($0.0, 0.0, 0.0$) | Engineering Interpretation |
| :--- | :--- | :--- | :--- |
| **X** | **+X**: Vehicle Right (Passenger)<br>**-X**: Vehicle Left (Driver) | Centerline of lateral symmetry | **Perspective Note**: A person standing in the passenger cabin looking directly into the outlet module sees **Vehicle Left (+X world)** on their **left**, and **Vehicle Right (-X world)** on their **right**. |
| **Y** | **+Y**: Forward (into Cabin)<br>**-Y**: Rearward (into Dash Interior) | Front-most finished face of outer cowl bezel | $Y = 0.0$ is the cabin boundary plane. All structural cavity components, brackets, and wiring extend along $-Y$. |
| **Z** | **+Z**: Upward (towards Vehicle Roof)<br>**-Z**: Downward (towards Floorpan) | Bottom edge of lower bezel chin | $Z = 0.0$ is the lowest point of the plastic trim. The smooth curved roof arch peaks at $Z = +95.40\text{ mm}$. |

---

### 2. SYSTEM ARCHITECTURE & 3-PART MATED TOPOLOGY

The system consists of three precisely mated physical subsystems located at:
`c:\Users\Elliot\Documents\antigravity\hv_lock\accurate_models\`

```text
       CABIN INTERIOR (+Y)
               │
   ┌───────────▼───────────┐
   │  Outer Housing Bezel  │  X in [-71.15, +71.15], Z in [0, 95.40], Y in [-58.80, 0.0]
   │  & Stamped Aluminum   │  Window: X in [-57.30, +57.30], Z in [34.00, 84.20]
   └───────────┬───────────┘
               │ Seated in window recess at Y = -3.00 mm
   ┌───────────▼───────────┐
   │   AC Outlet Box Body  │  X in [-55.88, +55.88], Z in [36.20, 82.20], Y in [-36.21, -3.00]
   │   [H17a]: 16.79 mm Gap│  Holes on plate completely exposed ahead of Y = -36.21 mm!
   │   [H17b]:  9.10 mm Gap│  Bottom of box sits 9.10 mm vertically off aluminum plate.
   └───────────┬───────────┘
               │ Collar extends along -Y from Y = -36.21 to Y = -58.58 mm at X = +27.0 mm
   ┌───────────▼───────────┐
   │  Orange HV Connector  │  Plug body: X in [+6.55, +47.45], Y in [-95.51, -40.91]
   │  [GAP]: 4.70 mm Seated│  Plugs into collar; 17.67 mm penetration inside connector shroud.
   │  Rear Flexible Cable  │  Corrugated conduit & cable extends rearward to Y = -165.91 mm.
   └───────────────────────┘
               │
      DASHBOARD INTERIOR (-Y)
```

#### A. Subsystem 1: Outer Housing Bezel & Stamped Aluminum Frame
- **File**: `mated_outer_housing.stl` / `outer_housing_model.stl`
- **Bounding Box**: $X \in [-71.15, +71.15]\text{ mm}$ ($142.30\text{ mm}$ `[H1]`), $Y \in [-58.80, 0.0]\text{ mm}$ ($58.80\text{ mm}$ `[H7a]`), $Z \in [0.0, 95.40]\text{ mm}$ ($95.40\text{ mm}$ `[H2]`).
- **Roof Profile**: 100% smooth continuous curved arch. Wings never extend above the roof arch.
- **Window Aperture**: $114.60\text{ mm}$ wide `[H3]` $\times 50.20\text{ mm}$ high `[H4]`, spanning $Z \in [34.00, 84.20]\text{ mm}$. Recessed internal step at $Y = -3.00\text{ mm}$ `[H14]`.
- **Lower Chin**: Protrudes $30.77\text{ mm}$ high `[H5]` at front, $7.10\text{ mm}$ total depth `[H5b]`. Extends $27.10\text{ mm}$ vertically below the aluminum plate root `[H16f]`.
- **Side Wings**: Inner clear air span $140.50\text{ mm}$ `[H11]`, wall thickness $2.60\text{ mm}$ `[H13]`. Front edge at $Z = 88.50\text{ mm}$, slopes gently by $5.0\text{ mm}$ ($5.6^\circ$) to $Z = 83.50\text{ mm}$ at $Y = -58.80\text{ mm}$. Bottom edge terminates flush with window bottom at $Z = 34.00\text{ mm}$ (never extends below the aluminum plate).
- **Stamped Aluminum Plate**:
  - Width: $120.20\text{ mm}$ `[H12]` ($10.15\text{ mm}$ air gap `[H11b]` to each side wing).
  - Root Bend: Located at $Y = -5.60\text{ mm}, Z = 27.10\text{ mm}$ ($6.90\text{ mm}$ below window sill `[H16g]`).
  - Internal Bend Angle: $84.13^\circ$ `[H16b]` ($5.87^\circ$ upward pitch `[H16c]` towards ceiling).
  - Rear Extension: Extends to $Y = -53.00\text{ mm}$ `[H10]`, rear edge elevated to $Z = 31.97\text{ mm}$.
  - Chassis Bolt Holes:
    - **Central Hole `[H15d]`**: Round circular hole, $\varnothing 6.45\text{ mm}$, centered at $X = +5.28\text{ mm}, Y = -45.40\text{ mm}$ ($7.60\text{ mm}$ from back edge `[H15f]`).
    - **Outer Slot `[H15b]`**: Horizontal oval slot, $7.45\text{ mm}$ wide (X) $\times 6.45\text{ mm}$ high (Y), centered at $X = -39.63\text{ mm}, Y = -45.70\text{ mm}$ ($16.75\text{ mm}$ from side `[H15a]`, $7.30\text{ mm}$ from back edge `[H15g]`).
    - **Center-to-Center Spacing `[H15e]`**: $44.90\text{ mm}$. Edge-to-edge clear spacing `[H15c]`: $37.95\text{ mm}$.

#### B. Subsystem 2: AC Outlet Box Module
- **File**: `mated_outlet_box.stl` / `outlet_box_model.stl`
- **Body Bounding Box**: $X \in [-55.88, +55.88]\text{ mm}$ ($111.75\text{ mm}$ wide), $Y \in [-36.21, -3.00]\text{ mm}$ ($33.21\text{ mm}$ depth), $Z \in [36.20, 82.20]\text{ mm}$ ($46.00\text{ mm}$ height).
- **Cabin Faceplate Layout (Front View looking in -Y direction)**:
  - **LEFT Side (+X world / Screen Left)**: Spring-loaded flap door ("Max AC 120V, 16A") centered at $X = +27.0\text{ mm}$.
  - **RIGHT Side (-X world / Screen Right)**: Circular NEMA 5-15R 120V AC 3-prong outlet socket centered at $X = -27.0\text{ mm}$.
- **Rear Clearance to Aluminum Plate (`[H17a]`)**:
  - The back wall of the box stops at $Y = -36.21\text{ mm}$, exactly **$16.79\text{ mm}$ ahead** of the rear edge of the aluminum plate ($Y = -53.00\text{ mm}$).
  - Because the mounting holes span $Y \in [-45.70, -39.25]\text{ mm}$, having the back wall at $-36.21\text{ mm}$ provides **$3.04\text{ mm}$ of clear space ahead of the holes**. The chassis bolt holes are **100% unobstructed and accessible from above**.
- **Vertical Gap off Aluminum Plate (`[H17b]`)**:
  - The box bottom is elevated to $Z = 36.20\text{ mm}$, providing a **$9.10\text{ mm}$ vertical air gap** above the aluminum plate root ($Z = 27.10\text{ mm}$).
  - Within the $50.20\text{ mm}$ window opening ($Z \in [34.00, 84.20]\text{ mm}$), the box sits with a $2.20\text{ mm}$ bottom margin and a $2.00\text{ mm}$ top margin, vertically centered.
- **Receptacle Collar**:
  - Protrudes from the rear wall at $X = +27.0\text{ mm}$ (on the LEFT flank behind the flap door).
  - Cross-section: Outer width $22.70\text{ mm}$ `[D1]`, outer height $33.05\text{ mm}$ `[D2]`.
  - Protrusion: Extends $22.37\text{ mm}$ along $-Y$ `[C1]` from $Y = -36.21\text{ mm}$ to $Y = -58.58\text{ mm}$.
  - Latch Tooth: Located on top ($+Z$ face) at $Y = -44.94\text{ mm}$ ($8.73\text{ mm}$ from collar rim `[C2]`), width $2.00\text{ mm}$ `[C3]`, height $2.70\text{ mm}$ `[C4]`.

#### C. Subsystem 3: Orange HV Cable Connector Plug
- **File**: `mated_connector.stl` / `connector_model.stl`
- **Plug Bounding Box**: $X \in [+6.55, +47.45]\text{ mm}$ (centered at $X = +27.0\text{ mm}$), $Z \in [40.65, 77.75]\text{ mm}$ ($37.11\text{ mm}$ total height `[A4]`), $Y \in [-165.91, -40.91]\text{ mm}$.
- **Seated Engagement**:
  - Front shroud rim is seated at $Y = -40.91\text{ mm}$.
  - Seated Gap `[GAP]`: $4.70\text{ mm}$ between the connector shroud rim and the back of the outlet box ($Y = -36.21\text{ mm}$).
  - Collar Penetration: The receptacle collar penetrates $17.67\text{ mm}$ inside the female connector shroud cavity.
- **Rigid Body vs Flexible Cable**:
  - Rigid body extends $54.60\text{ mm}$ `[B7]` from $Y = -40.91\text{ mm}$ to $Y = -95.51\text{ mm}$.
  - Yellow spiral wrap and high-voltage cable extend rearward to $Y = -165.91\text{ mm}$.

#### D. Complete Mated Assembly Solid
- **Files**: `mated_assembly.stl` (Binary STL) & `mated_assembly.obj` (Wavefront OBJ with materials/colors)
- **Bounding Box**: $142.30\text{ mm}\text{ (W)} \times 166.71\text{ mm}\text{ (D)} \times 95.40\text{ mm}\text{ (H)}$.
- **Watertight Status**: Solid manifold geometry ($8,708\text{ faces}$).

---

### 3. COMPLETE CALIPER MEASUREMENT GROUND TRUTH DICTIONARY

Every caliper measurement taken during physical teardown is indexed below and tied to its respective geometric entity:

| Label | Physical Dimension Name | Value | Tolerance | Geometric Entity / Assembly Constraint |
| :--- | :--- | :--- | :--- | :--- |
| **`[H1]`** | Total Outer Frame Width | **142.30 mm** | $\pm 0.20$ | Widest lateral span of the outer cowl bezel |
| **`[H2]`** | Total Outer Frame Height | **95.40 mm** | $\pm 0.20$ | $Z = 0$ (chin tip) to $Z = 95.40$ (continuous curved roof arch) |
| **`[H3]`** | Window Aperture Width | **114.60 mm** | $\pm 0.15$ | Internal opening width framing the $111.75\text{ mm}$ box |
| **`[H4]`** | Window Aperture Height | **50.20 mm** | $\pm 0.15$ | Internal opening height framing the $46.00\text{ mm}$ box |
| **`[H5]`** | Lower Chin Front Height | **30.77 mm** | $\pm 0.20$ | Front visible height of bottom trim bar |
| **`[H5b]`**| Chin Total Depth (w/ ribs) | **7.10 mm** | $\pm 0.15$ | Thickness from front bezel face back to aluminum root |
| **`[H6]`** | Top Bezel Thickness | **11.20 mm** | $\pm 0.15$ | Distance from top of window to apex of roof arch |
| **`[H7a]`**| Side Wing Total Depth | **58.80 mm** | $\pm 0.25$ | Maximum depth of side wings along $-Y$ |
| **`[H9]`** | Top Shelf Flat Length | **34.00 mm** | $\pm 0.30$ | Horizontal flat segment of roof before gentle slope |
| **`[H10]`**| Aluminum Rear Extension | **53.00 mm** | $\pm 0.25$ | Rearmost edge of aluminum plate at $Y = -53.00\text{ mm}$ |
| **`[H11]`**| Inner Wing Clear Span | **140.50 mm** | $\pm 0.20$ | Clear lateral span between interior faces of wings |
| **`[H11b]`**| Wing-to-Aluminum Air Gap| **10.15 mm** | $\pm 0.15$ | Horizontal space between plate side edge and wing inner face |
| **`[H12]`**| Aluminum Plate Width | **120.20 mm** | $\pm 0.20$ | $140.50 - 2 \times 10.15 = 120.20\text{ mm}$ |
| **`[H13]`**| Side Wing Wall Thickness | **2.60 mm** | $\pm 0.10$ | Molded ABS wing wall thickness |
| **`[H14]`**| Window Recess Step Depth | **3.00 mm** | $\pm 0.15$ | Depth offset where outlet box seating lip rests |
| **`[H15a]`**| Outer Slot Side Offset | **16.75 mm** | $\pm 0.15$ | From aluminum edge to outer edge of oval slot |
| **`[H15b]`**| Outer Oval Slot | **7.45 x 6.45 mm**| $\pm 0.10$ | Horizontal oval slot ($X = 7.45\text{ mm}$, $Y = 6.45\text{ mm}$) |
| **`[H15c]`**| Holes Edge-to-Edge Spacing| **37.95 mm** | $\pm 0.15$ | Clear metal span between circular hole and oval slot |
| **`[H15d]`**| Central Hole Diameter | **Ø 6.45 mm** | $\pm 0.10$ | Circular chassis bolt hole |
| **`[H15e]`**| Holes Center-to-Center | **44.90 mm** | $\pm 0.15$ | Center-to-center lateral hole spacing |
| **`[H15f]`**| Central Hole Back Distance| **7.60 mm** | $\pm 0.15$ | From rear edge of aluminum plate to circular hole center |
| **`[H15g]`**| Oval Slot Back Distance | **7.30 mm** | $\pm 0.15$ | From rear edge of aluminum plate to oval slot center |
| **`[H16b]`**| Internal Bend Angle | **84.13°** | $\pm 0.25^\circ$| Calibrated from traced $67.0\text{ mm}$ chord ($2\arcsin(67/100)$) |
| **`[H16c]`**| Upward Pitch Angle | **5.87°** | $\pm 0.25^\circ$| $90.00^\circ - 84.13^\circ = 5.87^\circ$ upward inclination |
| **`[H16f]`**| Chin Extension Below Plate| **27.10 mm** | $\pm 0.20$ | Vertical distance from plate root down to chin tip |
| **`[H16g]`**| Plate Below Window Aperture| **6.90 mm** | $\pm 0.15$ | Vertical drop from window sill down to plate root |
| **`[H17a]`**| Box to Plate Back Clearance| **16.79 mm** | $\pm 0.15$ | Box back wall at $Y = -36.21\text{ mm}$; holes 100% uncovered! |
| **`[H17b]`**| Box Vertical Gap off Plate | **9.10 mm** | $\pm 0.20$ | Vertical air gap between plate root and box bottom |
| **`[A1]`** | Connector Shroud Outer Width| **36.10 mm** | $\pm 0.15$ | Shroud oval body width (40.90 mm including key rib) |
| **`[A4]`** | Total Plug Height | **37.11 mm** | $\pm 0.15$ | Overall vertical height including top latch tower |
| **`[B1]`** | Tower Axial Length | **36.75 mm** | $\pm 0.20$ | Length of the latch tower housing |
| **`[B7]`** | Connector Rigid Length | **54.60 mm** | $\pm 0.25$ | Front shroud rim to rear cable entry seal |
| **`[C1]`** | Collar Protrusion Length | **22.37 mm** | $\pm 0.15$ | Receptacle collar extension from back of outlet box |
| **`[C2]`** | Latch Tooth Distance | **8.73 mm** | $\pm 0.15$ | From collar rear rim to latch tooth center |
| **`[C3]`** | Latch Tooth Width | **2.00 mm** | $\pm 0.10$ | Lateral width of retention tooth |
| **`[C4]`** | Latch Tooth Height | **2.70 mm** | $\pm 0.10$ | Vertical protrusion height above collar top wall |
| **`[D1]`** | Collar Outer Width | **22.70 mm** | $\pm 0.15$ | Lateral width of receptacle collar |
| **`[D2]`** | Collar Outer Height | **33.05 mm** | $\pm 0.15$ | Vertical height of receptacle collar |
| **`[GAP]`**| Confirmed Seated Gap | **4.70 mm** | $\pm 0.10$ | Clearance between plug shroud rim and outlet box rear wall |

---

### 4. REPOSITORY FILE INVENTORY

All assets in [`accurate_models/`](file:///c:/Users/Elliot/Documents/antigravity/hv_lock/accurate_models):

| Filename | Type | Description |
| :--- | :--- | :--- |
| `mated_assembly.stl` | 3D CAD | Complete 3-part watertight assembly ($8,708\text{ faces}$) |
| `mated_assembly.obj` | 3D CAD | Pre-aligned 3-part assembly with vertex colors / materials |
| `mated_outer_housing.stl` | 3D CAD | Outer cowl bezel + stamped aluminum bracket |
| `mated_outlet_box.stl` | 3D CAD | Outlet box module seated at exact $Y=-36.21, Z=36.20\text{ mm}$ |
| `mated_connector.stl` | 3D CAD | Orange HV connector seated in collar ($4.70\text{ mm}$ gap) |
| `mated_assembly_blueprint_ai.png` | Image (5K) | High-contrast multimodal AI technical blueprint with all callouts |
| `mated_assembly_blueprint_ai.json`| Data | Structured machine-readable schema of all bounding boxes & labels |
| `generate_ai_blueprint.py` | Script | Python script that regenerates the AI blueprint & JSON |
| `build_accurate_models.py` | Script | Master CAD synthesis script generating all watertight STLs & OBJs |
| `render_accurate_blueprints.py` | Script | Standard 4-panel engineering orthographic rendering script |
| `outer_housing_measurements.json`| Data | JSON store of outer housing dimensions and physical parameters |
| `../caliper_measurements.csv` | Data | Master tabular CSV record of all physical measurements |
| `../caliper_measurements.xlsx`| Data | Master Excel workbook with calculations and formulas |

---

### 5. RULES FOR AI AGENTS DESIGNING RETENTION LOCK MECHANISMS

When creating or modifying physical mechanical lock components (e.g. anti-theft deadbolts, C-brackets, saddle clamps):

1. **Chassis Fastening Anchor**: The two mounting holes in the stamped aluminum plate at $Y \in [-45.70, -39.25]\text{ mm}$ are **100% uncovered** and available for mechanical through-bolts or threaded clamping studs.
2. **Connector Interlock**: A retention jaw can capture the connector rigid shoulder ($Y \in [-95.51, -40.91]\text{ mm}$) and lock against the back of the outlet box ($Y = -36.21\text{ mm}$) across the $4.70\text{ mm}$ seated gap.
3. **Lateral Clearance**: Maintain $\ge 1.0\text{ mm}$ clearance from the inner faces of the outer housing wings ($X = \pm 70.25\text{ mm}$) and $\ge 2.0\text{ mm}$ clearance above the sloping wing bottom edge ($Z = 34.00\text{ mm}$).
4. **Tool Access**: Any bolt securing the lock from the top must have clear vertical tool access within the window aperture ($X \in [-57.30, +57.30], Z > 34.00\text{ mm}$) or through the open rear chassis frame.
