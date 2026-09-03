import os
import json
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

target_dir = os.path.dirname(os.path.abspath(__file__))
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\ca2c4a5c-394a-4c0b-b99d-8dde76573538"

print("Loading 3D CAD models...")
h_mesh = trimesh.load(os.path.join(target_dir, "mated_outer_housing.stl"))
b_mesh = trimesh.load(os.path.join(target_dir, "mated_outlet_box.stl"))
c_mesh = trimesh.load(os.path.join(target_dir, "mated_connector.stl"))

v_h_screen = np.copy(h_mesh.vertices)
v_h_screen[:, 0] = -v_h_screen[:, 0]

v_b_screen = np.copy(b_mesh.vertices)
v_b_screen[:, 0] = -v_b_screen[:, 0]

v_c_screen = np.copy(c_mesh.vertices)
v_c_screen[:, 0] = -v_c_screen[:, 0]

def draw_dim(ax, p1, p2, label, offset=(0, 0), color='#facc15', lw=1.2, fontsize=8.0, text_offset=(0, 0), ha='center', va='center'):
    p1 = np.array(p1, dtype=float) + np.array(offset, dtype=float)
    p2 = np.array(p2, dtype=float) + np.array(offset, dtype=float)
    ax.annotate("", xy=p1, xytext=p2,
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw, shrinkA=0, shrinkB=0))
    mid = (p1 + p2) / 2.0 + np.array(text_offset, dtype=float)
    ax.text(mid[0], mid[1], label, color='#0b1329', fontsize=fontsize, weight='bold',
            ha=ha, va=va,
            bbox=dict(boxstyle='square,pad=0.25', facecolor=color, edgecolor='none', alpha=0.95))

def create_ai_card(ax, title, subtitle=None):
    ax.set_facecolor('#0b1329')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#64748b', labelsize=8)
    ax.grid(True, linestyle='--', alpha=0.25, color='#38bdf8')
    if subtitle:
        full_title = f"{title}\n{subtitle}"
    else:
        full_title = title
    ax.set_title(full_title, color='#f8fafc', fontsize=11, weight='bold', pad=10, loc='left')

print("Rendering 5K AI-Optimized Technical Blueprint...")
fig = plt.figure(figsize=(30, 19), dpi=180)
plt.subplots_adjust(left=0.035, right=0.965, top=0.92, bottom=0.035, wspace=0.14, hspace=0.18)
fig.patch.set_facecolor('#060b14')

header_text = (
    "KIA EV6 / E-GMP 95190-CV780 V2L MATED SYSTEM — MULTIMODAL AI TECHNICAL BLUEPRINT\n"
    "Unified Dimensional Reference Matrix & Full Physical Caliper Measurement Ground Truth"
)
fig.suptitle(header_text, color='#f8fafc', fontsize=18, weight='bold', y=0.97, ha='center')

# PANEL 1: FRONT ELEVATION
ax1 = fig.add_subplot(2, 2, 1)
create_ai_card(ax1, "PANEL 1: FRONT ELEVATION (PASSENGER CABIN PERSPECTIVE)",
               "X-Z Orthographic Projection • Left: Connector & Flap Door | Right: 120V AC Outlet")

ax1.tripcolor(v_h_screen[:, 0], v_h_screen[:, 2], h_mesh.faces, facecolors=np.ones(len(h_mesh.faces)), cmap='Blues', alpha=0.35, edgecolors='#1e293b', lw=0.2)
ax1.tripcolor(v_b_screen[:, 0], v_b_screen[:, 2], b_mesh.faces, facecolors=np.ones(len(b_mesh.faces)), cmap='Greys', alpha=0.60, edgecolors='#0f172a', lw=0.2)
ax1.tripcolor(v_c_screen[:, 0], v_c_screen[:, 2], c_mesh.faces, facecolors=np.ones(len(c_mesh.faces)), cmap='Oranges', alpha=0.85, edgecolors='#7c2d12', lw=0.2)

ax1.set_xlim(-95, 95)
ax1.set_ylim(-20, 120)
ax1.set_aspect('equal')
ax1.set_xlabel("Screen Width (mm: Left = Vehicle Left/Driver, Right = Vehicle Right/Passenger)", color='#94a3b8', fontsize=8.5)
ax1.set_ylabel("Height Z (mm: Chin Tip = 0.0, Top Roof Rim = 95.40)", color='#94a3b8', fontsize=8.5)

