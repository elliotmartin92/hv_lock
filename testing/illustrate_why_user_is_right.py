"""
illustrate_why_user_is_right.py
Visualizes why the user is 100% RIGHT:
- Shows the kinematic vector analysis of pulling rearward
- Demonstrates why a rear hook simply slides off backward into empty space
- Illustrates the 2 real mechanical solutions:
  A) FRONT-HOOK WRAP: Hooking over the FRONT face (120V face) so rear pull pulls TIGHT against the box.
  B) OPTION 2 COLLAR BRIDLE: Gripping the 4.7mm collar neck directly at the backplate.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 12), dpi=180)
plt.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.08, wspace=0.12)
fig.patch.set_facecolor('#070d19')

for ax in [ax1, ax2]:
    ax.set_facecolor('#0f172a')

# ------------------------------------------------------------------------------
# PANEL 1: WHY THE USER IS 100% RIGHT (THE REAR HOOK FAILS)
# ------------------------------------------------------------------------------
ax1.set_title("PANEL 1: WHY YOU ARE 100% RIGHT (The Rear Hook Fails)", color='#ef4444', fontsize=13, weight='bold', pad=15)

# Box (Rear face at X = 0, Front face at X = 48.15)
ax1.fill([0, 48.15, 48.15, 0], [0, 0, 42.67, 42.67], color='#334155', edgecolor='#64748b', lw=2, label='Outlet Box Body')
ax1.fill([-12.45, 48.15, 48.15, -12.45], [42.67, 42.67, 47.25, 47.25], color='#475569', edgecolor='#94a3b8', lw=2, label='Top Lid (12.45mm Rear Overhang)')

# 120V Front Socket
ax1.fill([48.15, 51.0, 51.0, 48.15], [5, 5, 37, 37], color='#64748b', label='120V Socket (Faces Windshield)')
ax1.text(55, 21, "FRONT\n(Faces\nWindshield)", color='#94a3b8', weight='bold', fontsize=9, va='center')

# Orange Plug (Rear)
ax1.fill([-54.6, 0, 0, -54.6], [8, 8, 34, 34], color='#ea580c', alpha=0.9, label='Orange Connector Body')
ax1.fill([-85, -54.6, -54.6, -85], [16, 16, 26, 26], color='#1e293b', label='Cable Boot')

# Failed Rear Hook Bracket
ax1.plot([-12.45, -12.45, -12.45, 20, 20, -54.6, -54.6],
         [32, 47.25 + 4, 47.25 + 4, 47.25 + 4, 47.25 + 4, 47.25 + 4, 5],
         color='#38bdf8', lw=3.5, ls='--', label='Bracket with Rear Hook')

# Rear Hook Lip
ax1.fill([-16.45, -12.45, -12.45, -16.45], [32, 32, 51.25, 51.25], color='#38bdf8', alpha=0.4)

# Pull Force Vector
ax1.annotate('', xy=(-95, 21), xytext=(-65, 21), arrowprops=dict(arrowstyle='->', color='#ef4444', lw=4))
ax1.text(-80, 25, "Cable Pull Force\n(Toward Rear of Car)", color='#ef4444', weight='bold', fontsize=10, ha='center')

# Bracket Motion Vector
ax1.annotate('', xy=(-32, 52), xytext=(-16, 52), arrowprops=dict(arrowstyle='->', color='#ef4444', lw=3.5, ls=':'))
ax1.text(-24, 58, "Bracket slides BACKWARDS\nright off the lid!", color='#ef4444', weight='bold', fontsize=9.5, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#070d19', edgecolor='#ef4444', lw=1.5))

ax1.annotate('FATAL FLAW IDENTIFIED:\nThe hook drops behind the box.\nWhen cable pulls rearward (away from box),\nit pulls the hook AWAY into empty air!',
             xy=(-14.45, 38), xytext=(-75, 50),
             arrowprops=dict(arrowstyle='->', color='#ef4444', lw=2),
             color='#fca5a5', weight='bold', fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#070d19', edgecolor='#ef4444', lw=1.5))

ax1.set_xlim(-105, 75)
ax1.set_ylim(-15, 80)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.legend(loc='lower left', fontsize=8.5, facecolor='#070d19', edgecolor='#334155', labelcolor='white')

# ------------------------------------------------------------------------------
# PANEL 2: THE 2 REAL MECHANICAL SOLUTIONS THAT ACTUALLY WORK
# ------------------------------------------------------------------------------
ax2.set_title("PANEL 2: THE 2 WORKING SOLUTIONS THAT CANNOT PULL OFF", color='#22c55e', fontsize=13, weight='bold', pad=15)

# SOLUTION A: FRONT-HOOK CLAMP (Hooks FRONT face of box)
ax2.fill([0, 48.15, 48.15, 0], [0, 0, 42.67, 42.67], color='#334155', edgecolor='#64748b', lw=2)
ax2.fill([48.15, 51.0, 51.0, 48.15], [5, 5, 37, 37], color='#64748b')
ax2.fill([-54.6, 0, 0, -54.6], [8, 8, 34, 34], color='#ea580c', alpha=0.9)
ax2.fill([-85, -54.6, -54.6, -85], [16, 16, 26, 26], color='#1e293b')

# True Front-Hook C-Spine (Wraps over top and hooks DOWN IN FRONT OF 120V FACE)
ax2.plot([52, 52, -54.6, -54.6], [24, 47.25 + 4, 47.25 + 4, 5], color='#22c55e', lw=3.5, label='Solution A: Front-Hook Clamp')
ax2.fill([48.15, 52, 52, 48.15], [20, 20, 51.25, 51.25], color='#22c55e', alpha=0.4)
ax2.fill([-60.6, -54.6, -54.6, -60.6], [5, 5, 37, 37], color='#22c55e', alpha=0.9, label='Keeper (Traps Plug Shoulder)')

# Compression Force Vector on Front Hook
ax2.annotate('', xy=(48.15, 35), xytext=(48.15 + 15, 35), arrowprops=dict(arrowstyle='->', color='#22c55e', lw=3.5))
ax2.text(48.15 + 18, 35, "BEARS IN COMPRESSION\nAGAINST FRONT OF BOX!\n(100% Rigid Positive Lock)",
         color='#4ade80', weight='bold', fontsize=9.0, va='center')

# Pull Force Vector
ax2.annotate('', xy=(-95, 21), xytext=(-65, 21), arrowprops=dict(arrowstyle='->', color='#ef4444', lw=4))
ax2.text(-80, 25, "Cable Pull Force", color='#ef4444', weight='bold', fontsize=10, ha='center')

card_b = (
    "SOLUTION B: OPTION 2 COLLAR CLAMP (No Box Contact Needed)\n"
    "• Clamps directly into the 4.7mm exposed neck between plug rim & outlet backplate\n"
    "• Grips the collar neck in pure compression — pulls directly against the rear wall\n"
    "• Zero dependency on box dimensions, lid overhang, or front 120V socket!"
)
ax2.text(0.04, 0.05, card_b, transform=ax2.transAxes, color='#38bdf8', fontsize=9.0, weight='bold',
         bbox=dict(boxstyle='round,pad=0.45', facecolor='#070d19', edgecolor='#0284c7', lw=1.5))

ax2.set_xlim(-105, 115)
ax2.set_ylim(-15, 80)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.legend(loc='upper left', fontsize=8.5, facecolor='#070d19', edgecolor='#334155', labelcolor='white')

out_file = os.path.join(artifact_dir, "why_user_is_right.png")
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "why_user_is_right.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved explanation diagram to:", out_file)
