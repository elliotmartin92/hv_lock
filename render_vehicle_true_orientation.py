"""
render_vehicle_true_orientation.py
Renders the EXACT vehicle orientation as described by the user:
- Front of black box has the 120V AC plug facing the WINDSHIELD (Forward / +Y)
- Connector comes in from the BACK (Rear / -Y)
- Looking from the back forward, the connector is on the RIGHT side (X > 0)
- The 111.75mm box body extends to the LEFT (X < 0)
- The lid is on TOP (+Z), overhanging 12.45mm towards the rear (-Y)
- Clear, professional labels with ZERO overlaps
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

# Dimensions
BOX_W = 111.75   # X: Long width across car
BOX_D = 48.15    # Y: Front-to-back depth (120V face to connector face)
BOX_H = 42.67    # Z: Vertical height (bottom to top lid)
LID_OH = 12.45   # Y: Lid overhang at the rear
LID_T = 4.58     # Z: Lid thickness

CONN_W = 36.10   # X: Orange connector body width
CONN_D = 20.80   # Z or Y depending on connector oval
CONN_L = 54.60   # Y: Rigid connector axial length extending rearward
CABLE_D = 17.00  # Cable boot diameter
WALL_T = 4.00    # Bracket wall thickness

fig = plt.figure(figsize=(26, 18), dpi=180)
fig.patch.set_facecolor('#070d19')

ax_rear = fig.add_subplot(2, 2, 1)      # Panel 1: REAR ELEVATION (Looking forward towards windshield)
ax_side = fig.add_subplot(2, 2, 2)      # Panel 2: SIDE ELEVATION (Looking from right side)
ax_top = fig.add_subplot(2, 2, 3)       # Panel 3: TOP PLAN VIEW (Looking down from above)
ax_iso = fig.add_subplot(2, 2, 4, projection='3d') # Panel 4: 3D ISOMETRIC IN VEHICLE

for ax in [ax_rear, ax_side, ax_top, ax_iso]:
    ax.set_facecolor('#0f172a')

def draw_dim(ax, p1, p2, text, offset=(0, 0), text_pos=None, color='#38bdf8', va='center', ha='center', fontsize=9.5):
    ax.annotate('', xy=p1, xytext=p2,
                arrowprops=dict(arrowstyle='<->', color=color, lw=2.0))
    if text_pos is None:
        text_pos = ((p1[0] + p2[0]) / 2.0 + offset[0], (p1[1] + p2[1]) / 2.0 + offset[1])
    ax.text(text_pos[0], text_pos[1], text, color=color, weight='bold', fontsize=fontsize,
            ha=ha, va=va, bbox=dict(boxstyle='round,pad=0.25', facecolor='#070d19', edgecolor=color, lw=1.2))

# ==============================================================================
# 1. REAR ELEVATION VIEW (Looking forward towards windshield)
# ==============================================================================
ax_rear.set_title("1. REAR ELEVATION VIEW (Looking Forward Toward Windshield)", color='white', fontsize=13, weight='bold', pad=15)

# Box: X = -BOX_W to 0 (or centered). Let's put Right Edge at X = 0, so box spans from X = -BOX_W to 0!
# Connector is on the RIGHT (X = -CONN_W - 5 to -5 mm)
conn_right_x = -CONN_W - 6.0
conn_z = (BOX_H - 33.05) / 2.0 # Vertically centered on collar

# Box Body
ax_rear.add_patch(patches.Rectangle((-BOX_W, 0), BOX_W, BOX_H, facecolor='#334155', edgecolor='#64748b', lw=2))
# Top Lid
ax_rear.add_patch(patches.Rectangle((-BOX_W - 2, BOX_H), BOX_W + 4, LID_T, facecolor='#475569', edgecolor='#94a3b8', lw=2))

# Connector Mating Face / Cross Section (on the RIGHT)
ax_rear.add_patch(patches.Rectangle((conn_right_x, conn_z), CONN_W, 33.05, facecolor='#ea580c', edgecolor='#c2410c', lw=2))
# Cable coming straight back at the viewer
ax_rear.add_patch(patches.Circle((conn_right_x + CONN_W/2, conn_z + 33.05/2), CABLE_D/2, facecolor='#1e293b', edgecolor='#38bdf8', lw=2))
ax_rear.text(conn_right_x + CONN_W/2, conn_z + 33.05/2, "CABLE\nEXIT", color='white', weight='bold', fontsize=7.5, ha='center', va='center')

# C-Spine Rear View (Wraps right outer edge, open to left!)
bracket_w = CONN_W + 12.0
rect_sp_rear = patches.Rectangle((conn_right_x - 6.0, -4.0), bracket_w + WALL_T, BOX_H + LID_T + 8.0,
                                 facecolor='#0284c7', edgecolor='#38bdf8', lw=2.5, alpha=0.35)
ax_rear.add_patch(rect_sp_rear)

# Dimensions
draw_dim(ax_rear, (-BOX_W, BOX_H + 14), (0, BOX_H + 14), f"Box Width across car = {BOX_W:.2f} mm", offset=(0, 6))
draw_dim(ax_rear, (conn_right_x, -12), (conn_right_x + CONN_W, -12), f"Plug Width = {CONN_W:.1f} mm", offset=(0, -6), color='#fb923c')
draw_dim(ax_rear, (12, 0), (12, BOX_H), f"Height (E1) = {BOX_H:.2f} mm", offset=(8, 0), ha='left')

# Callouts
ax_rear.text(-BOX_W * 0.65, BOX_H * 0.5, "111.75mm Box Body Extends to the LEFT\n(Under Rear Seats / Chassis Mount)\n--> C-Spine stays open on this side!",
             color='#e2e8f0', fontsize=9.5, weight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#070d19', edgecolor='#94a3b8', lw=1.2))

ax_rear.text(conn_right_x + CONN_W/2, conn_z + 33.05 + 8, "ORANGE PLUG ON RIGHT",
             color='#fb923c', weight='bold', fontsize=9.5, ha='center',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#070d19', edgecolor='#ea580c', lw=1.2))

ax_rear.set_xlim(-BOX_W - 25, 35)
ax_rear.set_ylim(-25, BOX_H + 30)
ax_rear.set_aspect('equal')
ax_rear.axis('off')

# ==============================================================================
# 2. SIDE ELEVATION VIEW (Looking from Right Side across car to the left)
# ==============================================================================
ax_side.set_title("2. SIDE ELEVATION VIEW (Looking from Right Side: Front to Back)", color='white', fontsize=13, weight='bold', pad=15)

# Front (+Y = towards windshield, 120V outlet face): Y = BOX_D / 2
# Rear (-Y = towards rear of car, connector entrance): Y = -BOX_D / 2
front_y = BOX_D / 2.0
rear_y = -BOX_D / 2.0

# Box Body
ax_side.add_patch(patches.Rectangle((rear_y, 0), BOX_D, BOX_H, facecolor='#334155', edgecolor='#64748b', lw=2))
# 120V Outlet face on Front
ax_side.add_patch(patches.Rectangle((front_y, 4.0), 3.0, BOX_H - 8.0, facecolor='#64748b', edgecolor='#94a3b8', lw=1.5))
ax_side.text(front_y + 6.0, BOX_H / 2.0, "120V AC\nOUTLET\n(Faces\nWindshield)", color='#94a3b8', weight='bold', fontsize=8.5, va='center')

# Top Lid with 12.45mm REAR OVERHANG (extends past rear_y towards the rear)
ax_side.add_patch(patches.Rectangle((rear_y - LID_OH, BOX_H), BOX_D + LID_OH + 2.0, LID_T, facecolor='#475569', edgecolor='#94a3b8', lw=2))

# Orange Connector plugging in from the BACK (extends from rear_y rearward to rear_y - CONN_L)
ax_side.add_patch(patches.Rectangle((rear_y - CONN_L, conn_z), CONN_L, 33.05, facecolor='#ea580c', edgecolor='#c2410c', lw=2))
# Cable extending further rearward
ax_side.add_patch(patches.Rectangle((rear_y - CONN_L - 35.0, conn_z + (33.05 - CABLE_D)/2), 35.0, CABLE_D, facecolor='#1e293b', edgecolor='#475569', lw=1.5))

# Blue C-Spine Cross-Section (Hooks over rear overhang, traps plug shoulder at rear_y - CONN_L)
hook_lip_x = rear_y - LID_OH
spine_poly = [
    (front_y + WALL_T, BOX_H + LID_T + WALL_T),
    (hook_lip_x - WALL_T, BOX_H + LID_T + WALL_T),
    (hook_lip_x - WALL_T, BOX_H - 8.0), # Rear drop hook catching overhang
    (hook_lip_x, BOX_H - 8.0),
    (hook_lip_x, BOX_H + LID_T),
    (rear_y - CONN_L - 8.0, BOX_H + LID_T),
    # Drop down arm to plug shoulder
    (rear_y - CONN_L - 8.0, conn_z - 8.0),
    (rear_y - CONN_L - 2.0, conn_z - 8.0),
    (rear_y - CONN_L - 2.0, BOX_H + LID_T),
    (front_y + WALL_T, BOX_H + LID_T)
]
ax_side.add_patch(patches.Polygon(spine_poly, closed=True, facecolor='#0284c7', edgecolor='#38bdf8', lw=2.5, alpha=0.85))

# Green Keeper sliding under/behind shoulder
ax_side.add_patch(patches.Rectangle((rear_y - CONN_L - 6.0, conn_z - 4.0), 6.0, 33.05 + 8.0, facecolor='#22c55e', edgecolor='#4ade80', lw=2))

# Dimensions
draw_dim(ax_side, (rear_y, -14), (front_y, -14), f"Box Depth (E2) = {BOX_D:.2f} mm", offset=(0, -8))
draw_dim(ax_side, (hook_lip_x, BOX_H + LID_T + 14), (rear_y, BOX_H + LID_T + 14), f"Lid Overhang (E3) = {LID_OH:.2f} mm", offset=(0, 6), color='#4ade80')
draw_dim(ax_side, (rear_y - CONN_L, -14), (rear_y, -14), f"Rigid Plug Body = {CONN_L:.1f} mm", offset=(0, -8), color='#fb923c')

# Hook annotation
ax_side.annotate('POSITIVE MECHANICAL HOOK:\nCatches over 12.45mm lid overhang!',
                xy=(hook_lip_x - WALL_T/2, BOX_H - 4.0), xytext=(hook_lip_x - 18, BOX_H + 16),
                arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=2),
                color='#38bdf8', weight='bold', fontsize=8.5, ha='right',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#070d19', edgecolor='#38bdf8', lw=1.2))

# Pull force arrow (pulling rearward towards back of car)
ax_side.annotate('', xy=(rear_y - CONN_L - 45, conn_z + 16), xytext=(rear_y - CONN_L - 20, conn_z + 16),
                arrowprops=dict(arrowstyle='->', color='#ef4444', lw=3.0))
ax_side.text(rear_y - CONN_L - 32, conn_z + 24, "Cable Pull Force\n(Toward Rear of Car)", color='#ef4444', weight='bold', fontsize=8.5, ha='center')

ax_side.set_xlim(rear_y - CONN_L - 55, front_y + 40)
ax_side.set_ylim(-28, BOX_H + 35)
ax_side.set_aspect('equal')
ax_side.axis('off')

# ==============================================================================
# 3. TOP PLAN VIEW (Looking down from above the roof)
# ==============================================================================
ax_top.set_title("3. TOP PLAN VIEW (Looking Down from Above)", color='white', fontsize=13, weight='bold', pad=15)

# Box Lid footprint: X = -BOX_W to 0, Y = rear_y - LID_OH to front_y
ax_top.add_patch(patches.Rectangle((-BOX_W, rear_y), BOX_W, BOX_D, facecolor='#334155', edgecolor='#64748b', lw=2))
ax_top.add_patch(patches.Rectangle((-BOX_W, rear_y - LID_OH), BOX_W, LID_OH, facecolor='#475569', edgecolor='#94a3b8', lw=1.5, ls='--', alpha=0.6))
ax_top.text(-BOX_W/2, rear_y - LID_OH/2, "12.45mm Overhanging Lip at Rear", color='#94a3b8', fontsize=8.5, ha='center', va='center')

# 120V Outlet on front face
ax_top.text(-BOX_W/2, front_y - 8, "FRONT OF BOX (120V Wall Plug Facing Windshield)", color='#38bdf8', weight='bold', fontsize=9.5, ha='center')

# Orange Connector plugged in at the rear right
ax_top.add_patch(patches.Rectangle((conn_right_x, rear_y - CONN_L), CONN_W, CONN_L, facecolor='#ea580c', edgecolor='#c2410c', lw=2))
ax_top.add_patch(patches.Rectangle((conn_right_x + (CONN_W - CABLE_D)/2, rear_y - CONN_L - 35.0), CABLE_D, 35.0, facecolor='#1e293b', edgecolor='#475569', lw=1.5))

# C-Spine outline on top: Covers right end (conn_right_x - 6 to 0)
ax_top.add_patch(patches.Rectangle((conn_right_x - 6.0, rear_y - LID_OH - WALL_T), bracket_w + WALL_T, BOX_D + LID_OH + 2*WALL_T,
                                   facecolor='#0284c7', edgecolor='#38bdf8', lw=2.5, alpha=0.35))

# Green Keeper sliding in from left
ax_top.annotate('', xy=(conn_right_x - 2.0, rear_y - CONN_L), xytext=(conn_right_x - 28.0, rear_y - CONN_L),
                arrowprops=dict(arrowstyle='->', color='#22c55e', lw=3.0))
ax_top.text(conn_right_x - 30.0, rear_y - CONN_L, "Green Keeper\nSlides in from Left",
            color='#4ade80', weight='bold', fontsize=8.5, ha='right', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#070d19', edgecolor='#22c55e', lw=1.2))

# Windshield direction arrow
ax_top.annotate('', xy=(-BOX_W/2, front_y + 20), xytext=(-BOX_W/2, front_y + 4),
                arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=3.5))
ax_top.text(-BOX_W/2, front_y + 24, "TOWARD WINDSHIELD", color='#38bdf8', weight='bold', fontsize=10, ha='center')

draw_dim(ax_top, (-BOX_W, rear_y - LID_OH - 14), (0, rear_y - LID_OH - 14), f"Box Width = {BOX_W:.2f} mm", offset=(0, -6))
draw_dim(ax_top, (12, rear_y), (12, front_y), f"Depth = {BOX_D:.2f} mm", offset=(8, 0), ha='left')

ax_top.set_xlim(-BOX_W - 45, 35)
ax_top.set_ylim(rear_y - CONN_L - 45, front_y + 35)
ax_top.set_aspect('equal')
ax_top.axis('off')

# ==============================================================================
# 4. ISOMETRIC 3D VIEW (Vehicle Context)
# ==============================================================================
ax_iso.set_title("4. ISOMETRIC 3D VIEW (True In-Car Perspective)", color='white', fontsize=13, weight='bold', pad=15)

# Box + Lid
m_box = trimesh.creation.box(extents=[BOX_W, BOX_D, BOX_H])
m_box.apply_translation([-BOX_W/2, 0, BOX_H/2])

m_lid = trimesh.creation.box(extents=[BOX_W + 4, BOX_D + LID_OH + 2, LID_T])
m_lid.apply_translation([-BOX_W/2, -LID_OH/2, BOX_H + LID_T/2])

# Plug on Right, extending rearward
m_conn = trimesh.creation.box(extents=[CONN_W, CONN_L, 33.05])
m_conn.apply_translation([conn_right_x + CONN_W/2, rear_y - CONN_L/2, conn_z + 33.05/2])

# Exploded C-Spine on the Right
m_sp_top = trimesh.creation.box(extents=[bracket_w + WALL_T, BOX_D + LID_OH + 2*WALL_T + 4, WALL_T])
m_sp_top.apply_translation([conn_right_x + CONN_W/2, -LID_OH/2, BOX_H + LID_T + WALL_T/2 + 10.0])

m_sp_rear = trimesh.creation.box(extents=[bracket_w + WALL_T, WALL_T, 14.0])
m_sp_rear.apply_translation([conn_right_x + CONN_W/2, rear_y - LID_OH - WALL_T/2, BOX_H - 2.0 + 10.0])

m_sp_right = trimesh.creation.box(extents=[WALL_T, BOX_D + LID_OH + 2*WALL_T + 4, BOX_H + LID_T + 12.0])
m_sp_right.apply_translation([WALL_T/2, -LID_OH/2, (BOX_H + LID_T)/2 + 10.0])

m_sp_arm = trimesh.creation.box(extents=[bracket_w + WALL_T, WALL_T, BOX_H + 18.0])
m_sp_arm.apply_translation([conn_right_x + CONN_W/2, rear_y - CONN_L - WALL_T/2, conn_z + 10.0])

m_spine = trimesh.util.concatenate([m_sp_top, m_sp_rear, m_sp_right, m_sp_arm])

# Exploded Keeper (pulled left)
m_keeper = trimesh.creation.box(extents=[CONN_W + 6, 6.0, 33.05 + 6.0])
m_keeper.apply_translation([conn_right_x + CONN_W/2 - 28.0, rear_y - CONN_L - 3.0, conn_z + 33.05/2])

def plot_solid(ax, m, color, alpha=0.85, edge_color='#ffffff'):
    v = m.vertices
    f = m.faces
    pc = Poly3DCollection(v[f], facecolors=color, alpha=alpha)
    pc.set_edgecolor(edge_color)
    pc.set_linewidth(0.4)
    ax.add_collection3d(pc)

plot_solid(ax_iso, m_box, color='#475569', alpha=0.45, edge_color='#64748b')
plot_solid(ax_iso, m_lid, color='#334155', alpha=0.60, edge_color='#94a3b8')
plot_solid(ax_iso, m_conn, color='#ea580c', alpha=0.90, edge_color='#c2410c')
plot_solid(ax_iso, m_spine, color='#0284c7', alpha=0.92, edge_color='#38bdf8')
plot_solid(ax_iso, m_keeper, color='#22c55e', alpha=0.95, edge_color='#4ade80')

ax_iso.view_init(elev=26, azim=-40)
ax_iso.set_xlim(-BOX_W - 20, 25)
ax_iso.set_ylim(rear_y - CONN_L - 30, front_y + 25)
ax_iso.set_zlim(-15, BOX_H + 30)
ax_iso.axis('off')

card_text = (
    "VEHICLE ORIENTATION SUMMARY:\n"
    "• FRONT (+Y): 120V household socket facing windshield\n"
    "• BACK (-Y): Orange connector enters from rear\n"
    "• RIGHT (+X): Orange connector is on the right side\n"
    "• LEFT (-X): 111.75mm box body extends across vehicle\n"
    "• TOP (+Z): Blue bracket hooks over rear 12.45mm overhang\n"
    "• GREEN: Keeper slides in from left to lock plug shoulder"
)
ax_iso.text2D(0.04, 0.04, card_text, transform=ax_iso.transAxes, color='#e2e8f0', fontsize=8.5, weight='bold',
              bbox=dict(boxstyle='round,pad=0.45', facecolor='#070d19', edgecolor='#38bdf8', lw=1.5))

out_file = os.path.join(artifact_dir, "vehicle_true_orientation.png")
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "vehicle_true_orientation.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved vehicle true orientation blueprint to:", out_file)
