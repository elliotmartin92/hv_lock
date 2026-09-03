"""
illustrate_option2.py
Builds 3D CAD models of Option 2: The Interface-Only Split-Collar Bridle.
Renders an in-depth, annotated visual comparison showing exactly how it works
and how it avoids needing any box measurements.
"""

import math
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

# Load seated connector & housing context
housing_mesh = trimesh.load(os.path.join(target_dir, "testing", "seated_housing.stl"))
connector_mesh = trimesh.load(os.path.join(target_dir, "testing", "seated_connector.stl"))

# ==============================================================================
# BUILD OPTION 2 CAD GEOMETRY: INTERFACE SPLIT-COLLAR BRIDLE
# ==============================================================================
# Calibrated parameters:
COLLAR_W = 24.5  # Inner fit over D1=22.7mm collar + clearance
COLLAR_H = 34.5  # Inner fit over D2=33.05mm collar + clearance
GAP_L = 4.7      # Seated gap
PLUG_RIGID_L = 54.6 # B7
SHOULDER_Y = GAP_L + PLUG_RIGID_L # 59.3 mm

# Part 2A: Lower Receptacle Collar Jaw (clamps around 4.7mm neck)
# Sits at Y = 0 to 4.7mm, hugging the black collar
jaw_lower = trimesh.creation.box(extents=[COLLAR_W + 12.0, GAP_L, 16.0])
jaw_lower.apply_translation([0, GAP_L / 2.0, -COLLAR_H / 4.0])

# Bolt ears on left and right for clamping bolts
ear_left = trimesh.creation.box(extents=[10.0, GAP_L, 12.0])
ear_left.apply_translation([-(COLLAR_W/2.0 + 8.0), GAP_L / 2.0, 0])
ear_right = trimesh.creation.box(extents=[10.0, GAP_L, 12.0])
ear_right.apply_translation([(COLLAR_W/2.0 + 8.0), GAP_L / 2.0, 0])

# Part 2B: Upper Receptacle Collar Jaw with Forward Bridle Arms
jaw_upper = trimesh.creation.box(extents=[COLLAR_W + 12.0, GAP_L, 16.0])
jaw_upper.apply_translation([0, GAP_L / 2.0, COLLAR_H / 4.0 + 4.0])

# Forward Bridle Side Arms (spanning along left & right sides of the orange plug)
arm_left = trimesh.creation.box(extents=[5.0, SHOULDER_Y + 8.0, 14.0])
arm_left.apply_translation([-(COLLAR_W/2.0 + 10.0), (SHOULDER_Y + 8.0)/2.0, 0])

arm_right = trimesh.creation.box(extents=[5.0, SHOULDER_Y + 8.0, 14.0])
arm_right.apply_translation([(COLLAR_W/2.0 + 10.0), (SHOULDER_Y + 8.0)/2.0, 0])

# Rear Trap Bridge (Crosses behind the orange shoulder at Y = 59.3mm)
bridge_top = trimesh.creation.box(extents=[COLLAR_W + 25.0, 6.0, 8.0])
bridge_top.apply_translation([0, SHOULDER_Y + 4.0, 10.0])

bridge_bottom = trimesh.creation.box(extents=[COLLAR_W + 25.0, 6.0, 8.0])
bridge_bottom.apply_translation([0, SHOULDER_Y + 4.0, -10.0])

# Combine into Option 2 Upper Bridle & Lower Jaw
option2_bridle = trimesh.util.concatenate([jaw_upper, arm_left, arm_right, bridge_top, bridge_bottom, ear_left, ear_right])
option2_lower = jaw_lower

# Export Option 2 models for reference
os.makedirs(os.path.join(target_dir, "testing"), exist_ok=True)
option2_bridle.export(os.path.join(target_dir, "testing", "option2_bridle.stl"))
option2_lower.export(os.path.join(target_dir, "testing", "option2_clamp_jaw.stl"))

# ==============================================================================
# RENDER 4-PANEL COMPARISON & ILLUSTRATION OF OPTION 2
# ==============================================================================
fig = plt.figure(figsize=(26, 17), dpi=180)
plt.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.04, wspace=0.10, hspace=0.16)
fig.patch.set_facecolor('#070d19')

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

def setup_ax(ax, title, elev=22, azim=-55):
    ax.set_xlim(-55, 65)
    ax.set_ylim(-60, 105)
    ax.set_zlim(-30, 50)
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')
    ax.set_facecolor('#070d19')
    ax.set_title(title, color='white', fontsize=13, weight='bold', pad=12)

