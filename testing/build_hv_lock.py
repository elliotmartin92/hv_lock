"""
build_hv_lock.py
Parametric 3D CAD generator for the Kia EV6 / E-GMP V2L Exterior Cable Lock.
Generates:
  - hv_lock_saddle.stl / .obj (Stationary mounting base clamped to connector tower)
  - hv_lock_slider.stl / .obj (Exterior sliding deadbolt with tactile detents)
  - hv_lock_plate.stl / .obj  (Pre-arranged 1-click print plate)
  - hv_lock.scad              (OpenSCAD source file)
"""

import math
import numpy as np
import trimesh
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
import os

# ==============================================================================
# CALIBRATED DIMENSIONAL CONSTANTS (From Caliper Measurements)
# ==============================================================================
# Plug Connector
TOWER_WIDTH = 19.06        # [A3]
TOWER_LENGTH = 36.75       # [B1]
BODY_HEIGHT = 20.80        # [A2]
SHROUD_WIDTH = 36.10       # [A1]
SHROUD_WALL = 1.20         # [A5]
PLUG_TOTAL_HEIGHT = 37.11  # [A4]
BODY_RIGID_LENGTH = 54.60  # [B7]

# Receptacle & Latch Tooth
COLLAR_PROTRUSION = 22.37  # [C1]
TOOTH_DIST_FROM_RIM = 8.73 # [C2]
LATCH_TOOTH_WIDTH = 2.00   # [C3]
LATCH_TOOTH_HEIGHT = 2.70  # [C4]
GUIDE_RIBS_SPAN = 13.82    # [C5]
METAL_PLATE_GAP = 4.00     # [D3]
TOP_CLEARANCE = 8.27       # [D4]

# Kinematic Stroke
SLIDE_STROKE = 8.50        # [B3] (8.25mm + 0.25mm margin)

# Print Clearances (Tolerances for FDM 0.4mm nozzle)
CLEARANCE_SLIP = 0.35      # Sliding track clearance
CLEARANCE_SNAP = 0.25      # Push-fit clearance on tower

# ==============================================================================
# SADDLE BASE GEOMETRY
# ==============================================================================
# Saddle envelope:
# Sits over the top tower.
SADDLE_INNER_W = TOWER_WIDTH + 2 * CLEARANCE_SNAP   # ~19.56 mm
SADDLE_WALL_THICK = 2.20                            # Robust outer wall
SADDLE_OUTER_W = SADDLE_INNER_W + 2 * SADDLE_WALL_THICK # ~23.96 mm

SADDLE_LENGTH = 32.00      # Covers 32mm of the 36.75mm tower, leaving front rim clear
SADDLE_SKIRT_DEPTH = 12.00 # Downward grip skirt along tower flanks
SADDLE_TOP_THICK = 3.00    # Solid deck thickness above tower

# Guide Rail (Dovetail / T-Track on top of Saddle)
TRACK_NECK_W = 11.00
TRACK_FLANGE_W = 15.00
TRACK_H = 4.00
TRACK_NECK_H = 2.00
TRACK_FLANGE_H = 2.00

def create_box(extents, translation=[0, 0, 0]):
    """Helper to create a box mesh centered at translation."""
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(translation)
    return m

