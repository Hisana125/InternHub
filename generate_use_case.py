import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_stick_figure(ax, cx, cy, label, scale=1.0):
    """
    Draws an academic UML stick figure actor with true circular head and clean proportions.
    cy is the torso center.
    Returns the attachment point (attach_x, attach_y) at the chest.
    """
    head_r = 3.2 * scale
    head_cy = cy + 7.5 * scale
    
    # Head (True circle)
    head = patches.Circle((cx, head_cy), head_r, edgecolor='black', facecolor='white', lw=1.6, zorder=10)
    ax.add_patch(head)
    
    # Neck to Torso base
    neck_y = head_cy - head_r
    torso_bottom_y = cy - 5.0 * scale
    ax.plot([cx, cx], [neck_y, torso_bottom_y], color='black', lw=1.6, zorder=10)
    
    # Arms across chest
    arms_y = cy + 1.5 * scale
    arm_span = 4.6 * scale
    ax.plot([cx - arm_span, cx + arm_span], [arms_y, arms_y], color='black', lw=1.6, zorder=10)
    
    # Legs branching down
    leg_bottom_y = cy - 13.5 * scale
    leg_span = 3.8 * scale
    ax.plot([cx, cx - leg_span], [torso_bottom_y, leg_bottom_y], color='black', lw=1.6, zorder=10)
    ax.plot([cx, cx + leg_span], [torso_bottom_y, leg_bottom_y], color='black', lw=1.6, zorder=10)
    
    # Text Label below feet
    ax.text(cx, leg_bottom_y - 2.6 * scale, label, ha='center', va='top', fontsize=11.5, fontweight='normal', color='black', zorder=10)
    
    # Association line attachment point (chest intersection)
    return cx, arms_y

def generate_diagram():
    fig, ax = plt.subplots(figsize=(11, 13), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 116)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 1. System Boundary Box
    box_x = 33
    box_y = 3
    box_w = 34
    box_h = 109
    
    boundary = patches.Rectangle(
        (box_x, box_y), box_w, box_h,
        edgecolor='black', facecolor='white',
        linewidth=1.8, zorder=2
    )
    ax.add_patch(boundary)
    
    # System Title
    ax.text(
        box_x + box_w / 2, box_y + box_h - 2.8,
        "INTERNSHIP MANAGEMENT\nSYSTEM",
        ha='center', va='top',
        fontsize=11.5, fontweight='bold',
        color='black', zorder=5,
        linespacing=1.2
    )
    
    # 2. Use Cases List (15 Core Project Use Cases matching reference model)
    use_cases = [
        "Register / Login",
        "View / Edit Profile",
        "Upload Resume & Skills",
        "Search & Browse Internships",
        "Submit Internship Application",
        "Track Application Status",
        "View Alerts & Notifications",
        "Post New Internship",
        "Manage Internship Postings",
        "Review Applicant Profiles",
        "Shortlist / Select Applicants",
        "Verify & Approve Postings",
        "Manage Student Accounts",
        "Filter / Export Reports",
        "Logout"
    ]
    
    num_uc = len(use_cases)
    top_y = 100.0
    bottom_y = 8.5
    y_step = (top_y - bottom_y) / (num_uc - 1)
    
    rx = 13.2
    ry = 2.3
    center_x = box_x + box_w / 2
    
    uc_positions = []
    for i, name in enumerate(use_cases):
        cy = top_y - i * y_step
        ellipse = patches.Ellipse(
            (center_x, cy), rx * 2, ry * 2,
            edgecolor='black', facecolor='white',
            linewidth=1.35, zorder=4
        )
        ax.add_patch(ellipse)
        ax.text(
            center_x, cy, name,
            ha='center', va='center',
            fontsize=9.2, color='black',
            zorder=6
        )
        uc_positions.append((center_x, cy, rx, ry))
        
    # 3. Actors
    # Student on Left
    s_attach_x, s_attach_y = draw_stick_figure(ax, cx=12, cy=61.0, label="Student", scale=1.0)
    
    # Company on Upper Right
    c_attach_x, c_attach_y = draw_stick_figure(ax, cx=88, cy=55.0, label="Company", scale=1.0)
    
    # Admin on Lower Right
    a_attach_x, a_attach_y = draw_stick_figure(ax, cx=88, cy=20.0, label="Admin", scale=1.0)
    
    # 4. Association Lines
    # Student connections (indices: 0, 1, 2, 3, 4, 5, 6, 14)
    student_indices = [0, 1, 2, 3, 4, 5, 6, 14]
    for idx in student_indices:
        cx, cy, r_x, r_y = uc_positions[idx]
        target_x = cx - r_x
        target_y = cy
        ax.plot([s_attach_x, target_x], [s_attach_y, target_y], color='black', lw=1.1, zorder=3)
        
    # Company connections (indices: 0, 1, 7, 8, 9, 10, 13, 14)
    company_indices = [0, 1, 7, 8, 9, 10, 13, 14]
    for idx in company_indices:
        cx, cy, r_x, r_y = uc_positions[idx]
        target_x = cx + r_x
        target_y = cy
        ax.plot([c_attach_x, target_x], [c_attach_y, target_y], color='black', lw=1.1, zorder=3)
        
    # Admin connections (indices: 8, 9, 10, 11, 12, 13, 14)
    admin_indices = [8, 9, 10, 11, 12, 13, 14]
    for idx in admin_indices:
        cx, cy, r_x, r_y = uc_positions[idx]
        target_x = cx + r_x
        target_y = cy
        ax.plot([a_attach_x, target_x], [a_attach_y, target_y], color='black', lw=1.1, zorder=3)
        
    out_path = 'use_case_diagram.png'
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated {out_path} successfully!")

if __name__ == '__main__':
    generate_diagram()
