"""
illustrate_solution_b_reality.py
Visualizes:
1. Why Solution B (Collar Clamp) relies on friction and why the user's skepticism is 100% correct.
2. The real mechanical requirement: a forward-facing positive stop.
3. The 3 viable physical anchor points on the actual assembly.
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
# PANEL 1: WHY SOLUTION B (COLLAR CLAMP) FAILS IN REALITY
# ------------------------------------------------------------------------------
ax1.set_title("PANEL 1: WHY YOUR SKEPTICISM IS 100% CORRECT (Solution B Friction Flaw)", color='#ef4444', fontsize=13, weight='bold', pad=15)

# Housing Wall
ax1.fill([0, 25, 25, 0], [-25, -25, 25, 25], color='#334155', edgecolor='#64748b', lw=2, label='Outlet Housing Wall')

# Smooth 4.7mm Collar Neck
ax1.fill([-4.7, 0, 0, -4.7], [-15, -15, 15, 15], color='#1e293b', edgecolor='#475569', lw=1.5, label='Smooth 4.7mm Collar Neck')

# Orange Plug (Seated over collar)
ax1.fill([-59.3, -4.7, -4.7, -59.3], [-11, -11, 11, 11], color='#ea580c', edgecolor='#c2410c', lw=2, label='Orange Plug Body')
ax1.fill([-85, -59.3, -59.3, -85], [-8, -8, 8, 8], color='#1e293b', label='Cable')

# Solution B Clamp (Pinching the 4.7mm neck)
ax1.fill([-4.2, -0.5, -0.5, -4.2], [15, 15, 23, 23], color='#06b6d4', alpha=0.9, label='Solution B Clamp Jaw')
ax1.fill([-4.2, -0.5, -0.5, -4.2], [-23, -23, -15, -15], color='#a855f7', alpha=0.9, label='Lower Jaw')

# Bridle Arm to Shoulder
ax1.plot([-2.35, -2.35, -59.3, -59.3], [23, 26, 26, 11], color='#22d3ee', lw=3.0, label='Bridle Arm & Rear Trap')
ax1.plot([-2.35, -2.35, -59.3, -59.3], [-23, -26, -26, -11], color='#22d3ee', lw=3.0)

# Pull Force Vector
ax1.annotate('', xy=(-95, 0), xytext=(-65, 0), arrowprops=dict(arrowstyle='->', color='#ef4444', lw=4))
ax1.text(-80, 5, "Cable Pull Force", color='#ef4444', weight='bold', fontsize=10, ha='center')

# Slip Vector
ax1.annotate('', xy=(-15, 19), xytext=(-4.2, 19), arrowprops=dict(arrowstyle='->', color='#ef4444', lw=3, ls=':'))
ax1.text(-12, 32, "SLIPS OFF!\nNo lip on collar neck.\nOnly friction holds it.", color='#ef4444', weight='bold', fontsize=9.5, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#070d19', edgecolor='#ef4444', lw=1.5))

ax1.annotate('FATAL FLAW OF SOLUTION B:\nThe collar is a smooth straight cylinder.\nIt has NO forward-facing ridge or lip.\nPulling the cable pulls the clamp straight OFF the neck!',
             xy=(-2.35, 23), xytext=(-65, 45),
             arrowprops=dict(arrowstyle='->', color='#ef4444', lw=2),
             color='#fca5a5', weight='bold', fontsize=9.5,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#070d19', edgecolor='#ef4444', lw=1.5))

ax1.set_xlim(-105, 35)
ax1.set_ylim(-35, 65)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.legend(loc='lower left', fontsize=8.5, facecolor='#070d19', edgecolor='#334155', labelcolor='white')

# ------------------------------------------------------------------------------
# PANEL 2: THE 3 VIABLE POSITIVE MECHANICAL ANCHORS
# ------------------------------------------------------------------------------
ax2.set_title("PANEL 2: THE 3 REAL POSITIVE ANCHOR POINTS ON THE VEHICLE", color='#22c55e', fontsize=13, weight='bold', pad=15)

# Box Outline
ax2.fill([0, 48.15, 48.15, 0], [-25, -25, 25, 25], color='#334155', edgecolor='#64748b', lw=2)
# Orange Plug
ax2.fill([-59.3, 0, 0, -59.3], [-11, -11, 11, 11], color='#ea580c', alpha=0.85)
ax2.fill([-85, -59.3, -59.3, -85], [-8, -8, 8, 8], color='#1e293b')

# ANCHOR 1: FRONT FACE WRAP
ax2.plot([48.15, 52, 52, -59.3, -59.3], [10, 10, 32, 32, 11], color='#38bdf8', lw=3.0)
ax2.fill([48.15, 52, 52, 48.15], [5, 5, 25, 25], color='#38bdf8', alpha=0.4)
ax2.text(56, 18, "ANCHOR 1: Front-Face Hook\n• Hooks around 120V front wall\n• Squeezes box in pure compression\n• Pulling cable pulls hook TIGHTER!",
         color='#38bdf8', weight='bold', fontsize=9.0, va='center')

# ANCHOR 2: CHASSIS MOUNTING BOLT EYELET
# Draw silver plate tab with bolt
ax2.fill([0, 10, 10, 0], [25, 25, 38, 38], color='#94a3b8', label='Silver Chassis Flange')
ax2.plot([5, 5], [23, 42], color='#facc15', lw=4, label='Chassis Bolt')
ax2.plot([5, -59.3, -59.3], [38, 38, 11], color='#facc15', lw=2.5, ls='--')
ax2.text(12, 38, "ANCHOR 2: Chassis Bolt Tab\n• 3D printed eyelet under chassis bolt\n• Uses car frame's massive holding power\n• Rigid arm reaches to plug shoulder",
         color='#facc15', weight='bold', fontsize=9.0, va='center')

# ANCHOR 3: SNAP-TAB POCKET LOCK
# Recessed snap window on housing
ax2.fill([2, 8, 8, 2], [14, 14, 20, 20], color='#0f172a', edgecolor='#4ade80', lw=1.5)
ax2.plot([5, -59.3, -59.3], [17, 17, 11], color='#4ade80', lw=2.5, ls=':')
ax2.text(-25, -28, "ANCHOR 3: Molded Snap-Window Hook\n• Drops a positive locking tooth into\n  the square snap window above collar\n• 100% localized to outlet housing",
         color='#4ade80', weight='bold', fontsize=9.0)

ax2.set_xlim(-105, 95)
ax2.set_ylim(-35, 65)
ax2.set_aspect('equal')
ax2.axis('off')

out_file = os.path.join(artifact_dir, "solution_b_reality.png")
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "solution_b_reality.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved Solution B reality diagram to:", out_file)
