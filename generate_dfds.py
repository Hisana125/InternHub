import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'dfd_diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_canvas(width=14, height=10):
    fig, ax = plt.subplots(figsize=(width, height), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax

def draw_entity(ax, x, y, w, h, text, fontsize=12):
    """Draws an external entity (Rectangle)"""
    rect = patches.Rectangle(
        (x, y), w, h,
        edgecolor='black', facecolor='white',
        linewidth=1.8, zorder=3
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha='center', va='center',
        fontsize=fontsize, fontweight='bold',
        color='black', zorder=4
    )

def draw_process_oval(ax, cx, cy, rx, ry, text, fontsize=10):
    """Draws a process node (Ellipse)"""
    ellipse = patches.Ellipse(
        (cx, cy), rx * 2, ry * 2,
        edgecolor='black', facecolor='white',
        linewidth=1.8, zorder=3
    )
    ax.add_patch(ellipse)
    ax.text(
        cx, cy, text,
        ha='center', va='center',
        fontsize=fontsize, color='black',
        zorder=4, multialignment='center'
    )

def draw_process_circle(ax, cx, cy, r, text, fontsize=10):
    """Draws an intermediate circular process"""
    circle = patches.Circle(
        (cx, cy), r,
        edgecolor='black', facecolor='white',
        linewidth=1.8, zorder=3
    )
    ax.add_patch(circle)
    ax.text(
        cx, cy, text,
        ha='center', va='center',
        fontsize=fontsize, color='black',
        zorder=4, multialignment='center'
    )

def draw_datastore(ax, x, y, w, h, text, fontsize=10):
    """Draws an open-ended data store (Gane-Sarson / DeMarco style)"""
    ax.plot([x, x + w], [y + h, y + h], color='black', lw=1.8, zorder=3)
    ax.plot([x, x + w], [y, y], color='black', lw=1.8, zorder=3)
    ax.plot([x, x], [y, y + h], color='black', lw=1.8, zorder=3)
    
    div_x = x + w * 0.12
    ax.plot([div_x, div_x], [y, y + h], color='black', lw=1.8, zorder=3)
    
    ax.text(
        (div_x + x + w) / 2, y + h / 2, text,
        ha='center', va='center',
        fontsize=fontsize, color='black',
        zorder=4, multialignment='center'
    )

def draw_straight_arrow(ax, x1, y1, x2, y2, label=None, label_pos='side', fontsize=9):
    """Draws a straight arrow from (x1, y1) to (x2, y2) with label"""
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle='->,head_width=0.35,head_length=0.45',
            lw=1.3, color='black'
        ),
        zorder=2
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        offset_x, offset_y = 0, 0
        if label_pos == 'top':
            offset_y = 1.6
        elif label_pos == 'bottom':
            offset_y = -1.8
        elif label_pos == 'left':
            offset_x = -3.4
        elif label_pos == 'right':
            offset_x = 3.4
        ax.text(
            mx + offset_x, my + offset_y, label,
            ha='center', va='center',
            fontsize=fontsize, color='black',
            zorder=5
        )

def draw_bidirectional_arrow(ax, x1, y1, x2, y2):
    """Draws a bidirectional arrow between two nodes"""
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle='<->,head_width=0.35,head_length=0.45',
            lw=1.3, color='black'
        ),
        zorder=2
    )


