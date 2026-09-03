"""
visualize_true_box_orientation.py
Visualizes the true 3D module with:
- Width = 111.75 mm (Long axis)
- Depth = 48.15 mm (Front to Back)
- Height = 42.67 mm (Connector face to Lid top)
- Lid overhang = 12.45 mm at the rear
Shows how the bracket wraps around Front-to-Back (48.15mm) and Left end, clearing the 111.75mm body to the right.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

fig = plt.figure(figsize=(24, 11), dpi=180)
plt.subplots_adjust(left=0.03, right=0.97, top=0.92, bottom=0.05, wspace=0.10)
fig.patch.set_facecolor('#070d19')

# BOX DIMENSIONS
L_X = 111.75 # Long axis (Width in vehicle)
L_Y = 48.15  # Depth (Front-to-Back in vehicle)
L_Z = 42.67  # Height (Connector face to Lid top)
LID_OH = 12.45 # Rear overhang
LID_T = 4.58  # Lid thickness

def setup_ax(ax, title, elev=22, azim=-55):
    ax.set_facecolor('#070d19')
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')
    ax.set_title(title, color='white', fontsize=13, weight='bold', pad=12)

# VIEW 1: 3D True Box & Plug Position
ax1 = fig.add_subplot(1, 2, 1, projection='3d')

# 1. Black Box Body (111.75 x 48.15 x 42.67 mm)
box = trimesh.creation.box(extents=[L_X, L_Y, L_Z])
box.apply_translation([L_X / 2.0, -L_Y / 2.0, L_Z / 2.0])

# 2. Lid with 12.45mm Rear Overhang
lid = trimesh.creation.box(extents=[L_X, L_Y + LID_OH, LID_T])
lid.apply_translation([L_X / 2.0, (-L_Y / 2.0) - LID_OH / 2.0, L_Z + LID_T / 2.0])

# 3. Orange Connector (plugged into bottom left corner: X ~ 5 to 41 mm, Y ~ -24 mm)
conn_box = trimesh.creation.box(extents=[36.1, 20.8, 54.6])
conn_box.apply_translation([22.0, -24.0, -54.6 / 2.0])

def plot_mesh(ax, m, color, alpha=0.8, edge_color=None):
    v = m.vertices
    f = m.faces
    pc = Poly3DCollection(v[f], facecolors=color, alpha=alpha)
    if edge_color:
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.2)
    ax.add_collection3d(pc)

plot_mesh(ax1, box, color='#334155', alpha=0.7, edge_color='#64748b')
plot_mesh(ax1, lid, color='#1e293b', alpha=0.9, edge_color='#475569')
plot_mesh(ax1, conn_box, color='#ea580c', alpha=0.9, edge_color='#c2410c')

ax1.set_xlim(-20, 130)
ax1.set_ylim(-75, 25)
ax1.set_zlim(-60, 60)
setup_ax(ax1, "TRUE PHYSICAL GEOMETRY (As Installed in Vehicle)")

ax1.text2D(0.02, 0.94, "True Box Dimensions Confirmed:", transform=ax1.transAxes, color='#38bdf8', weight='bold', fontsize=11)
ax1.text2D(0.02, 0.87, f"• Long Axis (Width in car): {L_X} mm", transform=ax1.transAxes, color='#facc15', weight='bold', fontsize=10)
ax1.text2D(0.02, 0.81, f"• Front-to-Back Depth (E2): {L_Y} mm", transform=ax1.transAxes, color='#e2e8f0', fontsize=10)
ax1.text2D(0.02, 0.75, f"• Vertical Height (E1): {L_Z} mm", transform=ax1.transAxes, color='#e2e8f0', fontsize=10)
ax1.text2D(0.02, 0.69, f"• Rear Lid Overhang (E3): {LID_OH} mm wide x {LID_T} mm tall", transform=ax1.transAxes, color='#4ade80', weight='bold', fontsize=10)
ax1.text2D(0.02, 0.61, "Notice: Orange connector is located at the LEFT corner.\nThe solid 111.75mm box extends to the RIGHT.", transform=ax1.transAxes, color='#cbd5e1', fontsize=9.5)

# VIEW 2: How the Front-to-Back Bracket Wraps Around
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
plot_mesh(ax2, box, color='#334155', alpha=0.4, edge_color='#64748b')
plot_mesh(ax2, lid, color='#1e293b', alpha=0.5, edge_color='#475569')
plot_mesh(ax2, conn_box, color='#ea580c', alpha=0.85, edge_color='#c2410c')

# Design the Front-to-Back C-Clamp that only spans the connector width (~46mm) at the left corner!
# 1. Top Hook plate over lid
top_hook = trimesh.creation.box(extents=[46.0, L_Y + LID_OH + 6.0, 4.0])
top_hook.apply_translation([23.0, (-L_Y / 2.0) - LID_OH / 2.0, L_Z + LID_T + 2.0])

# 2. Rear Drop Hook (catches the 12.45mm overhang)
rear_lip = trimesh.creation.box(extents=[46.0, 4.0, LID_T + 6.0])
rear_lip.apply_translation([23.0, -L_Y - LID_OH - 1.0, L_Z - 2.0])

# 3. Front Drop Leg (drops down in FRONT of connector, where it's 100% open)
front_leg = trimesh.creation.box(extents=[46.0, 4.0, L_Z + 58.0])
front_leg.apply_translation([23.0, 2.0, (L_Z + LID_T) - (L_Z + 58.0)/2.0])

# 4. Left Outer Flank (wraps left outer end of box)
left_leg = trimesh.creation.box(extents=[4.0, L_Y + LID_OH + 6.0, L_Z + 20.0])
left_leg.apply_translation([-2.0, (-L_Y / 2.0) - LID_OH / 2.0, L_Z / 2.0])

# 5. Bottom Keeper Bar (sliding in under connector shoulder)
keeper = trimesh.creation.box(extents=[48.0, 18.0, 6.0])
keeper.apply_translation([23.0, -24.0, -56.0])

bracket = trimesh.util.concatenate([top_hook, rear_lip, front_leg, left_leg])
plot_mesh(ax2, bracket, color='#0284c7', alpha=0.90, edge_color='#38bdf8')
plot_mesh(ax2, keeper, color='#22c55e', alpha=0.95, edge_color='#4ade80')

ax2.set_xlim(-20, 130)
ax2.set_ylim(-75, 25)
ax2.set_zlim(-65, 60)
setup_ax(ax2, "SOLUTION: Front-to-Back C-Spine (Clears the 111.75mm Body)")

ax2.text2D(0.02, 0.94, "How This Eliminates the Conflict:", transform=ax2.transAxes, color='white', weight='bold', fontsize=11)
ax2.text2D(0.02, 0.87, "1. Front-to-Back Span: Hooks over the 48.15mm depth & 12.45mm lid overhang.", transform=ax2.transAxes, color='#38bdf8', fontsize=10)
ax2.text2D(0.02, 0.81, "2. Left End Flank: Wraps cleanly around the outer left edge of the box.", transform=ax2.transAxes, color='#e2e8f0', fontsize=10)
ax2.text2D(0.02, 0.75, "3. Right Side: Left OPEN! Does NOT interfere with the 111.75mm body or silver plate.", transform=ax2.transAxes, color='#4ade80', weight='bold', fontsize=10)
ax2.text2D(0.02, 0.69, "4. Bottom Keeper: Slides in from the open side to trap the orange shoulder.", transform=ax2.transAxes, color='#facc15', weight='bold', fontsize=10)

out_file = os.path.join(artifact_dir, "true_box_orientation.png")
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "true_box_orientation.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved true orientation render to:", out_file)
