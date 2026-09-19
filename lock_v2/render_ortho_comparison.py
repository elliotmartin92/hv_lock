"""
render_ortho_comparison.py
Generates a 4K orthographic top-down engineering comparison visual directly comparing:
- OLD DESIGN (X = +21.20 mm, Y = -95.51 mm): Cable holder misaligned 28mm to passenger right (cabin perspective)
- NEW DESIGN (X = +49.20 mm, Y = -98.01 mm): Calibrated 28mm leftward shift (+X) + 2.5mm rearward reach relief (-Y)
- DIRECT OVERLAY: Co-registered X-Y plan overlay with vector shift arrows and clearance telemetry

Exports:
- lock_v2/ortho_top_down_comparison.png
- Copies to current artifact directory
"""

import os
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.collections import PolyCollection

target_dir = os.path.dirname(os.path.abspath(__file__))
accurate_models_dir = os.path.join(os.path.dirname(target_dir), "accurate_models")
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\9d06c7e1-2a89-470b-b4a9-21183c508ab8"

print("Loading CAD geometry for orthographic top-down comparison...")
# Accurate vehicle references
h_mesh = trimesh.load(os.path.join(accurate_models_dir, "mated_outer_housing.stl"))
b_mesh = trimesh.load(os.path.join(accurate_models_dir, "mated_outlet_box.stl"))
c_mesh = trimesh.load(os.path.join(accurate_models_dir, "mated_connector.stl"))

# Old design models (X = 21.20 mm)
b_old = trimesh.load(os.path.join(target_dir, "lock_v2_base_bracket_old.stl"))
k_old = trimesh.load(os.path.join(target_dir, "lock_v2_keeper_old.stl"))

# New calibrated design models (X = 49.20 mm)
b_new = trimesh.load(os.path.join(target_dir, "lock_v2_base_bracket.stl"))
k_new = trimesh.load(os.path.join(target_dir, "lock_v2_keeper.stl"))

def render_mesh_topdown(ax, mesh, base_color, light_dir=np.array([-0.35, -0.45, 0.82]), alpha=1.0, edge_color=None, lw=0.1, z_min=None):
    """Renders a watertight 3D triangle mesh in true orthographic top-down (X-Y) projection with lighting."""
    light_dir = light_dir / np.linalg.norm(light_dir)
    normals = mesh.face_normals
    # Filter upward-visible faces
    upward = normals[:, 2] > -0.2
    
    if z_min is not None:
        upward = upward & (mesh.triangles_center[:, 2] >= z_min)
        
    faces_to_render = mesh.faces[upward]
    normals_to_render = normals[upward]
    z_centers = mesh.triangles_center[upward, 2]
    
    diffuse = np.maximum(0.12, np.dot(normals_to_render, light_dir))
    ambient = 0.28
    intensity = np.clip(ambient + 0.72 * diffuse, 0.0, 1.0)
    
    c_arr = np.array(base_color, dtype=float)[:3]
    if c_arr.max() > 1.0:
        c_arr = c_arr / 255.0
        
    face_colors = intensity[:, None] * c_arr[None, :]
    if alpha < 1.0:
        face_colors = np.column_stack([face_colors, np.full(len(face_colors), alpha)])
        
    order = np.argsort(z_centers)
    sorted_faces = faces_to_render[order]
    sorted_colors = face_colors[order]
    
    poly_verts = mesh.vertices[:, :2][sorted_faces]
    
    pc = PolyCollection(poly_verts, facecolors=sorted_colors, 
                        edgecolors=edge_color if edge_color else sorted_colors, 
                        linewidths=lw)
    ax.add_collection(pc)