# =============================================================================
# 1. LEVEL 0 DFD (CONTEXT DIAGRAM)
# =============================================================================
def generate_level_0():
    fig, ax = setup_canvas(width=13, height=8.5)
    
    # Center: Process 0
    draw_process_oval(ax, 50, 40, 16, 12, "Internship Management\nSystem\n(InternHub)", fontsize=13)
    
    # Top Entity: Admin
    draw_entity(ax, 41, 75, 18, 14, "Admin", fontsize=13)
    
    # Left Entity: Student
    draw_entity(ax, 6, 33, 18, 14, "Student", fontsize=13)
    
    # Right Entity: Company
    draw_entity(ax, 76, 33, 18, 14, "Company", fontsize=13)
    
    # Admin <-> Center
    draw_straight_arrow(ax, 46, 75, 46, 52, label="Request", label_pos='left', fontsize=10)
    draw_straight_arrow(ax, 54, 52, 54, 75, label="Response", label_pos='right', fontsize=10)
    
    # Student <-> Center
    draw_straight_arrow(ax, 24, 43, 34, 43, label="Request", label_pos='top', fontsize=10)
    draw_straight_arrow(ax, 34, 37, 24, 37, label="Response", label_pos='bottom', fontsize=10)
    
    # Company <-> Center
    draw_straight_arrow(ax, 76, 43, 66, 43, label="Request", label_pos='top', fontsize=10)
    draw_straight_arrow(ax, 66, 37, 76, 37, label="Response", label_pos='bottom', fontsize=10)
    
    out_path = os.path.join(OUTPUT_DIR, 'dfd_level_0.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")


# =============================================================================
# 2. LEVEL 1 ADMIN DFD
# =============================================================================
def generate_level_1_admin():
    fig, ax = setup_canvas(width=14, height=11)
    
    ax.text(50, 94, "DATA FLOW DIAGRAM (DFD) - LEVEL 1 ADMIN", ha='center', va='center', fontsize=15, fontweight='bold')
    ax.plot([15, 85], [91, 91], color='black', lw=1.5)
    
    draw_entity(ax, 5, 40, 14, 10, "Admin", fontsize=12)
    
    draw_process_circle(ax, 26, 45, 4.5, "Login", fontsize=10)
    draw_straight_arrow(ax, 19, 45, 21.5, 45)
    
    draw_datastore(ax, 18, 72, 16, 7, "Admin Table", fontsize=10)
    draw_bidirectional_arrow(ax, 26, 49.5, 26, 72)
    
    process_list = [
        ("View Dashboard\n& Statistics", "Dashboard", 81),
        ("Manage\nInternships", "Table Internships", 63),
        ("Manage\nApplications", "Table Applications", 45),
        ("View Registered\nStudents", "Table Students", 27),
        ("Manage\nNotifications", "Table Notifications", 9),
    ]
    
    stem_x = 37
    ax.plot([30.5, stem_x], [45, 45], color='black', lw=1.3)
    ax.plot([stem_x, stem_x], [9, 81], color='black', lw=1.3)
    
    for proc_name, store_name, y_pos in process_list:
        draw_straight_arrow(ax, stem_x, y_pos, 42.5, y_pos)
        draw_process_oval(ax, 54, y_pos, 11.5, 5.8, proc_name, fontsize=10)
        draw_bidirectional_arrow(ax, 65.5, y_pos, 77, y_pos)
        draw_datastore(ax, 77, y_pos - 4.5, 19, 9, store_name, fontsize=10)
        
    out_path = os.path.join(OUTPUT_DIR, 'dfd_level_1_admin.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")


# =============================================================================
# 3. LEVEL 1 STUDENT DFD
# =============================================================================
def generate_level_1_student():
    fig, ax = setup_canvas(width=14, height=11)
    
    ax.text(50, 94, "DATA FLOW DIAGRAM (DFD) - LEVEL 1 STUDENT", ha='center', va='center', fontsize=15, fontweight='bold')
    ax.plot([15, 85], [91, 91], color='black', lw=1.5)
    
    draw_entity(ax, 5, 40, 14, 10, "Student", fontsize=12)
    
    draw_process_circle(ax, 26, 45, 4.5, "Login /\nRegister", fontsize=9.5)
    draw_straight_arrow(ax, 19, 45, 21.5, 45)
    
    draw_datastore(ax, 18, 72, 16, 7, "Student Table", fontsize=10)
    draw_bidirectional_arrow(ax, 26, 49.5, 26, 72)
    
    process_list = [
        ("Manage Student\nProfile", "Table Students", 81),
        ("Search & Browse\nInternships", "Table Internships", 63),
        ("Apply for\nInternship", "Table Applications", 45),
        ("Track Application\nStatus", "Table Applications", 27),
        ("View In-App\nNotifications", "Table Notifications", 9),
    ]
    
    stem_x = 37
    ax.plot([30.5, stem_x], [45, 45], color='black', lw=1.3)
    ax.plot([stem_x, stem_x], [9, 81], color='black', lw=1.3)
    
    for proc_name, store_name, y_pos in process_list:
        draw_straight_arrow(ax, stem_x, y_pos, 42.5, y_pos)
        draw_process_oval(ax, 54, y_pos, 11.5, 5.8, proc_name, fontsize=10)
        draw_bidirectional_arrow(ax, 65.5, y_pos, 77, y_pos)
        draw_datastore(ax, 77, y_pos - 4.5, 19, 9, store_name, fontsize=10)
        
    out_path = os.path.join(OUTPUT_DIR, 'dfd_level_1_student.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")


# =============================================================================
# 4. LEVEL 1 COMPANY DFD
# =============================================================================
def generate_level_1_company():
    fig, ax = setup_canvas(width=14, height=11)
    
    ax.text(50, 94, "DATA FLOW DIAGRAM (DFD) - LEVEL 1 COMPANY", ha='center', va='center', fontsize=15, fontweight='bold')
    ax.plot([15, 85], [91, 91], color='black', lw=1.5)
    
    draw_entity(ax, 5, 40, 14, 10, "Company", fontsize=12)
    
    draw_process_circle(ax, 26, 45, 4.5, "Login /\nRegister", fontsize=9.5)
    draw_straight_arrow(ax, 19, 45, 21.5, 45)
    
    draw_datastore(ax, 18, 72, 16, 7, "Company Table", fontsize=10)
    draw_bidirectional_arrow(ax, 26, 49.5, 26, 72)
    
    process_list = [
        ("View Recruiter\nDashboard", "Dashboard", 81),
        ("Post & Manage\nInternships", "Table Internships", 63),
        ("View Applicant\nProfiles", "Table Students", 45),
        ("Update Application\nStatus", "Table Applications", 27),
        ("Send Alerts &\nNotifications", "Table Notifications", 9),
    ]
    
    stem_x = 37
    ax.plot([30.5, stem_x], [45, 45], color='black', lw=1.3)
    ax.plot([stem_x, stem_x], [9, 81], color='black', lw=1.3)
    
    for proc_name, store_name, y_pos in process_list:
        draw_straight_arrow(ax, stem_x, y_pos, 42.5, y_pos)
        draw_process_oval(ax, 54, y_pos, 11.5, 5.8, proc_name, fontsize=10)
        draw_bidirectional_arrow(ax, 65.5, y_pos, 77, y_pos)
        draw_datastore(ax, 77, y_pos - 4.5, 19, 9, store_name, fontsize=10)
        
    out_path = os.path.join(OUTPUT_DIR, 'dfd_level_1_company.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")


# =============================================================================
# 5. LEVEL 2 ADMIN DFD (SPACING PERFECTED)
# =============================================================================
def generate_level_2_admin():
    fig, ax = setup_canvas(width=15, height=13)
    
    ax.text(6, 95, "Level 2 Admin", ha='left', va='center', fontsize=16, fontweight='bold')
    
    # Left Entity: Admin
    draw_entity(ax, 3, 43, 13, 11, "Admin", fontsize=12)
    
    # 3 Intermediate Circles
    # Group 1: 4 items (y = 89, 82, 75, 68) -> circle center = 78.5
    # Group 2: 3 items (y = 56, 48.5, 41)   -> circle center = 48.5
    # Group 3: 2 items (y = 26, 17)         -> circle center = 21.5
    circles = [
        ("Manage\nInternships", 78.5),
        ("Manage\nApplications", 48.5),
        ("Manage\nStudents", 21.5),
    ]
    
    stem1_x = 21
    ax.plot([16, stem1_x], [48.5, 48.5], color='black', lw=1.3)
    ax.plot([stem1_x, stem1_x], [21.5, 78.5], color='black', lw=1.3)
    
    for name, cy in circles:
        draw_straight_arrow(ax, stem1_x, cy, 25.5, cy)
        draw_process_circle(ax, 31.5, cy, 6, name, fontsize=9.5)
        
    # Group 1: Sub-processes of Manage Internships
    g1_subs = [
        ("Post Internship", 89, 'single'),
        ("View Internships", 82, 'bi'),
        ("Edit Internship", 75, 'single'),
        ("Delete / Close", 68, 'single')
    ]
    stem_g1 = 43
    ax.plot([37.5, stem_g1], [78.5, 78.5], color='black', lw=1.3)
    ax.plot([stem_g1, stem_g1], [68, 89], color='black', lw=1.3)
    
    for sub_name, sy, arrow_type in g1_subs:
        draw_straight_arrow(ax, stem_g1, sy, 48.5, sy)
        draw_process_oval(ax, 57.5, sy, 9, 2.7, sub_name, fontsize=9.5)
        if arrow_type == 'bi':
            draw_bidirectional_arrow(ax, 66.5, sy, 79, sy)
        else:
            draw_straight_arrow(ax, 66.5, sy, 79, sy)
        draw_datastore(ax, 79, sy - 2.2, 17, 4.4, "Table Internships", fontsize=9)
        
    # Group 2: Sub-processes of Manage Applications
    g2_subs = [
        ("View Requests", 56, 'bi'),
        ("Approve / Select", 48.5, 'single'),
        ("Reject Application", 41, 'single')
    ]
    stem_g2 = 43
    ax.plot([37.5, stem_g2], [48.5, 48.5], color='black', lw=1.3)
    ax.plot([stem_g2, stem_g2], [41, 56], color='black', lw=1.3)
    
    for sub_name, sy, arrow_type in g2_subs:
        draw_straight_arrow(ax, stem_g2, sy, 48.5, sy)
        draw_process_oval(ax, 57.5, sy, 9, 2.7, sub_name, fontsize=9.5)
        if arrow_type == 'bi':
            draw_bidirectional_arrow(ax, 66.5, sy, 79, sy)
        else:
            draw_straight_arrow(ax, 66.5, sy, 79, sy)
        draw_datastore(ax, 79, sy - 2.2, 17, 4.4, "Table Applications", fontsize=9)
        
    # Group 3: Sub-processes of Manage Students
    g3_subs = [
        ("View Students", 26, 'bi'),
        ("Manage / Suspend", 17, 'single')
    ]
    stem_g3 = 43
    ax.plot([37.5, stem_g3], [21.5, 21.5], color='black', lw=1.3)
    ax.plot([stem_g3, stem_g3], [17, 26], color='black', lw=1.3)
    
    for sub_name, sy, arrow_type in g3_subs:
        draw_straight_arrow(ax, stem_g3, sy, 48.5, sy)
        draw_process_oval(ax, 57.5, sy, 9, 2.7, sub_name, fontsize=9.5)
        if arrow_type == 'bi':
            draw_bidirectional_arrow(ax, 66.5, sy, 79, sy)
        else:
            draw_straight_arrow(ax, 66.5, sy, 79, sy)
        draw_datastore(ax, 79, sy - 2.2, 17, 4.4, "Table Students", fontsize=9)
        
    out_path = os.path.join(OUTPUT_DIR, 'dfd_level_2_admin.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")


# =============================================================================
# 6. LEVEL 2 COMPANY DFD (SPACING PERFECTED)
# =============================================================================
def generate_level_2_company():
    fig, ax = setup_canvas(width=15, height=13)
    
    ax.text(6, 95, "Level 2 Company", ha='left', va='center', fontsize=16, fontweight='bold')
    
    draw_entity(ax, 3, 43, 13, 11, "Company", fontsize=12)
    
    circles = [
        ("Manage\nPostings", 78.5),
        ("Review &\nScreening", 48.5),
        ("Manage\nAlerts", 21.5),
    ]
    
    stem1_x = 21
    ax.plot([16, stem1_x], [48.5, 48.5], color='black', lw=1.3)
    ax.plot([stem1_x, stem1_x], [21.5, 78.5], color='black', lw=1.3)
    
    for name, cy in circles:
        draw_straight_arrow(ax, stem1_x, cy, 25.5, cy)
        draw_process_circle(ax, 31.5, cy, 6, name, fontsize=9.5)
        
    # Group 1: Sub-processes of Manage Postings
    g1_subs = [
        ("Create Posting", 89, 'single', "Table Internships"),
        ("View Postings", 82, 'bi', "Table Internships"),
        ("Edit Job Criteria", 75, 'single', "Table Internships"),
        ("Close Posting", 68, 'single', "Table Internships")
    ]
    stem_g1 = 43
    ax.plot([37.5, stem_g1], [78.5, 78.5], color='black', lw=1.3)
    ax.plot([stem_g1, stem_g1], [68, 89], color='black', lw=1.3)
    
    for sub_name, sy, arrow_type, store in g1_subs:
        draw_straight_arrow(ax, stem_g1, sy, 48.5, sy)
        draw_process_oval(ax, 57.5, sy, 9, 2.7, sub_name, fontsize=9.5)
        if arrow_type == 'bi':
            draw_bidirectional_arrow(ax, 66.5, sy, 79, sy)
        else:
            draw_straight_arrow(ax, 66.5, sy, 79, sy)
        draw_datastore(ax, 79, sy - 2.2, 17, 4.4, store, fontsize=9)
        
    # Group 2: Sub-processes of Review & Screening
    g2_subs = [
        ("View Applicants", 56, 'bi', "Table Applications"),
        ("View Profile Details", 48.5, 'bi', "Table Students"),
        ("Update Status", 41, 'single', "Table Applications")
    ]
    stem_g2 = 43
    ax.plot([37.5, stem_g2], [48.5, 48.5], color='black', lw=1.3)
    ax.plot([stem_g2, stem_g2], [41, 56], color='black', lw=1.3)
    
    for sub_name, sy, arrow_type, store in g2_subs:
        draw_straight_arrow(ax, stem_g2, sy, 48.5, sy)
        draw_process_oval(ax, 57.5, sy, 9, 2.7, sub_name, fontsize=9.5)
        if arrow_type == 'bi':
            draw_bidirectional_arrow(ax, 66.5, sy, 79, sy)
        else:
            draw_straight_arrow(ax, 66.5, sy, 79, sy)
        draw_datastore(ax, 79, sy - 2.2, 17, 4.4, store, fontsize=9)
        
    # Group 3: Sub-processes of Manage Alerts
    g3_subs = [
        ("Send Notification", 26, 'single', "Table Notifications"),
        ("View Status Logs", 17, 'bi', "Table Notifications")
    ]
    stem_g3 = 43
    ax.plot([37.5, stem_g3], [21.5, 21.5], color='black', lw=1.3)
    ax.plot([stem_g3, stem_g3], [17, 26], color='black', lw=1.3)
    
    for sub_name, sy, arrow_type, store in g3_subs:
        draw_straight_arrow(ax, stem_g3, sy, 48.5, sy)
        draw_process_oval(ax, 57.5, sy, 9, 2.7, sub_name, fontsize=9.5)
        if arrow_type == 'bi':
            draw_bidirectional_arrow(ax, 66.5, sy, 79, sy)
        else:
            draw_straight_arrow(ax, 66.5, sy, 79, sy)
        draw_datastore(ax, 79, sy - 2.2, 17, 4.4, store, fontsize=9)
        
    out_path = os.path.join(OUTPUT_DIR, 'dfd_level_2_company.png')
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path}")


if __name__ == "__main__":
    generate_level_0()
    generate_level_1_admin()
    generate_level_1_student()
    generate_level_1_company()
    generate_level_2_admin()
    generate_level_2_company()
    print("All DFDs generated successfully!")
