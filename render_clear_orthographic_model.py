"""
render_clear_orthographic_model.py
Renders a professional 4-panel engineering drawing with ZERO text overlap:
- Panel 1: Front Elevation (Looking directly at Front Face)
- Panel 2: Side Elevation (Looking at Left Side: Depth & Hook)
- Panel 3: Bottom Plan View (Looking up at Connector Seating Face)
- Panel 4: Isometric 3D View (Clean Exploded Solid Perspective)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

# Verified Dimensions
BOX_W = 111.75   # X: Long width of black box
BOX_D = 48.15    # Y: Front-to-back depth of box
BOX_H = 42.67    # Z: Height from connector face to top lid
LID_OH = 12.45   # Y: Lid overhang at the rear
LID_T = 4.58     # Z: Lid thickness

CONN_W = 36.10   # X: Orange connector body width
CONN_D = 20.80   # Y: Orange connector body depth
CONN_H = 54.60   # Z: Rigid connector body length (downward)
CABLE_D = 17.00  # Diameter of rubber cable
WALL_T = 4.00    # Bracket wall thickness

fig = plt.figure(figsize=(26, 18), dpi=180)
fig.patch.set_facecolor('#070d19')

ax_front = fig.add_subplot(2, 2, 1)
ax_front.set_facecolor('#0f172a')

ax_side = fig.add_subplot(2, 2, 2)
ax_side.set_facecolor('#0f172a')

ax_bottom = fig.add_subplot(2, 2, 3)
ax_bottom.set_facecolor('#0f172a')

ax_iso = fig.add_subplot(2, 2, 4, projection='3d')
ax_iso.set_facecolor('#0f172a')

def draw_dim(ax, p1, p2, text, offset=(0, 0), text_pos=None, color='#38bdf8', va='center', ha='center', fontsize=9.5):
    ax.annotate('', xy=p1, xytext=p2,
                arrowprops=dict(arrowstyle='<->', color=color, lw=2.0))
    if text_pos is None:
        text_pos = ((p1[0] + p2[0]) / 2.0 + offset[0], (p1[1] + p2[1]) / 2.0 + offset[1])
    ax.text(text_pos[0], text_pos[1], text, color=color, weight='bold', fontsize=fontsize,
            ha=ha, va=va, bbox=dict(boxstyle='round,pad=0.25', facecolor='#070d19', edgecolor=color, lw=1.2))

# ==============================================================================
# 1. FRONT ELEVATION
# ==============================================================================
ax_front.set_title("1. FRONT ELEVATION VIEW (Looking at Front Face)", color='white', fontsize=13, weight='bold', pad=15)

# Black Box Body
ax_front.add_patch(patches.Rectangle((0, 0), BOX_W, BOX_H, facecolor='#334155', edgecolor='#64748b', lw=2))
# Lid on top
ax_front.add_patch(patches.Rectangle((-2, BOX_H), BOX_W + 4, LID_T, facecolor='#475569', edgecolor='#94a3b8', lw=2))

# Connector & Cable
conn_x = 6.0
ax_front.add_patch(patches.Rectangle((conn_x, -CONN_H), CONN_W, CONN_H, facecolor='#ea580c', edgecolor='#c2410c', lw=2))
cable_x = conn_x + (CONN_W - CABLE_D) / 2.0
ax_front.add_patch(patches.Rectangle((cable_x, -CONN_H - 30), CABLE_D, 30, facecolor='#1e293b', edgecolor='#475569', lw=1.5))

# C-Spine Front Drop Wall (Blue)
bracket_w = CONN_W + 10.0 # 46.1mm
rect_sp_f = patches.Rectangle((-WALL_T, -CONN_H - 8), bracket_w + WALL_T, CONN_H + BOX_H + LID_T + 12,
                              facecolor='#0284c7', edgecolor='#38bdf8', lw=2.5, alpha=0.35)
ax_front.add_patch(rect_sp_f)

# Dimensions
draw_dim(ax_front, (0, BOX_H + 14), (BOX_W, BOX_H + 14), f"Box Width = {BOX_W:.2f} mm", offset=(0, 6))
draw_dim(ax_front, (conn_x, -CONN_H - 14), (conn_x + CONN_W, -CONN_H - 14), f"Plug Width = {CONN_W:.1f} mm", offset=(0, -6), color='#fb923c')
draw_dim(ax_front, (BOX_W + 12, 0), (BOX_W + 12, BOX_H), f"Height (E1) = {BOX_H:.2f} mm", offset=(8, 0), ha='left')
draw_dim(ax_front, (-18, -CONN_H), (-18, 0), f"Plug Body = {CONN_H:.1f} mm", offset=(-8, 0), color='#fb923c', ha='right')

ax_front.text(BOX_W * 0.65, BOX_H * 0.5, "Solid Box Body Continues to Right\n(Chassis Plate Mounts Here)\n--> Bracket leaves this side OPEN",
              color='#e2e8f0', fontsize=9.5, weight='bold', ha='center',
              bbox=dict(boxstyle='round,pad=0.4', facecolor='#070d19', edgecolor='#94a3b8', lw=1.2))

ax_front.set_xlim(-35, BOX_W + 40)
ax_front.set_ylim(-CONN_H - 50, BOX_H + 30)
ax_front.set_aspect('equal')
ax_front.axis('off')

# ==============================================================================
# 2. SIDE ELEVATION
# ==============================================================================
ax_side.set_title("2. SIDE ELEVATION VIEW (Looking at Left End: Depth & Hook)", color='white', fontsize=13, weight='bold', pad=15)

# Box Depth: Y = 0 (Front) to -BOX_D (Rear)
ax_side.add_patch(patches.Rectangle((-BOX_D, 0), BOX_D, BOX_H, facecolor='#334155', edgecolor='#64748b', lw=2))

# Lid with Rear Overhang
lid_rear_y = -BOX_D - LID_OH
ax_side.add_patch(patches.Rectangle((lid_rear_y, BOX_H), BOX_D + LID_OH + 2, LID_T, facecolor='#475569', edgecolor='#94a3b8', lw=2))

# Connector
conn_rear_y = (-BOX_D / 2.0) - (CONN_D / 2.0)
ax_side.add_patch(patches.Rectangle((conn_rear_y, -CONN_H), CONN_D, CONN_H, facecolor='#ea580c', edgecolor='#c2410c', lw=2))

# C-Spine Frame Cross Section
hook_poly = [
    (lid_rear_y - WALL_T, BOX_H + LID_T + WALL_T),
    (WALL_T + 2, BOX_H + LID_T + WALL_T),
    (WALL_T + 2, -CONN_H - 10),
    (2, -CONN_H - 10),
    (2, BOX_H + LID_T),
    (lid_rear_y, BOX_H + LID_T),
    (lid_rear_y, BOX_H - 8),
    (lid_rear_y - WALL_T, BOX_H - 8),
]
ax_side.add_patch(patches.Polygon(hook_poly, closed=True, facecolor='#0284c7', edgecolor='#38bdf8', lw=2.5, alpha=0.9))

# Keeper (Green) under plug shoulder
ax_side.add_patch(patches.Rectangle((conn_rear_y - 2, -CONN_H - 6), CONN_D + 4, 6, facecolor='#22c55e', edgecolor='#4ade80', lw=2))

# Dimensions placed completely outside geometry
draw_dim(ax_side, (-BOX_D, -14), (0, -14), f"Box Depth (E2) = {BOX_D:.2f} mm", offset=(0, -8))
draw_dim(ax_side, (lid_rear_y, BOX_H + LID_T + 14), (-BOX_D, BOX_H + LID_T + 14), f"Lid Overhang (E3) = {LID_OH:.2f} mm", offset=(0, 6), color='#4ade80')
draw_dim(ax_side, (14, 0), (14, BOX_H), f"Height (E1) = {BOX_H:.2f} mm", offset=(8, 0), ha='left')

# Clear hook callout on left margin
ax_side.annotate('POSITIVE MECHANICAL HOOK:\nCatches over 12.45mm lid overhang!\nPhysically cannot pull downward.',
                xy=(lid_rear_y - WALL_T/2, BOX_H - 4), xytext=(lid_rear_y - 12, BOX_H - 24),
                arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=2),
                color='#38bdf8', weight='bold', fontsize=9.0, ha='right',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#070d19', edgecolor='#38bdf8', lw=1.2))

# Pull force arrow
ax_side.annotate('', xy=(conn_rear_y + CONN_D/2, -CONN_H - 35), xytext=(conn_rear_y + CONN_D/2, -CONN_H - 15),
                arrowprops=dict(arrowstyle='->', color='#ef4444', lw=3.0))
ax_side.text(conn_rear_y + CONN_D/2 + 6, -CONN_H - 25, "Cable Pull Force", color='#ef4444', weight='bold', fontsize=9.0)

ax_side.set_xlim(-BOX_D - LID_OH - 38, 30)
ax_side.set_ylim(-CONN_H - 50, BOX_H + 30)
ax_side.set_aspect('equal')
ax_side.axis('off')

# ==============================================================================
# 3. BOTTOM VIEW
# ==============================================================================
ax_bottom.set_title("3. BOTTOM VIEW (Looking up at Seating Face)", color='white', fontsize=13, weight='bold', pad=15)

# Box Base
ax_bottom.add_patch(patches.Rectangle((0, -BOX_D), BOX_W, BOX_D, facecolor='#334155', edgecolor='#64748b', lw=2))
# Lid Overhang dashed at top (rear)
ax_bottom.add_patch(patches.Rectangle((0, -BOX_D - LID_OH), BOX_W, LID_OH, facecolor='#475569', edgecolor='#94a3b8', lw=1.5, ls='--', alpha=0.5))

# Plug
ax_bottom.add_patch(patches.Rectangle((conn_x, conn_rear_y), CONN_W, CONN_D, facecolor='#ea580c', edgecolor='#c2410c', lw=2.5))

# C-Spine Walls
ax_bottom.add_patch(patches.Rectangle((-WALL_T, -BOX_D - LID_OH - WALL_T), WALL_T, BOX_D + LID_OH + 2*WALL_T + 2, facecolor='#0284c7', edgecolor='#38bdf8', lw=2, alpha=0.8))
ax_bottom.add_patch(patches.Rectangle((-WALL_T, 2), bracket_w + WALL_T, WALL_T, facecolor='#0284c7', edgecolor='#38bdf8', lw=2, alpha=0.8))
ax_bottom.add_patch(patches.Rectangle((-WALL_T, -BOX_D - LID_OH - WALL_T), bracket_w + WALL_T, WALL_T, facecolor='#0284c7', edgecolor='#38bdf8', lw=2, alpha=0.8))

# Green Keeper Slide In arrow
ax_bottom.annotate('', xy=(conn_x + CONN_W + 2, conn_rear_y + CONN_D/2), xytext=(conn_x + CONN_W + 30, conn_rear_y + CONN_D/2),
                   arrowprops=dict(arrowstyle='->', color='#22c55e', lw=3.0))
ax_bottom.text(conn_x + CONN_W + 33, conn_rear_y + CONN_D/2, "Green Keeper Slides In\nFrom Open Right Side",
               color='#4ade80', weight='bold', fontsize=9.0, va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#070d19', edgecolor='#22c55e', lw=1.2))

# Dimensions placed cleanly in margins
draw_dim(ax_bottom, (0, 14), (BOX_W, 14), f"Box Width = {BOX_W:.2f} mm", offset=(0, 6))
draw_dim(ax_bottom, (-16, -BOX_D), (-16, 0), f"Depth = {BOX_D:.2f} mm", offset=(-8, 0), ha='right')
draw_dim(ax_bottom, (-16, -BOX_D - LID_OH), (-16, -BOX_D), f"Overhang = {LID_OH:.2f} mm", offset=(-8, 0), color='#4ade80', ha='right')

ax_bottom.set_xlim(-35, BOX_W + 40)
ax_bottom.set_ylim(-BOX_D - LID_OH - 25, 30)
ax_bottom.set_aspect('equal')
ax_bottom.axis('off')

# ==============================================================================
# 4. ISOMETRIC 3D VIEW (Exploded Assembly, ZERO text overlap)
# ==============================================================================
ax_iso.set_title("4. ISOMETRIC 3D VIEW (Exploded Assembly Perspective)", color='white', fontsize=13, weight='bold', pad=15)

# Box + Lid Meshes
m_box = trimesh.creation.box(extents=[BOX_W, BOX_D, BOX_H])
m_box.apply_translation([BOX_W/2, -BOX_D/2, BOX_H/2])

m_lid = trimesh.creation.box(extents=[BOX_W + 4, BOX_D + LID_OH + 2, LID_T])
m_lid.apply_translation([BOX_W/2, -BOX_D/2 - LID_OH/2, BOX_H + LID_T/2])

# Plug Mesh
m_conn = trimesh.creation.box(extents=[CONN_W, CONN_D, CONN_H])
m_conn.apply_translation([conn_x + CONN_W/2, conn_rear_y + CONN_D/2, -CONN_H/2])

# Exploded C-Spine (lifted slightly for clarity)
top_br = trimesh.creation.box(extents=[bracket_w + WALL_T, BOX_D + LID_OH + 2*WALL_T + 4, WALL_T])
top_br.apply_translation([bracket_w/2 - WALL_T/2, -BOX_D/2 - LID_OH/2, BOX_H + LID_T + WALL_T/2 + 12.0])

rear_hk = trimesh.creation.box(extents=[bracket_w + WALL_T, WALL_T, 14.0])
rear_hk.apply_translation([bracket_w/2 - WALL_T/2, -BOX_D - LID_OH - WALL_T/2, BOX_H - 2.0 + 12.0])

front_wall = trimesh.creation.box(extents=[bracket_w + WALL_T, WALL_T, BOX_H + CONN_H + LID_T + 6])
front_wall.apply_translation([bracket_w/2 - WALL_T/2, 2.0 + WALL_T/2, (BOX_H + LID_T) - (BOX_H + CONN_H + LID_T + 6)/2 + 12.0])

left_wall = trimesh.creation.box(extents=[WALL_T, BOX_D + LID_OH + 2*WALL_T + 4, BOX_H + CONN_H + LID_T + 6])
left_wall.apply_translation([-WALL_T/2, -BOX_D/2 - LID_OH/2, (BOX_H + LID_T) - (BOX_H + CONN_H + LID_T + 6)/2 + 12.0])

m_bracket = trimesh.util.concatenate([top_br, rear_hk, front_wall, left_wall])

# Exploded Keeper (pulled out to the right)
m_keeper = trimesh.creation.box(extents=[CONN_W + 8, CONN_D + 4, 7.0])
m_keeper.apply_translation([conn_x + CONN_W/2 + 28.0, conn_rear_y + CONN_D/2, -CONN_H - 4.0])

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
plot_solid(ax_iso, m_bracket, color='#0284c7', alpha=0.92, edge_color='#38bdf8')
plot_solid(ax_iso, m_keeper, color='#22c55e', alpha=0.95, edge_color='#4ade80')

ax_iso.view_init(elev=24, azim=-50)
ax_iso.set_xlim(-25, BOX_W + 30)
ax_iso.set_ylim(-BOX_D - LID_OH - 25, 25)
ax_iso.set_zlim(-CONN_H - 25, BOX_H + 35)
ax_iso.axis('off')

# Clean card at bottom with zero model overlap
card_text = (
    "EXPLODED ASSEMBLY KEY:\n"
    "• GREY: Outlet Box (111.75 mm wide x 48.15 mm deep)\n"
    "• ORANGE: OEM Plug at corner (36.1 mm wide)\n"
    "• BLUE: C-Spine Frame (Drops over 12.45mm rear hook)\n"
    "• GREEN: Keeper (Slides in under plug shoulder)\n"
    "✓ Right side left OPEN to clear 111.75mm body"
)
ax_iso.text2D(0.04, 0.04, card_text, transform=ax_iso.transAxes, color='#e2e8f0', fontsize=9.0, weight='bold',
              bbox=dict(boxstyle='round,pad=0.45', facecolor='#070d19', edgecolor='#38bdf8', lw=1.5))

out_blueprint = os.path.join(artifact_dir, "clear_orthographic_model.png")
plt.savefig(out_blueprint, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "clear_orthographic_model.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved clear orthographic model to:", out_blueprint)