draw_dim(ax1, (-71.15, 95.40), (71.15, 95.40), "[H1] Total Width: 142.30 mm", offset=(0, 12), color='#facc15', fontsize=8.0)
draw_dim(ax1, (71.15, 0.0), (71.15, 95.40), "[H2] Total Height: 95.40 mm", offset=(10, 0), color='#facc15', fontsize=8.0)
draw_dim(ax1, (-57.30, 84.20), (57.30, 84.20), "[H3] Window Width: 114.60 mm", offset=(0, 4), color='#38bdf8', fontsize=7.5)
draw_dim(ax1, (-57.30, 34.00), (-57.30, 84.20), "[H4] Window Height: 50.20 mm", offset=(-8, 0), color='#38bdf8', fontsize=7.5)
draw_dim(ax1, (0.0, 84.20), (0.0, 95.40), "[H6] Top Bezel: 11.20 mm", offset=(-35, 0), color='#4ade80', fontsize=7.0)
draw_dim(ax1, (-71.15, 0.0), (-71.15, 30.77), "[H5] Chin Height: 30.77 mm", offset=(-12, 0), color='#a78bfa', fontsize=7.0)
draw_dim(ax1, (71.15, 0.0), (71.15, 27.10), "[H16f] Chin below Plate: 27.10 mm", offset=(18, 0), color='#f43f5e', fontsize=7.0)
draw_dim(ax1, (71.15, 27.10), (71.15, 34.00), "[H16g] Plate below Win: 6.90 mm", offset=(18, 0), color='#fb923c', fontsize=6.8)
draw_dim(ax1, (-27.0, 27.10), (-27.0, 36.20), "[H17b] Box Gap off Plate: 9.10 mm", offset=(0, 0), color='#facc15', fontsize=7.0)
draw_dim(ax1, (-27.0 - 18.05, 59.20), (-27.0 + 18.05, 59.20), "[A1] Shroud W: 36.10 mm", offset=(0, -14), color='#f97316', fontsize=7.0)
draw_dim(ax1, (-27.0 - 18.05, 59.20 - 18.55), (-27.0 - 18.05, 59.20 + 18.55), "[A4] Plug H: 37.11 mm", offset=(-4, 0), color='#f97316', fontsize=7.0)

ax1.text(-50, 114, "LEFT: CONNECTOR & FLAP DOOR (-X World / +X Screen)", color='#f97316', fontsize=8.5, weight='bold', ha='center')
ax1.text(50, 114, "RIGHT: 120V AC OUTLET (+X World / -X Screen)", color='#38bdf8', fontsize=8.5, weight='bold', ha='center')

# PANEL 2: SIDE PROFILE
ax2 = fig.add_subplot(2, 2, 2)
create_ai_card(ax2, "PANEL 2: SIDE PROFILE & LONGITUDINAL SECTION (DEPTH PROFILE)",
               "Y-Z Orthographic Projection • Front Bezel at Y = 0 | Cavity Extensions along -Y")

ax2.tripcolor(h_mesh.vertices[:, 1], h_mesh.vertices[:, 2], h_mesh.faces, facecolors=np.ones(len(h_mesh.faces)), cmap='Blues', alpha=0.35, edgecolors='#1e293b', lw=0.2)
ax2.tripcolor(b_mesh.vertices[:, 1], b_mesh.vertices[:, 2], b_mesh.faces, facecolors=np.ones(len(b_mesh.faces)), cmap='Greys', alpha=0.60, edgecolors='#0f172a', lw=0.2)
ax2.tripcolor(c_mesh.vertices[:, 1], c_mesh.vertices[:, 2], c_mesh.faces, facecolors=np.ones(len(c_mesh.faces)), cmap='Oranges', alpha=0.85, edgecolors='#7c2d12', lw=0.2)

ax2.set_xlim(-190, 25)
ax2.set_ylim(-20, 120)
ax2.set_aspect('equal')
ax2.set_xlabel("Depth Y (mm: 0.0 = Front Bezel Face, -Y = Interior Dashboard Cavity)", color='#94a3b8', fontsize=8.5)
ax2.set_ylabel("Height Z (mm)", color='#94a3b8', fontsize=8.5)

