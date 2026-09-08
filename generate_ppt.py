import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    # Color Palette (Matching the web application's modern aesthetic)
    NAVY = RGBColor(31, 60, 136)       # #1F3C88 (Brand Blue)
    DARK_BLUE = RGBColor(15, 23, 42)   # #0F172A (Deep Slate)
    ACCENT_BLUE = RGBColor(37, 99, 235)# #2563EB (Electric Blue)
    TEAL = RGBColor(13, 148, 136)      # #0D9488 (Teal accent)
    EMERALD = RGBColor(16, 185, 129)   # #10B981 (Success Green)
    AMBER = RGBColor(217, 119, 6)      # #D97706 (Warning Amber)
    ROSE = RGBColor(225, 29, 72)       # #E11D48 (Crimson Red)
    BG_LIGHT = RGBColor(244, 247, 251) # #F4F7FB (Site Body background)
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    TEXT_MAIN = RGBColor(30, 41, 59)   # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    PILL_BG = RGBColor(238, 242, 255)

    def set_slide_background(slide, color=BG_LIGHT):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, category, title, subtitle=None):
        # Category pill / banner
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_BLUE

        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

        # Thin decorative divider line
        divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.85 if subtitle else 1.55), Inches(11.733), Inches(0.02))
        divider.fill.solid()
        divider.fill.fore_color.rgb = CARD_BORDER
        divider.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # ==========================================
    # SLIDE 1: Title Slide (Dark Elegance)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_BLUE)

    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    banner.fill.solid()
    banner.fill.fore_color.rgb = ACCENT_BLUE
    banner.line.fill.background()

    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(3.2), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(30, 41, 59)
    badge.line.color.rgb = ACCENT_BLUE
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "MCA FINAL PROJECT PRESENTATION"
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(147, 197, 253)
    p_b.alignment = PP_ALIGN.CENTER

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "InternHub"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "College Internship Management System"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(147, 197, 253)

    p3 = tf_t.add_paragraph()
    p3.text = "A Centralized Web-Based Portal Streamlining Campus Internship Opportunities & Application Tracking"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_before = Pt(10)

    card_stu = add_card(s1, Inches(1.0), Inches(4.3), Inches(5.4), Inches(2.3), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    tf_cs = card_stu.text_frame
    tf_cs.word_wrap = True
    p = tf_cs.paragraphs[0]
    p.text = "SUBMITTED BY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = tf_cs.add_paragraph()
    p.text = "HISANA HAMZA"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)

    p = tf_cs.add_paragraph()
    p.text = "Register No: MEA25MCA-2010"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    p = tf_cs.add_paragraph()
    p.text = "Master of Computer Applications (MCA)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)

    card_inst = add_card(s1, Inches(6.9), Inches(4.3), Inches(5.4), Inches(2.3), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    tf_ci = card_inst.text_frame
    tf_ci.word_wrap = True
    p = tf_ci.paragraphs[0]
    p.text = "GUIDANCE & INSTITUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    p = tf_ci.add_paragraph()
    p.text = "Project Guide: Mr. Adil Narakkoden"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)

    p = tf_ci.add_paragraph()
    p.text = "Assistant Professor, Dept. of Computer Applications"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(203, 213, 225)

    p = tf_ci.add_paragraph()
    p.text = "MEA Engineering College, Perinthalmanna"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(6)

    p = tf_ci.add_paragraph()
    p.text = "APJ Abdul Kalam Technological University (KTU)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)


    # ==========================================
    # SLIDE 2: Presentation Outline / Agenda
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Overview", "Presentation Outline", "Core topics covered as per the academic project guidelines")

    agenda_items = [
        ("01", "Project Overview & Objectives", "Background, motivation, and problem statement"),
        ("02", "Existing vs. Proposed System", "Critical comparative analysis and key advantages"),
        ("03", "Core Features & Architecture", "Key system capabilities and Django MVT design"),
        ("04", "Module Description", "Detailed breakdown of Student, Internship & Admin modules"),
        ("05", "Database Schema & Tables", "Relational entities, fields, constraints & ER model"),
        ("06", "Technology Stack Used", "Full-stack framework, DB, languages, libraries & tools"),
        ("07", "Testing & Implementation", "Unit, integration, security & verification strategies"),
        ("08", "Future Enhancements & Conclusion", "Roadmap for future upgrades and final summary")
    ]

    for idx, (num, title, desc) in enumerate(agenda_items):
        row = idx // 4
        col = idx % 4
        x = Inches(0.8 + col * 2.98)
        y = Inches(2.2 + row * 2.3)
        w = Inches(2.8)
        h = Inches(2.05)

        card = add_card(s2, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(4)


    # ==========================================
    # SLIDE 3: Project Overview & Background
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Introduction", "Project Overview", "Context, purpose, and significance of InternHub")

    card_left = add_card(s3, Inches(0.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = Inches(0.3)

    p = tf_l.paragraphs[0]
    p.text = "📌 Background & Context"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    points_l = [
        ("Industry-Academia Bridge:", " Internships offer students crucial exposure to real-world software workflows, hands-on development, and professional workplace standards."),
        ("Fragmented Information:", " In traditional college settings, opportunities are circulated haphazardly across notice boards, disparate messaging channels, and forwarded emails."),
        ("Lack of Direct Tracking:", " Students frequently lose track of their application status and deadlines, while placement coordinators struggle with disorganized records."),
        ("Administrative Overload:", " Manually gathering resumes, filtering applicants, and publishing updates via spreadsheets causes significant communication bottlenecks.")
    ]
    for b_title, b_body in points_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b_title + b_body
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

    card_right = add_card(s3, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_r = card_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = Inches(0.3)

    p = tf_r.paragraphs[0]
    p.text = "🚀 InternHub Solution"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    points_r = [
        ("Centralized Campus Portal:", " A unified, responsive web portal bringing verified internship listings directly to students in an accessible, structured environment."),
        ("Seamless Student Journey:", " Enables students to register, manage profiles, search listings using multi-field keywords, and apply with a single click."),
        ("Automated Feedback Loop:", " Eliminates uncertainty by providing live application tracking (Pending, Under Review, Shortlisted, Selected, Rejected) and in-app alerts."),
        ("Robust Administrative Control:", " Provides staff and coordinators full control via Django's secure admin interface to moderate listings and track candidates efficiently.")
    ]
    for b_title, b_body in points_r:
        p = tf_r.add_paragraph()
        p.text = "• " + b_title + b_body
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)


    # ==========================================
    # SLIDE 4: Project Objectives
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Project Scope", "Project Objectives", "Core strategic goals addressed by the InternHub platform")

    objectives = [
        ("🎯 Centralize Opportunity Discovery", "Provide a single authoritative platform where verified company internships are listed with comprehensive details (stipend, duration, location, required skills, and deadline)."),
        ("⚡ Streamline Online Applications", "Eliminate manual paperwork and email submissions by providing a quick, authenticated one-click application process directly linked to student academic profiles."),
        ("📊 Real-Time Application Tracking", "Offer students complete transparency into their application journey through a dynamic dashboard displaying real-time statuses (Pending, Shortlisted, Selected, Rejected)."),
        ("🛡️ Ensure Strict Data Integrity", "Enforce database-level unique constraints to prevent duplicate applications for the same opening, ensuring clean, fair, and reliable records."),
        ("🔔 Instant Notification Mechanism", "Keep students informed immediately about their submission confirmations and subsequent status transitions through an integrated in-app notification center."),
        ("⚙️ Empower Placement Coordinators", "Provide administrative personnel with robust CRUD capabilities for managing job listings, monitoring registered students, and reviewing applications seamlessly.")
    ]

    for idx, (title, desc) in enumerate(objectives):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 3.98)
        y = Inches(2.1 + row * 2.45)
        w = Inches(3.8)
        h = Inches(2.25)

        card = add_card(s4, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)


    # ==========================================
    # SLIDE 5: Existing System vs. Proposed System
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "System Analysis", "Existing System vs. Proposed System", "Comparative analysis highlighting key operational improvements")

    card_ex = add_card(s5, Inches(0.8), Inches(2.1), Inches(5.7), Inches(4.8), RGBColor(255, 241, 242), RGBColor(254, 205, 211))
    tf_ex = card_ex.text_frame
    tf_ex.word_wrap = True
    tf_ex.margin_left = tf_ex.margin_right = tf_ex.margin_top = Inches(0.3)

    p = tf_ex.paragraphs[0]
    p.text = "❌ Existing System (Manual / Fragmented)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ROSE

    ex_points = [
        ("Scattered Information Channels:", " Opportunities announced randomly across WhatsApp, physical boards, and forwarded departmental emails."),
        ("Paper-Based / Email Applications:", " Resumes submitted physically or to cluttered inboxes, leading to lost records and formatting inconsistencies."),
        ("No Real-Time Visibility:", " Students have no mechanism to track their application status; candidates remain uncertain about outcomes."),
        ("High Duplicate Risk:", " Students accidentally apply multiple times, creating redundant records and cluttering recruiter review queues."),
        ("Heavy Administrative Burden:", " Staff spend excessive hours manually verifying applicant data, logging entries in spreadsheets, and notifying candidates.")
    ]
    for t, d in ex_points:
        p = tf_ex.add_paragraph()
        p.text = "• " + t + d
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    card_pr = add_card(s5, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.8), RGBColor(240, 253, 244), RGBColor(187, 247, 208))
    tf_pr = card_pr.text_frame
    tf_pr.word_wrap = True
    tf_pr.margin_left = tf_pr.margin_right = tf_pr.margin_top = Inches(0.3)

    p = tf_pr.paragraphs[0]
    p.text = "✅ Proposed System (InternHub Portal)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(21, 128, 61)

    pr_points = [
        ("Single Centralized Hub:", " All campus internship drives organized in one standardized digital catalog with full parameters and deadlines."),
        ("1-Click Authenticated Application:", " Direct digital submission connecting candidate profile to the internship with automatic timestamping."),
        ("Dynamic Status Tracking:", " Live student dashboard showcasing distinct stages: Pending, Under Review, Shortlisted, Selected, Rejected."),
        ("Zero Duplication Guarantee:", " Database-enforced unique constraints strictly prevent repeated applications for the same opening."),
        ("Streamlined Management & Alerts:", " Dedicated admin console for instant status moderation paired with automated in-app notifications.")
    ]
    for t, d in pr_points:
        p = tf_pr.add_paragraph()
        p.text = "• " + t + d
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)


    # ==========================================
    # SLIDE 6: Comparative Feature Matrix
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "System Comparison", "Feature Comparison Matrix", "Direct side-by-side evaluation between Traditional and InternHub approaches")

    rows = 7
    cols = 3
    left = Inches(0.8)
    top = Inches(2.1)
    width = Inches(11.733)
    height = Inches(4.7)

    table_shape = s6.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(4.4)
    table.columns[2].width = Inches(4.533)

    headers = ["Evaluation Parameter", "Existing Manual System", "InternHub Proposed System"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT

    matrix_data = [
        ("Internship Listing & Discovery", "Scattered on social media, notice boards & informal chats", "Centralized, searchable web catalog with keyword filters"),
        ("Application Submission Process", "Manual hard copies, emails, or fragmented Google Forms", "Instant 1-click digital application tied to verified user profile"),
        ("Application Duplicate Prevention", "None; prone to multiple redundant submissions by same student", "Database UniqueConstraint strictly prevents duplicate submissions"),
        ("Application Status Transparency", "Students kept unaware; no systematic status feedback", "Real-time visual status updates (Pending, Shortlisted, Selected, etc.)"),
        ("Notification & Alerts", "Manual telephonic/email communication by coordinators", "Automated in-app notification engine with unread trackers"),
        ("Data Security & Storage", "Unprotected spreadsheets, physical registers & files", "Role-based Django auth, password hashing & relational MySQL DB")
    ]

    for row_idx, data in enumerate(matrix_data):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else RGBColor(248, 250, 252)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_BLUE if col_idx == 0 else (ROSE if col_idx == 1 else RGBColor(21, 128, 61))
            if col_idx == 0:
                p.font.bold = True


    # ==========================================
    # SLIDE 7: Core System Features
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Functionality", "Core System Features", "Comprehensive capabilities designed for students and administrators")

    features = [
        ("🔐 Secure Student Authentication", "Secure sign-up and login mechanism powered by Django Auth, featuring hashed passwords and protected student sessions."),
        ("🔎 Smart Keyword Search Filter", "Dynamic multi-attribute query engine filtering postings by job title, company name, location, and specific required skills."),
        ("⚡ 1-Click Application Engine", "Instant application submission associating verified student profile with targeted opening, complete with duplicate submission checks."),
        ("📊 Real-Time Analytics Dashboard", "Intuitive dashboard providing interactive count cards for Total, Pending, Selected, and Rejected applications."),
        ("🔔 In-App Notification Center", "Automated alert generation for application submissions and coordinator status changes, with read/unread tracking."),
        ("🛠️ Comprehensive Admin Panel", "Powerful administrative back-office for creating/editing postings, reviewing student data, and updating recruitment statuses.")
    ]

    for idx, (title, desc) in enumerate(features):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 3.98)
        y = Inches(2.1 + row * 2.45)
        w = Inches(3.8)
        h = Inches(2.25)

        card = add_card(s7, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)


    # ==========================================
    # SLIDE 8: System Architecture (Django MVT)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Architecture", "System Architecture & MVT Pattern", "Structural breakdown based on the Model-View-Template software design")

    arch_cols = [
        ("MODEL (Data Layer)", NAVY, [
            ("Django ORM Entities", "Translates Python classes into relational database schema without writing raw SQL."),
            ("Custom Models", "Defines Student, Internship, Application, and Notification entities."),
            ("Integrity Constraints", "Enforces foreign keys, cascading deletes, and unique student-internship constraints."),
            ("Database Backend", "Seamless connectivity to MySQL Database (with SQLite fallback for local test runs).")
        ]),
        ("VIEW (Business Logic Layer)", ACCENT_BLUE, [
            ("Request Dispatching", "Configured via config.urls and modular app routes (user_management, internships)."),
            ("Authentication Guards", "Protects endpoints using @login_required decorators to enforce authenticated sessions."),
            ("Search & Filtering", "Implements dynamic Q-object queries for multi-field internship search."),
            ("Business Workflows", "Handles registration, login/logout, application submissions, and notification generation.")
        ]),
        ("TEMPLATE (Presentation Layer)", TEAL, [
            ("Template Inheritance", "Modular architecture with base.html providing consistent site navigation and structure."),
            ("Dynamic Rendering", "Uses Django Template Language (DTL) tags to render conditional logic and loops."),
            ("Responsive Web Layouts", "Modern CSS flexbox and grid layouts optimized for desktops, tablets, and smartphones."),
            ("Feedback Messages", "Provides immediate visual alerts on form submissions, login errors, and status updates.")
        ])
    ]

    for idx, (head, color, bullets) in enumerate(arch_cols):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(2.1)
        w = Inches(3.8)
        h = Inches(4.8)

        card = add_card(s8, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color

        for b_title, b_desc in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b_title}: {b_desc}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_before = Pt(8)


    # ==========================================
    # SLIDE 9: Module Description - Structural Breakdown
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Modules", "System Module Breakdown", "Functional segregation of the InternHub web application into core subsystems")

    modules_summary = [
        ("Module 1: User Management & Authentication", "Handles student account creation, profile management, credentials verification, secure session control, and personal student dashboard analytics.", NAVY),
        ("Module 2: Internship Discovery & Search", "Provides dynamic cataloging of all available internship postings with multi-field search filters (title, company, location, skills) and full detail pages.", ACCENT_BLUE),
        ("Module 3: Application Engine & Duplicate Guard", "Manages the one-click student application submission process, validates duplicate restrictions, and records application timestamps.", TEAL),
        ("Module 4: Real-Time Tracking & Notifications", "Tracks student applications through recruitment stages and generates automatic in-app alerts whenever statuses are updated by coordinators.", EMERALD),
        ("Module 5: Admin Management & Moderation", "Provides privileged faculty and placement coordinators with tools to post internships, review applicant pools, and update hiring statuses.", AMBER)
    ]

    for idx, (title, desc, color) in enumerate(modules_summary):
        y = Inches(2.05 + idx * 0.98)
        card = add_card(s9, Inches(0.8), y, Inches(11.733), Inches(0.85))
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.12)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(2)


    # ==========================================
    # SLIDE 10: Module Deep Dive 1: User Management & Authentication
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Module Detail", "Module 1: User Management & Authentication", "Deep dive into user onboarding, identity management, and student profiles")

    u_cards = [
        ("📝 Registration & Account Setup", [
            ("Integrated User Creation", "Synchronizes Django's built-in User model with custom Student domain model."),
            ("Clean Validation", "StudentForm validates username availability, email formatting, and password standards."),
            ("OneToOne Relationship", "Strict 1-to-1 linkage between Django authentication user and Student record.")
        ]),
        ("🔐 Authentication & Security", [
            ("Secure Credential Check", "Uses Django authenticate() for verifying encrypted PBKDF2 password hashes."),
            ("Session State Management", "Maintains authenticated state with CSRF protection against cross-site attacks."),
            ("Access Control Decorator", "Secures student-only views using @login_required to prevent unauthorized access.")
        ]),
        ("👤 Profile & Dashboard Management", [
            ("Student Profile View/Edit", "Students can inspect and update their contact phone number, email, and enrolled course."),
            ("Live Application Counter", "Dashboard computes counts for Total, Pending, Selected, and Rejected applications."),
            ("Quick Navigational Actions", "Direct shortcuts to browse internships, check notifications, and track submissions.")
        ])
    ]

    for idx, (title, points) in enumerate(u_cards):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(2.1)
        w = Inches(3.8)
        h = Inches(4.8)

        card = add_card(s10, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        for p_title, p_desc in points:
            p = tf.add_paragraph()
            p.text = f"• {p_title}: {p_desc}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_before = Pt(10)


    # ==========================================
    # SLIDE 11: Module Deep Dive 2: Internship Discovery & Search
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Module Detail", "Module 2: Internship Discovery & Search", "Exploration engine allowing students to find, filter, and inspect opportunities")

    i_cards = [
        ("📋 Standardized Internship Listings", [
            ("Comprehensive Listing Details", "Displays Company Name, Job Role, Location, Duration, Monthly Stipend, and Required Skills."),
            ("Deadline Transparency", "Clear display of application closing dates to help students prioritize urgent openings."),
            ("Chronological Sorting", "Internship listings are automatically ordered by latest postings first (order_by('-created_at')).")
        ]),
        ("🔍 Dynamic Multi-Field Search Engine", [
            ("Universal Search Query", "Single search input checks across multiple database columns simultaneously."),
            ("Django Q-Object Filtering", "Executes complex OR-queries: title | company_name | location | skills_required."),
            ("Case-Insensitive Lookups", "Uses icontains lookup to ensure users find matches regardless of letter casing.")
        ]),
        ("📄 Detailed Internship View", [
            ("In-Depth Job Description", "Full textual scope outlining responsibilities, eligibility criteria, and deliverables."),
            ("Direct Call-to-Action", "Features a distinct 'Apply Now' action button that forwards directly to the application view."),
            ("State Awareness", "Intelligently flags if the logged-in student has already submitted an application.")
        ])
    ]

    for idx, (title, points) in enumerate(i_cards):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(2.1)
        w = Inches(3.8)
        h = Inches(4.8)

        card = add_card(s11, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

        for p_title, p_desc in points:
            p = tf.add_paragraph()
            p.text = f"• {p_title}: {p_desc}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_before = Pt(10)


    # ==========================================
    # SLIDE 12: Module Deep Dive 3 & 4: Applications & Notifications
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Module Detail", "Modules 3 & 4: Applications & Notifications", "Application submission engine, anti-duplicate constraint, and real-time alerts")

    app_notif_cards = [
        ("⚡ 1-Click Application Engine", [
            ("Profile Linkage", "Automatically binds the authenticated student's profile to the internship entry."),
            ("Default Pending State", "New applications are initialized with 'Pending' status upon submission."),
            ("Timestamp Tracking", "Records applied_at timestamp using auto_now_add for auditability.")
        ]),
        ("🛡️ Anti-Duplicate Enforcement", [
            ("Database Constraint", "Model utilizes models.UniqueConstraint(fields=['student', 'internship'])."),
            ("Pre-Validation in View", "Checks Application.objects.filter(student, internship) before rendering apply form."),
            ("User Alert Banner", "Displays 'Already Applied' badge if student attempts to re-apply.")
        ]),
        ("🔔 In-App Notifications Engine", [
            ("Submission Alert", "Automatically pushes confirmation notification upon successful submission."),
            ("Status Update Triggers", "Students receive instant notices when coordinators update candidate status."),
            ("Unread Counter & Read State", "Badges indicate unread notices; students can mark them as read.")
        ])
    ]

    for idx, (title, points) in enumerate(app_notif_cards):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(2.1)
        w = Inches(3.8)
        h = Inches(4.8)

        card = add_card(s12, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEAL

        for p_title, p_desc in points:
            p = tf.add_paragraph()
            p.text = f"• {p_title}: {p_desc}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_before = Pt(10)


    # ==========================================
    # SLIDE 13: Database Design & Entity Relationship (ER) Model
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Data Architecture", "Database Design & Entity Relationship (ER)", "Relational database schema modeled in Third Normal Form (3NF)")

    c_left = add_card(s13, Inches(0.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_cl = c_left.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_left = tf_cl.margin_right = tf_cl.margin_top = Inches(0.3)

    p = tf_cl.paragraphs[0]
    p.text = "📐 Relational Design Principles"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    er_points = [
        ("3NF Normalization:", " The schema is designed to 3NF standards, eliminating transitive dependencies, ensuring minimal redundancy and high data integrity."),
        ("User to Student (1 : 1):", " Each Django auth User maps to exactly one Student profile via a OneToOneField foreign key relationship."),
        ("Student to Application (1 : N):", " A student can apply to multiple distinct internship opportunities (protected by a unique composite constraint)."),
        ("Internship to Application (1 : N):", " A single internship opportunity can receive applications from multiple registered students."),
        ("Student to Notification (1 : N):", " Multiple system-generated notification messages are linked to an individual student.")
    ]
    for t, d in er_points:
        p = tf_cl.add_paragraph()
        p.text = "• " + t + d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    c_right = add_card(s13, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.8), RGBColor(248, 250, 252))
    tf_cr = c_right.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = tf_cr.margin_right = tf_cr.margin_top = Inches(0.3)

    p = tf_cr.paragraphs[0]
    p.text = "🔗 Core Entity Relationships"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    diagram_text = [
        ("1. auth_user [PK: id]", "Django Auth User (username, password, email)"),
        ("    │  (1 : 1 OneToOne)", ""),
        ("2. user_management_student [PK: id, FK: user_id]", "Student profile (name, phone, course, created_at)"),
        ("    ├────────┬──────── (1 : N Foreign Key)", ""),
        ("    │        ▼", ""),
        ("    │   internships_notification [PK: id, FK: student_id]", "Alerts & Status notifications (message, is_read)"),
        ("    ▼", ""),
        ("3. internships_application [PK: id]", "Composite: FK(student_id) + FK(internship_id) [STATUS]"),
        ("    ▲", ""),
        ("    │  (1 : N Foreign Key)", ""),
        ("4. internships_internship [PK: id]", "Internship postings (title, company, stipend, deadline)")
    ]

    for line, desc in diagram_text:
        p = tf_cr.add_paragraph()
        if desc:
            p.text = f"{line} → {desc}"
        else:
            p.text = line
        p.font.size = Pt(10)
        p.font.name = "Consolas"
        p.font.color.rgb = DARK_BLUE if "PK" in line else ACCENT_BLUE
        p.space_before = Pt(3)


    # ==========================================
    # SLIDE 14: Database Tables (Part 1: Student & Internship)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Database Schema", "Database Tables: Student & Internship", "Schema specifications, field types, and integrity constraints")

    card_t1 = add_card(s14, Inches(0.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_t1 = card_t1.text_frame
    tf_t1.word_wrap = True
    tf_t1.margin_left = tf_t1.margin_right = tf_t1.margin_top = Inches(0.2)

    p = tf_t1.paragraphs[0]
    p.text = "TABLE 1: Student (user_management_student)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY

    t1_shape = s14.shapes.add_table(7, 3, Inches(0.9), Inches(2.6), Inches(5.5), Inches(4.1))
    t1 = t1_shape.table
    t1.columns[0].width = Inches(1.5)
    t1.columns[1].width = Inches(1.8)
    t1.columns[2].width = Inches(2.2)

    t1_headers = ["Field Name", "Data Type", "Constraints"]
    for i, h in enumerate(t1_headers):
        cell = t1.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    t1_data = [
        ("id", "BIGINT / INT", "PRIMARY KEY, AUTO_INC"),
        ("user_id", "INT", "FOREIGN KEY -> auth_user"),
        ("name", "VARCHAR(100)", "NOT NULL"),
        ("email", "VARCHAR(254)", "NOT NULL"),
        ("phone", "VARCHAR(15)", "NOT NULL"),
        ("course", "VARCHAR(100)", "NOT NULL")
    ]
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            cell = t1.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_BLUE
            if c_idx == 0:
                p.font.bold = True

    card_t2 = add_card(s14, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_t2 = card_t2.text_frame
    tf_t2.word_wrap = True
    tf_t2.margin_left = tf_t2.margin_right = tf_t2.margin_top = Inches(0.2)

    p = tf_t2.paragraphs[0]
    p.text = "TABLE 2: Internship (internships_internship)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    t2_shape = s14.shapes.add_table(10, 3, Inches(6.9), Inches(2.6), Inches(5.5), Inches(4.1))
    t2 = t2_shape.table
    t2.columns[0].width = Inches(1.8)
    t2.columns[1].width = Inches(1.6)
    t2.columns[2].width = Inches(2.1)

    for i, h in enumerate(t1_headers):
        cell = t2.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = ACCENT_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    t2_data = [
        ("id", "BIGINT / INT", "PRIMARY KEY, AUTO_INC"),
        ("title", "VARCHAR(200)", "NOT NULL"),
        ("company_name", "VARCHAR(200)", "NOT NULL"),
        ("description", "TEXT", "NOT NULL"),
        ("location", "VARCHAR(100)", "NOT NULL"),
        ("duration", "VARCHAR(100)", "NOT NULL"),
        ("stipend", "VARCHAR(100)", "NOT NULL"),
        ("skills_required", "VARCHAR(300)", "NOT NULL"),
        ("application_deadline", "DATE", "NOT NULL")
    ]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_BLUE
            if c_idx == 0:
                p.font.bold = True


    # ==========================================
    # SLIDE 15: Database Tables (Part 2: Application & Notification)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Database Schema", "Database Tables: Application & Notification", "Schema specifications, foreign key linkages, and status constraints")

    card_t3 = add_card(s15, Inches(0.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_t3 = card_t3.text_frame
    tf_t3.word_wrap = True
    tf_t3.margin_left = tf_t3.margin_right = tf_t3.margin_top = Inches(0.2)

    p = tf_t3.paragraphs[0]
    p.text = "TABLE 3: Application (internships_application)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL

    t3_shape = s15.shapes.add_table(6, 3, Inches(0.9), Inches(2.6), Inches(5.5), Inches(4.1))
    t3 = t3_shape.table
    t3.columns[0].width = Inches(1.5)
    t3.columns[1].width = Inches(1.6)
    t3.columns[2].width = Inches(2.4)

    for i, h in enumerate(t1_headers):
        cell = t3.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TEAL
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    t3_data = [
        ("id", "BIGINT / INT", "PRIMARY KEY, AUTO_INC"),
        ("student_id", "INT", "FOREIGN KEY -> Student (CASCADE)"),
        ("internship_id", "INT", "FOREIGN KEY -> Internship (CASCADE)"),
        ("applied_at", "DATETIME", "NOT NULL, auto_now_add"),
        ("status", "VARCHAR(20)", "DEFAULT: 'Pending' [Choices: Pending, Under Review, Shortlisted, Selected, Rejected]")
    ]
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            cell = t3.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_BLUE
            if c_idx == 0:
                p.font.bold = True

    p_note = tf_t3.add_paragraph()
    p_note.text = "* Enforces UniqueConstraint: ['student', 'internship'] to prohibit duplicate entries."
    p_note.font.size = Pt(9.5)
    p_note.font.bold = True
    p_note.font.color.rgb = ROSE
    p_note.space_before = Pt(8)

    card_t4 = add_card(s15, Inches(6.8), Inches(2.1), Inches(5.7), Inches(4.8))
    tf_t4 = card_t4.text_frame
    tf_t4.word_wrap = True
    tf_t4.margin_left = tf_t4.margin_right = tf_t4.margin_top = Inches(0.2)

    p = tf_t4.paragraphs[0]
    p.text = "TABLE 4: Notification (internships_notification)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    t4_shape = s15.shapes.add_table(6, 3, Inches(6.9), Inches(2.6), Inches(5.5), Inches(4.1))
    t4 = t4_shape.table
    t4.columns[0].width = Inches(1.5)
    t4.columns[1].width = Inches(1.6)
    t4.columns[2].width = Inches(2.4)

    for i, h in enumerate(t1_headers):
        cell = t4.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = EMERALD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    t4_data = [
        ("id", "BIGINT / INT", "PRIMARY KEY, AUTO_INC"),
        ("student_id", "INT", "FOREIGN KEY -> Student (CASCADE)"),
        ("message", "TEXT", "NOT NULL"),
        ("is_read", "BOOLEAN", "DEFAULT: FALSE"),
        ("created_at", "DATETIME", "NOT NULL, auto_now_add")
    ]
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            cell = t4.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(248, 250, 252)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK_BLUE
            if c_idx == 0:
                p.font.bold = True


    # ==========================================
    # SLIDE 16: Technology Stack Used
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Technologies", "Technology Stack Used", "Tools, frameworks, and programming environments powering InternHub")

    tech_categories = [
        ("🐍 Backend Language", "Python 3.9+", "Core server-side language chosen for its clean syntax, readability, extensive ecosystem, and exceptional web framework maturity."),
        ("🌐 Web Framework", "Django 4.2 LTS", "High-level 'batteries-included' Python web framework providing built-in ORM, Admin console, CSRF protection, and session management."),
        ("🗄️ Relational Database", "MySQL & SQLite", "MySQL 8.x configured for production data persistence; SQLite utilized for rapid unit testing and local development agility."),
        ("🎨 Frontend UI", "HTML5 & CSS3", "Custom modern, responsive UI design featuring CSS grid/flexbox cards, dynamic status badges, and responsive layouts for mobile and desktop."),
        ("📦 Libraries & Tools", "PyMySQL / Forms", "PyMySQL / mysqlclient database driver, Django Form validation libraries, Python-pptx for documentation, and Git for version control."),
        ("💻 Development Environment", "VS Code & Powershell", "Visual Studio Code with Python linting & debugging, Django manage.py command-line tools, and virtual environments (venv).")
    ]

    for idx, (title, tech, desc) in enumerate(tech_categories):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 3.98)
        y = Inches(2.1 + row * 2.45)
        w = Inches(3.8)
        h = Inches(2.25)

        card = add_card(s16, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = tech
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(6)


    # ==========================================
    # SLIDE 17: System Testing & Quality Assurance
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "Verification", "System Testing & Quality Assurance", "Testing methodology ensuring stability, security, and operational reliability")

    test_phases = [
        ("🧪 Unit Testing", "Individual Models & Views", [
            ("Model Field Validation", "Verified data types, nullability, max lengths, and choice restrictions on status."),
            ("Custom String Output", "Tested __str__() representations for Student, Internship, and Notification models."),
            ("ORM Query Accuracy", "Tested ordering logic (-created_at) and keyword Q-object search filtering.")
        ]),
        ("🔄 Integration Testing", "End-to-End Workflows", [
            ("Student Onboarding", "Tested registration flow creating Django User and custom Student record simultaneously."),
            ("Application Flow", "Verified that applying creates Application record, updates counters, and sends notification."),
            ("Status Update Flow", "Confirmed that admin status changes update student dashboard and trigger notifications.")
        ]),
        ("🛡️ Security & Boundary Testing", "Security Safeguards", [
            ("Authentication Guards", "Verified that unauthorized URLs redirect unauthenticated users to the login screen."),
            ("Anti-Duplicate Constraint", "Tested that submitting duplicate applications is rejected both at DB and view levels."),
            ("CSRF & Injection Protection", "Validated Django CSRF token enforcement and ORM parameterization preventing SQLi.")
        ])
    ]

    for idx, (title, subtitle, bullets) in enumerate(test_phases):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(2.1)
        w = Inches(3.8)
        h = Inches(4.8)

        card = add_card(s17, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        p.space_before = Pt(3)

        for b_title, b_desc in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b_title}: {b_desc}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_MAIN
            p.space_before = Pt(10)


    # ==========================================
    # SLIDE 18: Future Enhancements
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, "Roadmap", "Future Enhancements", "Strategic expansion roadmap to scale InternHub into an enterprise ecosystem")

    enhancements = [
        ("🤖 AI Resume Parser & Matcher", "Integrate NLP to parse student resumes (PDF/DOCX), extract key skills, and recommend the best-matching internships automatically using ML similarity scoring."),
        ("🏢 Dedicated Recruiter / Company Portal", "Expand the platform beyond college admins to allow verified company HRs to create postings, review applicant pools, and shortlist candidates directly."),
        ("📅 Integrated Interview Scheduling", "Add an interactive scheduling calendar with Google Calendar / Zoom / WebRTC integration for scheduling and conducting virtual interviews."),
        ("📱 Native Mobile Application", "Develop cross-platform mobile apps using Flutter or React Native to provide push notifications, mobile application tracking, and instant alerts."),
        ("📩 Automated Email & SMS Alerts", "Integrate Celery background workers with SendGrid / Twilio to send instant SMS and email alerts whenever application statuses change."),
        ("🎓 Digital Certificate Issuance", "Implement automated, cryptographically verifiable digital certificate generation upon successful completion of an internship.")
    ]

    for idx, (title, desc) in enumerate(enhancements):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8 + col * 3.98)
        y = Inches(2.1 + row * 2.45)
        w = Inches(3.8)
        h = Inches(2.25)

        card = add_card(s18, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)


    # ==========================================
    # SLIDE 19: Conclusion & Summary
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, "Summary", "Conclusion & Project Impact", "Key deliverables, project milestones, and value delivered by InternHub")

    c_summary_cards = [
        ("🏆 Project Achievements", [
            ("Unified Campus Portal", "Successfully replaced fragmented, manual internship search methods with a centralized digital catalog."),
            ("Transparent Student Journey", "Delivered real-time status visibility (Pending, Shortlisted, Selected, Rejected) eliminating student uncertainty."),
            ("Data Integrity Guaranteed", "Enforced database constraints that prevent duplicate applications and maintain clean records."),
            ("Productive Administration", "Significantly streamlined the administrative overhead of listing openings and reviewing applicants.")
        ]),
        ("💡 Key Takeaways & Technical Growth", [
            ("Full-Stack Django Mastery", "Deep practical experience architecting Django MVT systems, ORM relationships, forms, and custom admin views."),
            ("Database Normalization", "Designed a robust, scalable MySQL schema in 3NF with cascading foreign keys and composite constraints."),
            ("Responsive Web Design", "Developed clean, mobile-friendly frontend templates with dynamic DTL rendering and modern CSS aesthetics."),
            ("Production Readiness", "System is fully functional, secure, tested, and primed for campus-wide institutional deployment.")
        ])
    ]

    for idx, (title, bullets) in enumerate(c_summary_cards):
        x = Inches(0.8 + idx * 5.95)
        y = Inches(2.1)
        w = Inches(5.78)
        h = Inches(4.8)

        card = add_card(s19, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = NAVY

        for b_title, b_desc in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b_title}: {b_desc}"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN
            p.space_before = Pt(12)


    # ==========================================
    # SLIDE 20: Thank You & Q&A Slide
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20, DARK_BLUE)

    banner20 = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    banner20.fill.solid()
    banner20.fill.fore_color.rgb = ACCENT_BLUE
    banner20.line.fill.background()

    c_box = s20.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.333), Inches(2.2))
    tf_cb = c_box.text_frame
    tf_cb.word_wrap = True
    p = tf_cb.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf_cb.add_paragraph()
    p.text = "Questions & Answers / Discussion"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(8)

    p = tf_cb.add_paragraph()
    p.text = "InternHub — College Internship Management System"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(10)

    card_ty = add_card(s20, Inches(2.5), Inches(4.5), Inches(8.333), Inches(2.0), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
    tf_ty = card_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_top = Inches(0.25)

    p = tf_ty.paragraphs[0]
    p.text = "HISANA HAMZA  |  Register No: MEA25MCA-2010"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf_ty.add_paragraph()
    p.text = "Project Guide: Mr. Adil Narakkoden, Assistant Professor"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = tf_ty.add_paragraph()
    p.text = "Department of Computer Applications — MEA Engineering College, Perinthalmanna"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = tf_ty.add_paragraph()
    p.text = "APJ Abdul Kalam Technological University (KTU)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.alignment = PP_ALIGN.CENTER

    output_filename = "InternHub_College_Internship_Management_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully as '{output_filename}' ({len(prs.slides)} slides)")

if __name__ == "__main__":
    create_presentation()