def create_saddle_base():
    """
    Builds the stationary saddle base:
    - Inner U-channel clipping over the connector tower.
    - Side snap retention ribs.
    - Upper T-slot guide rails.
    - Travel end-stop and detent pockets.
    """
    # 1. Main saddle body block:
    body_extents = [SADDLE_OUTER_W, SADDLE_LENGTH, SADDLE_SKIRT_DEPTH + SADDLE_TOP_THICK]
    body_center = [0, SADDLE_LENGTH / 2.0, (SADDLE_TOP_THICK - SADDLE_SKIRT_DEPTH) / 2.0]
    main_block = create_box(body_extents, body_center)
    
    # Inner pocket cavity for the tower:
    pocket_extents = [SADDLE_INNER_W, SADDLE_LENGTH + 2.0, SADDLE_SKIRT_DEPTH + 1.0]
    pocket_center = [0, SADDLE_LENGTH / 2.0, -SADDLE_SKIRT_DEPTH / 2.0]
    pocket_box = create_box(pocket_extents, pocket_center)
    
    saddle_mesh = main_block.difference(pocket_box, engine='manifold')
    
    # 2. Side Snap Retention Ridges on inner skirts:
    snap_left = create_box([0.7, SADDLE_LENGTH - 4.0, 1.2],
                           [-SADDLE_INNER_W / 2.0 + 0.35, SADDLE_LENGTH / 2.0, -SADDLE_SKIRT_DEPTH + 2.0])
    snap_right = create_box([0.7, SADDLE_LENGTH - 4.0, 1.2],
                            [SADDLE_INNER_W / 2.0 - 0.35, SADDLE_LENGTH / 2.0, -SADDLE_SKIRT_DEPTH + 2.0])
    
    saddle_mesh = saddle_mesh.union([snap_left, snap_right], engine='manifold')
    
    # 3. T-Track Rails on top face (Z in [SADDLE_TOP_THICK, SADDLE_TOP_THICK + TRACK_H]):
    rail_neck = create_box([TRACK_NECK_W, SADDLE_LENGTH, TRACK_NECK_H],
                           [0, SADDLE_LENGTH / 2.0, SADDLE_TOP_THICK + TRACK_NECK_H / 2.0])
    rail_flange = create_box([TRACK_FLANGE_W, SADDLE_LENGTH, TRACK_FLANGE_H],
                             [0, SADDLE_LENGTH / 2.0, SADDLE_TOP_THICK + TRACK_NECK_H + TRACK_FLANGE_H / 2.0])
    
    saddle_mesh = saddle_mesh.union([rail_neck, rail_flange], engine='manifold')
    
    # 4. Rear End-Stop Wall at Y = SADDLE_LENGTH:
    stop_wall = create_box([SADDLE_OUTER_W, 3.0, TRACK_H + 1.5],
                           [0, SADDLE_LENGTH - 1.5, SADDLE_TOP_THICK + (TRACK_H + 1.5) / 2.0])
    saddle_mesh = saddle_mesh.union(stop_wall, engine='manifold')
    
    # 5. Detent Notches on upper flange:
    detent_cut_locked_l = create_box([1.4, 2.0, 1.5], [-TRACK_FLANGE_W / 2.0 + 0.4, 8.0, SADDLE_TOP_THICK + TRACK_H - 0.5])
    detent_cut_locked_r = create_box([1.4, 2.0, 1.5], [TRACK_FLANGE_W / 2.0 - 0.4, 8.0, SADDLE_TOP_THICK + TRACK_H - 0.5])
    detent_cut_unlocked_l = create_box([1.4, 2.0, 1.5], [-TRACK_FLANGE_W / 2.0 + 0.4, 8.0 + SLIDE_STROKE, SADDLE_TOP_THICK + TRACK_H - 0.5])
    detent_cut_unlocked_r = create_box([1.4, 2.0, 1.5], [TRACK_FLANGE_W / 2.0 - 0.4, 8.0 + SLIDE_STROKE, SADDLE_TOP_THICK + TRACK_H - 0.5])
    
    saddle_mesh = saddle_mesh.difference([detent_cut_locked_l, detent_cut_locked_r,
                                          detent_cut_unlocked_l, detent_cut_unlocked_r], engine='manifold')
    
    return saddle_mesh


