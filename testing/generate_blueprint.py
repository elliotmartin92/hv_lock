"""
generate_blueprint.py
Generates a comprehensive 3-panel mechanical blueprint:
  Panel 1: 3D Isometric View of the Assembled Lock Mechanism
  Panel 2: 2D Dimensioned Orthographic Projections (Top & Side Views)
  Panel 3: Kinematic Cross-Section (LOCKED vs UNLOCKED Stroke Comparison)
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

# Load meshes
saddle_mesh = trimesh.load(os.path.join(target_dir, "hv_lock_saddle.stl"))
slider_mesh = trimesh.load(os.path.join(target_dir, "hv_lock_slider.stl"))

# Create 3-panel figure
fig = plt.figure(figsize=(26, 9.5), dpi=180)
plt.subplots_adjust(left=0.03, right=0.97, top=0.91, bottom=0.06, wspace=0.15)
fig.patch.set_facecolor('#0f172a') # Slate 900

# ==============================================================================
# PANEL 1: 3D ISOMETRIC ASSEMBLY
# ==============================================================================
ax1 = fig.add_subplot(1, 3, 1, projection='3d')
ax1.set_facecolor('#0f172a')

def add_mesh_3d(ax, mesh, color, alpha=0.9, edge_color=None):
    # Downsample if needed for fast render
    m = mesh
    if len(m.faces) > 4000:
        m = m.simplify_quadric_decimation(4000)
    v = m.vertices
    f = m.faces
    triangles = v[f]
    pc = Poly3DCollection(triangles, facecolors=color, alpha=alpha)
    if edge_color:
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.2)
    ax.add_collection3d(pc)

# Plot Saddle Base in Cyan/Steel Blue
add_mesh_3d(ax1, saddle_mesh, color='#0284c7', alpha=0.85, edge_color='#38bdf8')

# Plot Slider in Orange (positioned in Locked State: slide offset Y = 0)
add_mesh_3d(ax1, slider_mesh, color='#ea580c', alpha=0.95, edge_color='#fb923c')

# Set 3D limits and view
all_bounds = np.vstack([saddle_mesh.bounds, slider_mesh.bounds])
min_b = all_bounds.min(axis=0)
max_b = all_bounds.max(axis=0)
max_range = (max_b - min_b).max() / 1.8
mid_b = (max_b + min_b) / 2.0

ax1.set_xlim(mid_b[0] - max_range, mid_b[0] + max_range)
ax1.set_ylim(mid_b[1] - max_range, mid_b[1] + max_range)
ax1.set_zlim(mid_b[2] - max_range, mid_b[2] + max_range)

ax1.view_init(elev=28, azim=-55)
ax1.set_title("PANEL 1: 3D Isometric Assembly (Locked State)", color='white', fontsize=13, weight='bold', pad=12)
ax1.axis('off')

# Add 3D Legend annotations
ax1.text2D(0.05, 0.92, "■ Sliding Deadbolt (Orange)", transform=ax1.transAxes, color='#fb923c', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.87, "■ Saddle Base (Cyan)", transform=ax1.transAxes, color='#38bdf8', weight='bold', fontsize=11)
ax1.text2D(0.05, 0.82, "⮞ Front Locking Tongue (Y < 0)", transform=ax1.transAxes, color='#fdba74', fontsize=9.5)


# ==============================================================================
# PANEL 2: 2D ORTHOGRAPHIC PROJECTIONS & TOLERANCES
# ==============================================================================
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_facecolor('#1e293b') # Slate 800

# Draw Top-down silhouette
# Saddle outer boundary: X in [-12, 12], Y in [0, 32]
ax2.plot([-11.98, 11.98, 11.98, -11.98, -11.98], [0, 0, 32, 32, 0], color='#38bdf8', lw=2.2, label='Saddle Base')
# Tower inner pocket: X in [-9.78, 9.78], Y in [0, 32]
ax2.plot([-9.78, 9.78, 9.78, -9.78, -9.78], [0, 0, 32, 32, 0], color='#0284c7', ls='--', lw=1.5, label='Inner Tower Pocket (19.56mm)')

# Slider in Locked position:
# Carriage: X in [-12, 12], Y in [0, 20]
# Tongue: X in [-5.75, 5.75], Y in [-14, 0]
tongue_x = [-5.75, 5.75, 5.75, -5.75, -5.75]
tongue_y = [-14, -14, 0, 0, -14]
ax2.plot(tongue_x, tongue_y, color='#ea580c', lw=2.2, label='Locking Tongue')

# Tooth Pocket: X in [-2, 2], Y in [-9.5, -6.5]
ax2.plot([-2, 2, 2, -2, -2], [-9.75, -9.75, -6.25, -6.25, -9.75], color='#facc15', lw=1.8, label='Tooth Capture Pocket')

# Receptacle Latch Tooth (Housing reference): X in [-1, 1], Y = -8.73
ax2.plot([-1, 1, 1, -1, -1], [-9.23, -9.23, -8.23, -8.23, -9.23], color='#ef4444', lw=2.0, label='Housing Latch Tooth (C2=8.73mm)')

# Annotate key dimensions
def draw_arrow_h(ax, y, x1, x2, text, c='#38bdf8'):
    ax.annotate('', xy=(x1, y), xytext=(x2, y), arrowprops=dict(arrowstyle='<->', color=c, lw=1.5))
    ax.text((x1+x2)/2, y+1.0, text, color=c, fontsize=9.5, weight='bold', ha='center')

def draw_arrow_v(ax, x, y1, y2, text, c='#fb923c'):
    ax.annotate('', xy=(x, y1), xytext=(x, y2), arrowprops=dict(arrowstyle='<->', color=c, lw=1.5))
    ax.text(x+1.2, (y1+y2)/2, text, color=c, fontsize=9.5, weight='bold', va='center', rotation=-90)

draw_arrow_h(ax2, 36.0, -11.98, 11.98, "Outer Width: 23.96 mm", '#38bdf8')
draw_arrow_h(ax2, 28.0, -9.78, 9.78, "Tower Pocket: 19.56 mm", '#38bdf8')
draw_arrow_h(ax2, -18.0, -5.75, 5.75, "Tongue Width: 11.50 mm", '#fb923c')
draw_arrow_v(ax2, 15.5, 0, 32, "Saddle Length: 32.0 mm", '#38bdf8')
draw_arrow_v(ax2, -8.5, -14, 0, "Tongue Reach: 14.0 mm", '#fb923c')
draw_arrow_v(ax2, 8.5, -8.73, 0, "Tooth Offset: 8.73 mm", '#facc15')

ax2.set_xlim(-22, 22)
ax2.set_ylim(-26, 42)
ax2.set_aspect('equal')
ax2.set_title("PANEL 2: 2D Orthographic Feature Layout (Top-Down)", color='white', fontsize=13, weight='bold', pad=12)
ax2.grid(True, color='#334155', ls=':', lw=0.8)
ax2.tick_params(colors='#94a3b8', labelsize=9)
ax2.set_xlabel("X (Transverse Width - mm)", color='#94a3b8', fontsize=10)
ax2.set_ylabel("Y (Axial Length - mm)", color='#94a3b8', fontsize=10)
ax2.legend(loc='lower left', fontsize=8.5, facecolor='#0f172a', edgecolor='#334155', labelcolor='white')


# ==============================================================================
# PANEL 3: KINEMATIC STROKE ANALYSIS (LOCKED VS UNLOCKED)
# ==============================================================================
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_facecolor('#1e293b')

# Y-Z Cross Section at X = 0 (Centerline)
# Upper sub-plot: UNLOCKED STATE (Slide retracted by 8.5mm)
# Lower sub-plot: LOCKED STATE (Slide forward at Y = 0)

# Helper to draw cross-section profile:
def draw_state(ax, y_base, label, is_locked=True):
    # Saddle profile: Y in [0, 32], Z in [-12, 7]
    saddle_poly_y = [0, 32, 32, 29, 29, 0, 0]
    saddle_poly_z = np.array([3, 3, 8.5, 8.5, 3, 3, 3]) + y_base
    ax.plot(saddle_poly_y, saddle_poly_z, color='#38bdf8', lw=2.0)
    
    # Skirt
    ax.plot([0, 0], np.array([3, -12]) + y_base, color='#0284c7', lw=1.5, ls='--')
    ax.plot([32, 32], np.array([3, -12]) + y_base, color='#0284c7', lw=1.5, ls='--')
    
    # Latch tooth at Y = -8.73, Z = [0, 2.7]
    tooth_y = [-9.73, -8.73, -8.73, -9.73]
    tooth_z = np.array([0, 2.7, 0, 0]) + y_base
    ax.fill(tooth_y, tooth_z, color='#ef4444', alpha=0.9, edgecolor='#b91c1c', lw=1.5)
    ax.text(-8.73, y_base + 3.8, "Tooth", color='#f87171', fontsize=8.5, ha='center', weight='bold')
    
    # Receptacle rim at Y = 0
    ax.axvline(0, color='#64748b', ls=':', lw=1.0)
    
    slide_offset = 0.0 if is_locked else 8.5
    # Slider profile:
    # Tongue: Y in [-14 + offset, 0 + offset], Z in [2.0, 6.2]
    # Carriage: Y in [0 + offset, 20 + offset], Z in [3.0, 10.0]
    sy = [-14 + slide_offset, 0 + slide_offset, 0 + slide_offset, 20 + slide_offset, 20 + slide_offset, -14 + slide_offset, -14 + slide_offset]
    sz = np.array([2.0, 2.0, 3.0, 10.0, 3.0, 3.0, 2.0]) + y_base
    
    c_fill = '#ea580c' if is_locked else '#3b82f6'
    ax.plot(sy, sz, color='#fb923c', lw=2.2)
    
    # Pocket inside tongue:
    py = [-9.5 + slide_offset, -6.5 + slide_offset, -6.5 + slide_offset, -9.5 + slide_offset, -9.5 + slide_offset]
    pz = np.array([2.0, 2.0, 4.8, 4.8, 2.0]) + y_base
    ax.plot(py, pz, color='#facc15', lw=1.8)
    
    status_text = "LOCKED: Tongue Captures Tooth (8.5mm Stroke)" if is_locked else "UNLOCKED: Retracted 8.5mm (Clear to Disconnect)"
    status_color = '#4ade80' if is_locked else '#60a5fa'
    ax.text(10, y_base + 12.0, f"● {status_text}", color=status_color, fontsize=11, weight='bold')

# Draw both states
draw_state(ax3, y_base=18.0, label="LOCKED", is_locked=True)
draw_state(ax3, y_base=-10.0, label="UNLOCKED", is_locked=False)

# Draw Stroke Travel Arrow
ax3.annotate('', xy=(8.5, 3.0), xytext=(0, 3.0),
             arrowprops=dict(arrowstyle='<->', color='#facc15', lw=2.2))
ax3.text(4.25, 4.5, "8.50 mm Stroke", color='#facc15', fontsize=10, weight='bold', ha='center')

ax3.set_xlim(-18, 38)
ax3.set_ylim(-26, 36)
ax3.set_title("PANEL 3: Kinematic Cross-Section (Y-Z Stroke Analysis)", color='white', fontsize=13, weight='bold', pad=12)
ax3.grid(True, color='#334155', ls=':', lw=0.8)
ax3.tick_params(colors='#94a3b8', labelsize=9)
ax3.set_xlabel("Y (Axial Length - mm)", color='#94a3b8', fontsize=10)
ax3.set_ylabel("Z (Elevation - mm)", color='#94a3b8', fontsize=10)

# Save Blueprint
out_img = os.path.join(target_dir, "hv_lock_blueprint.png")
art_img = os.path.join(artifact_dir, "hv_lock_blueprint.png")
plt.savefig(out_img, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig(art_img, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved blueprints to:", out_img)