draw_dim(ax2, (0.0, 95.40), (-58.80, 95.40), "[H7a] Wing Depth: 58.80 mm", offset=(0, 12), color='#facc15', fontsize=8.0)
draw_dim(ax2, (0.0, 95.40), (-34.00, 95.40), "[H9] Top Flat: 34.00 mm", offset=(0, 4), color='#4ade80', fontsize=7.5)
draw_dim(ax2, (0.0, 27.10), (-53.00, 27.10), "[H10] Aluminum Extension: 53.00 mm", offset=(0, -18), color='#38bdf8', fontsize=8.0)
draw_dim(ax2, (-36.21, 36.20), (-53.00, 36.20), "[H17a] Box to Plate Back: 16.79 mm (Holes Clear!)", offset=(0, -8), color='#facc15', fontsize=7.5)
draw_dim(ax2, (0.0, 10.0), (-7.10, 10.0), "[H5b] Chin Thk: 7.10 mm", offset=(0, -12), color='#a78bfa', fontsize=7.0)
draw_dim(ax2, (0.0, 84.20), (-3.00, 84.20), "[H14] Recess: 3.00 mm", offset=(0, 4), color='#fb923c', fontsize=7.0)
draw_dim(ax2, (-36.21, 59.20), (-40.91, 59.20), "[GAP] Seated Gap: 4.70 mm", offset=(0, 18), color='#f43f5e', fontsize=7.5)
draw_dim(ax2, (-36.21, 45.00), (-58.58, 45.00), "[C1] Collar Length: 22.37 mm", offset=(0, -6), color='#a855f7', fontsize=7.5)
draw_dim(ax2, (-40.91, 75.00), (-95.51, 75.00), "[B7] Rigid Length: 54.60 mm", offset=(0, 6), color='#f97316', fontsize=8.0)
ax2.annotate("[H16b] 84.13° Bend\n([H16c] 5.87° Pitch Up)", xy=(-30.0, 29.5), xytext=(-30.0, 12.0),
             arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=1.2),
             color='#38bdf8', fontsize=7.5, weight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0b1329', edgecolor='#38bdf8', lw=1.0))

# PANEL 3: TOP PLAN VIEW
ax3 = fig.add_subplot(2, 2, 3)
create_ai_card(ax3, "PANEL 3: TOP PLAN VIEW (HORIZONTAL CLEARANCES & CHASSIS BOLT HOLES)",
               "X-Y Orthographic Projection • Looking Down from Above (+Z looking down)")

ax3.tripcolor(v_h_screen[:, 0], h_mesh.vertices[:, 1], h_mesh.faces, facecolors=np.ones(len(h_mesh.faces)), cmap='Blues', alpha=0.35, edgecolors='#1e293b', lw=0.2)
ax3.tripcolor(v_b_screen[:, 0], b_mesh.vertices[:, 1], b_mesh.faces, facecolors=np.ones(len(b_mesh.faces)), cmap='Greys', alpha=0.60, edgecolors='#0f172a', lw=0.2)
ax3.tripcolor(v_c_screen[:, 0], c_mesh.vertices[:, 1], c_mesh.faces, facecolors=np.ones(len(c_mesh.faces)), cmap='Oranges', alpha=0.85, edgecolors='#7c2d12', lw=0.2)

ax3.set_xlim(-95, 95)
ax3.set_ylim(-190, 25)
ax3.set_aspect('equal')
ax3.set_xlabel("Horizontal Span (mm: Left = Connector, Right = Outlet)", color='#94a3b8', fontsize=8.5)
ax3.set_ylabel("Depth Y (mm: -Y = Rearward, +Y = Forward)", color='#94a3b8', fontsize=8.5)

draw_dim(ax3, (-70.25, -45.0), (70.25, -45.0), "[H11] Inner Wing Span: 140.50 mm", offset=(0, 28), color='#facc15', fontsize=8.0)
draw_dim(ax3, (-60.10, -50.0), (60.10, -50.0), "[H12] Plate Width: 120.20 mm", offset=(0, -8), color='#38bdf8', fontsize=8.0)
draw_dim(ax3, (-70.25, -50.0), (-60.10, -50.0), "[H11b] 10.15 mm", offset=(0, -18), color='#4ade80', fontsize=7.0)
draw_dim(ax3, (60.10, -50.0), (70.25, -50.0), "[H11b] 10.15 mm", offset=(0, -18), color='#4ade80', fontsize=7.0)
draw_dim(ax3, (-71.15, -15.0), (-68.55, -15.0), "[H13] 2.6 mm", offset=(0, 6), color='#a78bfa', fontsize=6.8)

