// ==============================================================================
// Kia EV6 / E-GMP V2L Exterior Cable Lock - OpenSCAD Parametric Source
// Calibrated from User Caliper Measurements
// ==============================================================================

// Dimensional Constants (mm)
tower_width = 19.06;        // [A3]
tower_length = 36.75;      // [B1]
tooth_dist = 8.73; // [C2]
tooth_width = 2.0;  // [C3]
tooth_height = 2.7;// [C4]
slide_stroke = 8.5;      // [B3]
clearance_slip = 0.35;  // FDM print clearance

// Modules
module saddle_base() {
    difference() {
        translate([0, 16, -4.5]) cube([23.96, 32, 15], center=true);
        translate([0, 16, -6.5]) cube([19.56, 34, 13], center=true);
    }
    translate([0, 16, 4]) cube([11, 32, 2], center=true);
    translate([0, 16, 6]) cube([15, 32, 2], center=true);
    translate([0, 30.5, 5]) cube([23.96, 3, 5.5], center=true);
}

module sliding_deadbolt() {
    difference() {
        translate([0, 10, 6.5]) cube([23.96, 20, 7], center=true);
        translate([0, 10, 4]) cube([11.7, 22, 3.35], center=true);
        translate([0, 10, 6]) cube([15.7, 22, 2.35], center=true);
    }
    difference() {
        translate([0, -7, 3.6]) cube([11.5, 14, 4.2], center=true);
        translate([0, -8, 3.1]) cube([4, 3.5, 3.2], center=true);
    }
    for (y = [4, 7.5, 11, 14.5, 17.5]) {
        translate([0, y, 10.45]) cube([19.96, 1.2, 0.9], center=true);
    }
}

saddle_base();
translate([35, 0, 0]) sliding_deadbolt();