# ==============================================================================
# SLIDING DEADBOLT GEOMETRY
# ==============================================================================
def create_sliding_deadbolt():
    """
    Builds the exterior sliding deadbolt:
    - Internal T-slot carriage with 0.35mm sliding clearance.
    - Forward-extending locking tongue with latch catch hook.
    - Ergonomic textured thumb grip.
    - Integrated tactile detent nubs.
    """
    SLIDER_CARRIAGE_LEN = 20.00
    SLIDER_OUTER_W = SADDLE_OUTER_W
    SLIDER_TOTAL_H = TRACK_H + 3.00
    
    # 1. Main carriage block:
    c_extents = [SLIDER_OUTER_W, SLIDER_CARRIAGE_LEN, SLIDER_TOTAL_H]
    c_center = [0, SLIDER_CARRIAGE_LEN / 2.0, SADDLE_TOP_THICK + SLIDER_TOTAL_H / 2.0]
    carriage = create_box(c_extents, c_center)
    
    # Internal T-slot cavity (matching rail + CLEARANCE_SLIP):
    c_neck_w = TRACK_NECK_W + 2 * CLEARANCE_SLIP    # 11.70 mm
    c_flange_w = TRACK_FLANGE_W + 2 * CLEARANCE_SLIP# 15.70 mm
    c_neck_h = TRACK_NECK_H + CLEARANCE_SLIP        # 2.35 mm
    c_flange_h = TRACK_FLANGE_H + CLEARANCE_SLIP    # 2.35 mm
    
    cavity_neck = create_box([c_neck_w, SLIDER_CARRIAGE_LEN + 2.0, c_neck_h + 1.0],
                             [0, SLIDER_CARRIAGE_LEN / 2.0, SADDLE_TOP_THICK + (c_neck_h + 1.0) / 2.0 - 0.5])
    cavity_flange = create_box([c_flange_w, SLIDER_CARRIAGE_LEN + 2.0, c_flange_h],
                               [0, SLIDER_CARRIAGE_LEN / 2.0, SADDLE_TOP_THICK + TRACK_NECK_H + c_flange_h / 2.0])
    
    carriage = carriage.difference([cavity_neck, cavity_flange], engine='manifold')
    
    # 2. Forward Locking Tongue:
    TONGUE_W = 11.50
    TONGUE_LEN = 14.00
    TONGUE_H = 4.20
    
    tongue_extents = [TONGUE_W, TONGUE_LEN, TONGUE_H]
    tongue_center = [0, -TONGUE_LEN / 2.0, SADDLE_TOP_THICK + TONGUE_H / 2.0 - 1.5]
    tongue = create_box(tongue_extents, tongue_center)
    
    # Latch tooth capture pocket inside tongue:
    pocket = create_box([4.0, 3.5, 3.2],
                        [0, -8.0, SADDLE_TOP_THICK - 1.5 + 3.2 / 2.0])
    
    # Entrance bevel/ramp at tongue tip for smooth sliding over the sloped tooth:
    ramp = create_box([TONGUE_W + 1.0, 4.0, 3.0],
                      [0, -TONGUE_LEN + 1.5, SADDLE_TOP_THICK - 1.5 + 1.0])
    
    tongue = tongue.difference([pocket, ramp], engine='manifold')
    slider = carriage.union(tongue, engine='manifold')
    
    # 3. Ergonomic Thumb Grip Ridges on top face:
    ridge_z = SADDLE_TOP_THICK + SLIDER_TOTAL_H
    for ry in [4.0, 7.5, 11.0, 14.5, 17.5]:
        ridge = create_box([SLIDER_OUTER_W - 4.0, 1.2, 0.9],
                           [0, ry, ridge_z + 0.45])
        slider = slider.union(ridge, engine='manifold')
        
    # 4. Integrated Tactile Detent Nubs:
    nub_l = create_box([0.8, 1.6, 1.2],
                       [-c_flange_w / 2.0 + 0.4, 8.0, SADDLE_TOP_THICK + TRACK_NECK_H + c_flange_h / 2.0])
    nub_r = create_box([0.8, 1.6, 1.2],
                       [c_flange_w / 2.0 - 0.4, 8.0, SADDLE_TOP_THICK + TRACK_NECK_H + c_flange_h / 2.0])
    slider = slider.union([nub_l, nub_r], engine='manifold')
    
    return slider

