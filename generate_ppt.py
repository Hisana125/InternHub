import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_10_slide_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette (Simple, modern, professional)
    NAVY = RGBColor(31, 60, 136)         # #1F3C88 (Brand Blue)
    DARK_BLUE = RGBColor(15, 23, 42)     # #0F172A (Deep Slate)
    ACCENT_BLUE = RGBColor(37, 99, 235)  # #2563EB (Electric Blue)
    GREEN = RGBColor(16, 149, 90)        # #10955A (Success Green)
    RED = RGBColor(220, 38, 38)          # #DC2626 (Alert Red)
    BG_LIGHT = RGBColor(244, 247, 251)   # #F4F7FB (Body background)
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    TEXT_DARK = RGBColor(30, 41, 59)     # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B

    def set_bg(slide, color=BG_LIGHT):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, tag, title, subtitle=None):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.3))
        tf_t = tag_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_tag = tf_t.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_BLUE

        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.35))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

        # Divider line
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.75 if subtitle else 1.45), Inches(11.733), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = CARD_BORDER
        div.line.fill.background()

    def add_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme, Elegant & Simple)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, DARK_BLUE)

    top_strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = ACCENT_BLUE
    top_strip.line.fill.background()

    # Title Card
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "InternHub"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "College Internship Management System"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "A simple web portal for students to find internships and track applications online."
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(10)

    # Details Cards
    c1 = add_card(s1, Inches(1.0), Inches(4.2), Inches(5.4), Inches(2.4), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    t1 = c1.text_frame
    t1.word_wrap = True
    t1.margin_left = t1.margin_right = Inches(0.3)
    t1.margin_top = Inches(0.25)
    
    p = t1.paragraphs[0]
    p.text = "STUDENT DETAILS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = t1.add_paragraph()
    p.text = "HISANA HAMZA"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)

    p = t1.add_paragraph()
    p.text = "Reg. No: MEA25MCA-2010"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    p = t1.add_paragraph()
    p.text = "Master of Computer Applications (MCA)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    c2 = add_card(s1, Inches(6.9), Inches(4.2), Inches(5.4), Inches(2.4), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    t2 = c2.text_frame
    t2.word_wrap = True
    t2.margin_left = t2.margin_right = Inches(0.3)
    t2.margin_top = Inches(0.25)

    p = t2.paragraphs[0]
    p.text = "GUIDE & INSTITUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(52, 211, 153)

    p = t2.add_paragraph()
    p.text = "Guide: Mr. Adil Narakkoden"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)

    p = t2.add_paragraph()
    p.text = "Assistant Professor, Dept. of Computer Applications"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(203, 213, 225)

    p = t2.add_paragraph()
    p.text = "MEA Engineering College, Perinthalmanna"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)

    p = t2.add_paragraph()
    p.text = "APJ Abdul Kalam Technological University (KTU)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)


    # =========================================================================
    # SLIDE 2: Project Overview
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Slide 2 • Introduction", "Project Overview", "What is InternHub and why was it created?")

    c_ov1 = add_card(s2, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.9))
    tf = c_ov1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.35)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "💡 What is InternHub?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    ov_points_1 = [
        ("A Centralized Website:", " InternHub is an easy-to-use web application built for college students and placement coordinators."),
        ("One Single Platform:", " It brings all available internship openings into one organized website instead of keeping them on notice boards."),
        ("Direct Online Apply:", " Students can easily register, view job details, and apply online with a single click."),
        ("Live Status Tracking:", " Students can check whether their application is Pending, Shortlisted, Selected, or Rejected in real time.")
    ]
    for h, b in ov_points_1:
        p = tf.add_paragraph()
        p.text = "• " + h + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)

    c_ov2 = add_card(s2, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.9))
    tf = c_ov2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.35)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "❓ Why is it Needed?"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    ov_points_2 = [
        ("Lost Opportunities:", " In colleges, internship news is often shared across WhatsApp groups or physical notices. Many students miss them."),
        ("Manual Paperwork:", " Collecting printed resumes and filling Google Forms creates confusion and delays."),
        ("No Updates for Students:", " After applying, students do not know if they were shortlisted or rejected."),
        ("Heavy Work for Staff:", " Teachers and placement officers have to manually track hundreds of student applications in Excel sheets.")
    ]
    for h, b in ov_points_2:
        p = tf.add_paragraph()
        p.text = "• " + h + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(12)


    # =========================================================================
    # SLIDE 3: Project Objectives
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Slide 3 • Goals", "Project Objectives", "The main aims of the InternHub system")

    objs = [
        ("🎯 Centralize Listings", "Bring all college internship opportunities into one website with clear details like stipend, duration, and last date to apply."),
        ("⚡ 1-Click Online Apply", "Allow students to apply directly online without paperwork, automatically attaching their student academic profile."),
        ("📊 Real-Time Status Tracking", "Give students complete transparency so they can see their application status (Pending, Shortlisted, Selected, Rejected)."),
        ("🛡️ Prevent Duplicate Applies", "Automatically stop students from accidentally applying twice for the same internship opening."),
        ("🔔 In-App Notifications", "Send instant alerts to students inside the app whenever their application status is updated by the coordinator."),
        ("🛠️ Simplify Admin Work", "Provide college administrators an easy control panel to post internships, view applicants, and update hiring statuses.")
    ]

    for idx, (head, body) in enumerate(objs):
        r = idx // 3
        c = idx % 3
        x = Inches(0.8 + c * 3.98)
        y = Inches(2.0 + r * 2.5)
        w = Inches(3.8)
        h = Inches(2.3)

        card = add_card(s3, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)


    # =========================================================================
    # SLIDE 4: Existing System vs. Proposed System
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Slide 4 • Analysis", "Existing System vs. Proposed System", "How InternHub improves the old manual way of managing internships")

    # Left: Existing
    c_ex = add_card(s4, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.9), RGBColor(255, 241, 242), RGBColor(254, 205, 211))
    tf = c_ex.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.35)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "❌ Existing System (Manual Process)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RED

    ex_list = [
        ("Scattered Notices:", " Jobs posted on physical boards or forwarded in WhatsApp groups; easily missed by students."),
        ("Manual Submissions:", " Resumes submitted via paper copies or messy email inboxes."),
        ("Zero Status Visibility:", " Students have no way to know if their application was checked, accepted, or rejected."),
        ("Duplicate Applications:", " Students re-apply multiple times by mistake, confusing the coordinators."),
        ("Heavy Manual Work:", " Staff must record everything manually in Excel, causing delays and errors.")
    ]
    for h, b in ex_list:
        p = tf.add_paragraph()
        p.text = "• " + h + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

    # Right: Proposed
    c_pr = add_card(s4, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.9), RGBColor(240, 253, 244), RGBColor(187, 247, 208))
    tf = c_pr.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.35)
    tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "✅ Proposed System (InternHub)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = GREEN

    pr_list = [
        ("Single Central Portal:", " All internship drives are organized in one clean, searchable website."),
        ("1-Click Digital Apply:", " Students apply directly using their profile with an instant timestamp."),
        ("Live Progress Tracking:", " Students can see their current status anytime (Pending, Selected, etc.)."),
        ("Duplicate Protection:", " The database automatically blocks duplicate applications for the same job."),
        ("Fast Admin Management:", " Administrators can easily post jobs, review applicants, and send notifications.")
    ]
    for h, b in pr_list:
        p = tf.add_paragraph()
        p.text = "• " + h + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)


    # =========================================================================
    # SLIDE 5: Core Features
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Slide 5 • Features", "Core Features", "Key capabilities designed for students and administrators")

    feats = [
        ("🔐 Dual-Portal Authentication", "Separate secure logins for students (KTU credentials) and verified corporate recruiters/companies."),
        ("🔍 Smart Search & Filtering", "Dynamic search bar to filter opportunities by title, skills, stipend, location, and application deadline."),
        ("⚡ 1-Click Application System", "Instant application workflow that automatically attaches verified student profile & uploaded PDF resume."),
        ("📊 Role-Based Dashboards", "Tailored dashboards for students (application tracking) and recruiters (job listings & candidate evaluation)."),
        ("🔔 Real-Time Notification Center", "Instant in-app alerts notifying students whenever their application review status is updated."),
        ("🛠️ College Placement Admin", "Comprehensive administrative control center to audit recruitment drives, manage students, and view analytics.")
    ]

    for idx, (head, body) in enumerate(feats):
        r = idx // 3
        c = idx % 3
        x = Inches(0.8 + c * 3.98)
        y = Inches(2.0 + r * 2.5)
        w = Inches(3.8)
        h = Inches(2.3)

        card = add_card(s5, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)


    # =========================================================================
    # SLIDE 6: Module Description
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Slide 6 • System Structure", "Module Description", "Three integrated functional modules designed for Students, Recruiters, and College Placement Admin")

    modules = [
        ("🎓 Module 1: Student Portal", NAVY, "ACTOR: REGISTERED STUDENTS", [
            ("Academic Onboarding:", " Students register with KTU Reg No, MCA/B.Tech course branch, contact info, and upload PDF resume."),
            ("Job Discovery & Search:", " Search vacancies with dynamic multi-filters across technical skills, stipend, location, and deadlines."),
            ("1-Click Digital Apply:", " Submits application in one click, automatically binding verified academic profile and resume."),
            ("Anti-Duplicate Guard:", " Enforces database unique constraints to prevent accidental duplicate applications."),
            ("Live Progress Tracking:", " Real-time dashboard showing application status (Pending, Under Review, Shortlisted, Selected, Rejected).")
        ], "⚡ Outcome: Seamless 1-click apply & full transparency"),

        ("🏢 Module 2: Recruiter / Company Portal", ACCENT_BLUE, "ACTOR: CORPORATE RECRUITERS", [
            ("Company Registration:", " Corporate sign-up with company name, recruiter credentials, industry, website, and office address."),
            ("Internship Publishing:", " Recruiters post job drives with roles, stipend, duration, required skill tags, and deadline dates."),
            ("Applicant Screening:", " Inspect candidate roster, review academic credentials, and download student PDF resumes."),
            ("Status Transition Engine:", " Move applicants through evaluation states (Under Review ➔ Shortlisted ➔ Selected / Rejected)."),
            ("Recruiter Analytics:", " Monitor applicant counts, track drive performance, and manage active internship postings.")
        ], "⚡ Outcome: Accelerated candidate review & hiring"),

        ("🛡️ Module 3: Placement Admin & Governance", GREEN, "ACTOR: COLLEGE PLACEMENT CELL", [
            ("Student Verification:", " Validate student registration numbers and course details against college institutional records."),
            ("Corporate Oversight:", " Moderate registered company profiles and audit postings to ensure legitimate campus opportunities."),
            ("Application Auditing:", " Centralized oversight over all campus recruitment drives, department stats, and placement history."),
            ("Notification Dispatch:", " System-wide trigger engine that automatically dispatches in-app alerts upon status changes."),
            ("Access Control & Security:", " Django Admin panel with role-based access, session security, and MySQL database integrity.")
        ], "⚡ Outcome: 100% Campus placement governance & security")
    ]

    for idx, (title, col, role_badge, items, footer_tag) in enumerate(modules):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(1.95)
        w = Inches(3.8)
        h = Inches(4.95)

        card = add_card(s6, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.24)
        tf.margin_top = Inches(0.18)

        # Title
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        # Role Badge
        p = tf.add_paragraph()
        p.text = role_badge
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(2)

        # Bullet Items
        for h_item, b_item in items:
            p = tf.add_paragraph()
            p.text = f"• {h_item} {b_item}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(5)

        # Mini footer highlight inside card
        f_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95 + idx * 3.98), Inches(6.35), Inches(3.5), Inches(0.42))
        f_box.fill.solid()
        f_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
        f_box.line.color.rgb = col
        f_box.line.width = Pt(1)

        tf_f = f_box.text_frame
        tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_right = Inches(0.12)
        tf_f.margin_top = Inches(0.06)
        p_f = tf_f.paragraphs[0]
        p_f.text = footer_tag
        p_f.font.size = Pt(8.8)
        p_f.font.bold = True
        p_f.font.color.rgb = col
        p_f.alignment = PP_ALIGN.CENTER


    # =========================================================================
    # SLIDE 7: Project Workflow (End-to-End Multi-Tier Process)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Slide 7 • System Workflow", "Project Workflow", "End-to-end operational lifecycle connecting Students, Recruiters, and College Placement Admin")

    phases = [
        ("01", "Registration & Setup", NAVY, "👤 Student & Recruiter", [
            ("Student Onboarding:", " Students register with KTU Reg No, MCA/B.Tech course, contact details & PDF resume upload."),
            ("Company Account:", " Recruiter registers corporate profile with website, contact person & company description."),
            ("Account Verification:", " Django authentication validates accounts for secure role-based dashboard access.")
        ]),
        ("02", "Vacancy Posting", ACCENT_BLUE, "🏢 Recruiter & Placement", [
            ("Drive Creation:", " Recruiter posts role details, monthly stipend, duration, location & required skill tags."),
            ("Deadline Scheduling:", " Strict application deadline set to organize candidate intake systematically."),
            ("Portal Publishing:", " Vacancies are validated and broadcast across the college student network.")
        ]),
        ("03", "1-Click Application", GREEN, "🎓 College Student", [
            ("Skill-Based Search:", " Students filter opportunities by programming skills, stipend, and deadlines."),
            ("1-Click Digital Apply:", " Submits application instantly linking student profile & uploaded PDF resume."),
            ("Anti-Duplicate Rule:", " Database uniquely prevents multiple applications to the same opportunity.")
        ]),
        ("04", "Screening & Alerts", RGBColor(124, 58, 237), "💼 Recruiter ➔ Student", [
            ("Resume Evaluation:", " Recruiter views applicant roster, reviews qualifications, and downloads resumes."),
            ("Status Progression:", " Moves candidates through Pending ➔ Under Review ➔ Shortlisted ➔ Selected."),
            ("Real-Time Dispatch:", " System dispatches instant in-app notification alerts directly to the student.")
        ])
    ]

    for idx, (p_num, p_title, p_col, p_role, p_points) in enumerate(phases):
        x = Inches(0.8 + idx * 2.98)
        y = Inches(1.95)
        w = Inches(2.78)
        h = Inches(3.55)

        card = add_card(s7, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.20)
        tf.margin_top = Inches(0.18)

        # Step Number & Title
        p = tf.paragraphs[0]
        p.text = f"PHASE {p_num} • {p_title.upper()}"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = p_col

        # Role Badge
        p = tf.add_paragraph()
        p.text = p_role
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(2)

        # Points
        for h_pt, b_pt in p_points:
            p = tf.add_paragraph()
            p.text = f"• {h_pt} {b_pt}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(6)

        # Connector between cards (except last card)
        if idx < 3:
            conn_box = s7.shapes.add_textbox(Inches(0.8 + idx * 2.98 + 2.78), Inches(3.4), Inches(0.20), Inches(0.4))
            tf_conn = conn_box.text_frame
            tf_conn.word_wrap = False
            tf_conn.margin_left = tf_conn.margin_right = tf_conn.margin_top = tf_conn.margin_bottom = 0
            p_conn = tf_conn.paragraphs[0]
            p_conn.text = "➔"
            p_conn.font.size = Pt(14)
            p_conn.font.bold = True
            p_conn.font.color.rgb = ACCENT_BLUE
            p_conn.alignment = PP_ALIGN.CENTER

    # Bottom Progression Banner (Status Lifecycle Pipeline)
    c_pipe = add_card(s7, Inches(0.8), Inches(5.65), Inches(11.72), Inches(1.42), RGBColor(255, 255, 255), CARD_BORDER)
    tf_p = c_pipe.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_right = Inches(0.25)
    tf_p.margin_top = Inches(0.12)

    p = tf_p.paragraphs[0]
    p.text = "📌 APPLICATION LIFECYCLE & STATUS PROGRESSION PIPELINE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY

    status_boxes = [
        ("1. Pending", RGBColor(217, 119, 6), "Student submitted application; timestamp recorded, duplicate check verified, awaiting review."),
        ("2. Under Review", ACCENT_BLUE, "Recruiter or Placement Coordinator is examining academic profile and candidate resume."),
        ("3. Shortlisted", RGBColor(124, 58, 237), "Student cleared preliminary screening; invited for interview or online evaluation."),
        ("4. Selected / Rejected", GREEN, "Final hiring decision updated; automated real-time notification alert dispatched to student.")
    ]

    for s_idx, (s_title, s_col, s_desc) in enumerate(status_boxes):
        sx = Inches(1.0 + s_idx * 2.85)
        sy = Inches(6.05)
        sw = Inches(2.70)
        sh = Inches(0.92)

        s_shape = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, sw, sh)
        s_shape.fill.solid()
        s_shape.fill.fore_color.rgb = RGBColor(248, 250, 252)
        s_shape.line.color.rgb = s_col
        s_shape.line.width = Pt(1)

        s_tf = s_shape.text_frame
        s_tf.word_wrap = True
        s_tf.margin_left = s_tf.margin_right = Inches(0.12)
        s_tf.margin_top = Inches(0.08)

        p = s_tf.paragraphs[0]
        p.text = s_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = s_col

        p = s_tf.add_paragraph()
        p.text = s_desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(2)


    # =========================================================================
    # SLIDE 8: Database Tables
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Slide 8 • Database", "Database Tables", "The 5 core relational tables used to store and manage project data")

    tables_row1 = [
        ("1. Student Table (user_management_student)", NAVY, [
            ("id:", " Unique student ID (Primary Key)"),
            ("user_id:", " Links to Django Auth User login"),
            ("registration_number:", " Unique KTU College Reg No"),
            ("name, email, phone:", " Contact details of the student"),
            ("course & resume:", " Degree branch & PDF resume file")
        ]),
        ("2. Company Table (internships_company)", RGBColor(124, 58, 237), [
            ("id:", " Unique company ID (Primary Key)"),
            ("user_id:", " Links to Django Auth User login"),
            ("company_name & email:", " Organization identity & email"),
            ("phone & website:", " Recruiter contact & web URL"),
            ("address & description:", " Physical office & company info")
        ]),
        ("3. Internship Table (internships_internship)", ACCENT_BLUE, [
            ("id:", " Unique internship ID (Primary Key)"),
            ("company_id:", " Foreign Key linking to Company"),
            ("title & company_name:", " Role title & hiring organization"),
            ("location, duration, stipend:", " Work terms & monthly pay"),
            ("skills_required & deadline:", " Skill criteria & last apply date")
        ])
    ]

    for idx, (t_title, t_col, t_fields) in enumerate(tables_row1):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(1.95)
        w = Inches(3.78)
        h = Inches(2.35)

        card = add_card(s8, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.22)
        tf.margin_top = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = t_col

        for f_name, f_desc in t_fields:
            p = tf.add_paragraph()
            p.text = f"• {f_name}{f_desc}"
            p.font.size = Pt(9.8)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(3)

    tables_row2 = [
        ("4. Application Table (internships_application)", GREEN, [
            ("id:", " Unique application ID (Primary Key)"),
            ("student_id & internship_id:", " Foreign Keys linking student profile to internship opening"),
            ("applied_at & status:", " Application timestamp and state (Pending, Under Review, Shortlisted, Selected, Rejected)"),
            ("* Unique Constraint:", " (student_id, internship_id) prevents duplicate applications for the same opening")
        ]),
        ("5. Notification Table (internships_notification)", RGBColor(217, 119, 6), [
            ("id:", " Unique notification ID (Primary Key)"),
            ("student_id:", " Foreign Key targeting the student receiving the alert"),
            ("message:", " Automated alert text dispatched upon recruiter status updates"),
            ("is_read & created_at:", " Read state tracking boolean and real-time generation timestamp")
        ])
    ]

    for idx, (t_title, t_col, t_fields) in enumerate(tables_row2):
        x = Inches(0.8 + idx * 5.95)
        y = Inches(4.50)
        w = Inches(5.77)
        h = Inches(2.40)

        card = add_card(s8, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.20)

        p = tf.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = t_col

        for f_name, f_desc in t_fields:
            p = tf.add_paragraph()
            p.text = f"• {f_name}{f_desc}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(4)


    # =========================================================================
    # SLIDE 9: Technology Stack Used
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Slide 9 • Tech Stack", "Technology Stack Used", "Programming language, database, framework, and tools used")

    tech_items = [
        ("🐍 Programming Language", "Python 3.9+", "Primary backend language. Chosen because it is clean, easy to read, and has robust web framework support."),
        ("🌐 Web Framework", "Django 4.2 LTS", "A robust Python web framework providing built-in security, user authentication, ORM, and admin panel."),
        ("🗄️ Relational Database", "MySQL Database", "MySQL is the active database storing student records, company profiles, job postings, applications, and alerts."),
        ("🎨 Frontend (UI)", "HTML5 & CSS3", "Clean, responsive user interface with modern card layouts optimized for desktop, tablet, and mobile browsers."),
        ("📦 Libraries & Drivers", "mysqlclient & Forms", "mysqlclient (MySQLdb) connects Django to MySQL. Django Forms handles strict server-side validation."),
        ("💻 Development Tools", "VS Code & Git", "Visual Studio Code used as primary code editor, with Git utilized for source code version management.")
    ]

    for idx, (t_title, t_sub, t_desc) in enumerate(tech_items):
        r = idx // 3
        c = idx % 3
        x = Inches(0.8 + c * 3.98)
        y = Inches(2.0 + r * 2.5)
        w = Inches(3.8)
        h = Inches(2.3)

        card = add_card(s9, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.22)

        p = tf.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = t_sub
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = t_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(5)


    # =========================================================================
    # SLIDE 10: Future Enhancements
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "Slide 10 • Roadmap", "Future Enhancements", "Useful features and extensions designed for future production releases")

    enhances = [
        ("🤖 AI Resume Parser & Matcher", "Automatically scan student PDF resumes, extract technical skills, and recommend the best-fitting internships."),
        ("🏢 Recruiter Interview Scheduler", "Add an in-app calendar to schedule interview rounds and integrate with Google Meet or Zoom."),
        ("📩 Automated Email & SMS Alerts", "Send automated email and SMS messages to students when an interview is scheduled or status changes."),
        ("📊 Placement Analytics & Export", "Generate downloadable placement PDF/Excel reports and analytics for college accreditation records."),
        ("📱 Native Mobile Application", "Develop an Android and iOS mobile app using Flutter so students can receive push notifications on mobile."),
        ("🎓 Digital Completion Certificates", "Automatically issue verifiable, cryptographically signed digital completion certificates upon finishing internships.")
    ]

    for idx, (head, body) in enumerate(enhances):
        r = idx // 3
        c = idx % 3
        x = Inches(0.8 + c * 3.98)
        y = Inches(2.0 + r * 2.5)
        w = Inches(3.8)
        h = Inches(2.3)

        card = add_card(s10, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)


    # =========================================================================
    # SLIDE 11: Conclusion & Thank You
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11, DARK_BLUE)

    top_strip11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_strip11.fill.solid()
    top_strip11.fill.fore_color.rgb = ACCENT_BLUE
    top_strip11.line.fill.background()

    # Left: Conclusion Summary Card
    c_concl = add_card(s11, Inches(1.0), Inches(1.2), Inches(5.4), Inches(5.2), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    tf_cc = c_concl.text_frame
    tf_cc.word_wrap = True
    tf_cc.margin_left = tf_cc.margin_right = Inches(0.35)
    tf_cc.margin_top = Inches(0.3)

    p = tf_cc.paragraphs[0]
    p.text = "🎯 Project Conclusion"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)

    concl_points = [
        ("Solves a Real Campus Problem:", " Replaces slow, manual circulars and scattered WhatsApp messages with a unified, transparent portal."),
        ("Empowers College Students:", " Direct 1-click applications, resume linkage, live tracking, and instantaneous status notifications."),
        ("Empowers Companies & Admins:", " Recruiters easily manage drives and evaluate candidates; placement cell gains complete audit oversight."),
        ("Solid Engineering Foundation:", " Built on Django's proven MVT architecture with a robust, normalized MySQL relational database.")
    ]
    for h, b in concl_points:
        p = tf_cc.add_paragraph()
        p.text = "• " + h + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(14)

    # Right: Thank You Box
    c_ty = add_card(s11, Inches(6.9), Inches(1.2), Inches(5.4), Inches(5.2), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    tf_ty = c_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_right = Inches(0.35)
    tf_ty.margin_top = Inches(0.5)

    p = tf_ty.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf_ty.add_paragraph()
    p.text = "Any Questions or Comments?"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(10)

    p = tf_ty.add_paragraph()
    p.text = "InternHub — College Internship Management System"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(14)

    p = tf_ty.add_paragraph()
    p.text = "HISANA HAMZA  |  MEA25MCA-2010\nMEA Engineering College, Perinthalmanna\nAPJ Abdul Kalam Technological University (KTU)"
    p.font.size = Pt(11.5)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(20)

    # Attempt to save to multiple standard presentation filenames
    filenames_to_save = [
        "InternHub_Final_Presentation.pptx",
        "InternHub_College_Internship_Management_Presentation.pptx",
        "InternHub_Project_Presentation_Final.pptx",
        "InternHub_Project_Presentation_Updated.pptx",
        "InternHub_Project_Presentation_10_Slides.pptx"
    ]
    saved_files = []
    for fname in filenames_to_save:
        try:
            prs.save(fname)
            saved_files.append(fname)
            print(f"Presentation saved successfully as '{fname}' ({len(prs.slides)} slides)")
        except PermissionError:
            print(f"Notice: '{fname}' is currently locked by another application. Skipping.")

    if not saved_files:
        fallback = "InternHub_Presentation_New.pptx"
        prs.save(fallback)
        print(f"Saved to fallback file '{fallback}' ({len(prs.slides)} slides)")

create_presentation = create_10_slide_presentation

if __name__ == "__main__":
    create_10_slide_presentation()
