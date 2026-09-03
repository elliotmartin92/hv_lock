"""
illustrate_width_clarification.py
Creates an annotated visual diagram showing the view looking at the female receptacle face,
clarifying the 'Left-to-Right' wider dimension vs the narrower dimension, and showing
where the C-bracket legs must sit.
"""

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11), dpi=180)
plt.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.08, wspace=0.12)
fig.patch.set_facecolor('#070d19')

# ------------------------------------------------------------------------------
# PANEL 1: SCHEMATIC LOOKING DIRECTLY AT THE RECEPTACLE FACE
# ------------------------------------------------------------------------------
ax1.set_facecolor('#0f172a')

# Box footprint looking at the connector face
# Let's say the black box section is ~50mm x ~48mm, but the whole module with silver plate is wider (~110mm)
# Black box body
ax1.fill([0, 50, 50, 0], [0, 0, 48, 48], color='#334155', alpha=0.9, label='Black Box Body')
# Silver plate extending to the right
ax1.fill([50, 125, 125, 50], [0, 0, 48, 48], color='#64748b', alpha=0.5, label='Silver Mounting Bracket')

# Female Collar Location
# Collar is 22.7mm wide x 33.05mm tall
ax1.fill([10, 34, 34, 10], [7.5, 7.5, 40.5, 40.5], color='#0284c7', alpha=0.9, label='Female Receptacle Collar')

# Connector Shroud (Plugging into collar) - 36.1mm wide x 20.8mm tall (or 33mm with tower)
ax1.plot([4, 40, 40, 4, 4], [3, 3, 44, 44, 3], color='#ea580c', lw=2.5, ls='--', label='Orange Plug Outline (36.1mm wide)')

# Dimension A: The dimension you measured (49.65mm) - Black box section alone
ax1.annotate('', xy=(0, -8), xytext=(50, -8), arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=3))
ax1.text(25, -13, "Dimension you measured (49.65 mm)\n[Width of Black Box Section alone]",
         color='#38bdf8', weight='bold', fontsize=9.5, ha='center', va='top')

# Dimension B: The wider dimension across the whole assembly (including silver plate)
ax1.annotate('', xy=(0, 56), xytext=(125, 56), arrowprops=dict(arrowstyle='<->', color='#ec4899', lw=3))
ax1.text(62.5, 61, "The Wider Dimension (Black Box + Silver Plate ~110-130mm)\n[Is this the wider dimension you are seeing?]",
         color='#ec4899', weight='bold', fontsize=9.5, ha='center', va='bottom')

# Dimension C: Depth of the box (48.15mm)
ax1.annotate('', xy=(-8, 0), xytext=(-8, 48), arrowprops=dict(arrowstyle='<->', color='#facc15', lw=3))
ax1.text(-12, 24, "Box Depth (E2)\n48.15 mm", color='#facc15', weight='bold', fontsize=9.5, ha='right', va='center')

# C-Bracket Legs shown in green!
# Leg 1 (Left)
ax1.fill([-5, 0, 0, -5], [-5, -5, 53, 53], color='#22c55e', alpha=0.7)
# Leg 2 (Right) - Can it sit between black box and silver plate, or must it go outside?
ax1.fill([50, 55, 55, 50], [-5, -5, 53, 53], color='#22c55e', alpha=0.7)
ax1.text(-2.5, 24, "C-Spine\nLeft Leg", color='white', weight='bold', fontsize=8, ha='center', va='center', rotation=90)
ax1.text(52.5, 24, "C-Spine\nRight Leg", color='white', weight='bold', fontsize=8, ha='center', va='center', rotation=90)

ax1.set_xlim(-35, 145)
ax1.set_ylim(-30, 80)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title("VIEW A: Looking Directly at the Face Where Connector Plugs In", color='white', fontsize=12.5, weight='bold', pad=12)
ax1.legend(loc='upper right', fontsize=8, facecolor='#070d19', edgecolor='#334155', labelcolor='white')

# ------------------------------------------------------------------------------
# PANEL 2: PHOTO OF THE ACTUAL MODULE WITH LABELED AXES
# ------------------------------------------------------------------------------
ax2.set_facecolor('#0f172a')
img_front_path = os.path.join(artifact_dir, "pwVL1Z3.jpg")
im_front = Image.open(img_front_path)
ax2.imshow(im_front)
ax2.axis('off')
ax2.set_title("VIEW B: Real Module Reference (Where the Bracket Straddles)", color='white', fontsize=12.5, weight='bold', pad=12)

w_f, h_f = im_front.size

# Arrow for Black Box section width (what you measured: 49.65mm)
ax2.annotate('', xy=(0.31*w_f, 0.50*h_f), xytext=(0.50*w_f, 0.50*h_f),
             arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=3.5))
ax2.text(0.405*w_f, 0.47*h_f, "Black Section Width (49.65 mm)\n✓ Bracket Straddles THIS Section",
         color='#38bdf8', weight='bold', fontsize=10, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#070d19', edgecolor='#38bdf8', lw=1.5))

# Arrow for Total Width across Silver Plate
ax2.annotate('', xy=(0.31*w_f, 0.22*h_f), xytext=(0.70*w_f, 0.22*h_f),
             arrowprops=dict(arrowstyle='<->', color='#ec4899', lw=3.5))
ax2.text(0.505*w_f, 0.18*h_f, "Total Module Width (including Silver Plate ~110mm)\n❌ Do NOT wrap around this — car mounting bolts block it!",
         color='#ec4899', weight='bold', fontsize=9.5, ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#070d19', edgecolor='#ec4899', lw=1.5))

out_path = os.path.join(artifact_dir, "width_clarification.png")
plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "width_clarification.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved width clarification image to:", out_path)
