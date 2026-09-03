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
    print("Rendering mated_assembly_blueprint.png (3-Part System)...")
    h_mesh = trimesh.load(os.path.join(target_dir, "mated_outer_housing.stl"))
    b_mesh = trimesh.load(os.path.join(target_dir, "mated_outlet_box.stl"))
    c_mesh = trimesh.load(os.path.join(target_dir, "mated_connector.stl"))
    
    fig = plt.figure(figsize=(24, 15), dpi=160)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.04, wspace=0.12, hspace=0.18)
    fig.patch.set_facecolor('#070d19')
    
    fig.suptitle("KIA EV6 / E-GMP 95190-CV780 V2L COMPLETE 3-PART MATED ASSEMBLY\nOuter Housing Bezel + AC Outlet Box + Orange HV Connector (Front-Facing View: Outlet on Right, Connector on Left)",
                 color='white', fontsize=16, weight='bold', y=0.96)
    
    # 1. PANEL 1: FRONT ELEVATION (2D True Projection: X vs Z)
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_facecolor('#0f172a')
    ax1.set_title("PANEL 1: Front Elevation (Cabin View: Outlet on RIGHT, Connector on LEFT)", color='white', fontsize=12, weight='bold', pad=10)
    ax1.tripcolor(h_mesh.vertices[:, 0], h_mesh.vertices[:, 2], h_mesh.faces, facecolors=np.ones(len(h_mesh.faces)), cmap='Blues', alpha=0.35, edgecolors='#1e293b', lw=0.2)
    ax1.tripcolor(b_mesh.vertices[:, 0], b_mesh.vertices[:, 2], b_mesh.faces, facecolors=np.ones(len(b_mesh.faces)), cmap='Greys', alpha=0.6, edgecolors='#0f172a', lw=0.2)
    ax1.tripcolor(c_mesh.vertices[:, 0], c_mesh.vertices[:, 2], c_mesh.faces, facecolors=np.ones(len(c_mesh.faces)), cmap='Oranges', alpha=0.85, edgecolors='#7c2d12', lw=0.2)
    ax1.set_xlim(-85, 85)
    ax1.set_ylim(-15, 115)
    ax1.set_aspect('equal')
    ax1.tick_params(colors='#94a3b8')
    ax1.set_xlabel("X (Width, mm: -X Left / Driver, +X Right / Passenger)", color='#94a3b8', fontsize=10)
    ax1.set_ylabel("Z (Height, mm: Chin Bottom = 0, Roof Rim = 95.40)", color='#94a3b8', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.25, color='#38bdf8')
    
    txt1 = (
        "FRONT CABIN ORIENTATION (CONFIRMED):\n"
        "• LEFT: Orange Connector & Flap Door (-X)\n"
        "• RIGHT: Circular 120V AC Outlet Socket (+X)\n"
        "• [H1] Total Width: 142.30 mm\n"
        "• [H2] Total Height: 95.40 mm (Smooth Curved Roof)\n"
        "• [H3] Window Aperture: 114.60 mm x 50.20 mm [H4]\n"
        "• Chin Protrusion: 27.10 mm Below Aluminum Plate"
    )
    ax1.text(0.03, 0.95, txt1, transform=ax1.transAxes, color='#38bdf8', fontsize=9.5, va='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # 2. PANEL 2: SIDE PROFILE (2D True Projection: Y vs Z)
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor('#0f172a')
    ax2.set_title("PANEL 2: Side Profile (Depth & Seating: Cable Extending Rearward)", color='white', fontsize=12, weight='bold', pad=10)
    ax2.tripcolor(h_mesh.vertices[:, 1], h_mesh.vertices[:, 2], h_mesh.faces, facecolors=np.ones(len(h_mesh.faces)), cmap='Blues', alpha=0.35, edgecolors='#1e293b', lw=0.2)
    ax2.tripcolor(b_mesh.vertices[:, 1], b_mesh.vertices[:, 2], b_mesh.faces, facecolors=np.ones(len(b_mesh.faces)), cmap='Greys', alpha=0.6, edgecolors='#0f172a', lw=0.2)
    ax2.tripcolor(c_mesh.vertices[:, 1], c_mesh.vertices[:, 2], c_mesh.faces, facecolors=np.ones(len(c_mesh.faces)), cmap='Oranges', alpha=0.85, edgecolors='#7c2d12', lw=0.2)
    ax2.set_xlim(-185, 20)
    ax2.set_ylim(-15, 115)
    ax2.set_aspect('equal')
    ax2.tick_params(colors='#94a3b8')
    ax2.set_xlabel("Y (Depth, mm: +Y Cabin Front, -Y Interior Dash Cavity)", color='#94a3b8', fontsize=10)
    ax2.set_ylabel("Z (Height, mm)", color='#94a3b8', fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.25, color='#38bdf8')
    
    txt2 = (
        "CONFIRMED DEPTH & VERTICAL CLEARANCES:\n"
        "• [H17a] Back of Box to Back of Plate: 16.79 mm (Holes Uncovered!)\n"
        "• [H17b] Box Vertical Gap off Plate: 9.10 mm (Centered in Window)\n"
        "• [H7a] Side Wall Depth: 58.80 mm (Gentle 5.6° Wing Slope)\n"
        "• Aluminum Plate: 6.90 mm Below Window Aperture [H16g]\n"
        "• Internal Bend Angle: 84.13° (5.87° Upward Pitch)\n"
        "• Connector Seated Gap: 4.70 mm (17.67 mm Engagement)\n"
        "• Cable Extends Rearward into Dash Cavity (-Y)"
    )
    ax2.text(0.03, 0.95, txt2, transform=ax2.transAxes, color='#38bdf8', fontsize=9.5, va='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # 3. PANEL 3: TOP PLAN VIEW (2D True Projection: X vs Y)
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0f172a')
    ax3.set_title("PANEL 3: Top Plan View (Wings & Floor Plate Span: Looking Down from Above)", color='white', fontsize=12, weight='bold', pad=10)
    ax3.tripcolor(h_mesh.vertices[:, 0], h_mesh.vertices[:, 1], h_mesh.faces, facecolors=np.ones(len(h_mesh.faces)), cmap='Blues', alpha=0.35, edgecolors='#1e293b', lw=0.2)
    ax3.tripcolor(b_mesh.vertices[:, 0], b_mesh.vertices[:, 1], b_mesh.faces, facecolors=np.ones(len(b_mesh.faces)), cmap='Greys', alpha=0.6, edgecolors='#0f172a', lw=0.2)
    ax3.tripcolor(c_mesh.vertices[:, 0], c_mesh.vertices[:, 1], c_mesh.faces, facecolors=np.ones(len(c_mesh.faces)), cmap='Oranges', alpha=0.85, edgecolors='#7c2d12', lw=0.2)
    ax3.set_xlim(-85, 85)
    ax3.set_ylim(-185, 20)
    ax3.set_aspect('equal')
    ax3.tick_params(colors='#94a3b8')
    ax3.set_xlabel("X (Width, mm)", color='#94a3b8', fontsize=10)
    ax3.set_ylabel("Y (Depth, mm: -Y Rearward, +Y Forward)", color='#94a3b8', fontsize=10)
    ax3.grid(True, linestyle='--', alpha=0.25, color='#38bdf8')
    
    txt3 = (
        "HORIZONTAL SPAN & HOLE CLEARANCES:\n"
        "• [H17a] 16.79 mm Clearance Ahead of Rear Plate Edge\n"
        "• Chassis Bolt Holes Completely Exposed (Zero Box Overhang!)\n"
        "• [H11] Inner Wing Clear Span: 140.50 mm\n"
        "• Aluminum Floor Plate Width: 120.20 mm\n"
        "• [H11b] Space Between Wing & Aluminum: 10.15 mm\n"
        "• Connector Placed on Left Flank (Clear of Chassis Bolt)"
    )
    ax3.text(0.03, 0.95, txt3, transform=ax3.transAxes, color='#38bdf8', fontsize=9.5, va='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # 4. PANEL 4: 3D ISOMETRIC VIEW (Cabin Perspective: Looking from Front-Left at Bezel)
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    ax4.set_facecolor('#0f172a')
    ax4.set_title("PANEL 4: 3D Isometric Mated Perspective (Cabin Front-Quarter View)", color='#22c55e', fontsize=12, weight='bold', pad=10)
    
    def add_mesh_3d(mesh, color, edge_color, alpha=0.85):
        v = mesh.vertices
        f = mesh.faces[::2]
        pc = Poly3DCollection(v[f], facecolors=color, alpha=alpha)
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.2)
        ax4.add_collection3d(pc)

    add_mesh_3d(h_mesh, '#334155', '#1e293b', alpha=0.8)
    add_mesh_3d(b_mesh, '#475569', '#0f172a', alpha=0.85)
    add_mesh_3d(c_mesh, '#ea580c', '#7c2d12', alpha=0.95)

    ax4.set_xlim(-85, 85)
    ax4.set_ylim(-185, 20)
    ax4.set_zlim(-10, 110)
    ax4.view_init(elev=22, azim=-125)
    ax4.axis('off')
    
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