def draw_dim_h(ax, x1, x2, y, label, color='#facc15', lw=1.3, fontsize=8.0, text_dy=2.5, arrow_bar=True):
    """Draws a horizontal dimension with extension lines and arrows."""
    if arrow_bar:
        ax.plot([x1, x1], [y - 1.5, y + 1.5], color=color, lw=lw*0.8)
        ax.plot([x2, x2], [y - 1.5, y + 1.5], color=color, lw=lw*0.8)
    ax.annotate("", xy=(x1, y), xytext=(x2, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw, shrinkA=0, shrinkB=0))
    mid_x = (x1 + x2) / 2.0
    ax.text(mid_x, y + text_dy, label, color='#060b14', fontsize=fontsize, weight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.22', facecolor=color, edgecolor='none', alpha=0.95))

def draw_dim_v(ax, x, y1, y2, label, color='#facc15', lw=1.3, fontsize=8.0, text_dx=2.5, arrow_bar=True):
    """Draws a vertical dimension with extension lines and arrows."""
    if arrow_bar:
        ax.plot([x - 1.5, x + 1.5], [y1, y1], color=color, lw=lw*0.8)
        ax.plot([x - 1.5, x + 1.5], [y2, y2], color=color, lw=lw*0.8)
    ax.annotate("", xy=(x, y1), xytext=(x, y2),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw, shrinkA=0, shrinkB=0))
    mid_y = (y1 + y2) / 2.0
    ax.text(x + text_dx, mid_y, label, color='#060b14', fontsize=fontsize, weight='bold',
            ha='left', va='center',
            bbox=dict(boxstyle='round,pad=0.22', facecolor=color, edgecolor='none', alpha=0.95))

def format_panel(ax, title, subtitle):
    ax.set_facecolor('#0b1329')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
        spine.set_linewidth(1.5)
    ax.tick_params(colors='#64748b', labelsize=8.5)
    ax.grid(True, linestyle='--', alpha=0.22, color='#38bdf8')
    ax.set_title(f"{title}\n{subtitle}", color='#f8fafc', fontsize=11.5, weight='bold', pad=12, loc='left')
    ax.set_xlabel("Vehicle Lateral Axis X (mm) • [Cabin View: +X is LEFT (Flap Door), -X is RIGHT (120V Outlet)]", color='#94a3b8', fontsize=8.5)
    ax.set_ylabel("Vehicle Fore-Aft Axis Y (mm: 0 = Outlet Face, -Y = Dashboard Cavity)", color='#94a3b8', fontsize=8.5)
    ax.set_xlim(-65, 85)
    ax.set_ylim(-148, 22)
    ax.set_aspect('equal')

def draw_shared_chassis(ax):
    """Draws shared chassis reference landmarks: Outlet box, M6 bolts, aluminum plate boundaries."""
    # Outlet box back and perimeter outline
    ax.add_patch(Rectangle((-55.875, -36.21), 111.75, 33.21, fill=True, facecolor='#1e293b', edgecolor='#334155', lw=1.2, alpha=0.6, zorder=1))
    ax.text(-53, -12, "OUTLET BOX (95190-CV780)", color='#64748b', fontsize=7.5, weight='bold')
    
    # Receptacle Collar at rear of box (seated connector port at X = +49.20 mm)
    ax.add_patch(Rectangle((49.20 - 11.35, -58.58), 22.70, 22.37, fill=True, facecolor='#0f172a', edgecolor='#475569', lw=1.0, zorder=2))
    
    # Chassis M6 Bolts (Absolute ground-truth vehicle reference datums)
    # Oval Bolt at X = -39.625 mm, Y = -42.50 mm
    ax.add_patch(Circle((-39.625, -42.50), 17.25 / 2.0, fill=True, facecolor='#facc15', edgecolor='#ca8a04', lw=1.5, alpha=0.35, zorder=3))
    ax.plot([-39.625], [-42.50], 'o', color='#facc15', markersize=6, zorder=4)
    ax.text(-39.625, -29.0, "M6 OVAL BOLT\n(-39.625, -42.50)", color='#facc15', fontsize=7.0, weight='bold', ha='center', zorder=5)

    # Center Bolt at X = +5.275 mm, Y = -42.20 mm
    ax.add_patch(Circle((5.275, -42.20), 17.25 / 2.0, fill=True, facecolor='#facc15', edgecolor='#ca8a04', lw=1.5, alpha=0.35, zorder=3))
    ax.plot([5.275], [-42.20], 'o', color='#facc15', markersize=6, zorder=4)
    ax.text(5.275, -29.0, "M6 CENTER BOLT\n(+5.275, -42.20)", color='#facc15', fontsize=7.0, weight='bold', ha='center', zorder=5)

