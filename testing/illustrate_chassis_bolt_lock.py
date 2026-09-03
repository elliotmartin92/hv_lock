"""
illustrate_chassis_bolt_lock.py
Illustrates Anchor Option 2: The Chassis Bolt Cantilever Lock.
Shows:
1. Exact relationship between the lower silver plate bolt and the connector (to the right).
2. Slotted U-fork design (loosen bolt 2 turns, slide under washer, retighten).
3. Stiffened gusset arm bearing against the steel plate.
4. Why the bolt being to the left is actually an engineering advantage (rock solid, short 35mm arm).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

fig = plt.figure(figsize=(25, 14), dpi=180)
plt.subplots_adjust(left=0.04, right=0.96, top=0.92, bottom=0.06, wspace=0.12)
fig.patch.set_facecolor('#070d19')

ax1 = fig.add_subplot(1, 2, 1) # 2D Plan View (Looking down from above car floor)
ax2 = fig.add_subplot(1, 2, 2, projection='3d') # 3D Perspective

for ax in [ax1, ax2]:
    ax.set_facecolor('#0f172a')

# ------------------------------------------------------------------------------
# PANEL 1: 2D TOP VIEW (Looking Down at Silver Plate & Connector)
# ------------------------------------------------------------------------------
ax1.set_title("PANEL 1: 2D PLAN VIEW (Chassis Bolt to Connector Span)", color='white', fontsize=13, weight='bold', pad=15)

# Coordinate system:
# X = 0 is center of orange connector
# X < 0 is towards the LEFT (where silver plate & chassis bolts are)
# Y = 0 is the rear face of the housing
# Y > 0 is rearward (towards cable exit)
# Y < 0 is forward (towards 120V socket / windshield)

# Connector center at X = 0
# Collar: X = -18 to +18, Y = -22 to 0
# Orange Plug: X = -18 to +18, Y = 0 to 59.3
ax1.fill([-18.05, 18.05, 18.05, -18.05], [0, 0, 59.3, 59.3], color='#ea580c', edgecolor='#c2410c', lw=2, label='Orange Connector Body')
ax1.fill([-8.5, 8.5, 8.5, -8.5], [59.3, 90.0, 90.0, 59.3], color='#1e293b', edgecolor='#475569', lw=1.5, label='Cable Boot')

# Silver Plate (to the LEFT: X = -22.0 to -75.0, Y = -4.0 to 4.0)
ax1.fill([-75, -22, -22, -75], [-4, -4, 4, 4], color='#94a3b8', edgecolor='#cbd5e1', lw=2, label='Silver Steel Mounting Bracket')

# Lower Bolt Hole center at X = -42.0 mm, Y = 0.0 mm
bolt_x = -42.0
bolt_y = 0.0
bolt_dia = 6.0
washer_dia = 14.0

# Bolt Head & Washer
ax1.add_patch(patches.Circle((bolt_x, bolt_y), washer_dia/2, facecolor='#facc15', edgecolor='#ca8a04', lw=2, label='Chassis Bolt Head & Washer'))
ax1.add_patch(patches.Circle((bolt_x, bolt_y), bolt_dia/2, facecolor='#070d19', edgecolor='#facc15', lw=1.5))

# OPTION 2 BRACKET (Green):
# 1. Slotted U-Fork under washer: X = -50 to -34, Y = -10 to 10
# 2. Stiff Gusset Arm spanning from X = -34 to X = +22
# 3. Rear Horseshoe Trap at Y = 59.3 mm
bracket_x = [
    bolt_x - 10, bolt_x + 10, bolt_x + 10, 22, 22, 10, 10, -10, -10, bolt_x - 10
]
# Let's draw the bracket cleanly with patches
# Base Plate under washer
fork_plate = patches.Rectangle((bolt_x - 12, -10), 24, 20, facecolor='#22c55e', edgecolor='#4ade80', lw=2, alpha=0.9)
ax1.add_patch(fork_plate)
# Fork slot cutout
fork_slot = patches.Rectangle((bolt_x - 4, -12), 8, 14, facecolor='#0f172a', edgecolor='#4ade80', lw=1.5)
ax1.add_patch(fork_slot)

# Cantilever Bridge Arm from Bolt to Connector (X = bolt_x + 10 to 22, Y = 0 to 65)
arm_poly = [
    (bolt_x + 5, -8),
    (bolt_x + 5, 8),
    (18, 55),
    (24, 65),
    (-24, 65),
    (-24, 55),
    (bolt_x - 5, 8),
    (bolt_x - 5, -8)
]
ax1.add_patch(patches.Polygon(arm_poly, closed=True, facecolor='#22c55e', edgecolor='#4ade80', lw=2.5, alpha=0.75, label='3D Printed Cantilever Lock'))

# Cable U-slot behind shoulder
ax1.add_patch(patches.Circle((0, 59.3 + 4), 9.5, facecolor='#0f172a', edgecolor='#22c55e', lw=2))

# Dimension Arrows
def draw_dim(p1, p2, text, offset=(0, 0), color='#38bdf8'):
    ax1.annotate('', xy=p1, xytext=p2, arrowprops=dict(arrowstyle='<->', color=color, lw=2))
    ax1.text((p1[0]+p2[0])/2 + offset[0], (p1[1]+p2[1])/2 + offset[1], text,
             color=color, weight='bold', fontsize=9.5, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#070d19', edgecolor=color, lw=1.2))

draw_dim((bolt_x, 22), (0, 22), f"Short Span = {abs(bolt_x):.1f} mm", offset=(0, 5))
draw_dim((28, 0), (28, 59.3), "Shoulder Reach = 59.3 mm", offset=(16, 0), color='#fb923c')

# Annotations
ax1.annotate('SLOTTED U-FORK:\nJust loosen chassis bolt 2 turns,\nslide fork under washer, retighten!\nZero bolt removal needed.',
             xy=(bolt_x, 10), xytext=(bolt_x - 22, 45),
             arrowprops=dict(arrowstyle='->', color='#facc15', lw=2),
             color='#fde047', weight='bold', fontsize=9.0, ha='center',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#070d19', edgecolor='#facc15', lw=1.5))

ax1.annotate('POSITIVE MECHANICAL STOP:\nHorseshoe collar wraps behind\nrigid orange shoulder (Y = 59.3mm).\nCable cannot pull out!',
             xy=(0, 65), xytext=(0, 85),
             arrowprops=dict(arrowstyle='->', color='#4ade80', lw=2),
             color='#86efac', weight='bold', fontsize=9.0, ha='center',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#070d19', edgecolor='#22c55e', lw=1.5))

ax1.annotate('BEARS FLAT AGAINST STEEL PLATE:\nTorque is countered by broad contact\nagainst the solid steel bracket.',
             xy=(-32, 0), xytext=(-55, -22),
             arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=2),
             color='#7dd3fc', weight='bold', fontsize=9.0, ha='center',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#070d19', edgecolor='#38bdf8', lw=1.5))

ax1.set_xlim(-85, 50)
ax1.set_ylim(-35, 95)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.legend(loc='lower left', fontsize=8.5, facecolor='#070d19', edgecolor='#334155', labelcolor='white')

# ------------------------------------------------------------------------------
# PANEL 2: 3D PERSPECTIVE VIEW
# ------------------------------------------------------------------------------
ax2.set_title("PANEL 2: 3D PERSPECTIVE (Chassis Bolt Lock in Action)", color='white', fontsize=13, weight='bold', pad=15)

# Build 3D Trimesh representation
# 1. Silver plate
m_plate = trimesh.creation.box(extents=[55.0, 2.5, 75.0])
m_plate.apply_translation([-48.0, 0, 10.0])

# 2. Bolt & Washer
m_washer = trimesh.creation.cylinder(radius=7.0, height=2.0)
m_washer.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
m_washer.apply_translation([bolt_x, 2.0, 0])

# 3. Orange Connector
m_plug = trimesh.creation.box(extents=[36.1, 59.3, 20.8])
m_plug.apply_translation([0, 59.3/2.0, 0])

# 4. Lock Bracket (Green)
# Fork tab
m_tab = trimesh.creation.box(extents=[24.0, 4.0, 26.0])
m_tab.apply_translation([bolt_x, 4.0, 0])
# Diagonal bridge arm
m_arm = trimesh.creation.box(extents=[48.0, 60.0, 6.0])
m_arm.apply_translation([-18.0, 30.0, 10.0])
# Rear collar trap
m_trap = trimesh.creation.box(extents=[44.0, 8.0, 24.0])
m_trap.apply_translation([0, 59.3 + 4.0, 0])

m_lock = trimesh.util.concatenate([m_tab, m_arm, m_trap])

def plot_solid(ax, m, color, alpha=0.85, edge_color='#ffffff'):
    v = m.vertices
    f = m.faces
    pc = Poly3DCollection(v[f], facecolors=color, alpha=alpha)
    pc.set_edgecolor(edge_color)
    pc.set_linewidth(0.3)
    ax.add_collection3d(pc)

plot_solid(ax2, m_plate, color='#94a3b8', alpha=0.5, edge_color='#cbd5e1')
plot_solid(ax2, m_washer, color='#facc15', alpha=0.95, edge_color='#eab308')
plot_solid(ax2, m_plug, color='#ea580c', alpha=0.85, edge_color='#c2410c')
plot_solid(ax2, m_lock, color='#22c55e', alpha=0.92, edge_color='#4ade80')

ax2.view_init(elev=28, azim=-45)
ax2.set_xlim(-80, 40)
ax2.set_ylim(-15, 85)
ax2.set_zlim(-25, 45)
ax2.axis('off')

card_summary = (
    "WHY THE BOLT BEING TO THE LEFT IS ACTUALLY A BENEFIT:\n"
    "1. ULTRA SHORT LEVER ARM: Only ~42mm span from bolt to plug.\n"
    "2. UNLIMITED HOLDING POWER: Anchors to M6 steel chassis bolt.\n"
    "3. EASY INSTALL: Slotted fork slides under loosened bolt washer.\n"
    "4. CLEAN PACKAGING: Leaves 120V outlet face & lid 100% untouched!"
)
ax2.text2D(0.04, 0.04, card_summary, transform=ax2.transAxes, color='#e2e8f0', fontsize=8.5, weight='bold',
           bbox=dict(boxstyle='round,pad=0.45', facecolor='#070d19', edgecolor='#22c55e', lw=1.5))

out_file = os.path.join(artifact_dir, "chassis_bolt_lock.png")
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "chassis_bolt_lock.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved Chassis Bolt Lock diagram to:", out_file)
