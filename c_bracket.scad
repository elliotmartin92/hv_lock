// ==============================================================================
// c_bracket.scad
// Parametric OpenSCAD Source for Vehicle-Accurate Right-Hand Corner C-Bracket
// Kia EV6 / E-GMP 95190-CV780 Outlet Box & V2L Connector Lock
// ==============================================================================

$fn = 40;

// Housing & Seated Plug Calibrated Dimensions (mm)
BOX_W = 111.75;         // Long width across car (extends to the left)
BOX_D = 48.15;          // Front-to-back depth (120V face to rear connector face)
BOX_H = 42.67;          // Vertical height (bottom to top lid)
LID_OH = 12.45;         // Rear lid lip overhang
LID_T = 4.58;           // Lid lip vertical thickness

CONN_W = 36.10;         // Orange plug width
CONN_L = 54.60;         // Rigid body length to shoulder
SEATED_GAP = 4.70;      // Front rim to housing gap
PLUG_SHOULDER_Y = SEATED_GAP + CONN_L; // 59.30 mm

CABLE_R = 8.50;         // Cable boot radius (~17mm diameter)
WALL_T = 4.00;          // Structural wall thickness
BRACKET_W = CONN_W + 12.0; // 48.10 mm (Right-hand corner span)

module vehicle_c_spine() {
    difference() {
        union() {
            // 1. Top Plate (Rests on lid above right-hand corner)
            translate([-BRACKET_W, -(BOX_D + LID_OH), BOX_H])
                cube([BRACKET_W, BOX_D + LID_OH + WALL_T, WALL_T]);
            
            // 2. Positive Hook (Catches 12.45mm rear lid overhang)
            translate([-BRACKET_W, -LID_OH - WALL_T, BOX_H - (LID_T + 4.0)])
                cube([BRACKET_W, WALL_T, LID_T + 4.0]);
            
            // 3. Right Outer Flank (Wraps exterior right end of the box)
            translate([0, -(BOX_D + LID_OH), -15.0])
                cube([WALL_T, BOX_D + LID_OH + PLUG_SHOULDER_Y + 10.0, BOX_H + WALL_T + 15.0]);
            
            // 4. Rear Drop Arm at Plug Shoulder
            translate([-BRACKET_W, PLUG_SHOULDER_Y, -15.0])
                cube([BRACKET_W, WALL_T + 4.0, BOX_H + WALL_T + 15.0]);
            
            // 5. Track Housing at Bottom
            translate([-BRACKET_W - 2.0, PLUG_SHOULDER_Y, -15.0])
                cube([BRACKET_W + 4.0, 12.0, 16.0]);
        }
        
        // Slide track slot for Keeper (open on left side)
        translate([-BRACKET_W - 10.0, PLUG_SHOULDER_Y + 3.0, -13.0])
            cube([BRACKET_W + 15.0, 7.0, 12.0]);
        
        // Cable exit cutout
        translate([-BRACKET_W/2, PLUG_SHOULDER_Y + 10.0, 0])
            rotate([90, 0, 0])
                cylinder(r = CABLE_R + 3.0, h = 40.0, center = true);
        
        // Connector clearance pocket
        translate([-BRACKET_W + 2.0, 0, -10.0])
            cube([CONN_W + 4.0, PLUG_SHOULDER_Y + 2.0, BOX_H + 5.0]);
    }
}

module slide_keeper() {
    difference() {
        union() {
            // Main Keeper Bar
            translate([-BRACKET_W, PLUG_SHOULDER_Y + 3.5, -12.0])
                cube([BRACKET_W, 6.0, 13.0]);
            
            // Ergonomic Thumb Pull Tab (on left accessible side)
            translate([-BRACKET_W - 10.0, PLUG_SHOULDER_Y + 2.0, -12.0])
                cube([10.0, 9.0, 16.0]);
        }
        
        // Cable Cradle Slot (U-cutout)
        translate([-BRACKET_W/2, PLUG_SHOULDER_Y + 6.0, -6.0])
            rotate([90, 0, 0])
                cylinder(r = CABLE_R + 1.2, h = 25.0, center = true);
        translate([-BRACKET_W/2 - (CABLE_R + 1.2), PLUG_SHOULDER_Y - 5.0, -6.0])
            cube([2 * (CABLE_R + 1.2), 25.0, 18.0]);
    }
}

// Render Assembled State
color([0.05, 0.52, 0.78, 0.95]) vehicle_c_spine();
color([0.13, 0.77, 0.37, 0.95]) slide_keeper();