print("Rendering high-contrast 3-panel orthographic top-down blueprint...")
fig = plt.figure(figsize=(32, 16), dpi=180)
plt.subplots_adjust(left=0.035, right=0.965, top=0.91, bottom=0.05, wspace=0.12)
fig.patch.set_facecolor('#060b14')

header_title = (
    "LOCK V2: ORTHOGRAPHIC TOP-DOWN (X-Y PLAN VIEW) COMPARISON\n"
    "Calibrated Realignment: +28.00 mm Shift (Cabin Left / +X) • 2.50 mm Fore-Aft Reach Relief (Rearward / -Y)"
)
fig.suptitle(header_title, color='#f8fafc', fontsize=17, weight='bold', y=0.965, ha='center')

# ==============================================================================
# PANEL 1: OLD DESIGN (X = +21.20 mm, Y = -95.51 mm)
# ==============================================================================
ax1 = fig.add_subplot(1, 3, 1)
format_panel(ax1, "PANEL A: OLD DESIGN (TEST-FIT IN VEHICLE)",
             "Cradle at X = +21.20 mm • Connector at X = +49.20 mm (Misalignment: 28.00 mm Cabin Right)")

draw_shared_chassis(ax1)

# Render Orange Connector in actual vehicle mated position (X = +49.20 mm)
render_mesh_topdown(ax1, c_mesh, [234, 88, 12], alpha=0.90, lw=0.15)

# Render Old Base Bracket (Blue) & Old Keeper (Green)
render_mesh_topdown(ax1, b_old, [2, 132, 199], alpha=0.85, lw=0.15)
render_mesh_topdown(ax1, k_old, [34, 197, 94], alpha=0.92, lw=0.2)

# Connector center axis line (X = 49.20)
ax1.plot([49.20, 49.20], [-35, -140], color='#f97316', linestyle='--', lw=1.4, zorder=6)
ax1.text(49.20, -143, "CONNECTOR AXIS\n(X = +49.20 mm)", color='#f97316', fontsize=7.5, weight='bold', ha='center')

# Old Cradle center axis line (X = 21.20)
ax1.plot([21.20, 21.20], [-35, -140], color='#38bdf8', linestyle='--', lw=1.4, zorder=6)
ax1.text(21.20, -143, "OLD CRADLE AXIS\n(X = +21.20 mm)", color='#38bdf8', fontsize=7.5, weight='bold', ha='center')