# PANEL 1: 3D VIEW OF OPTION 2 INSTALLED IN CONTEXT
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
plot_m(ax1, housing_mesh, color='#475569', alpha=0.40, edge_color='#64748b')
plot_m(ax1, connector_mesh, color='#f97316', alpha=0.75, edge_color='#c2410c')
plot_m(ax1, option2_bridle, color='#06b6d4', alpha=0.95, edge_color='#22d3ee')
plot_m(ax1, option2_lower, color='#a855f7', alpha=0.95, edge_color='#c084fc')
setup_ax(ax1, "VIEW 1: Option 2 — Interface Split-Collar Bridle (Assembled)")

ax1.text2D(0.02, 0.94, "■ Upper Bridle Frame (Cyan)", transform=ax1.transAxes, color='#22d3ee', weight='bold', fontsize=11)
ax1.text2D(0.02, 0.88, "■ Lower Clamp Jaw (Purple)", transform=ax1.transAxes, color='#c084fc', weight='bold', fontsize=11)
ax1.text2D(0.02, 0.80, "• Grips ONLY the 4.7mm exposed receptacle neck.", transform=ax1.transAxes, color='#e2e8f0', fontsize=9.5)
ax1.text2D(0.02, 0.74, "• Zero contact with the vehicle's black box lid.", transform=ax1.transAxes, color='#4ade80', weight='bold', fontsize=9.5)
ax1.text2D(0.02, 0.68, "• Needs 0 box measurements & ignores vehicle trim!", transform=ax1.transAxes, color='#facc15', weight='bold', fontsize=9.5)

# PANEL 2: EXPLODED 3D VIEW (HOW IT ASSEMBLES)
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
plot_m(ax2, housing_mesh, color='#475569', alpha=0.30, edge_color='#64748b')
plot_m(ax2, connector_mesh, color='#f97316', alpha=0.60, edge_color='#c2410c')

bridle_exp = option2_bridle.copy()
bridle_exp.apply_translation([0, 0, 18.0])
plot_m(ax2, bridle_exp, color='#06b6d4', alpha=0.95, edge_color='#22d3ee')

lower_exp = option2_lower.copy()
lower_exp.apply_translation([0, 0, -18.0])
plot_m(ax2, lower_exp, color='#a855f7', alpha=0.95, edge_color='#c084fc')
setup_ax(ax2, "VIEW 2: Exploded Assembly (2-Piece Clamp Around Neck)")

ax2.text2D(0.02, 0.94, "How Option 2 Assembles Around Connector:", transform=ax2.transAxes, color='white', weight='bold', fontsize=11)
ax2.text2D(0.02, 0.86, "1. Upper Bridle drops over plug & sits in 4.7mm gap.", transform=ax2.transAxes, color='#e2e8f0', fontsize=9.5)
ax2.text2D(0.02, 0.80, "2. Lower Jaw comes up from bottom into 4.7mm gap.", transform=ax2.transAxes, color='#e2e8f0', fontsize=9.5)
ax2.text2D(0.02, 0.74, "3. Tighten two M3 bolts on left/right ears to pinch neck.", transform=ax2.transAxes, color='#c084fc', weight='bold', fontsize=9.5)
ax2.text2D(0.02, 0.68, "4. Rear bridge traps plug shoulder at Y = 59.3mm.", transform=ax2.transAxes, color='#22d3ee', fontsize=9.5)

# PANEL 3: 2D KINEMATIC LOAD PATH (THE PROS & MECHANICAL REALITY)
ax3 = fig.add_subplot(2, 2, 3)
ax3.set_facecolor('#0f172a')

# Housing Wall
ax3.fill([-20, 0, 0, -20], [-25, -25, 30, 30], color='#334155', alpha=0.8, label='Housing Wall')
# Exposed Collar Neck (4.7mm)
ax3.fill([0, 4.7, 4.7, 0], [-17, -17, 17, 17], color='#1e293b', label='4.7mm Collar Neck')
# Orange Plug Body
ax3.fill([4.7, 59.3, 59.3, 4.7], [-10.4, -9.0, 9.0, 10.4], color='#f97316', alpha=0.85, label='Orange Plug Body')
ax3.fill([59.3, 85.0, 85.0, 59.3], [-8.5, -8.5, 8.5, 8.5], color='#334155', label='Cable Boot')

