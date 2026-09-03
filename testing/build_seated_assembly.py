"""
build_seated_assembly.py
Generates an accurate 3D CAD model of the V2L Orange Cable Connector SEATED onto the 
Black Outlet Receptacle Housing (Kia EV6 / E-GMP 95190-CV780), calibrated to the 
exact 4.7mm seated gap confirmed by the user.
"""

import math
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

def create_box(extents, translation=[0, 0, 0]):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(translation)
    return m

def create_cylinder(radius, height, translation=[0, 0, 0], transform=None):
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=28)
    if transform is not None:
        m.apply_transform(transform)
    m.apply_translation(translation)
    return m

# ==============================================================================
# DIMENSIONAL CONSTANTS (Calibrated from User Caliper Measurements & Photos)
# ==============================================================================
# Housing (95190-CV780)
HOUSING_BOX_W = 60.0       # Transverse width across module
HOUSING_BOX_L = 115.0      # Length of module
HOUSING_BOX_H = 38.0       # Depth/height of module box
COLLAR_OUTER_W = 32.5      # Receptacle outer width [D1]
COLLAR_OUTER_H = 20.8      # Receptacle outer height [D2]
COLLAR_PROTRUSION = 22.37  # Protrusion from housing backplate [C1]
TOOTH_DIST_FROM_RIM = 8.73 # Latch tooth location from collar rim [C2]
TOOTH_HEIGHT = 2.70        # Latch tooth protrusion [C4]
TOOTH_WIDTH = 2.00         # Latch tooth width [C3]

# Connector
SHROUD_W = 36.10           # Shroud outer width [A1]
SHROUD_H = 20.80           # Shroud body height [A2]
TOWER_W = 19.06            # Latch tower width [A3]
TOWER_L = 36.75            # Latch tower length [B1]
PLUG_TOTAL_H = 37.11       # Total plug height [A4]
BODY_RIGID_L = 54.60       # Rigid plug length [B7]
SEATED_GAP = 4.70          # Confirmed distance from plug rim to housing backplate

# ==============================================================================
# 1. BUILD ACCURATE OUTLET HOUSING MESH
# ==============================================================================
def build_housing_mesh():
    # Backplate plane is at Y = 0.
    # Housing box body extends in Y <= 0 (towards negative Y: Y in [-HOUSING_BOX_L, 0])
    # The receptacle collar protrudes into positive Y: Y in [0, COLLAR_PROTRUSION]
    # Receptacle collar rim is at Y = COLLAR_PROTRUSION (22.37 mm)
    
    # Module main box
    box_body = create_box([HOUSING_BOX_W, 55.0, HOUSING_BOX_H],
                          [0, -27.5, HOUSING_BOX_H / 2.0 - 15.0])
    
    # Protruding Receptacle Collar (Y in [0, COLLAR_PROTRUSION])
    collar_center = [0, COLLAR_PROTRUSION / 2.0, 0]
    collar = create_box([COLLAR_OUTER_W, COLLAR_PROTRUSION, COLLAR_OUTER_H], collar_center)
    
    # Hollow socket cavity inside collar (collar wall ~1.8mm)
    cavity = create_box([COLLAR_OUTER_W - 3.6, COLLAR_PROTRUSION + 1.0, COLLAR_OUTER_H - 3.6],
                        [0, (COLLAR_PROTRUSION + 1.0) / 2.0, 0])
    collar = collar.difference(cavity, engine='manifold')
    
    # Latch tooth on top surface of collar (Z = COLLAR_OUTER_H / 2):
    # Tooth is at distance TOOTH_DIST_FROM_RIM from the collar rim (Y = COLLAR_PROTRUSION - TOOTH_DIST_FROM_RIM)
    tooth_y = COLLAR_PROTRUSION - TOOTH_DIST_FROM_RIM # 22.37 - 8.73 = 13.64 mm
    tooth = create_box([TOOTH_WIDTH, 3.0, TOOTH_HEIGHT],
                       [0, tooth_y, COLLAR_OUTER_H / 2.0 + TOOTH_HEIGHT / 2.0])
    
    # Guide ribs flanking tooth
    rib_l = create_box([1.8, 12.0, 2.5], [-6.0, tooth_y, COLLAR_OUTER_H / 2.0 + 1.25])
    rib_r = create_box([1.8, 12.0, 2.5], [6.0, tooth_y, COLLAR_OUTER_H / 2.0 + 1.25])
    
    # Inverted U-notch and step on housing wall above connector (at Y=0, Z > COLLAR_OUTER_H/2)
    notch_relief = create_box([8.0, 6.0, 10.0], [0, -3.0, COLLAR_OUTER_H / 2.0 + 5.0])
    
    # Silver stamped metal chassis plate (4.0mm to the right of collar)
    bracket = create_box([2.5, 65.0, 55.0],
                         [COLLAR_OUTER_W / 2.0 + 4.0 + 1.25, -15.0, 10.0])
    # Hole in bracket
    rot_y = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
    bracket_hole = create_cylinder(radius=3.0, height=10.0,
                                   translation=[COLLAR_OUTER_W / 2.0 + 4.0 + 1.25, 10.0, 10.0],
                                   transform=rot_y)
    bracket = bracket.difference(bracket_hole, engine='manifold')
    
    housing = box_body.union([collar, tooth, rib_l, rib_r], engine='manifold')
    housing = housing.difference(notch_relief, engine='manifold')
    
    return housing, bracket

