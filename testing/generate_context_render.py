"""
generate_context_render.py
Generates realistic contextual 3D CAD meshes and multi-angle renders showing:
  1. The OEM Orange Cable Plug Connector with rear cable
  2. The OEM Black Outlet Housing Receptacle & Metal Chassis Plate
  3. The 3D Printed Saddle Base mounted on the plug
  4. The 3D Printed Sliding Deadbolt in both UNLOCKED and LOCKED states
  5. A cutaway cross-section showing how the deadbolt captures the latch tooth
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

def create_box(extents, translation=[0, 0, 0]):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(translation)
    return m

def create_cylinder(radius, height, translation=[0, 0, 0], transform=None):
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=24)
    if transform is not None:
        m.apply_transform(transform)
    m.apply_translation(translation)
    return m

# ==============================================================================
# BUILD CONTEXTUAL OEM CONNECTOR MESHES
# ==============================================================================
def build_orange_plug():
    """Builds a representative 3D mesh of the orange cable plug."""
    # Main oval body (length 54.6, width 33.0, height 20.8)
    body = create_box([33.0, 50.0, 20.8], [0, 25.0, -10.4])
    # Top latch tower (width 19.06, length 36.75, height 7.0 above body -> Z in [0, 3])
    tower = create_box([19.06, 36.75, 7.0], [0, 18.375, 0.5])
    # Side key ribs
    rib_r = create_box([2.5, 30.0, 3.5], [16.5 + 1.25, 20.0, -10.4])
    # Cable boot at rear (cylinder along Y axis)
    rot_x = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    cable = create_cylinder(radius=7.5, height=35.0, translation=[0, 65.0, -10.4], transform=rot_x)
    
    plug = body.union([tower, rib_r, cable], engine='manifold')
    return plug

def build_outlet_housing():
    """Builds a representative 3D mesh of the outlet housing & mating collar."""
    # Large black housing bulkhead/wall
    bulkhead = create_box([70.0, 6.0, 65.0], [0, -25.0, -10.0])
    # Protruding black collar (extends 22.37mm from bulkhead forward to Y = 0)
    collar = create_box([30.0, 22.37, 18.5], [0, -11.18, -10.4])
    # Latch tooth on top surface of collar:
    # Located at C2 = 8.73mm behind front rim -> Y = -8.73mm
    tooth = create_box([2.0, 2.5, 2.7], [0, -8.73, 0.25])
    # Side guide ribs flanking tooth (C5 = 13.82mm span)
    rib_l = create_box([1.8, 14.0, 2.8], [-6.0, -9.0, 0.3])
    rib_r = create_box([1.8, 14.0, 2.8], [6.0, -9.0, 0.3])
    
    # Silver stamped chassis mounting bracket (4mm to the right of collar)
    bracket = create_box([3.0, 45.0, 75.0], [19.0, -10.0, -10.0])
    
    housing = bulkhead.union([collar, tooth, rib_l, rib_r], engine='manifold')
    return housing, bracket

# Load 3D printed parts
saddle = trimesh.load(os.path.join(target_dir, "hv_lock_saddle.stl"))
slider = trimesh.load(os.path.join(target_dir, "hv_lock_slider.stl"))
plug = build_orange_plug()
housing, bracket = build_outlet_housing()

# Save contextual models as OBJ for 3D inspection
plug.export(os.path.join(target_dir, "context_plug.obj"))
housing.export(os.path.join(target_dir, "context_housing.obj"))
bracket.export(os.path.join(target_dir, "context_bracket.obj"))

# ==============================================================================
# RENDER 4-PANEL CONTEXTUAL FIGURE
# ==============================================================================
fig = plt.figure(figsize=(26, 18), dpi=180)
plt.subplots_adjust(left=0.03, right=0.97, top=0.94, bottom=0.04, wspace=0.10, hspace=0.14)
fig.patch.set_facecolor('#0f172a') # Slate 900

def plot_mesh(ax, mesh, color, alpha=0.9, edge_color=None, offset=[0, 0, 0]):
    m = mesh.copy()
    if any(offset):
        m.apply_translation(offset)
    if len(m.faces) > 3500:
        m = m.simplify_quadric_decimation(3500)
    v = m.vertices
    f = m.faces
    triangles = v[f]
    pc = Poly3DCollection(triangles, facecolors=color, alpha=alpha)
    if edge_color:
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.2)
    ax.add_collection3d(pc)

# Set view bounds helper
def set_view_bounds(ax, center=[0, 10, 0], radius=32, elev=28, azim=-125):
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')
    ax.set_facecolor('#0f172a')

# ------------------------------------------------------------------------------
# PANEL 1: EXPLODED ASSEMBLY VIEW (HOW PARTS FIT ON THE PLUG)
# ------------------------------------------------------------------------------
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
plot_mesh(ax1, plug, color='#f97316', alpha=0.9, edge_color='#c2410c')
plot_mesh(ax1, saddle, color='#0284c7', alpha=0.95, edge_color='#38bdf8', offset=[0, 0, 16.0])
plot_mesh(ax1, slider, color='#22c55e', alpha=0.95, edge_color='#15803d', offset=[0, 0, 32.0])

set_view_bounds(ax1, center=[0, 25, 10], radius=36, elev=26, azim=-55)
ax1.set_title("VIEW 1: Exploded Assembly (How the Lock Installs on the Cable Plug)", color='white', fontsize=13, weight='bold', pad=10)

ax1.text2D(0.05, 0.92, "① Orange Cable Plug (OEM Connector)", transform=ax1.transAxes, color='#fb923c', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.86, "② 3D Printed Saddle Base (Clips over Tower)", transform=ax1.transAxes, color='#38bdf8', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.80, "③ 3D Printed Sliding Deadbolt (Rides on T-Rail)", transform=ax1.transAxes, color='#4ade80', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.74, "Press Saddle down onto Tower -> Slide Deadbolt into track", transform=ax1.transAxes, color='#94a3b8', fontsize=9.5)

# ------------------------------------------------------------------------------
# PANEL 2: ASSEMBLED IN UNLOCKED POSITION (FREE TO INSERT / REMOVE)
# ------------------------------------------------------------------------------
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
# Housing Receptacle (front rim at Y=0)
plot_mesh(ax2, housing, color='#475569', alpha=0.7, edge_color='#334155')
plot_mesh(ax2, bracket, color='#94a3b8', alpha=0.4, edge_color='#cbd5e1')
# Plug mated to housing (rim at Y=0)
plot_mesh(ax2, plug, color='#f97316', alpha=0.9, edge_color='#c2410c')
# Saddle installed in position
plot_mesh(ax2, saddle, color='#0284c7', alpha=0.95, edge_color='#38bdf8')
# Slider retracted by +8.5mm in Y (UNLOCKED)
plot_mesh(ax2, slider, color='#eab308', alpha=0.95, edge_color='#ca8a04', offset=[0, 8.5, 0])

# View from side-angle where both collar tooth and slider are clearly visible
set_view_bounds(ax2, center=[0, 5, 2], radius=32, elev=32, azim=-60)
ax2.set_title("VIEW 2: Plugged In — UNLOCKED State (Slider Retracted 8.5mm)", color='white', fontsize=13, weight='bold', pad=10)
ax2.text2D(0.05, 0.92, "● UNLOCKED: Deadbolt pulled back by 8.5mm", transform=ax2.transAxes, color='#facc15', weight='bold', fontsize=11)
ax2.text2D(0.05, 0.86, "Deadbolt does NOT engage receptacle tooth", transform=ax2.transAxes, color='#cbd5e1', fontsize=10)
ax2.text2D(0.05, 0.80, "Cable can be freely inserted or unplugged", transform=ax2.transAxes, color='#cbd5e1', fontsize=10)

# ------------------------------------------------------------------------------
# PANEL 3: ASSEMBLED IN LOCKED POSITION (PHYSICALLY SECURED)
# ------------------------------------------------------------------------------
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
# Housing Receptacle
plot_mesh(ax3, housing, color='#475569', alpha=0.7, edge_color='#334155')
plot_mesh(ax3, bracket, color='#94a3b8', alpha=0.4, edge_color='#cbd5e1')
# Plug mated
plot_mesh(ax3, plug, color='#f97316', alpha=0.9, edge_color='#c2410c')
# Saddle installed
plot_mesh(ax3, saddle, color='#0284c7', alpha=0.95, edge_color='#38bdf8')
# Slider pushed forward (LOCKED, offset Y = 0)
plot_mesh(ax3, slider, color='#22c55e', alpha=0.95, edge_color='#15803d', offset=[0, 0, 0])

set_view_bounds(ax3, center=[0, 5, 2], radius=32, elev=32, azim=-60)
ax3.set_title("VIEW 3: Plugged In — LOCKED State (Deadbolt Slid Forward)", color='white', fontsize=13, weight='bold', pad=10)
ax3.text2D(0.05, 0.92, "● LOCKED: Deadbolt pushed forward with thumb", transform=ax3.transAxes, color='#4ade80', weight='bold', fontsize=11)
ax3.text2D(0.05, 0.86, "Tongue extends over collar & locks behind housing tooth", transform=ax3.transAxes, color='#cbd5e1', fontsize=10)
ax3.text2D(0.05, 0.80, "Blocks connector withdrawal completely", transform=ax3.transAxes, color='#cbd5e1', fontsize=10)

# ------------------------------------------------------------------------------
# PANEL 4: CLOSE-UP LONGITUDINAL CROSS-SECTION (INTERNAL ENGAGEMENT)
# ------------------------------------------------------------------------------
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_facecolor('#1e293b')

collar_x = [-22.37, 0, 0, -22.37, -22.37]
collar_y = [-2.0, -2.0, 0.0, 0.0, -2.0]
ax4.fill(collar_x, collar_y, color='#475569', alpha=0.8, label='Outlet Housing Collar')

tooth_x = [-9.73, -8.73, -8.73, -9.73, -9.73]
tooth_y = [0.0, 0.0, 2.7, 0.0, 0.0]
ax4.fill(tooth_x, tooth_y, color='#ef4444', alpha=0.95, edgecolor='#b91c1c', lw=2, label='Housing Latch Tooth (C2=8.73mm, H=2.7mm)')

plug_x = [0, 36.75, 36.75, 0, 0]
plug_y = [-2.0, -2.0, 3.0, 3.0, -2.0]
ax4.plot(plug_x, plug_y, color='#f97316', lw=2.5, label='Orange Plug Tower (B1=36.75mm)')

saddle_x = [0, 32, 32, 29, 29, 0, 0]
saddle_y = [3.0, 3.0, 8.5, 8.5, 7.0, 7.0, 3.0]
ax4.plot(saddle_x, saddle_y, color='#38bdf8', lw=2.5, label='Saddle Base (T-Rail)')

tongue_x = [-14.0, 0.0, 0.0, 20.0, 20.0, -14.0, -14.0]
tongue_y = [1.8, 1.8, 3.0, 10.0, 3.0, 5.7, 5.7]
ax4.plot(tongue_x, tongue_y, color='#22c55e', lw=3.0, label='Sliding Deadbolt (LOCKED)')

pocket_x = [-9.5, -6.5, -6.5, -9.5, -9.5]
pocket_y = [1.8, 1.8, 5.0, 5.0, 1.8]
ax4.plot(pocket_x, pocket_y, color='#facc15', lw=2.0, ls='--', label='Internal Tooth Capture Pocket')

ret_x = np.array(tongue_x) + 8.5
ret_y = np.array(tongue_y)
ax4.plot(ret_x, ret_y, color='#eab308', lw=1.5, ls=':', label='Deadbolt Retracted (UNLOCKED, 8.5mm back)')

ax4.axvline(0, color='#94a3b8', ls='--', lw=1.2)
ax4.text(0.5, -3.5, "Mating Interface Rim (Y = 0)", color='#94a3b8', fontsize=9.5)

ax4.annotate('Locking Pocket DROPS OVER Tooth\nBlocks Connector Withdrawal',
             xy=(-8.73, 2.7), xytext=(-22.0, 8.5),
             arrowprops=dict(arrowstyle='->', color='#4ade80', lw=2.0),
             color='#4ade80', weight='bold', fontsize=10.5,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor='#4ade80'))

ax4.annotate('Saddle Clamps\nFirmly to Tower',
             xy=(16.0, 3.0), xytext=(12.0, -3.0),
             arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=1.8),
             color='#38bdf8', weight='bold', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#0f172a', edgecolor='#38bdf8'))

ax4.set_xlim(-25, 40)
ax4.set_ylim(-5, 13)
ax4.set_aspect('equal')
ax4.set_title("VIEW 4: Longitudinal Cross-Section (How Deadbolt Locks onto Tooth)", color='white', fontsize=13, weight='bold', pad=10)
ax4.grid(True, color='#334155', ls=':', lw=0.8)
ax4.tick_params(colors='#94a3b8', labelsize=9)
ax4.set_xlabel("Y (Axial Length - mm)", color='#94a3b8', fontsize=10)
ax4.set_ylabel("Z (Elevation - mm)", color='#94a3b8', fontsize=10)
ax4.legend(loc='upper right', fontsize=8.0, facecolor='#0f172a', edgecolor='#334155', labelcolor='white')

# Save contextual blueprint
out_img = os.path.join(target_dir, "hv_lock_context_render.png")
art_img = os.path.join(artifact_dir, "hv_lock_context_render.png")
plt.savefig(out_img, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig(art_img, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved context renders to:", out_img)
