"""
generate_box_measuring_guide.py
Creates an annotated, high-contrast visual measuring guide on the user's actual photos
for measuring the 3-4 required dimensions of the black outlet box.
"""

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"

# Load source photos
img_side_path = os.path.join(artifact_dir, ".user_uploaded", "media_1788384465199.jpg")
img_front_path = os.path.join(artifact_dir, "pwVL1Z3.jpg")

im_side = Image.open(img_side_path)
im_front = Image.open(img_front_path)

# Create figure
fig = plt.figure(figsize=(24, 14), dpi=180)
plt.subplots_adjust(left=0.03, right=0.97, top=0.92, bottom=0.05, wspace=0.08, hspace=0.12)
fig.patch.set_facecolor('#070d19')

# ------------------------------------------------------------------------------
# PANEL 1: SIDE VIEW (BOX HEIGHT, DEPTH, AND LID OVERHANG)
# ------------------------------------------------------------------------------
ax1 = fig.add_subplot(1, 2, 1)
ax1.imshow(im_side)
ax1.axis('off')
ax1.set_title("PANEL A: Side View — Box Height, Depth & Lid Lip", color='white', fontsize=14, weight='bold', pad=12)

# Coordinates on im_side (width ~1024, height ~1365 approx)
w_s, h_s = im_side.size

# E1: Box Height (Vertical distance from connector face to top lid)
# Lid top is approx y = 0.23*h_s, connector face is approx y = 0.49*h_s, x ~ 0.35*w_s
x_e1 = 0.28 * w_s
y_e1_top = 0.225 * h_s
y_e1_bot = 0.490 * h_s

ax1.annotate('', xy=(x_e1, y_e1_top), xytext=(x_e1, y_e1_bot),
             arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=3.5))
ax1.plot([x_e1 - 25, x_e1 + 35], [y_e1_top, y_e1_top], color='#38bdf8', lw=2.5)
ax1.plot([x_e1 - 25, x_e1 + 35], [y_e1_bot, y_e1_bot], color='#38bdf8', lw=2.5)

ax1.text(x_e1 - 40, (y_e1_top + y_e1_bot)/2,
         "E1: BOX HEIGHT\n(Collar Face to Top of Lid)\n[Est: ~38 - 42 mm]",
         color='#38bdf8', weight='bold', fontsize=11, ha='right', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#070d19', edgecolor='#38bdf8', lw=2.0))

# E2: Box Depth (Front-to-back length across the box body)
# Rear wall is approx x = 0.32*w_s, front wall is approx x = 0.65*w_s, y ~ 0.36*h_s
x_e2_back = 0.305 * w_s
x_e2_front = 0.655 * w_s
y_e2 = 0.360 * h_s

ax1.annotate('', xy=(x_e2_back, y_e2), xytext=(x_e2_front, y_e2),
             arrowprops=dict(arrowstyle='<->', color='#facc15', lw=3.5))
ax1.plot([x_e2_back, x_e2_back], [y_e2 - 30, y_e2 + 30], color='#facc15', lw=2.5)
ax1.plot([x_e2_front, x_e2_front], [y_e2 - 30, y_e2 + 30], color='#facc15', lw=2.5)

ax1.text((x_e2_back + x_e2_front)/2, y_e2 + 55,
         "E2: BOX DEPTH\n(Front Wall to Rear Wall)\n[Est: ~45 - 50 mm]",
         color='#facc15', weight='bold', fontsize=11, ha='center', va='top',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#070d19', edgecolor='#facc15', lw=2.0))

# E3: Lid Overhang Lip (How far the lid rim overhangs the rear wall)
# Lid rim is at x ~ 0.28*w_s, rear wall is at x ~ 0.315*w_s, y ~ 0.245*h_s
x_e3_rim = 0.280 * w_s
x_e3_wall = 0.315 * w_s
y_e3 = 0.245 * h_s

ax1.annotate('', xy=(x_e3_rim, y_e3), xytext=(x_e3_wall, y_e3),
             arrowprops=dict(arrowstyle='<->', color='#4ade80', lw=3.0))
ax1.plot([x_e3_rim, x_e3_rim], [y_e3 - 25, y_e3 + 25], color='#4ade80', lw=2.0)
ax1.plot([x_e3_wall, x_e3_wall], [y_e3 - 25, y_e3 + 25], color='#4ade80', lw=2.0)

ax1.text(x_e3_rim - 30, y_e3 - 40,
         "E3: LID LIP OVERHANG\n(Rim past Rear Wall)\n[Est: ~3.0 - 4.5 mm]",
         color='#4ade80', weight='bold', fontsize=10.5, ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#070d19', edgecolor='#4ade80', lw=1.8))

# ------------------------------------------------------------------------------
# PANEL 2: FRONT/TOP 3/4 VIEW (BOX WIDTH & CLEARANCE)
# ------------------------------------------------------------------------------
ax2 = fig.add_subplot(1, 2, 2)
ax2.imshow(im_front)
ax2.axis('off')
ax2.set_title("PANEL B: Front View — Box Width & Side Flange", color='white', fontsize=14, weight='bold', pad=12)

w_f, h_f = im_front.size

# E4: Box Width across the black housing section (width of lid/casing)
# Collar is on left, width of black box section across
x_e4_left = 0.31 * w_f
x_e4_right = 0.49 * w_f
y_e4 = 0.35 * h_f

ax2.annotate('', xy=(x_e4_left, y_e4), xytext=(x_e4_right, y_e4),
             arrowprops=dict(arrowstyle='<->', color='#ec4899', lw=3.5))
ax2.plot([x_e4_left, x_e4_left], [y_e4 - 35, y_e4 + 35], color='#ec4899', lw=2.5)
ax2.plot([x_e4_right, x_e4_right], [y_e4 - 35, y_e4 + 35], color='#ec4899', lw=2.5)

ax2.text((x_e4_left + x_e4_right)/2, y_e4 - 55,
         "E4: BOX WIDTH\n(Across Black Section)\n[Est: ~48 - 56 mm]",
         color='#ec4899', weight='bold', fontsize=11, ha='center', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#070d19', edgecolor='#ec4899', lw=2.0))

# Also add summary instruction card inside Panel 2
summary_text = (
    "CALIPER MEASUREMENT INSTRUCTIONS:\n\n"
    "• E1 (Box Height): Place outside caliper jaws between the flat face\n"
    "  where the connector plugs in, up to the top flat surface of the lid.\n\n"
    "• E2 (Box Depth): Measure from the front vertical wall of the box\n"
    "  to the rear vertical wall.\n\n"
    "• E3 (Lid Overhang): Use the caliper depth rod or jaws to measure how\n"
    "  far the lid lip sticks out past the rear wall.\n\n"
    "• E4 (Box Width): Measure the width of the black box section.\n\n"
    "Once you reply with E1, E2, E3 (and E4), the C-Bracket CAD will\n"
    "be 100% matched to your exact physical hardware!"
)

ax2.text(0.50, 0.06, summary_text, transform=ax2.transAxes,
         color='#f1f5f9', fontsize=10.5, fontfamily='monospace', weight='bold',
         ha='center', va='bottom',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#0f172a', edgecolor='#3b82f6', lw=2.0))

out_path = os.path.join(artifact_dir, "box_measuring_guide.png")
plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.savefig(os.path.join(target_dir, "box_measuring_guide.png"), facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved box measuring guide to:", out_path)