# ==============================================================================
# 2. BUILD ACCURATE ORANGE CONNECTOR MESH
# ==============================================================================
def build_connector_mesh():
    # When SEATED:
    # Front rim of orange connector is at Y = SEATED_GAP = 4.70 mm.
    # The connector body extends into positive Y from Y = 4.70 mm to Y = 4.70 + BODY_RIGID_L = 59.30 mm.
    # The black collar (which goes up to Y = 22.37 mm) is nested inside the orange connector!
    
    plug_start_y = SEATED_GAP # 4.70 mm
    
    # Outer orange shroud (starts at Y = 4.70, length = 32.0 mm)
    shroud_len = 32.0
    shroud = create_box([SHROUD_W, shroud_len, SHROUD_H],
                        [0, plug_start_y + shroud_len / 2.0, 0])
    
    # Internal hollow cavity of shroud (slides over collar)
    # Cavity depth = 17.67 mm (from 4.70 to 22.37)
    shroud_cavity = create_box([COLLAR_OUTER_W + 0.6, 18.5, COLLAR_OUTER_H + 0.6],
                               [0, plug_start_y + 18.5 / 2.0 - 0.5, 0])
    shroud = shroud.difference(shroud_cavity, engine='manifold')
    
    # Rear connector body (from Y = 4.70 + 30.0 to 4.70 + BODY_RIGID_L)
    rear_body_len = BODY_RIGID_L - 30.0 # 24.6 mm
    rear_body = create_box([28.0, rear_body_len, 18.0],
                           [0, plug_start_y + 30.0 + rear_body_len / 2.0, 0])
    
    # Top latch tower (width TOWER_W = 19.06, length TOWER_L = 36.75, height ~10mm above body)
    tower_z = SHROUD_H / 2.0 + 5.0 # Z in [10.4, 20.4]
    tower = create_box([TOWER_W, TOWER_L, 10.0],
                       [0, plug_start_y + TOWER_L / 2.0, tower_z])
    
    # Yellow slider track cavity on tower
    track_cavity = create_box([12.0, 24.0, 6.0],
                              [0, plug_start_y + 16.0, tower_z + 2.0])
    tower = tower.difference(track_cavity, engine='manifold')
    
    # Foam tape on tower
    foam = create_box([TOWER_W + 1.2, 10.0, 10.8],
                      [0, plug_start_y + 6.0, tower_z])
    
    # Rear cable exit boot (cylinder along Y axis)
    rot_x = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    cable_start_y = plug_start_y + BODY_RIGID_L
    cable = create_cylinder(radius=8.0, height=45.0,
                            translation=[0, cable_start_y + 22.5, 0],
                            transform=rot_x)
    
    connector = shroud.union([rear_body, tower, foam, cable], engine='manifold')
    return connector

# Build meshes
print("Building seated housing and connector...")
housing_mesh, bracket_mesh = build_housing_mesh()
connector_mesh = build_connector_mesh()