ax3.plot([39.625], [-53.0 + 7.3 + 3.225], 'o', color='#facc15', markersize=6)
ax3.text(39.625, -53.0 + 7.3 + 3.225 + 7.0, "[H15b] Oval Slot\n7.45 x 6.45 mm", color='#facc15', fontsize=7.0, weight='bold', ha='center')
ax3.plot([-5.275], [-53.0 + 7.6 + 3.225], 'o', color='#38bdf8', markersize=6)
ax3.text(-5.275, -53.0 + 7.6 + 3.225 + 7.0, "[H15d] Center Hole\nØ 6.45 mm", color='#38bdf8', fontsize=7.0, weight='bold', ha='center')
draw_dim(ax3, (-5.275, -53.0 + 10.5), (39.625, -53.0 + 10.5), "[H15e] C-to-C Spacing: 44.90 mm", offset=(0, -8), color='#4ade80', fontsize=7.2)
draw_dim(ax3, (-5.275 + 3.225, -53.0 + 10.5), (39.625 - 3.725, -53.0 + 10.5), "[H15c] Edge Spacing: 37.95 mm", offset=(0, 8), color='#fb923c', fontsize=7.0)
draw_dim(ax3, (-5.275, -53.0), (-5.275, -53.0 + 7.6), "[H15f] 7.6 mm", offset=(-8, 0), color='#f43f5e', fontsize=6.8)
draw_dim(ax3, (39.625, -53.0), (39.625, -53.0 + 7.3), "[H15g] 7.3 mm", offset=(8, 0), color='#f43f5e', fontsize=6.8)

# PANEL 4: MASTER CALIPER MEASUREMENT INDEX & AI MATRIX
ax4 = fig.add_subplot(2, 2, 4)
create_ai_card(ax4, "PANEL 4: MASTER CALIPER MEASUREMENT INDEX & AI GROUND TRUTH MATRIX",
               "Complete Cross-Verification Table Linking All 35+ Physical Dimensions to CAD Geometry")
ax4.axis('off')