# Option 2 Clamp Jaw in 4.7mm neck
ax3.fill([0.5, 4.2, 4.2, 0.5], [17, 17, 24, 24], color='#06b6d4', alpha=0.9, label='Upper Collar Clamp')
ax3.fill([0.5, 4.2, 4.2, 0.5], [-24, -24, -17, -17], color='#a855f7', alpha=0.9, label='Lower Clamp Jaw')
# Bridle Arm spanning to shoulder
ax3.plot([2.35, 2.35, 63.3, 63.3], [24, 26, 26, 12], color='#22d3ee', lw=3.5, label='Bridle Arm & Rear Bridge')
ax3.plot([2.35, 2.35, 63.3, 63.3], [-24, -26, -26, -12], color='#22d3ee', lw=3.5)

# Clamping bolt arrows
ax3.annotate('', xy=(2.35, 17), xytext=(2.35, 23), arrowprops=dict(arrowstyle='->', color='#facc15', lw=3))
ax3.annotate('', xy=(2.35, -17), xytext=(2.35, -23), arrowprops=dict(arrowstyle='->', color='#facc15', lw=3))
ax3.text(8.0, 20, "M3 Clamping\nBolts Pinch Neck", color='#facc15', weight='bold', fontsize=9.0)

# Pull arrow
ax3.annotate('', xy=(75, 0), xytext=(95, 0), arrowprops=dict(arrowstyle='->', color='#ef4444', lw=3.5))
ax3.text(85, 4, "Cable Pull", color='#ef4444', weight='bold', fontsize=9.5, ha='center')

# Trap reaction
ax3.annotate('', xy=(59.3, 10), xytext=(63.3, 10), arrowprops=dict(arrowstyle='->', color='#22d3ee', lw=3))
ax3.text(50, 14, "Rear Bridge Traps\nPlug Shoulder", color='#22d3ee', weight='bold', fontsize=8.5, ha='center')

ax3.set_xlim(-25, 105)
ax3.set_ylim(-32, 38)
ax3.set_aspect('equal')
ax3.set_title("VIEW 3: Kinematic Load Path (Interface Collar Clamp)", color='white', fontsize=13, weight='bold', pad=12)
ax3.grid(True, color='#1e293b', ls=':', lw=0.8)
ax3.tick_params(colors='#94a3b8', labelsize=9)
ax3.set_xlabel("Y (Axial mm)", color='#94a3b8', fontsize=9.5)
ax3.set_ylabel("Z (Elevation mm)", color='#94a3b8', fontsize=9.5)
ax3.legend(loc='lower left', fontsize=8.0, facecolor='#070d19', edgecolor='#334155', labelcolor='white')

# PANEL 4: SIDE-BY-SIDE TRADEOFF MATRIX (OPTION 1 VS OPTION 2)
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_facecolor('#0f172a')
ax4.axis('off')
ax4.set_title("VIEW 4: Engineering Tradeoff Matrix — Option 1 vs Option 2", color='white', fontsize=13, weight='bold', pad=12)

table_data = [
    ["Feature / Criterion", "Option 1: Box C-Bracket (Concept 2)", "Option 2: Interface Collar Clamp"],
    ["Measurements Required", "Needs 3 box dimensions (E1, E2, E3)", "ZERO new measurements (uses current data)"],
    ["Vehicle Clearance", "Needs ~10mm clearance behind box lid", "Works 100% locally at connector seam"],
    ["Hardware Needed", "100% Toolless (Slide-in plastic keeper)", "Requires 2x M3/M4 bolts + nuts"],
    ["Anchor Method", "Positive mechanical hook over box lid", "Friction clamp around 4.7mm collar neck"],
    ["Installation Speed", "Instant 2-second slide & lock", "Requires screwdriver to bolt clamp jaws"],
    ["Pullout Strength", "Extreme (>40 kg / 90 lbs positive stop)", "Moderate (depends on friction/bolt tightness)"]
]

col_widths = [0.28, 0.36, 0.36]
cell_colors = []
for r in range(len(table_data)):
    if r == 0:
        cell_colors.append(['#1e293b', '#0284c7', '#0d9488'])
    elif r % 2 == 1:
        cell_colors.append(['#1e293b', '#0f172a', '#0f172a'])
    else:
        cell_colors.append(['#1e293b', '#1e293b', '#1e293b'])

tab = ax4.table(cellText=table_data, colWidths=col_widths, cellLoc='center', loc='center', cellColours=cell_colors)
tab.auto_set_font_size(False)
tab.set_fontsize(9.5)
tab.scale(1.0, 2.2)

for (row, col), cell in tab.get_celld().items():
    cell.set_edgecolor('#334155')
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
    else:
        cell.set_text_props(color='#cbd5e1')

out_path = os.path.join(artifact_dir, "option2_illustrated.png")
plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "option2_illustrated.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved Option 2 illustration successfully to:", out_path)
