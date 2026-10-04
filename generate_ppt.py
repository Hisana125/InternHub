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
        ("🔐 Student Login & Profiles", "Simple sign-up and secure login. Students can view and update their personal and academic details anytime."),
        ("🔍 Smart Job Search", "Fast search bar to filter internships by job title, company name, location, or required programming skills."),
        ("⚡ 1-Click Application", "Instant application submission that connects the student's profile directly to the chosen internship."),
        ("📊 Student Dashboard", "Clear dashboard showing counts for Total Applied, Pending, Selected, and Rejected applications."),
        ("🔔 Notification Alerts", "Built-in notification center with an unread badge that informs students whenever their status changes."),
        ("🛠️ Admin Control Panel", "Dedicated admin panel for staff to post internships, review registered students, and update application results.")
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
    add_header(s6, "Slide 6 • System Structure", "Module Description", "The 3 main functional modules of the InternHub project")

    modules = [
        ("👤 Module 1: User Management", NAVY, [
            ("Student Registration:", " Students sign up with username, password, email, phone, and course."),
            ("Secure Authentication:", " Login and logout protected by Django's password security."),
            ("Profile Management:", " Students can view and update their contact details."),
            ("Personal Dashboard:", " Shows live summary cards of application progress.")
        ]),
        ("💼 Module 2: Internship Portal", ACCENT_BLUE, [
            ("Job Listings:", " Displays company name, role, stipend, location, duration, and deadline."),
            ("Keyword Search:", " Search across job titles, company names, cities, and required skills."),
            ("Details Page:", " Full job description and requirements with an 'Apply' button."),
            ("Chronological Order:", " Newest internships always appear at the top.")
        ]),
        ("📋 Module 3: Application & Alerts", GREEN, [
            ("1-Click Apply:", " Links the student profile to the selected internship."),
            ("Anti-Duplicate Rule:", " Prevents student from submitting twice to the same opening."),
            ("Status Tracking:", " Shows statuses: Pending, Under Review, Shortlisted, Selected, Rejected."),
            ("In-App Notifications:", " Informs students as soon as coordinator updates their status.")
        ])
    ]

    for idx, (title, col, items) in enumerate(modules):
        x = Inches(0.8 + idx * 3.98)
        y = Inches(2.0)
        w = Inches(3.8)
        h = Inches(4.9)

        card = add_card(s6, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.28)
        tf.margin_top = Inches(0.25)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col

        for h_item, b_item in items:
            p = tf.add_paragraph()
            p.text = f"• {h_item} {b_item}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(10)


    # =========================================================================
    # SLIDE 7: Database Tables
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "Slide 7 • Database", "Database Tables", "The 4 core tables used to store and manage project data")

    tables = [
        ("1. Student Table (user_management_student)", NAVY, [
            ("id:", " Unique student ID (Primary Key)"),
            ("user_id:", " Links to Django Auth User login"),
            ("name, email, phone:", " Contact details of the student"),
            ("course:", " Enrolled course (e.g., MCA, B.Tech)")
        ]),
        ("2. Internship Table (internships_internship)", ACCENT_BLUE, [
            ("id:", " Unique internship ID (Primary Key)"),
            ("title & company_name:", " Job role and hiring company"),
            ("location, duration, stipend:", " Work terms & pay"),
            ("skills_required & deadline:", " Skill requirements & last date")
        ]),
        ("3. Application Table (internships_application)", GREEN, [
            ("id:", " Unique application ID (Primary Key)"),
            ("student_id & internship_id:", " Foreign Keys connecting student to job"),
            ("applied_at:", " Date and time of application"),
            ("status:", " Pending, Shortlisted, Selected, or Rejected"),
            ("* Unique Rule:", " A student cannot apply twice for the same job")
        ]),
        ("4. Notification Table (internships_notification)", RGBColor(217, 119, 6), [
            ("id:", " Unique notification ID (Primary Key)"),
            ("student_id:", " Target student receiving the alert"),
            ("message:", " Alert text (e.g., 'Application Submitted')"),
            ("is_read:", " True/False (Tracks unread messages)")
        ])
    ]

    for idx, (t_title, t_col, t_fields) in enumerate(tables):
        r = idx // 2
        c = idx % 2
        x = Inches(0.8 + c * 5.95)
        y = Inches(2.0 + r * 2.5)
        w = Inches(5.78)
        h = Inches(2.35)

        card = add_card(s7, x, y, w, h)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = t_col

        for f_name, f_desc in t_fields:
            p = tf.add_paragraph()
            p.text = f"• {f_name}{f_desc}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(4)


    # =========================================================================
    # SLIDE 8: Technology Stack Used
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "Slide 8 • Tech Stack", "Technology Stack Used", "Programming language, database, framework, and tools used")

    tech_items = [
        ("🐍 Programming Language", "Python 3.9+", "Primary backend language. Chosen because it is clean, easy to read, and has great web framework support."),
        ("🌐 Web Framework", "Django 4.2 LTS", "A robust Python web framework that comes with built-in security, user authentication, and admin panel."),
        ("🗄️ Relational Database", "MySQL Database", "MySQL is the active database storing all student records, job postings, applications, and notifications."),
        ("🎨 Frontend (UI)", "HTML5 & CSS3", "Clean and responsive user interface with card layouts that look great on both desktop screens and mobile phones."),
        ("📦 Libraries & Drivers", "mysqlclient & Forms", "mysqlclient (MySQLdb) connects Django to MySQL. Django Forms handles user input validation."),
        ("💻 Development Tools", "VS Code & Git", "Visual Studio Code used as the code editor, and Git used for source code version management.")
    ]

    for idx, (t_title, t_sub, t_desc) in enumerate(tech_items):
        r = idx // 3
        c = idx % 3
        x = Inches(0.8 + c * 3.98)
        y = Inches(2.0 + r * 2.5)
        w = Inches(3.8)
        h = Inches(2.3)

        card = add_card(s8, x, y, w, h)
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
    # SLIDE 9: Future Enhancements
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "Slide 9 • Roadmap", "Future Enhancements", "Useful features that can be added in future versions")

    enhances = [
        ("🤖 AI Resume Parser & Matcher", "Automatically scan student PDF resumes, extract technical skills, and recommend the best-fitting internships."),
        ("🏢 Direct Company/Recruiter Login", "Allow hiring managers from companies to post their own internships and shortlist students directly."),
        ("📩 Automated Email & SMS Alerts", "Send instant email and SMS messages to students when an interview is scheduled or an application is accepted."),
        ("📅 Integrated Interview Scheduling", "Add an in-app calendar to schedule interview dates and connect with Google Meet or Zoom."),
        ("📱 Mobile Application", "Develop an Android and iOS mobile app using Flutter so students can apply and check alerts on their phones."),
        ("🎓 Digital Completion Certificates", "Automatically generate verified digital certificates for students upon successful completion of their internship.")
    ]

    for idx, (head, body) in enumerate(enhances):
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
    # SLIDE 10: Conclusion & Thank You
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, DARK_BLUE)

    top_strip10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_strip10.fill.solid()
    top_strip10.fill.fore_color.rgb = ACCENT_BLUE
    top_strip10.line.fill.background()

    # Left: Conclusion Summary Card
    c_concl = add_card(s10, Inches(1.0), Inches(1.2), Inches(5.4), Inches(5.2), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
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
        ("Solves a Real Problem:", " Replaces slow, manual paper circulars with an easy, centralized website."),
        ("Empowers Students:", " Provides full transparency with 1-click apply, real-time status tracking, and instant alerts."),
        ("Reduces Staff Workload:", " Cuts down coordinator effort and completely prevents duplicate applications."),
        ("Clean Architecture:", " Built on Django's proven MVT architecture with a safe, normalized MySQL database.")
    ]
    for h, b in concl_points:
        p = tf_cc.add_paragraph()
        p.text = "• " + h + b
        p.font.size = Pt(11.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(14)

    # Right: Thank You Box
    c_ty = add_card(s10, Inches(6.9), Inches(1.2), Inches(5.4), Inches(5.2), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
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

    output_filename = "InternHub_College_Internship_Management_Presentation.pptx"
    try:
        prs.save(output_filename)
        print(f"Presentation saved successfully as '{output_filename}' ({len(prs.slides)} slides)")
    except PermissionError:
        alt_filename = "InternHub_Project_Presentation_10_Slides.pptx"
        prs.save(alt_filename)
        print(f"Primary file was open in PowerPoint. Presentation saved as '{alt_filename}' ({len(prs.slides)} slides)")

if __name__ == "__main__":
    create_10_slide_presentation()