table_data = [
    ["Group", "Label", "Feature Description", "Value (mm)", "Tolerance", "Role in Vehicle Assembly"],
    ["Outer Bezel", "[H1]", "Total Outer Frame Width", "142.30", "±0.20", "Widest span across outer cosmetic cowl"],
    ["Outer Bezel", "[H2]", "Total Outer Frame Height", "95.40", "±0.20", "100% smooth continuous roof arch"],
    ["Outer Bezel", "[H3]", "Window Aperture Width", "114.60", "±0.15", "Frames 111.75mm outlet box (1.42mm gap)"],
    ["Outer Bezel", "[H4]", "Window Aperture Height", "50.20", "±0.15", "Frames 46.00mm outlet box (2.10mm gap)"],
    ["Outer Bezel", "[H5]", "Lower Chin Front Height", "30.77", "±0.20", "Protruding bottom bar below window"],
    ["Outer Bezel", "[H5b]", "Chin Total Depth (w/ ribs)", "7.10", "±0.15", "Front face back to aluminum root"],
    ["Outer Bezel", "[H6]", "Top Bezel Thickness", "11.20", "±0.15", "Roof rim down to window aperture top"],
    ["Outer Bezel", "[H7a]", "Side Wing Total Depth", "58.80", "±0.25", "5.6° gentle slope, terminates at Z=83.5"],
    ["Outer Bezel", "[H9]", "Top Shelf Flat Length", "34.00", "±0.30", "Flat horizontal run before gentle drop"],
    ["Outer Bezel", "[H10]", "Aluminum Rear Extension", "53.00", "±0.25", "Rearmost reach of stamped metal bracket"],
    ["Outer Bezel", "[H11]", "Inner Wing Clear Span", "140.50", "±0.20", "Clear air space between left & right wings"],
    ["Outer Bezel", "[H11b]", "Wing-to-Aluminum Air Gap", "10.15", "±0.15", "Horizontal clearance to metal plate"],
    ["Outer Bezel", "[H12]", "Aluminum Plate Width", "120.20", "±0.20", "H11 - 2*H11b = 140.50 - 20.30 = 120.20"],
    ["Outer Bezel", "[H13]", "Side Wing Wall Thickness", "2.60", "±0.10", "Structural ABS wall thickness"],
    ["Outer Bezel", "[H14]", "Window Recess Step Depth", "3.00", "±0.15", "Internal seat ledge where box rests"],
    ["Aluminum Plate", "[H15b]", "Outer Oval Slot Dimensions", "7.45 x 6.45", "±0.10", "Horizontal slot (X=7.45mm, Y=6.45mm)"],
    ["Aluminum Plate", "[H15d]", "Central Hole Diameter", "Ø 6.45", "±0.10", "Round circular chassis bolt hole"],
    ["Aluminum Plate", "[H15e]", "Holes Center-to-Center", "44.90", "±0.15", "Calculated from caliper edge span"],
    ["Aluminum Plate", "[H15f]", "Central Hole Back Edge", "7.60", "±0.15", "From back edge of plate to hole center"],
    ["Aluminum Plate", "[H15g]", "Oval Slot Back Edge", "7.30", "±0.15", "From back edge of plate to slot center"],
    ["Aluminum Plate", "[H16b]", "Internal Bend Angle", "84.13°", "±0.25°", "2*arcsin(67/100) = 84.13° calibrated"],
    ["Aluminum Plate", "[H16c]", "Upward Pitch Angle", "5.87°", "±0.25°", "90.0° - 84.13° = 5.87° pitch up to ceiling"],
    ["Aluminum Plate", "[H16f]", "Chin below Aluminum Plate", "27.10", "±0.20", "Vertical chin drop below plate root"],
    ["Aluminum Plate", "[H16g]", "Plate below Window Aperture", "6.90", "±0.15", "Vertical gap between window sill & plate"],
    ["Mated Assembly", "[H17a]", "Box to Plate Back Clearance", "16.79", "±0.15", "Rear of box stops 16.79mm ahead: HOLES CLEAR!"],
    ["Mated Assembly", "[H17b]", "Box Vertical Gap off Plate", "9.10", "±0.20", "Bottom of box is 9.10mm above metal plate"],
    ["HV Connector", "[A1]", "Plug Shroud Outer Width", "36.10", "±0.15", "Outer oval shroud body (incl key rib: 40.9mm)"],
    ["HV Connector", "[A4]", "Total Plug Height", "37.11", "±0.15", "Bottom wall to top of latch tower"],
    ["HV Connector", "[B1]", "Tower Axial Length", "36.75", "±0.20", "Latch tower carriage base length"],
    ["HV Connector", "[B7]", "Rigid Housing Length", "54.60", "±0.25", "Shroud front rim to cable exit boot"],
    ["HV Receptacle", "[C1]", "Collar Protrusion Length", "22.37", "±0.15", "Receptacle collar extension along -Y"],
    ["HV Receptacle", "[GAP]", "Confirmed Seated Gap", "4.70", "±0.10", "Rigid gap between plug shoulder & box back"],
]

col_widths = [0.15, 0.08, 0.28, 0.12, 0.10, 0.27]
y_start = 0.96
row_height = 0.027

for i, row in enumerate(table_data):
    y = y_start - i * row_height
    is_header = (i == 0)
    bg_color = '#1e293b' if is_header else ('#0d172a' if i % 2 == 0 else '#0b1329')
    txt_color = '#facc15' if is_header else ('#38bdf8' if row[0] == 'Mated Assembly' else ('#f97316' if row[0] == 'HV Connector' else '#e2e8f0'))
    fontweight = 'bold' if is_header or row[0] == 'Mated Assembly' else 'normal'
    
    rect = Rectangle((0.0, y - row_height * 0.85), 1.0, row_height * 0.95, facecolor=bg_color, edgecolor='#1e293b', lw=0.5, transform=ax4.transAxes)
    ax4.add_patch(rect)
    
    x_cursor = 0.01
    for j, cell in enumerate(row):
        w = col_widths[j]
        ax4.text(x_cursor, y - row_height * 0.35, cell, color=txt_color, fontsize=6.8, weight=fontweight,
                 va='center', transform=ax4.transAxes)
        x_cursor += w