# Export individual and assembly STLs/OBJs
housing_mesh.export(os.path.join(target_dir, "seated_housing.stl"))
bracket_mesh.export(os.path.join(target_dir, "seated_bracket.stl"))
connector_mesh.export(os.path.join(target_dir, "seated_connector.stl"))

# Full Seated Assembly
full_assembly = trimesh.util.concatenate([housing_mesh, bracket_mesh, connector_mesh])
full_assembly.export(os.path.join(target_dir, "seated_assembly.stl"))
full_assembly.export(os.path.join(target_dir, "seated_assembly.obj"))
full_assembly.export(os.path.join(artifact_dir, "seated_assembly.stl"))
full_assembly.export(os.path.join(artifact_dir, "seated_assembly.obj"))
print("Saved seated assembly meshes.")

# ==============================================================================
# RENDER MULTI-VIEW HIGH-RES BLUEPRINT OF THE SEATED ASSEMBLY
# ==============================================================================
fig = plt.figure(figsize=(26, 16), dpi=180)
plt.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.05, wspace=0.10, hspace=0.15)
fig.patch.set_facecolor('#0f172a')

def plot_m(ax, mesh, color, alpha=0.9, edge_color=None):
    m = mesh.copy()
    if len(m.faces) > 3500:
        m = m.simplify_quadric_decimation(3500)
    v = m.vertices
    f = m.faces
    pc = Poly3DCollection(v[f], facecolors=color, alpha=alpha)
    if edge_color:
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.2)
    ax.add_collection3d(pc)

def setup_3d_ax(ax, title, elev=25, azim=-50):
    ax.set_xlim(-45, 55)
    ax.set_ylim(-35, 95)
    ax.set_zlim(-25, 45)
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')
    ax.set_facecolor('#0f172a')
    ax.set_title(title, color='white', fontsize=13, weight='bold', pad=10)

# ------------------------------------------------------------------------------
# VIEW 1: 3D ISOMETRIC VIEW OF SEATED ASSEMBLY
# ------------------------------------------------------------------------------
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
plot_m(ax1, housing_mesh, color='#334155', alpha=0.8, edge_color='#475569')
plot_m(ax1, bracket_mesh, color='#94a3b8', alpha=0.5, edge_color='#cbd5e1')
plot_m(ax1, connector_mesh, color='#f97316', alpha=0.9, edge_color='#c2410c')
setup_3d_ax(ax1, "VIEW 1: 3D Isometric View (Accurately Seated Assembly)", elev=28, azim=-55)

ax1.text2D(0.05, 0.92, "■ Outlet Housing (Grey / Slate)", transform=ax1.transAxes, color='#94a3b8', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.86, "■ Orange Cable Connector (Orange)", transform=ax1.transAxes, color='#fb923c', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.80, "■ Stamped Chassis Bracket (Silver)", transform=ax1.transAxes, color='#cbd5e1', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.74, "● 4.7mm Seated Gap between Rim & Housing", transform=ax1.transAxes, color='#38bdf8', weight='bold', fontsize=10)

# ------------------------------------------------------------------------------
# VIEW 2: TOP-DOWN VIEW (X-Y PLANE)
# ------------------------------------------------------------------------------
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
plot_m(ax2, housing_mesh, color='#334155', alpha=0.8, edge_color='#475569')
plot_m(ax2, bracket_mesh, color='#94a3b8', alpha=0.5, edge_color='#cbd5e1')
plot_m(ax2, connector_mesh, color='#f97316', alpha=0.9, edge_color='#c2410c')
setup_3d_ax(ax2, "VIEW 2: Top-Down Plan View (Showing 4.7mm Gap & Metal Bracket)", elev=88, azim=-90)

# ------------------------------------------------------------------------------
# VIEW 3: SIDE ELEVATION (Y-Z PLANE)
# ------------------------------------------------------------------------------
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
plot_m(ax3, housing_mesh, color='#334155', alpha=0.8, edge_color='#475569')
plot_m(ax3, bracket_mesh, color='#94a3b8', alpha=0.3, edge_color='#cbd5e1')
plot_m(ax3, connector_mesh, color='#f97316', alpha=0.9, edge_color='#c2410c')
setup_3d_ax(ax3, "VIEW 3: Side Elevation View (Y-Z Alignment)", elev=5, azim=0)