def generate_openscad_source(filepath):
    """Generates an editable OpenSCAD parametric file."""
    scad_code = f"""// ==============================================================================
// Kia EV6 / E-GMP V2L Exterior Cable Lock - OpenSCAD Parametric Source
// Calibrated from User Caliper Measurements
// ==============================================================================

// Dimensional Constants (mm)
tower_width = {TOWER_WIDTH};        // [A3]
tower_length = {TOWER_LENGTH};      // [B1]
tooth_dist = {TOOTH_DIST_FROM_RIM}; // [C2]
tooth_width = {LATCH_TOOTH_WIDTH};  // [C3]
tooth_height = {LATCH_TOOTH_HEIGHT};// [C4]
slide_stroke = {SLIDE_STROKE};      // [B3]
clearance_slip = {CLEARANCE_SLIP};  // FDM print clearance

// Modules
module saddle_base() {{
    difference() {{
        translate([0, 16, -4.5]) cube([23.96, 32, 15], center=true);
        translate([0, 16, -6.5]) cube([19.56, 34, 13], center=true);
    }}
    translate([0, 16, 4]) cube([11, 32, 2], center=true);
    translate([0, 16, 6]) cube([15, 32, 2], center=true);
    translate([0, 30.5, 5]) cube([23.96, 3, 5.5], center=true);
}}

module sliding_deadbolt() {{
    difference() {{
        translate([0, 10, 6.5]) cube([23.96, 20, 7], center=true);
        translate([0, 10, 4]) cube([11.7, 22, 3.35], center=true);
        translate([0, 10, 6]) cube([15.7, 22, 2.35], center=true);
    }}
    difference() {{
        translate([0, -7, 3.6]) cube([11.5, 14, 4.2], center=true);
        translate([0, -8, 3.1]) cube([4, 3.5, 3.2], center=true);
    }}
    for (y = [4, 7.5, 11, 14.5, 17.5]) {{
        translate([0, y, 10.45]) cube([19.96, 1.2, 0.9], center=true);
    }}
}}

saddle_base();
translate([35, 0, 0]) sliding_deadbolt();
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(scad_code)
    print(f"Generated OpenSCAD file: {filepath}")

def main():
    target_dir = r"c:\Users\Elliot\Documents\antigravity\hv_lock"
    artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\bcff0673-e2b6-492e-8df2-3d38d1a52185"
    
    print("Building Saddle Base...")
    saddle = create_saddle_base()
    print(f"Saddle: watertight={saddle.is_watertight}, volume={saddle.volume:.1f} mm^3, bounds={saddle.bounds}")
    
    print("Building Sliding Deadbolt...")
    slider = create_sliding_deadbolt()
    print(f"Slider: watertight={slider.is_watertight}, volume={slider.volume:.1f} mm^3, bounds={slider.bounds}")
    
    for out_dir in [target_dir, artifact_dir]:
        saddle_stl = os.path.join(out_dir, "hv_lock_saddle.stl")
        saddle_obj = os.path.join(out_dir, "hv_lock_saddle.obj")
        saddle.export(saddle_stl)
        saddle.export(saddle_obj)
        print("Exported Saddle to:", saddle_stl)
        
        slider_stl = os.path.join(out_dir, "hv_lock_slider.stl")
        slider_obj = os.path.join(out_dir, "hv_lock_slider.obj")
        slider.export(slider_stl)
        slider.export(slider_obj)
        print("Exported Slider to:", slider_stl)
        
        s_plate = saddle.copy()
        s_plate.apply_translation([0, 0, -s_plate.bounds[0][2]])
        
        sl_plate = slider.copy()
        sl_plate.apply_translation([0, 0, -sl_plate.bounds[0][2]])
        sl_plate.apply_translation([SADDLE_OUTER_W + 15.0, 0, 0])
        
        plate = trimesh.util.concatenate([s_plate, sl_plate])
        plate_stl = os.path.join(out_dir, "hv_lock_plate.stl")
        plate_obj = os.path.join(out_dir, "hv_lock_plate.obj")
        plate.export(plate_stl)
        plate.export(plate_obj)
        print("Exported Combined Plate to:", plate_stl)
        
        scad_path = os.path.join(out_dir, "hv_lock.scad")
        generate_openscad_source(scad_path)

if __name__ == "__main__":
    main()
