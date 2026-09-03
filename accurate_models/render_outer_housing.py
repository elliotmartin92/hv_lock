import os
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock\accurate_models"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\ca2c4a5c-394a-4c0b-b99d-8dde76573538"

stl_path = os.path.join(target_dir, "outer_housing_model.stl")
mesh = trimesh.load(stl_path)

fig = plt.figure(figsize=(20, 14), dpi=180, facecolor='#0b1120')

ax_front = fig.add_subplot(2, 2, 1)
ax_side  = fig.add_subplot(2, 2, 2)
ax_top   = fig.add_subplot(2, 2, 3)
ax_iso   = fig.add_subplot(2, 2, 4, projection='3d')

for ax in [ax_front, ax_side, ax_top]:
    ax.set_facecolor('#0f172a')
    ax.grid(True, linestyle='--', alpha=0.25, color='#38bdf8')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#1e293b')

def draw_dim_h(ax, x1, x2, y, label, color='#38bdf8', offset=5):
    ax.annotate('', xy=(x1, y), xytext=(x2, y),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.8, shrinkA=0, shrinkB=0))
    ax.plot([x1, x1], [y - 3, y + 3], color=color, lw=1.2)
    ax.plot([x2, x2], [y - 3, y + 3], color=color, lw=1.2)
    ax.text((x1 + x2) / 2, y + offset, label, color='white', fontweight='bold', fontsize=9,
            ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', facecolor='#0369a1', edgecolor=color, lw=1, alpha=0.9))

def draw_dim_v(ax, x, y1, y2, label, color='#38bdf8', offset=5):
    ax.annotate('', xy=(x, y1), xytext=(x, y2),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.8, shrinkA=0, shrinkB=0))
    ax.plot([x - 3, x + 3], [y1, y1], color=color, lw=1.2)
    ax.plot([x - 3, x + 3], [y2, y2], color=color, lw=1.2)
    ax.text(x + offset, (y1 + y2) / 2, label, color='white', fontweight='bold', fontsize=9,
            ha='left', va='center', bbox=dict(boxstyle='round,pad=0.2', facecolor='#0369a1', edgecolor=color, lw=1, alpha=0.9))

v = mesh.vertices
f = mesh.faces

# 1. FRONT VIEW (X vs Z)
ax_front.set_title("VIEW 1: FRONT ELEVATION (Completely Smooth Curved Arch Over Top)", color='#38bdf8', fontsize=12, fontweight='bold', pad=10)
ax_front.tripcolor(v[:, 0], v[:, 2], f, facecolors=np.ones(len(f)), cmap='Blues', alpha=0.45, edgecolors='#1e293b', lw=0.2)
ax_front.set_xlabel("X (Width, mm)", color='#94a3b8', fontsize=10)
ax_front.set_ylabel("Z (Height, mm)", color='#94a3b8', fontsize=10)
ax_front.set_xlim(-90, 95)
ax_front.set_ylim(-15, 115)
ax_front.set_aspect('equal')

draw_dim_h(ax_front, -71.15, 71.15, 104, "[H1] Total Outer Width: 142.30 mm", color='#f59e0b', offset=3)
draw_dim_h(ax_front, -57.3, 57.3, 59.1, "[H3] Window: 114.60 mm", color='#10b981', offset=3)
draw_dim_v(ax_front, 78, 0, 95.4, "[H2] Total Height: 95.40 mm", color='#f59e0b', offset=4)
draw_dim_v(ax_front, 60, 34.0, 84.2, "[H4] Window H: 50.20 mm", color='#10b981', offset=4)
draw_dim_v(ax_front, -60, 27.1, 34.0, "Plate to Window: 6.90 mm", color='#f59e0b', offset=-115)
draw_dim_v(ax_front, -78, 0, 27.1, "Chin: 27.10 mm", color='#ec4899', offset=-60)

# 2. SIDE VIEW (Y vs Z) - GENTLE WING SLOPE & FLUSH ROOF ALIGNMENT
ax_side.set_title("VIEW 2: SIDE PROFILE (Gentle Wing Slope, Wings Strictly Below Top Roof)", color='#38bdf8', fontsize=12, fontweight='bold', pad=10)
ax_side.tripcolor(v[:, 1], v[:, 2], f, facecolors=np.ones(len(f)), cmap='Blues', alpha=0.45, edgecolors='#1e293b', lw=0.2)
ax_side.set_xlabel("Y (Depth, mm: +Y Cabin Front, -Y Interior Rear)", color='#94a3b8', fontsize=10)
ax_side.set_ylabel("Z (Height, mm)", color='#94a3b8', fontsize=10)
ax_side.set_xlim(-75, 20)
ax_side.set_ylim(-15, 115)
ax_side.set_aspect('equal')

