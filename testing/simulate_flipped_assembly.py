"""
simulate_flipped_assembly.py
Compares the photo pwVL1Z3.jpg as taken vs. with the black box flipped 180 degrees
relative to the aluminum bracket, showing where the collar and the two bolt holes end up.
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

im = Image.open(r'C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185\pwVL1Z3.jpg')
w, h = im.size

# In pwVL1Z3.jpg:
# Black box is approximately on the left (x: 0.15*w to 0.48*w, y: 0.15*h to 0.85*h)
# Aluminum plate & bezel are on the right (x: 0.40*w to 0.85*w, y: 0.15*h to 0.85*h)

crop_box = im.crop((int(0.18*w), int(0.20*h), int(0.48*w), int(0.82*h)))
crop_alum = im.crop((int(0.42*w), int(0.20*h), int(0.85*w), int(0.82*h)))

# Flipped box (rotated 180)
flipped_box = crop_box.rotate(180, expand=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12), dpi=180)
fig.patch.set_facecolor('#070d19')

# As photographed (Upside Down)
ax1.set_facecolor('#0f172a')
ax1.set_title("CONFIGURATION A: As Photographed in pwVL1Z3\n(User: 'Black box is upside down')", color='#ef4444', weight='bold', fontsize=12, pad=12)
ax1.imshow(im.crop((int(0.18*w), int(0.20*h), int(0.85*w), int(0.82*h))))
ax1.axis('off')
ax1.text(0.05, 0.05, "• Collar at BOTTOM near Hole 1\n• Yellow label upside down", transform=ax1.transAxes,
         color='white', weight='bold', fontsize=11, bbox=dict(facecolor='#ef4444', alpha=0.8, pad=5))

# Correctly Flipped Assembly
# Composite flipped box side-by-side with aluminum plate
bw, bh = flipped_box.size
aw, ah = crop_alum.size
comp_h = max(bh, ah)
comp_w = bw + aw
composite = Image.new('RGB', (comp_w, comp_h), (15, 23, 42))
composite.paste(flipped_box, (0, (comp_h - bh)//2))
composite.paste(crop_alum, (bw - 40, (comp_h - ah)//2))

ax2.set_facecolor('#0f172a')
ax2.set_title("CONFIGURATION B: Corrected Assembly\n(Black box flipped 180° right-side up)", color='#22c55e', weight='bold', fontsize=12, pad=12)
ax2.imshow(composite)
ax2.axis('off')
ax2.text(0.05, 0.90, "• Collar moves to TOP near Hole 2!\n• Yellow label reads right-side up\n• Hole 2 is still RIGHT NEXT TO the collar!", transform=ax2.transAxes,
         color='white', weight='bold', fontsize=11, bbox=dict(facecolor='#22c55e', alpha=0.8, pad=5))

out_file = os.path.join(artifact_dir, "assembly_orientation_check.png")
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "assembly_orientation_check.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved orientation check to:", out_file)