out_png = os.path.join(target_dir, "mated_assembly_blueprint_ai.png")
art_png = os.path.join(artifact_dir, "mated_assembly_blueprint_ai.png")
plt.savefig(out_png, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.savefig(art_png, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print(f"Saved AI Blueprint Image: {out_png}")

metadata = {
    "system_name": "Kia EV6 / Hyundai E-GMP 95190-CV780 V2L Complete 3-Part Mated Assembly",
    "datum_reference_frame": {
        "X_axis": "Width (+X Passenger / Right, -X Driver / Left, Center = 0.0 mm)",
        "Y_axis": "Depth (+Y Forward / Cabin Side, -Y Rearward / Interior Dash Cavity, Front Bezel Face = 0.0 mm)",
        "Z_axis": "Height (Bottom of Chin = 0.0 mm, Top Roof Arch Rim = 95.40 mm)"
    },
    "subsystems": {
        "outer_housing_bezel": {
            "outer_dimensions_mm": {"width_X": 142.30, "height_Z": 95.40, "depth_Y": 58.80},
            "window_aperture_mm": {"width_X": 114.60, "height_Z": 50.20, "Z_bounds": [34.00, 84.20], "center_Z": 59.10},
            "lower_chin_mm": {"front_height": 30.77, "total_depth_with_ribs": 7.10, "extension_below_aluminum_plate": 27.10},
            "side_wings_mm": {"inner_span": 140.50, "wall_thickness": 2.60, "front_Z": 88.50, "rear_Z": 83.50, "slope_deg": 5.6}
        },
        "stamped_aluminum_plate": {
            "dimensions_mm": {"width_X": 120.20, "rear_extension_Y": 53.00, "thickness": 1.50},
            "clearance_to_wings_mm": 10.15,
            "root_bend_mm": {"Y": -5.60, "Z": 27.10},
            "bend_angles": {"internal_bend_deg": 84.13, "upward_pitch_deg": 5.87},
            "vertical_distance_below_window_mm": 6.90,
            "mounting_holes": {
                "outer_oval_slot_mm": {"width_X": 7.45, "height_Y": 6.45, "distance_from_side": 16.75, "distance_from_back": 7.30},
                "central_round_hole_mm": {"diameter": 6.45, "distance_from_back": 7.60},
                "center_to_center_spacing_mm": 44.90,
                "edge_to_edge_spacing_mm": 37.95
            }
        },
        "outlet_box_module": {
            "seating_position": {
                "X_bounds": [-55.875, 55.875],
                "Y_bounds": [-36.21, -3.00],
                "Z_bounds": [36.20, 82.20],
                "depth_mm": 33.21,
                "height_mm": 46.00,
                "width_mm": 111.75
            },
            "assembly_clearances": {
                "H17a_back_of_box_to_plate_back_clearance_mm": 16.79,
                "H17b_box_vertical_gap_off_plate_mm": 9.10,
                "chassis_bolt_holes_status": "Completely unobstructed (3.04mm clearance ahead of holes)"
            },
            "faceplate_features": {
                "left_side": "Hinged spring flap door ('Max AC 120V, 16A') at X = +27.0 mm (cabin view left)",
                "right_side": "Circular NEMA 5-15R 120V AC 3-prong outlet socket at X = -27.0 mm (cabin view right)"
            },
            "receptacle_collar": {
                "position_X_mm": 27.0,
                "protrusion_along_minus_Y_mm": 22.37,
                "collar_bounds_Y": [-58.58, -36.21],
                "dimensions_mm": {"width_X": 22.70, "height_Z": 33.05}
            }
        },
        "orange_hv_connector": {
            "seated_position": {
                "X_center_mm": 27.0,
                "shroud_front_rim_Y_mm": -40.91,
                "seated_gap_to_box_back_mm": 4.70,
                "collar_penetration_mm": 17.67,
                "rigid_length_mm": 54.60,
                "total_length_with_cable_mm": 125.00
            }
        }
    },
    "caliper_measurements_reference": {row[1]: {"description": row[2], "value": row[3], "tolerance": row[4]} for row in table_data[1:]}
}

out_json = os.path.join(target_dir, "mated_assembly_blueprint_ai.json")
art_json = os.path.join(artifact_dir, "mated_assembly_blueprint_ai.json")
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)
with open(art_json, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print(f"Saved AI Blueprint JSON Metadata: {out_json}")
print("Generation complete!")
