import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFont

SCALE = 2
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)

ROOT_DIR = os.path.abspath(r"c:\Users\hisan\OneDrive\Documents\Project\InternHub")
DIAGRAMS_DIR = os.path.join(ROOT_DIR, "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def get_fonts():
    try:
        font_entity = ImageFont.truetype("arialbd.ttf", 15 * SCALE)
        font_login = ImageFont.truetype("arialbd.ttf", 14 * SCALE)
        font_major = ImageFont.truetype("arial.ttf", 12.5 * SCALE)
        font_proc = ImageFont.truetype("arial.ttf", 12.5 * SCALE)
        font_sub = ImageFont.truetype("arial.ttf", 11.5 * SCALE)
        font_store = ImageFont.truetype("arial.ttf", 13 * SCALE)
        font_flow = ImageFont.truetype("arial.ttf", 9.5 * SCALE)
    except Exception:
        font_entity = ImageFont.load_default()
        font_login = ImageFont.load_default()
        font_major = ImageFont.load_default()
        font_proc = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_store = ImageFont.load_default()
        font_flow = ImageFont.load_default()
    return font_entity, font_login, font_major, font_proc, font_sub, font_store, font_flow

def draw_arrow(draw, start, end, fill=LINE_COLOR, width=int(1.8*SCALE), head_len=int(9*SCALE)):
    draw.line([start, end], fill=fill, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    
    x1 = end[0] - head_len * math.cos(angle - math.pi / 7)
    y1 = end[1] - head_len * math.sin(angle - math.pi / 7)
    x2 = end[0] - head_len * math.cos(angle + math.pi / 7)
    y2 = end[1] - head_len * math.sin(angle + math.pi / 7)
    draw.polygon([end, (x1, y1), (x2, y2)], fill=fill)

def draw_dfd_store(draw, x1, y1, x2, y2, label, font):
    w = int(1.8 * SCALE)
    draw.line([(x1, y1), (x2, y1)], fill=LINE_COLOR, width=w)
    draw.line([(x1, y2), (x2, y2)], fill=LINE_COLOR, width=w)
    draw.line([(x1, y1), (x1, y2)], fill=LINE_COLOR, width=w)
    inner_x = x1 + 18 * SCALE
    draw.line([(inner_x, y1), (inner_x, y2)], fill=LINE_COLOR, width=w)
    
    bb = draw.textbbox((0, 0), label, font=font)
    lw = bb[2] - bb[0]
    lh = bb[3] - bb[1]
    draw.text((inner_x + (x2 - inner_x - lw) // 2, (y1 + y2 - lh) // 2), label, fill=TEXT_COLOR, font=font)

def save_image(img, target_filename, target_dims):
    downsampled = img.resize(target_dims, Image.Resampling.LANCZOS)
    path1 = os.path.join(DIAGRAMS_DIR, target_filename)
    path2 = os.path.join(ROOT_DIR, target_filename)
    downsampled.save(path1, "PNG", dpi=(300, 300))
    downsampled.save(path2, "PNG", dpi=(300, 300))
    print(f"Saved: {path1} and {path2}")

# 1. DFD LEVEL 0
def generate_dfd_level_0():
    WIDTH = 1300 * SCALE
    HEIGHT = 700 * SCALE
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    try:
        font_ent = ImageFont.truetype("arialbd.ttf", 17 * SCALE)
        font_proc = ImageFont.truetype("arial.ttf", 16.5 * SCALE)
        font_fl = ImageFont.truetype("arial.ttf", 13.5 * SCALE)
    except Exception:
        font_ent = ImageFont.load_default()
        font_proc = ImageFont.load_default()
        font_fl = ImageFont.load_default()

    CX = 650 * SCALE
    CY = 470 * SCALE
    RX = 175 * SCALE
    RY = 80 * SCALE

    draw.ellipse([CX - RX, CY - RY, CX + RX, CY + RY], outline=LINE_COLOR, width=2 * SCALE, fill=(255, 255, 255))
    proc_text1 = "College Internship"
    proc_text2 = "Management System"
    bb1 = draw.textbbox((0, 0), proc_text1, font=font_proc)
    bb2 = draw.textbbox((0, 0), proc_text2, font=font_proc)
    draw.text((CX - (bb1[2] - bb1[0]) // 2, CY - (bb1[3] - bb1[1]) - 4 * SCALE), proc_text1, fill=TEXT_COLOR, font=font_proc)
    draw.text((CX - (bb2[2] - bb2[0]) // 2, CY + 4 * SCALE), proc_text2, fill=TEXT_COLOR, font=font_proc)

    TOP_W = 240 * SCALE
    TOP_H = 105 * SCALE
    TOP_X1 = CX - TOP_W // 2
    TOP_Y1 = 60 * SCALE
    TOP_X2 = CX + TOP_W // 2
    TOP_Y2 = TOP_Y1 + TOP_H
    draw.rectangle([TOP_X1, TOP_Y1, TOP_X2, TOP_Y2], outline=LINE_COLOR, width=2 * SCALE, fill=(255, 255, 255))
    bb_adm = draw.textbbox((0, 0), "Admin", font=font_ent)
    draw.text((CX - (bb_adm[2] - bb_adm[0]) // 2, (TOP_Y1 + TOP_Y2 - (bb_adm[3] - bb_adm[1])) // 2), "Admin", fill=TEXT_COLOR, font=font_ent)

    SIDE_W = 240 * SCALE
    SIDE_H = 105 * SCALE
    LEFT_X1 = 80 * SCALE
    LEFT_Y1 = CY - SIDE_H // 2
    LEFT_X2 = LEFT_X1 + SIDE_W
    LEFT_Y2 = LEFT_Y1 + SIDE_H
    draw.rectangle([LEFT_X1, LEFT_Y1, LEFT_X2, LEFT_Y2], outline=LINE_COLOR, width=2 * SCALE, fill=(255, 255, 255))
    bb_stu = draw.textbbox((0, 0), "Student", font=font_ent)
    draw.text(((LEFT_X1 + LEFT_X2 - (bb_stu[2] - bb_stu[0])) // 2, (LEFT_Y1 + LEFT_Y2 - (bb_stu[3] - bb_stu[1])) // 2), "Student", fill=TEXT_COLOR, font=font_ent)

    RIGHT_X2 = (1300 - 80) * SCALE
    RIGHT_X1 = RIGHT_X2 - SIDE_W
    RIGHT_Y1 = CY - SIDE_H // 2
    RIGHT_Y2 = RIGHT_Y1 + SIDE_H
    draw.rectangle([RIGHT_X1, RIGHT_Y1, RIGHT_X2, RIGHT_Y2], outline=LINE_COLOR, width=2 * SCALE, fill=(255, 255, 255))
    bb_comp = draw.textbbox((0, 0), "Company", font=font_ent)
    draw.text(((RIGHT_X1 + RIGHT_X2 - (bb_comp[2] - bb_comp[0])) // 2, (RIGHT_Y1 + RIGHT_Y2 - (bb_comp[3] - bb_comp[1])) // 2), "Company", fill=TEXT_COLOR, font=font_ent)

    GAP = 40 * SCALE
    adm_down_x = CX - GAP
    draw_arrow(draw, (adm_down_x, TOP_Y2), (adm_down_x, CY - RY), width=int(1.8*SCALE))
    draw.text((adm_down_x - 70 * SCALE, (TOP_Y2 + CY - RY) // 2 - 10 * SCALE), "Request", fill=TEXT_COLOR, font=font_fl)

    adm_up_x = CX + GAP
    draw_arrow(draw, (adm_up_x, CY - RY), (adm_up_x, TOP_Y2), width=int(1.8*SCALE))
    draw.text((adm_up_x + 35 * SCALE, (TOP_Y2 + CY - RY) // 2 - 10 * SCALE), "Response", fill=TEXT_COLOR, font=font_fl)

    Y_GAP = 30 * SCALE
    stu_req_y = CY - Y_GAP
    draw_arrow(draw, (LEFT_X2, stu_req_y), (CX - RX, stu_req_y), width=int(1.8*SCALE))
    draw.text(((LEFT_X2 + CX - RX) // 2 - 25 * SCALE, stu_req_y - 25 * SCALE), "Request", fill=TEXT_COLOR, font=font_fl)

    stu_resp_y = CY + Y_GAP
    draw_arrow(draw, (CX - RX, stu_resp_y), (LEFT_X2, stu_resp_y), width=int(1.8*SCALE))
    draw.text(((LEFT_X2 + CX - RX) // 2 - 30 * SCALE, stu_resp_y + 10 * SCALE), "Response", fill=TEXT_COLOR, font=font_fl)

    comp_req_y = CY - Y_GAP
    draw_arrow(draw, (RIGHT_X1, comp_req_y), (CX + RX, comp_req_y), width=int(1.8*SCALE))
    draw.text(((CX + RX + RIGHT_X1) // 2 - 25 * SCALE, comp_req_y - 25 * SCALE), "Request", fill=TEXT_COLOR, font=font_fl)

    comp_resp_y = CY + Y_GAP
    draw_arrow(draw, (CX + RX, comp_resp_y), (RIGHT_X1, comp_resp_y), width=int(1.8*SCALE))
    draw.text(((CX + RX + RIGHT_X1) // 2 - 30 * SCALE, comp_resp_y + 10 * SCALE), "Response", fill=TEXT_COLOR, font=font_fl)

    save_image(img, "dfd_level_0.png", (1300, 700))

# 2. DFD LEVEL 1 - CLEAN SINGLE ARROW INTO LOGIN
def render_dfd1(entity_name, table_name, items, output_filename):
    WIDTH = 1250 * SCALE
    HEIGHT = 800 * SCALE
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    f_ent, f_login, _, f_proc, _, f_store, f_flow = get_fonts()

    proc_ys = [
        int(120 * SCALE),
        int(250 * SCALE),
        int(380 * SCALE),
        int(510 * SCALE),
        int(640 * SCALE)
    ]
    
    ent_w = int(130 * SCALE)
    ent_h = int(75 * SCALE)
    ent_cx = int(80 * SCALE)
    ent_cy = proc_ys[2]
    ent_x1 = ent_cx - ent_w // 2
    ent_y1 = ent_cy - ent_h // 2
    ent_x2 = ent_x1 + ent_w
    ent_y2 = ent_y1 + ent_h
    
    draw.rectangle([ent_x1, ent_y1, ent_x2, ent_y2], outline=LINE_COLOR, width=int(1.8 * SCALE), fill=(255, 255, 255))
    bb_ent = draw.textbbox((0, 0), entity_name, font=f_ent)
    draw.text((ent_cx - (bb_ent[2] - bb_ent[0]) // 2, ent_cy - (bb_ent[3] - bb_ent[1]) // 2), entity_name, fill=TEXT_COLOR, font=f_ent)

    LOGIN_CX = int(240 * SCALE)
    LOGIN_CY = proc_ys[2]
    LOGIN_R = int(42 * SCALE)
    
    draw.ellipse([LOGIN_CX - LOGIN_R, LOGIN_CY - LOGIN_R, LOGIN_CX + LOGIN_R, LOGIN_CY + LOGIN_R], outline=LINE_COLOR, width=int(1.8 * SCALE), fill=(255, 255, 255))
    bb_log = draw.textbbox((0, 0), "Login", font=f_login)
    draw.text((LOGIN_CX - (bb_log[2] - bb_log[0]) // 2, LOGIN_CY - (bb_log[3] - bb_log[1]) // 2), "Login", fill=TEXT_COLOR, font=f_login)

    # Clean single arrow from Entity to Login labeled Request
    bb_rf = draw.textbbox((0, 0), "Request", font=f_flow)
    bb_rs = draw.textbbox((0, 0), "Response", font=f_flow)

    draw_arrow(draw, (ent_x2, ent_cy), (LOGIN_CX - LOGIN_R, ent_cy))
    draw.text(((ent_x2 + LOGIN_CX - LOGIN_R - (bb_rf[2] - bb_rf[0])) // 2, ent_cy - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

    top_store_w = int(160 * SCALE)
    top_store_h = int(55 * SCALE)
    top_x1 = int(160 * SCALE)
    top_x2 = top_x1 + top_store_w
    top_y1 = int(70 * SCALE)
    top_y2 = top_y1 + top_store_h
    
    draw_dfd_store(draw, top_x1, top_y1, top_x2, top_y2, table_name, f_store)

    top_req_x = LOGIN_CX - int(16 * SCALE)
    draw_arrow(draw, (top_req_x, LOGIN_CY - LOGIN_R), (top_req_x, top_y2))
    draw.text((top_req_x - int(45 * SCALE), (top_y2 + LOGIN_CY - LOGIN_R) // 2 - int(6 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

    top_resp_x = LOGIN_CX + int(16 * SCALE)
    draw_arrow(draw, (top_resp_x, top_y2), (top_resp_x, LOGIN_CY - LOGIN_R))
    draw.text((top_resp_x + int(8 * SCALE), (top_y2 + LOGIN_CY - LOGIN_R) // 2 - int(6 * SCALE)), "Response", fill=TEXT_COLOR, font=f_flow)

    BUS_X = int(360 * SCALE)
    draw.line([(LOGIN_CX + LOGIN_R, LOGIN_CY), (BUS_X, LOGIN_CY)], fill=LINE_COLOR, width=int(1.8 * SCALE))
    draw.line([(BUS_X, proc_ys[0]), (BUS_X, proc_ys[4])], fill=LINE_COLOR, width=int(1.8 * SCALE))

    PROC_CX = int(585 * SCALE)
    PROC_RX = int(135 * SCALE)
    PROC_RY = int(45 * SCALE)
    
    STORE_X1 = int(875 * SCALE)
    STORE_X2 = int(1110 * SCALE)
    STORE_H = int(56 * SCALE)

    for i, (proc_text, store_text) in enumerate(items):
        py = proc_ys[i]

        draw_arrow(draw, (BUS_X, py), (PROC_CX - PROC_RX, py))
        draw.text(((BUS_X + PROC_CX - PROC_RX - (bb_rf[2] - bb_rf[0])) // 2, py - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

        draw.ellipse([PROC_CX - PROC_RX, py - PROC_RY, PROC_CX + PROC_RX, py + PROC_RY], outline=LINE_COLOR, width=int(1.8 * SCALE), fill=(255, 255, 255))
        
        lines = proc_text.split("\n")
        if len(lines) == 1:
            bb = draw.textbbox((0, 0), lines[0], font=f_proc)
            draw.text((PROC_CX - (bb[2] - bb[0]) // 2, py - (bb[3] - bb[1]) // 2), lines[0], fill=TEXT_COLOR, font=f_proc)
        else:
            bb1 = draw.textbbox((0, 0), lines[0], font=f_proc)
            bb2 = draw.textbbox((0, 0), lines[1], font=f_proc)
            draw.text((PROC_CX - (bb1[2] - bb1[0]) // 2, py - int(14 * SCALE)), lines[0], fill=TEXT_COLOR, font=f_proc)
            draw.text((PROC_CX - (bb2[2] - bb2[0]) // 2, py + int(4 * SCALE)), lines[1], fill=TEXT_COLOR, font=f_proc)

        p_req_y = py - int(10 * SCALE)
        p_resp_y = py + int(10 * SCALE)

        draw_arrow(draw, (PROC_CX + PROC_RX, p_req_y), (STORE_X1, p_req_y))
        draw.text(((PROC_CX + PROC_RX + STORE_X1 - (bb_rf[2] - bb_rf[0])) // 2, p_req_y - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

        draw_arrow(draw, (STORE_X1, p_resp_y), (PROC_CX + PROC_RX, p_resp_y))
        draw.text(((PROC_CX + PROC_RX + STORE_X1 - (bb_rs[2] - bb_rs[0])) // 2, p_resp_y + int(3 * SCALE)), "Response", fill=TEXT_COLOR, font=f_flow)

        sy1 = py - STORE_H // 2
        sy2 = py + STORE_H // 2
        draw_dfd_store(draw, STORE_X1, sy1, STORE_X2, sy2, store_text, f_store)

    save_image(img, output_filename, (1250, 800))

# 3. DFD LEVEL 2
def render_clustered_dfd2(entity_name, clusters, output_filename):
    WIDTH = 1350 * SCALE
    HEIGHT = 1000 * SCALE
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    f_ent, _, f_major, _, f_sub, f_store, f_flow = get_fonts()

    group_y_coords = [
        [int(65 * SCALE), int(145 * SCALE), int(225 * SCALE), int(305 * SCALE)],
        [int(430 * SCALE), int(500 * SCALE), int(570 * SCALE)],
        [int(735 * SCALE), int(815 * SCALE)]
    ]
    
    major_cy = [
        int(185 * SCALE),
        int(500 * SCALE),
        int(775 * SCALE)
    ]
    
    ent_w = int(130 * SCALE)
    ent_h = int(75 * SCALE)
    ent_cx = int(85 * SCALE)
    ent_cy = major_cy[1]
    ent_x1 = ent_cx - ent_w // 2
    ent_y1 = ent_cy - ent_h // 2
    ent_x2 = ent_x1 + ent_w
    ent_y2 = ent_y1 + ent_h
    
    draw.rectangle([ent_x1, ent_y1, ent_x2, ent_y2], outline=LINE_COLOR, width=int(1.8 * SCALE), fill=(255, 255, 255))
    bb_ent = draw.textbbox((0, 0), entity_name, font=f_ent)
    draw.text((ent_cx - (bb_ent[2] - bb_ent[0]) // 2, ent_cy - (bb_ent[3] - bb_ent[1]) // 2), entity_name, fill=TEXT_COLOR, font=f_ent)

    BUS1_X = int(245 * SCALE)
    bb_rf = draw.textbbox((0, 0), "Request", font=f_flow)
    bb_rs = draw.textbbox((0, 0), "Response", font=f_flow)

    draw.line([(ent_x2, ent_cy), (BUS1_X, ent_cy)], fill=LINE_COLOR, width=int(1.8 * SCALE))
    draw.text(((ent_x2 + BUS1_X - (bb_rf[2] - bb_rf[0])) // 2, ent_cy - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

    draw.line([(BUS1_X, major_cy[0]), (BUS1_X, major_cy[2])], fill=LINE_COLOR, width=int(1.8 * SCALE))

    MAJOR_CX = int(365 * SCALE)
    MAJOR_R = int(56 * SCALE)

    SUB_CX = int(680 * SCALE)
    SUB_RX = int(96 * SCALE)
    SUB_RY = int(28 * SCALE)

    STORE_X1 = int(960 * SCALE)
    STORE_X2 = int(1250 * SCALE)
    STORE_H = int(48 * SCALE)

    for g_idx, cluster in enumerate(clusters):
        major_label = cluster['major']
        sub_items = cluster['subs']
        m_cy = major_cy[g_idx]

        draw_arrow(draw, (BUS1_X, m_cy), (MAJOR_CX - MAJOR_R, m_cy))

        draw.ellipse([MAJOR_CX - MAJOR_R, m_cy - MAJOR_R, MAJOR_CX + MAJOR_R, m_cy + MAJOR_R], outline=LINE_COLOR, width=int(1.8 * SCALE), fill=(255, 255, 255))
        m_lines = major_label.split("\n")
        if len(m_lines) == 1:
            bb = draw.textbbox((0, 0), m_lines[0], font=f_major)
            draw.text((MAJOR_CX - (bb[2] - bb[0]) // 2, m_cy - (bb[3] - bb[1]) // 2), m_lines[0], fill=TEXT_COLOR, font=f_major)
        else:
            bb1 = draw.textbbox((0, 0), m_lines[0], font=f_major)
            bb2 = draw.textbbox((0, 0), m_lines[1], font=f_major)
            draw.text((MAJOR_CX - (bb1[2] - bb1[0]) // 2, m_cy - int(12 * SCALE)), m_lines[0], fill=TEXT_COLOR, font=f_major)
            draw.text((MAJOR_CX - (bb2[2] - bb2[0]) // 2, m_cy + int(4 * SCALE)), m_lines[1], fill=TEXT_COLOR, font=f_major)

        BUS2_X = int(520 * SCALE)
        sub_ys = group_y_coords[g_idx]

        draw.line([(MAJOR_CX + MAJOR_R, m_cy), (BUS2_X, m_cy)], fill=LINE_COLOR, width=int(1.8 * SCALE))
        draw.text(((MAJOR_CX + MAJOR_R + BUS2_X - (bb_rf[2] - bb_rf[0])) // 2, m_cy - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

        draw.line([(BUS2_X, sub_ys[0]), (BUS2_X, sub_ys[-1])], fill=LINE_COLOR, width=int(1.8 * SCALE))

        for s_idx, (sub_name, store_name, is_dual) in enumerate(sub_items):
            sy = sub_ys[s_idx]

            draw_arrow(draw, (BUS2_X, sy), (SUB_CX - SUB_RX, sy))

            draw.ellipse([SUB_CX - SUB_RX, sy - SUB_RY, SUB_CX + SUB_RX, sy + SUB_RY], outline=LINE_COLOR, width=int(1.8 * SCALE), fill=(255, 255, 255))
            bb_sub = draw.textbbox((0, 0), sub_name, font=f_sub)
            draw.text((SUB_CX - (bb_sub[2] - bb_sub[0]) // 2, sy - (bb_sub[3] - bb_sub[1]) // 2), sub_name, fill=TEXT_COLOR, font=f_sub)

            st_y1 = sy - STORE_H // 2
            st_y2 = sy + STORE_H // 2
            draw_dfd_store(draw, STORE_X1, st_y1, STORE_X2, st_y2, store_name, f_store)

            s_req_y = sy - int(8 * SCALE)
            s_resp_y = sy + int(8 * SCALE)
            
            if is_dual:
                draw_arrow(draw, (SUB_CX + SUB_RX, s_req_y), (STORE_X1, s_req_y))
                draw.text(((SUB_CX + SUB_RX + STORE_X1 - (bb_rf[2] - bb_rf[0])) // 2, s_req_y - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

                draw_arrow(draw, (STORE_X1, s_resp_y), (SUB_CX + SUB_RX, s_resp_y))
                draw.text(((SUB_CX + SUB_RX + STORE_X1 - (bb_rs[2] - bb_rs[0])) // 2, s_resp_y + int(3 * SCALE)), "Response", fill=TEXT_COLOR, font=f_flow)
            else:
                draw_arrow(draw, (SUB_CX + SUB_RX, sy), (STORE_X1, sy))
                draw.text(((SUB_CX + SUB_RX + STORE_X1 - (bb_rf[2] - bb_rf[0])) // 2, sy - int(13 * SCALE)), "Request", fill=TEXT_COLOR, font=f_flow)

    save_image(img, output_filename, (1350, 1000))

if __name__ == "__main__":
    generate_dfd_level_0()

    student_items = [
        ("View Dashboard\n& Statistics", "Dashboard"),
        ("Manage Profile\n& Resume", "Students"),
        ("Search & Browse\nInternships", "Internships"),
        ("Submit Internship\nApplication", "Applications"),
        ("View Status\n& Notifications", "Notifications")
    ]
    render_dfd1("Student", "Student Table", student_items, "dfd_level_1_student.png")

    company_items = [
        ("View Dashboard\n& Statistics", "Dashboard"),
        ("Manage Company\nProfile", "Companies"),
        ("Post & Manage\nInternships", "Internships"),
        ("Review Student\nApplicants", "Applications"),
        ("Update Hiring\nStatus", "Notifications")
    ]
    render_dfd1("Company", "Company Table", company_items, "dfd_level_1_company.png")

    admin_items = [
        ("View Dashboard\n& Statistics", "Dashboard"),
        ("Manage Student\nDirectory", "Students"),
        ("Manage Company\nProfiles", "Companies"),
        ("Manage Internship\nPostings", "Internships"),
        ("View Applications\n& Reports", "Applications")
    ]
    render_dfd1("Admin", "Admin Table", admin_items, "dfd_level_1_admin.png")

    admin_clusters = [
        {
            'major': "Manage\nCompanies",
            'subs': [
                ("Register Company", "Table Companies", False),
                ("View Companies", "Table Companies", True),
                ("Edit Company", "Table Companies", False),
                ("Delete Company", "Table Companies", False),
            ]
        },
        {
            'major': "Manage\nStudents",
            'subs': [
                ("View Students", "Table Students", True),
                ("Verify Reg No", "Table Students", False),
                ("Delete Student", "Table Students", False),
            ]
        },
        {
            'major': "Manage\nInternships",
            'subs': [
                ("View Postings", "Table Internships", True),
                ("Delete Posting", "Table Internships", False),
            ]
        }
    ]
    render_clustered_dfd2("Admin", admin_clusters, "dfd_level_2_admin.png")

    company_clusters = [
        {
            'major': "Manage\nInternships",
            'subs': [
                ("Post Internship", "Table Internships", False),
                ("View Postings", "Table Internships", True),
                ("Edit Posting", "Table Internships", False),
                ("Close Posting", "Table Internships", False),
            ]
        },
        {
            'major': "Manage\nApplicants",
            'subs': [
                ("View Applicants", "Table Applications", True),
                ("Shortlist Candidate", "Table Applications", False),
                ("Select / Reject", "Table Applications", False),
            ]
        },
        {
            'major': "Manage\nProfile",
            'subs': [
                ("View Profile", "Table Companies", True),
                ("Update Profile", "Table Companies", False),
            ]
        }
    ]
    render_clustered_dfd2("Company", company_clusters, "dfd_level_2_company.png")

    student_clusters = [
        {
            'major': "Manage\nApplications",
            'subs': [
                ("Apply Internship", "Table Applications", False),
                ("View Applications", "Table Applications", True),
                ("Track Status", "Table Applications", True),
                ("Withdraw Application", "Table Applications", False),
            ]
        },
        {
            'major': "Browse\nInternships",
            'subs': [
                ("Search Internships", "Table Internships", True),
                ("Filter by Branch", "Table Internships", True),
                ("View Details", "Table Internships", True),
            ]
        },
        {
            'major': "Manage\nProfile",
            'subs': [
                ("View Profile", "Table Students", True),
                ("Update Resume / CV", "Table Students", False),
            ]
        }
    ]
    render_clustered_dfd2("Student", student_clusters, "dfd_level_2_student.png")

    print("\nMASTER BUILD COMPLETE!")
