"""
render_accurate_blueprints.py
Generates clean, dimensioned technical blueprints and 3D isometric visualizations:
1. connector_blueprint.png
2. outlet_box_blueprint.png
3. mated_assembly_blueprint.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh

target_dir = os.path.dirname(os.path.abspath(__file__))
artifact_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\adc92446-2de3-4394-b3dd-ecf0f0ccb51d"

def plot_mesh(ax, mesh, color=None, alpha=0.95, edge_color=None, max_faces=6000):
    m = mesh.copy()
    v = m.vertices
    f = m.faces
    if len(f) > max_faces:
        step = int(np.ceil(len(f) / max_faces))
        f = f[::step]
    triangles = v[f]
    
    if color is None:
        if hasattr(m.visual, 'vertex_colors') and len(m.visual.vertex_colors) > 0:
            face_colors = np.mean(m.visual.vertex_colors[f], axis=1) / 255.0
            pc = Poly3DCollection(triangles, facecolors=face_colors, alpha=alpha)
        else:
            pc = Poly3DCollection(triangles, facecolors='#ea580c', alpha=alpha)
    else:
        pc = Poly3DCollection(triangles, facecolors=color, alpha=alpha)
        
    if edge_color:
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.3)
    ax.add_collection3d(pc)

def setup_ax_3d(ax, title, xlim, ylim, zlim, elev=25, azim=-55):
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    ax.view_init(elev=elev, azim=azim)
    ax.axis('off')
    ax.set_facecolor('#0b1329')
    ax.set_title(title, color='white', fontsize=12.5, weight='bold', pad=12)

def draw_dim_arrow(ax, p1, p2, text, offset=(0, 0), color='#38bdf8', fontsize=9.5, ha='center', va='center'):
    ax.annotate('', xy=p1, xytext=p2, arrowprops=dict(arrowstyle='<->', color=color, lw=1.8))
    mid_x = (p1[0] + p2[0]) / 2.0 + offset[0]
    mid_y = (p1[1] + p2[1]) / 2.0 + offset[1]
    ax.text(mid_x, mid_y, text, color=color, fontsize=fontsize, weight='bold', ha=ha, va=va,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#070d19', edgecolor=color, lw=1.2, alpha=0.9))

# ==============================================================================
# 1. RENDER CONNECTOR BLUEPRINT
# ==============================================================================
def render_connector_blueprint():
    print("Rendering connector_blueprint.png...")
    conn = trimesh.load(os.path.join(target_dir, "connector_model.obj"))
    
    fig = plt.figure(figsize=(24, 15), dpi=160)
    plt.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.04, wspace=0.10, hspace=0.18)
    fig.patch.set_facecolor('#070d19')
    
    fig.suptitle("V2L ORANGE CABLE CONNECTOR (KIA EV6 / E-GMP 95190-CV780)\nForensic Caliper-Calibrated 3D CAD Blueprint",
                 color='white', fontsize=17, weight='bold', y=0.96)
    
    # PANEL 1: Front Mating Face (Looking into +Z rim)
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    plot_mesh(ax1, conn, edge_color='#7c2d12')
    setup_ax_3d(ax1, "PANEL 1: Front Mating Face View (Looking into Plug Cavity)",
                xlim=[-24, 24], ylim=[-16, 28], zlim=[-35, 5], elev=90, azim=-90)
    
    txt1 = (
        "PANEL A DIMENSIONS CONFIRMED:\n"
        "• [A1] Shroud Outer Width: 36.10 mm (incl. tab)\n"
        "• [A2] Shroud Body Height: 20.80 mm\n"
        "• [A3] Tower Outer Width: 19.06 mm\n"
        "• [A4] Total Plug Height: 37.11 mm\n"
        "• [A5] Shroud Wall Thickness: 1.20 mm\n"
        "• [A6] Side Key Rib Protrusion: 4.80 mm\n"
        "------------------------------------\n"
        "INTERNAL FEATURES:\n"
        "• Red silicone perimeter sealing gasket\n"
        "• Grey dielectric core with dual AC leaf contacts\n"
        "• Front open portal for collar latch tooth"
    )
    ax1.text2D(0.03, 0.95, txt1, transform=ax1.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 2: Side Profile View (Looking along X Axis)
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    plot_mesh(ax2, conn, edge_color='#7c2d12')
    setup_ax_3d(ax2, "PANEL 2: Side Profile View (Showing Length & Clamp Ring)",
                xlim=[-24, 24], ylim=[-18, 28], zlim=[-115, 5], elev=0, azim=0)
    
    txt2 = (
        "PANEL B DIMENSIONS CONFIRMED:\n"
        "• [B1] Tower Axial Length: 36.75 mm\n"
        "• [B7] Body Rigid Length: 54.60 mm\n"
        "• [A4] Total Height: 37.11 mm\n"
        "• Front Protective Black Foam Tape Wrap\n"
        "• Black Dual-Snap Retention Clamp Ring\n"
        "• Yellow Spiral Protective Cable Wrap\n"
        "• Contoured Ergonomic Side Thumb Recesses"
    )
    ax2.text2D(0.03, 0.95, txt2, transform=ax2.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 3: Top Plan View (Looking down at Latch Tower along Y Axis)
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    plot_mesh(ax3, conn, edge_color='#7c2d12')
    setup_ax_3d(ax3, "PANEL 3: Top Plan View (Latch Tower & CPA Carriage)",
                xlim=[-24, 24], ylim=[-16, 28], zlim=[-65, 5], elev=0, azim=-90)
    
    txt3 = (
        "CPA SLIDER & MECHANISM:\n"
        "• [B2] Slider Track Inner Width: 17.80 mm\n"
        "• [B3] Slider Stroke Length: 8.25 mm\n"
        "• [B4] Slider Total Length: 23.00 mm\n"
        "• [B5] Slider Width: 7.30 mm\n"
        "• [B6] Slider Thickness: 4.45 mm\n"
        "• 4 raised tactile grip ridges on thumb pad\n"
        "• Yellow CPA guide carriage inside tower"
    )
    ax3.text2D(0.03, 0.95, txt3, transform=ax3.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 4: 3D Isometric View
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    plot_mesh(ax4, conn, edge_color='#7c2d12')
    setup_ax_3d(ax4, "PANEL 4: 3D Isometric Perspective View",
                xlim=[-30, 30], ylim=[-22, 30], zlim=[-110, 10], elev=28, azim=-55)
    
    for b_dir in [target_dir, artifact_dir]:
        plt.savefig(os.path.join(b_dir, "connector_blueprint.png"), facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Saved connector_blueprint.png")

# ==============================================================================
# 2. RENDER OUTLET BOX BLUEPRINT
# ==============================================================================
def render_outlet_box_blueprint():
    print("Rendering outlet_box_blueprint.png...")
    box = trimesh.load(os.path.join(target_dir, "outlet_box_model.obj"))
    
    fig = plt.figure(figsize=(24, 15), dpi=160)
    plt.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.04, wspace=0.10, hspace=0.18)
    fig.patch.set_facecolor('#070d19')
    
    fig.suptitle("VEHICLE OUTLET BOX MODULE (KIA EV6 / E-GMP 95190-CV780)\nForensic Caliper-Calibrated 3D CAD Blueprint",
                 color='white', fontsize=17, weight='bold', y=0.96)
    
    # PANEL 1: Front Elevation View
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    plot_mesh(ax1, box, edge_color='#64748b')
    setup_ax_3d(ax1, "PANEL 1: Front Elevation View (Installed Orientation)",
                xlim=[-5, 128], ylim=[-55, 5], zlim=[-28, 48], elev=0, azim=-90)
    
    txt1 = (
        "ENCLOSURE & RECEPTACLE DIMENSIONS:\n"
        "• Long Axis (Box Width alone): 111.75 mm\n"
        "• [E1] Vertical Box Height: 42.67 mm\n"
        "• [C1] Collar Protrusion: 22.37 mm\n"
        "• [D3] Metal Plate Clearance: 4.00 mm\n"
        "• Front Latch Relief Notch for Connector Latch\n"
        "• Dual Front Lid Snap Retention Claws"
    )
    ax1.text2D(0.03, 0.95, txt1, transform=ax1.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 2: Left Side Elevation (Showing Depth & Rear Overhang)
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    plot_mesh(ax2, box, edge_color='#64748b')
    setup_ax_3d(ax2, "PANEL 2: Left Side Elevation (Depth & Rear Lid Overhang)",
                xlim=[-5, 128], ylim=[-65, 5], zlim=[-28, 48], elev=0, azim=180)
    
    txt2 = (
        "DEPTH & OVERHANG DIMENSIONS:\n"
        "• [E2] Front-to-Back Depth: 48.15 mm\n"
        "• [E3a] Lid Overhang Lip Thickness: 4.58 mm\n"
        "• [E3b] Lid Rear Overhang Width: 12.45 mm\n"
        "• 3 Vertical Recessed Grooves on Side Wall\n"
        "• Front-Biased Collar Position (Clearance Behind)"
    )
    ax2.text2D(0.03, 0.95, txt2, transform=ax2.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 3: Bottom Seating Plan View (Looking up at Collar Port)
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    plot_mesh(ax3, box, edge_color='#64748b')
    setup_ax_3d(ax3, "PANEL 3: Bottom Seating Face & Collar Port Features",
                xlim=[-5, 128], ylim=[-65, 5], zlim=[-28, 48], elev=-90, azim=-90)
    
    txt3 = (
        "PORT & CONTACT FEATURES:\n"
        "• [D2] Collar Outer Span: 33.05 mm (along X axis)\n"
        "• [D1] Collar Outer Width: 22.70 mm (along Y axis)\n"
        "• [C2] Tooth Distance from Rim: 8.73 mm\n"
        "• [C3] Latch Tooth Width: 2.00 mm\n"
        "• [C4] Latch Tooth Height: 2.70 mm\n"
        "• [C5] Flanking Guide Ribs: 13.82 mm outside span\n"
        "• Dual Internal AC Blade Terminals (ACL, ACN)"
    )
    ax3.text2D(0.03, 0.95, txt3, transform=ax3.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 4: 3D Isometric View
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    plot_mesh(ax4, box, edge_color='#64748b')
    setup_ax_3d(ax4, "PANEL 4: 3D Isometric Perspective View",
                xlim=[-10, 130], ylim=[-68, 10], zlim=[-28, 52], elev=28, azim=-55)
    
    for b_dir in [target_dir, artifact_dir]:
        plt.savefig(os.path.join(b_dir, "outlet_box_blueprint.png"), facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Saved outlet_box_blueprint.png")

# ==============================================================================
# 3. RENDER MATED ASSEMBLY BLUEPRINT
# ==============================================================================
def render_mated_blueprint():
    print("Rendering mated_assembly_blueprint.png...")
    mated = trimesh.load(os.path.join(target_dir, "mated_assembly.obj"))
    
def render_mated_blueprint():
    print("Rendering mated_assembly_blueprint.png (3-Part System)...")
    h_mesh = trimesh.load(os.path.join(target_dir, "mated_outer_housing.stl"))
    b_mesh = trimesh.load(os.path.join(target_dir, "mated_outlet_box.stl"))
    c_mesh = trimesh.load(os.path.join(target_dir, "mated_connector.stl"))
    
    fig = plt.figure(figsize=(24, 15), dpi=160)
    plt.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.04, wspace=0.10, hspace=0.18)
    fig.patch.set_facecolor('#070d19')
    
    fig.suptitle("KIA EV6 / E-GMP 95190-CV780 V2L COMPLETE 3-PART MATED ASSEMBLY\nOuter Housing Bezel + AC Outlet Box + Orange HV Connector",
                 color='white', fontsize=17, weight='bold', y=0.96)
    
    # PANEL 1: Front Elevation Mated View (Cabin Perspective)
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    plot_mesh(ax1, h_mesh, color='#334155', edge_color='#1e293b')
    plot_mesh(ax1, b_mesh, color='#475569', edge_color='#0f172a')
    plot_mesh(ax1, c_mesh, color='#ea580c', edge_color='#7c2d12')
    setup_ax_3d(ax1, "PANEL 1: Front Elevation Mated View (Cabin Perspective)",
                xlim=[-85, 85], ylim=[-75, 15], zlim=[-10, 110], elev=0, azim=90)
    
    txt1 = (
        "CONFIRMED FRONT INTERFACE:\n"
        "• [H1] Total Outer Width: 142.30 mm\n"
        "• [H2] Total Outer Height: 95.40 mm (100% Smooth Arch)\n"
        "• [H3] Window Aperture: 114.60 mm x 50.20 mm [H4]\n"
        "• Outlet Box Seated Centered with 1.42 mm Side Gap\n"
        "• Left: Spring Flap Door ('Max AC 120V, 16A')\n"
        "• Right: Circular NEMA 5-15R 120V AC Outlet\n"
        "• Lower Chin Protrusion: 27.10 mm Below Plate"
    )
    ax1.text2D(0.03, 0.95, txt1, transform=ax1.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 2: Left Side Elevation Mated View
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    plot_mesh(ax2, h_mesh, color='#334155', edge_color='#1e293b')
    plot_mesh(ax2, b_mesh, color='#475569', edge_color='#0f172a')
    plot_mesh(ax2, c_mesh, color='#ea580c', edge_color='#7c2d12')
    setup_ax_3d(ax2, "PANEL 2: Side Elevation Mated View (Depth & Seating)",
                xlim=[-85, 85], ylim=[-185, 15], zlim=[-10, 110], elev=0, azim=0)
    
    txt2 = (
        "SIDE DEPTH & CLEARANCES:\n"
        "• [H7a] Side Wall Depth: 58.80 mm (Gentle 5.6° Wing Slope)\n"
        "• Wings Flush Under Curved Roof Arch (Never Extend Above)\n"
        "• Aluminum Plate: 6.90 mm Below Window Aperture\n"
        "• Internal Bend Angle: 84.13° (5.87° Upward Pitch)\n"
        "• Connector Plugs into Rear Collar at Z = 44.65 mm\n"
        "• Verified Seated Gap: 4.70 mm\n"
        "• Heavy-Gauge Cable Extends Rearward into Dash Cavity"
    )
    ax2.text2D(0.03, 0.95, txt2, transform=ax2.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 3: Top Plan Mated View
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    plot_mesh(ax3, h_mesh, color='#334155', edge_color='#1e293b')
    plot_mesh(ax3, b_mesh, color='#475569', edge_color='#0f172a')
    plot_mesh(ax3, c_mesh, color='#ea580c', edge_color='#7c2d12')
    setup_ax_3d(ax3, "PANEL 3: Top Plan Mated View (Wings & Floor Plate Span)",
                xlim=[-85, 85], ylim=[-185, 15], zlim=[-10, 110], elev=90, azim=-90)
    
    txt3 = (
        "HORIZONTAL CLEARANCES:\n"
        "• [H11] Inner Wing Clear Span: 140.50 mm\n"
        "• Aluminum Floor Plate Width: 120.20 mm\n"
        "• [H11b] Space Between Wing & Aluminum: 10.15 mm\n"
        "• Aluminum Floor Holes: 7.45x6.45 Oval + Ø 6.45 Round\n"
        "• Central Hole 7.60 mm from Back, Oval 7.30 mm from Back\n"
        "• Connector Placed on Left Flank (Clear of Chassis Bolt)"
    )
    ax3.text2D(0.03, 0.95, txt3, transform=ax3.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 4: 3D Isometric View
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    plot_mesh(ax4, h_mesh, color='#334155', edge_color='#1e293b')
    plot_mesh(ax4, b_mesh, color='#475569', edge_color='#0f172a')
    plot_mesh(ax4, c_mesh, color='#ea580c', edge_color='#7c2d12')
    setup_ax_3d(ax4, "PANEL 4: 3D Isometric Mated Perspective",
                xlim=[-85, 85], ylim=[-185, 15], zlim=[-10, 110], elev=25, azim=-55)
    
    art_dir = r"C:\Users\Elliot\.gemini\antigravity\brain\ca2c4a5c-394a-4c0b-b99d-8dde76573538"
    os.makedirs(art_dir, exist_ok=True)
    for b_dir in [target_dir, art_dir]:
        plt.savefig(os.path.join(b_dir, "mated_assembly_blueprint.png"), facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Saved mated_assembly_blueprint.png")


if __name__ == '__main__':
    render_connector_blueprint()
    render_outlet_box_blueprint()
    render_mated_blueprint()
    print("All blueprints successfully rendered!")