# ------------------------------------------------------------------------------
# VIEW 4: 2D CROSS-SECTION & PROPOSED EXTERNAL CLAMP ARCHITECTURES
# ------------------------------------------------------------------------------
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_facecolor('#1e293b')

# Draw housing backplate and collar outline
# Housing wall at Y <= 0
ax4.fill([-30, 0, 0, -30, -30], [-18, -18, 25, 25, -18], color='#334155', alpha=0.9, label='Housing Box Wall')
# Protruding collar: Y in [0, 22.37], Z in [-10.4, 10.4]
ax4.plot([0, 22.37, 22.37, 0], [10.4, 10.4, -10.4, -10.4], color='#64748b', lw=2.0, label='Receptacle Collar (Hidden inside)')

# Latch tooth at Y = 13.64 (22.37 - 8.73)
ax4.fill([12.64, 14.64, 14.64, 12.64], [10.4, 10.4, 13.1, 10.4], color='#ef4444', alpha=0.9, label='Covered Latch Tooth (Inside!)')

# Orange connector body (starts at Y = 4.70, ends at Y = 59.30)
ax4.plot([4.7, 59.3, 59.3, 4.7, 4.7], [10.4, 9.0, -9.0, -10.4, 10.4], color='#f97316', lw=2.5, label='Orange Connector Shroud')
# Orange tower (starts at Y = 4.7, ends at Y = 41.45, Z in [10.4, 20.4])
ax4.plot([4.7, 41.45, 41.45, 4.7, 4.7], [10.4, 10.4, 20.4, 20.4, 10.4], color='#ea580c', lw=2.2, label='Orange Tower')

# Annotate 4.7mm gap
ax4.annotate('', xy=(0, -14), xytext=(4.7, -14), arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=2.5))
ax4.text(2.35, -12, "4.7mm", color='#38bdf8', weight='bold', fontsize=9, ha='center')

# ANNOTATE PROPOSED EXTERNAL CLAMP CONCEPT (Concept: Housing-to-Plug Clamping Harness)
# Upper clamp arm hooks housing flange at Y = -20
# Lower clamp arm hooks behind orange connector shoulder at Y = 59.3
clamp_y = [-25, -25, -5, 4.7, 62, 62, 59.3]
clamp_z = [25, 29, 29, 26, 26, -15, -15]
ax4.plot(clamp_y, clamp_z, color='#22c55e', lw=3.0, ls='--', label='Proposed External Clamp / Retainer (Concept A)')

# Callout on Clamp Anchors
ax4.annotate('Upper Hook: Grips Housing Lip / Notches',
             xy=(-20, 28), xytext=(-28, 35),
             arrowprops=dict(arrowstyle='->', color='#4ade80', lw=2.0),
             color='#4ade80', weight='bold', fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor='#4ade80'))

ax4.annotate('Lower Clamp: Wraps Behind Plug Shoulder',
             xy=(60, -14), xytext=(35, -24),
             arrowprops=dict(arrowstyle='->', color='#4ade80', lw=2.0),
             color='#4ade80', weight='bold', fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor='#4ade80'))

ax4.set_xlim(-35, 75)
ax4.set_ylim(-30, 42)
ax4.set_aspect('equal')
ax4.set_title("VIEW 4: Cross-Section & External Clamp / Retainer Strategy", color='white', fontsize=13, weight='bold', pad=10)
ax4.grid(True, color='#334155', ls=':', lw=0.8)
ax4.tick_params(colors='#94a3b8', labelsize=9)
ax4.set_xlabel("Y (Axial Length - mm)", color='#94a3b8', fontsize=10)
ax4.set_ylabel("Z (Elevation - mm)", color='#94a3b8', fontsize=10)
ax4.legend(loc='lower left', fontsize=7.5, facecolor='#0f172a', edgecolor='#334155', labelcolor='white')

# Save figure
out_img = os.path.join(target_dir, "seated_assembly_blueprint.png")
art_img = os.path.join(artifact_dir, "seated_assembly_blueprint.png")
plt.savefig(out_img, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig(art_img, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved seated assembly blueprint to:", out_img)
