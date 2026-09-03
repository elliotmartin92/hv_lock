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
    
    fig = plt.figure(figsize=(24, 15), dpi=160)
    plt.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.04, wspace=0.10, hspace=0.18)
    fig.patch.set_facecolor('#070d19')
    
    fig.suptitle("V2L CONNECTOR & OUTLET BOX MATED ASSEMBLY\nAccurate Geometric Engagement & Mechanical Clearances",
                 color='white', fontsize=17, weight='bold', y=0.96)
    
    # PANEL 1: Front Elevation Mated View
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    plot_mesh(ax1, mated, edge_color='#475569')
    setup_ax_3d(ax1, "PANEL 1: Front Elevation Mated View",
                xlim=[-5, 128], ylim=[-55, 10], zlim=[-125, 48], elev=0, azim=-90)
    
    txt1 = (
        "CONFIRMED MATED CLEARANCES:\n"
        "• [GAP] Seated Gap: 4.70 mm (confirmed by user)\n"
        "• Collar Insertion Depth: 17.67 mm\n"
        "• Latch Tooth Engaged & Covered (Inside Shroud!)\n"
        "• Forward-Facing Latch Tower under Box Relief Notch\n"
        "• 4.00 mm Clearance to Silver Stamped Bracket"
    )
    ax1.text2D(0.03, 0.95, txt1, transform=ax1.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 2: Left Side Elevation Mated View
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    plot_mesh(ax2, mated, edge_color='#475569')
    setup_ax_3d(ax2, "PANEL 2: Left Side Elevation (Depth Profile & Seating)",
                xlim=[-5, 128], ylim=[-65, 10], zlim=[-125, 48], elev=0, azim=180)
    
    txt2 = (
        "SIDE DEPTH ALIGNMENT:\n"
        "• Front Flush Alignment (Latch Tower to Box Front)\n"
        "• 12.45 mm Rear Lid Overhang Shelf\n"
        "• Box Depth: 48.15 mm\n"
        "• 3 Vertical Side Wall Grooves Clear\n"
        "• Plug Shoulder Seated at -4.70 mm"
    )
    ax2.text2D(0.03, 0.95, txt2, transform=ax2.transAxes, color='#38bdf8', fontsize=9.5,
               va='top', linespacing=1.35,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#0b1329', edgecolor='#38bdf8', alpha=0.92, lw=1.2))

    # PANEL 3: 2D Longitudinal Cutaway Section
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0b1329')
    ax3.set_title("PANEL 3: Longitudinal Cross-Section of Mated Interface", color='white', fontsize=12.5, weight='bold', pad=12)
    
    # 2D cross-section schematic
    # Box body at Z = 0 to 42.67
    ax3.fill([-25, 45, 45, -25, -25], [0, 0, 42.67, 42.67, 0], color='#334155', alpha=0.95, label='Outlet Box Body')
    # Lid with 12.45mm rear overhang
    ax3.fill([-37.45, 45, 45, -37.45, -37.45], [38.09, 38.09, 42.67, 42.67, 38.09], color='#1e293b', alpha=0.95, label='Lid (12.45mm Overhang)')
    # Collar protruding down to -22.37mm
    ax3.fill([-11.35, 11.35, 11.35, -11.35, -11.35], [-22.37, -22.37, 0, 0, -22.37], color='#0f172a', edgecolor='#94a3b8', lw=2.0, label='Receptacle Collar')
    # Latch tooth at Z = -13.64mm
    ax3.fill([11.35, 14.05, 14.05, 11.35, 11.35], [-15.0, -15.0, -12.3, -12.3, -15.0], color='#ef4444', label='Covered Latch Tooth')
    # Orange connector shroud (rim at -4.70mm, body down to -59.30mm)
    ax3.plot([12.55, 12.55, 15.5, 15.5, -12.55, -12.55], [-4.70, -32.0, -32.0, -59.3, -59.3, -4.70], color='#ea580c', lw=3.0, label='Orange Connector Shroud')
    # Latch tower with foam tape
    ax3.plot([12.55, 22.0, 22.0, 15.5], [-4.70, -4.70, -41.45, -41.45], color='#f97316', lw=2.5, label='Latch Tower & Foam Wrap')
    
    # Dimension lines on 2D section
    draw_dim_arrow(ax3, (16.0, 0), (16.0, -4.70), "4.70 mm Seated Gap", offset=(8.0, 0), color='#38bdf8')
    draw_dim_arrow(ax3, (-14.0, 0), (-14.0, -22.37), "22.37 mm Collar", offset=(-10.0, 0), color='#facc15')
    draw_dim_arrow(ax3, (-28.0, -4.70), (-28.0, -22.37), "17.67 mm Engagement", offset=(-8.0, 0), color='#4ade80')
    draw_dim_arrow(ax3, (-37.45, 45.0), (-25.0, 45.0), "12.45 mm Overhang", offset=(0, 2.5), color='#f43f5e')
    
    ax3.set_xlim(-55, 55)
    ax3.set_ylim(-70, 55)
    ax3.set_aspect('equal')
    ax3.axis('off')
    ax3.legend(loc='lower left', facecolor='#070d19', edgecolor='#334155', labelcolor='white', fontsize=8.5)

    # PANEL 4: 3D Isometric View
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    plot_mesh(ax4, mated, edge_color='#475569')
    setup_ax_3d(ax4, "PANEL 4: 3D Isometric Mated Perspective",
                xlim=[-10, 130], ylim=[-68, 10], zlim=[-125, 52], elev=28, azim=-55)
    
    for b_dir in [target_dir, artifact_dir]:
        plt.savefig(os.path.join(b_dir, "mated_assembly_blueprint.png"), facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Saved mated_assembly_blueprint.png")

if __name__ == '__main__':
    render_connector_blueprint()
    render_outlet_box_blueprint()
    render_mated_blueprint()
    print("All blueprints successfully rendered!")