draw_dim_h(ax_side, -58.8, 0.0, 104, "[H7a] Side Wall Depth: 58.80 mm", color='#10b981', offset=3)
draw_dim_h(ax_side, -7.10, 0.0, 15, "Chin: 7.10 mm", color='#ec4899', offset=4)
draw_dim_h(ax_side, -34.0, 0.0, 98, "[H9] Top Shelf: 34.00 mm", color='#38bdf8', offset=3)

# Highlight wing slope and heights:
draw_dim_v(ax_side, -5.6, 0, 27.10, "Chin: 27.10mm", color='#ec4899', offset=3)
draw_dim_v(ax_side, -5.6, 27.10, 34.00, "Gap: 6.90mm", color='#f59e0b', offset=3)
draw_dim_v(ax_side, -62.0, 34.0, 83.50, "Rear wing: 83.50mm", color='#38bdf8', offset=-95)
draw_dim_v(ax_side, -34.0, 34.0, 88.50, "Front wing: 88.50mm (flush)", color='#38bdf8', offset=-105)
draw_dim_v(ax_side, -53.0, 0, 31.97, "Plate back: 31.97mm", color='#22c55e', offset=3)

# 3. TOP VIEW (X vs Y) - 10.15 MM GAP TO WINGS & HORIZONTAL OVAL
ax_top.set_title("VIEW 3: TOP PLAN (Exact 10.15 mm Space to Wings & Horizontal Oval Slot)", color='#38bdf8', fontsize=12, fontweight='bold', pad=10)
ax_top.tripcolor(v[:, 0], v[:, 1], f, facecolors=np.ones(len(f)), cmap='Blues', alpha=0.45, edgecolors='#1e293b', lw=0.2)
ax_top.set_xlabel("X (Width, mm)", color='#94a3b8', fontsize=10)
ax_top.set_ylabel("Y (Depth, mm)", color='#94a3b8', fontsize=10)
ax_top.set_xlim(-90, 95)
ax_top.set_ylim(-75, 15)
ax_top.set_aspect('equal')

draw_dim_h(ax_top, -70.25, 70.25, -68, "[H11] Inner Wing Span: 140.50 mm", color='#f59e0b', offset=3)
draw_dim_h(ax_top, -60.10, 60.10, -58, "Aluminum Width: 120.20 mm", color='#22c55e', offset=3)

# 10.15 mm horizontal space callouts
draw_dim_h(ax_top, -70.25, -60.10, -50, "10.15mm space", color='#38bdf8', offset=2)
draw_dim_h(ax_top, 60.10, 70.25, -50, "10.15mm space", color='#38bdf8', offset=2)

# Highlight Holes:
oval_patch = Ellipse((-39.625, -42.475), 7.45, 6.45, color='#ef4444', fill=True, alpha=0.9, zorder=5)
circle_c   = plt.Circle((5.275, -42.175), 6.45/2.0, color='#ef4444', fill=True, alpha=0.9, zorder=5)
ax_top.add_patch(oval_patch)
ax_top.add_patch(circle_c)

# Dimension callouts in X:
draw_dim_h(ax_top, -60.10, -43.35, -28, "16.75mm offset", color='#f59e0b', offset=2)
draw_dim_h(ax_top, -43.35, -35.90, -35, "Oval 7.45x6.45", color='#ef4444', offset=2)
draw_dim_h(ax_top, -35.90, 2.05, -28, "37.95mm gap", color='#10b981', offset=2)
draw_dim_h(ax_top, 2.05, 8.50, -35, "Ø 6.45", color='#ef4444', offset=2)

# Dimension callouts in Y from back edge (Y = -53.0):
draw_dim_v(ax_top, -48.0, -53.0, -45.7, "7.3mm to back", color='#ef4444', offset=-50)
draw_dim_v(ax_top, 15.0, -53.0, -45.4, "7.6mm to back", color='#10b981', offset=4)

# 4. ISOMETRIC 3D SOLID SHADED
ax_iso.set_facecolor('#0f172a')
ax_iso.set_title("VIEW 4: 3D ISOMETRIC SOLID (Wings Flush Under Roof Arch)", color='#22c55e', fontsize=12, fontweight='bold', pad=10)

sample_faces = mesh.faces[::2]
poly3d = Poly3DCollection(mesh.vertices[sample_faces], alpha=0.88, edgecolor='#0f172a', lw=0.2)
poly3d.set_facecolor('#334155')
ax_iso.add_collection3d(poly3d)

ax_iso.set_xlim(-80, 80)
ax_iso.set_ylim(-65, 15)
ax_iso.set_zlim(0, 100)
ax_iso.view_init(elev=28, azim=-55)
ax_iso.axis('off')

out_art = os.path.join(artifact_dir, "outer_housing_blueprint.png")
out_ws = os.path.join(target_dir, "outer_housing_blueprint.png")

plt.tight_layout()
plt.savefig(out_art, dpi=180, facecolor=fig.get_facecolor(), edgecolor='none')
plt.savefig(out_ws, dpi=180, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Updated outer housing blueprint saved successfully to both locations!")