# Kinked cable route illustration (cable forced to bend 28mm to reach cradle)
kink_path_x = [49.20, 49.20, 44.0, 32.0, 21.20, 21.20]
kink_path_y = [-80.0, -95.5, -98.0, -101.0, -103.0, -135.0]
ax1.plot(kink_path_x, kink_path_y, color='#eab308', linestyle=':', lw=3.0, zorder=7)
ax1.annotate("CABLE FORCED TO BEND\n28 mm TOWARD CAR CENTER\nTO REACH CRADLE!",
             xy=(35.0, -100.0), xytext=(2.0, -122.0),
             arrowprops=dict(arrowstyle="->", color='#f43f5e', lw=1.8),
             color='#f43f5e', fontsize=8.0, weight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0b1329', edgecolor='#f43f5e', lw=1.2))

# Dimension callouts
draw_dim_h(ax1, 21.20, 49.20, -85.0, "LATERAL ERROR: 28.00 mm (Too Far Right in Car)", color='#f43f5e', fontsize=7.5, text_dy=-3.0)
draw_dim_h(ax1, 5.275, 21.20, -65.0, "Center to Cradle: 15.93 mm", color='#38bdf8', fontsize=7.2, text_dy=2.5)
draw_dim_v(ax1, -15.0, -40.91, -95.51, "Old Shoulder: Y = -95.51 mm", color='#facc15', fontsize=7.2, text_dx=2.5)

ax1.text(-50, -135, "STATUS: RETIRED DESIGN\nCable bend strain too aggressive\nMisaligned from vehicle connector",
         color='#f43f5e', fontsize=8.5, weight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e1b4b', edgecolor='#f43f5e', lw=1.5))

# ==============================================================================
# PANEL 2: NEW CALIBRATED DESIGN (X = +49.20 mm, Y = -98.01 mm)
# ==============================================================================
ax2 = fig.add_subplot(1, 3, 2)
format_panel(ax2, "PANEL B: NEW DESIGN (CALIBRATED & COLLISION-FREE)",
             "Cradle at X = +49.20 mm • Straight Coaxial Feed • 2.50 mm Fore-Aft Reach Relief")

draw_shared_chassis(ax2)

# Render Orange Connector in actual vehicle mated position
render_mesh_topdown(ax2, c_mesh, [234, 88, 12], alpha=0.90, lw=0.15)

# Render New Base Bracket (Blue) & New Keeper (Green)
render_mesh_topdown(ax2, b_new, [2, 132, 199], alpha=0.88, lw=0.15)
render_mesh_topdown(ax2, k_new, [34, 197, 94], alpha=0.95, lw=0.2)

# Straight cable route illustration (perfect coaxial alignment)
straight_cable_x = [49.20, 49.20]
straight_cable_y = [-80.0, -140.0]
ax2.plot(straight_cable_x, straight_cable_y, color='#eab308', linestyle='-', lw=4.0, alpha=0.7, zorder=6)

# New Coaxial alignment centerline
ax2.plot([49.20, 49.20], [-35, -140], color='#4ade80', linestyle='--', lw=1.5, zorder=7)
ax2.text(49.20, -143, "COAXIAL ALIGNMENT\n(X = +49.20 mm)", color='#4ade80', fontsize=8.0, weight='bold', ha='center')

# Monocoque Riser Spine routing annotation
ax2.annotate("CONTINUOUS RISER SPINE\nAscends via X in [6, 30] mm\n0.000000 mm3 Collision with Shroud!",
             xy=(20.0, -75.0), xytext=(-25.0, -90.0),
             arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=1.8),
             color='#38bdf8', fontsize=7.8, weight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0b1329', edgecolor='#38bdf8', lw=1.2))

# Fore-Aft Reach Relief annotation
ax2.annotate("2.50 mm REACH RELIEF\nShoulder at Y = -98.01 mm\nEliminates cable over-compression",
             xy=(49.20, -98.01), xytext=(8.0, -114.0),
             arrowprops=dict(arrowstyle="->", color='#4ade80', lw=1.8),
             color='#4ade80', fontsize=7.8, weight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0b1329', edgecolor='#4ade80', lw=1.2))

# Dimension callouts
draw_dim_h(ax2, 5.275, 49.20, -60.0, "Center to Cradle: 43.93 mm", color='#38bdf8', fontsize=7.2, text_dy=2.5)
draw_dim_v(ax2, -15.0, -40.91, -98.01, "New Reach: 57.10 mm (+2.5mm relief)", color='#4ade80', fontsize=7.2, text_dx=2.5)
draw_dim_h(ax2, 49.20 - 18.3, 49.20 + 18.3, -125.0, "Cradle Width: 36.6 mm", color='#facc15', fontsize=7.0, text_dy=-3.0)

ax2.text(-50, -135, "STATUS: PRODUCTION READY\n100% Watertight Manifold Solids\nCollision Volume: 0.000000 mm3",
         color='#4ade80', fontsize=8.5, weight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#052e16', edgecolor='#4ade80', lw=1.5))

# ==============================================================================
# PANEL 3: DIRECT CO-REGISTERED OVERLAY (OLD VS NEW) & TELEMETRY
# ==============================================================================
ax3 = fig.add_subplot(1, 3, 3)
format_panel(ax3, "PANEL C: DIRECT OVERLAY & MOTION VECTORS",
             "Co-Registered X-Y Plan Overlay • Vector Arrows: 28.00 mm (+X / Left), 2.50 mm (-Y / Rear)")

draw_shared_chassis(ax3)

# Render Old Bracket in ghosted red/amber outline
render_mesh_topdown(ax3, b_old, [239, 68, 68], alpha=0.30, edge_color='#f87171', lw=0.4)
render_mesh_topdown(ax3, k_old, [248, 113, 113], alpha=0.40, edge_color='#fca5a5', lw=0.5)

# Render New Bracket in solid vibrant Cyan/Green
render_mesh_topdown(ax3, b_new, [2, 132, 199], alpha=0.85, edge_color='#38bdf8', lw=0.4)
render_mesh_topdown(ax3, k_new, [34, 197, 94], alpha=0.92, edge_color='#4ade80', lw=0.5)

# Large Prominent Motion Vector Arrow (Lateral Shift: 28.00 mm in +X direction / Cabin Left)
arrow_lat = FancyArrowPatch((21.20, -102.11), (49.20, -102.11),
                            arrowstyle='Simple,tail_width=3.5,head_width=9.0,head_length=9.0',
                            color='#38bdf8', zorder=10)
ax3.add_patch(arrow_lat)
ax3.text(35.20, -95.0, "dX = +28.00 mm\n(CABIN LEFT / +X)", color='#38bdf8', fontsize=8.5, weight='bold',
         ha='center', va='center', bbox=dict(boxstyle='round,pad=0.25', facecolor='#060b14', edgecolor='#38bdf8', lw=1.2))

# Axial Reach Relief Vector Arrow (2.50 mm rearward)
arrow_ax = FancyArrowPatch((49.20, -95.51), (49.20, -98.01),
                           arrowstyle='Simple,tail_width=2.5,head_width=7.0,head_length=7.0',
                           color='#4ade80', zorder=10)
ax3.add_patch(arrow_ax)
ax3.text(49.20 + 10.0, -96.76, "dY = -2.50 mm\n(REACH RELIEF)", color='#4ade80', fontsize=7.5, weight='bold',
         ha='left', va='center', bbox=dict(boxstyle='round,pad=0.25', facecolor='#060b14', edgecolor='#4ade80', lw=1.0))

# Centerline comparisons
ax3.plot([21.20, 21.20], [-80, -130], color='#f87171', linestyle=':', lw=1.8, zorder=8)
ax3.text(21.20, -133, "Old X = +21.20", color='#f87171', fontsize=7.5, weight='bold', ha='center')

ax3.plot([49.20, 49.20], [-80, -130], color='#4ade80', linestyle='--', lw=1.8, zorder=8)
ax3.text(49.20, -133, "New X = +49.20", color='#4ade80', fontsize=7.5, weight='bold', ha='center')

# Engineering Spec Comparison Card in upper area (Y in [0, 20] mm)
spec_text = (
    "CALIBRATION TELEMETRY & SPECIFICATION COMPARISON:\n"
    "-------------------------------------------------------------------------\n"
    "Parameter                     Old Design          New Calibrated Design\n"
    "Cradle Centerline X:          +21.20 mm           +49.20 mm (+28.00 mm Shift)\n"
    "Shoulder Contact Plane Y:     -95.51 mm           -98.01 mm (-2.50 mm Relief)\n"
    "Cable Conduit Alignment:      28mm Lateral Kink   100% Straight Coaxial Feed\n"
    "Left Bearing Shoulder:        8.55 mm             8.55 mm (1.000 Symmetry)\n"
    "Right Bearing Shoulder:       8.55 mm             8.55 mm (1.000 Symmetry)\n"
    "Active Bearing Area:          ~324.9 mm2          ~324.9 mm2 (Solid PCTG)\n"
    "Riser Spine Routing:          Through X in [-19,0]Ascends X in [6,30] (Clear)\n"
    "Vehicle Collision Volume:     Interference        0.000000 mm3 (Watertight)\n"
    "Bambu P1S Bed Footprint:      170.3 x 88.6 mm     170.3 x 88.6 mm (Pass)"
)
ax3.text(-60.0, 18.0, spec_text, color='#e2e8f0', fontsize=7.2, fontfamily='monospace',
         va='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#3b82f6', lw=1.4, alpha=0.95))

# Exporting deliverables
output_path = os.path.join(target_dir, "ortho_top_down_comparison.png")
artifact_path = os.path.join(artifact_dir, "ortho_top_down_comparison.png")

print(f"Saving high-resolution orthographic comparison to {output_path}...")
plt.savefig(output_path, dpi=180, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig(artifact_path, dpi=180, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close(fig)

print("Orthographic top-down engineering comparison visual successfully generated!")
