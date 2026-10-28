import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = Presentation()
    # 16:9 Widescreen layout (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6]

    # Simple & Clean Color Palette
    WHITE = RGBColor(255, 255, 255)
    NAVY = RGBColor(15, 23, 42)          # Slate 900 (Main Title & Headers)
    BLUE = RGBColor(37, 99, 235)         # Primary Blue (Accents & Highlights)
    LIGHT_BLUE = RGBColor(239, 246, 255) # Soft Blue Card BG
    CARD_BG = RGBColor(248, 250, 252)    # Slate 50 (Neutral Card BG)
    BORDER = RGBColor(226, 232, 240)     # Slate 200 (Clean divider lines)
    DARK_TEXT = RGBColor(30, 41, 59)     # Slate 800 (Readable Body Text)
    MUTED = RGBColor(100, 116, 139)      # Slate 500 (Captions & Footers)
    GREEN = RGBColor(22, 163, 74)        # Green Accent
    AMBER = RGBColor(217, 119, 6)        # Amber Accent

    def add_header(slide, title_text, category="DEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING (AI & ML)"):
        # Top banner category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.73), Inches(0.35))
        tf_cat = cat_box.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE
        p_cat.font.name = "Calibri"

        # Main slide title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.73), Inches(0.7))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.font.name = "Calibri"

        # Clean Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.73), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE
        line.line.color.rgb = BLUE

        # Subtle Footer
        foot_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.73), Inches(0.015))
        foot_line.fill.solid()
        foot_line.fill.fore_color.rgb = BORDER
        foot_line.line.color.rgb = BORDER

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.02), Inches(11.73), Inches(0.35))
        tf_foot = foot_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Video Activity Recognition with 3D CNN & Grad-CAM  |  Dept of AI & ML"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = MUTED
        p_foot.font.name = "Calibri"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.0)
        return shape

    # =========================================================================
    # SLIDE 1: Simple Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_card(s1, Inches(0.8), Inches(0.8), Inches(11.73), Inches(5.9), bg_color=WHITE, border_color=BLUE)
    
    # Department Tag
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(6.5), Inches(0.42))
    badge.fill.solid()
    badge.fill.fore_color.rgb = LIGHT_BLUE
    badge.line.color.rgb = BLUE
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "DEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = BLUE
    p_b.font.name = "Calibri"
    p_b.alignment = PP_ALIGN.CENTER

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.9), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "Video Activity Recognition"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.font.name = "Calibri"

    p2 = tf1.add_paragraph()
    p2.text = "Using 3D Convolutional Neural Networks (3D-CNN) & Grad-CAM Explainable AI"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = BLUE
    p2.font.name = "Calibri"

    p3 = tf1.add_paragraph()
    p3.text = "Spatiotemporal Action Classification with Real-Time Attention Heatmaps & Live Camera Predictor"
    p3.font.size = Pt(14)
    p3.font.color.rgb = MUTED
    p3.font.name = "Calibri"

    # Quick Highlights Box
    highlights = [
        ("Architecture", "3D-CNN (Conv3D)"),
        ("Explainability", "3D Grad-CAM (XAI)"),
        ("Framework", "PyTorch 2.1 & OpenCV"),
        ("Live Interface", "30 FPS Real-Time Predictor")
    ]
    for i, (head, val) in enumerate(highlights):
        x = Inches(1.2 + i * 2.75)
        add_card(s1, x, Inches(4.35), Inches(2.6), Inches(1.5), bg_color=LIGHT_BLUE, border_color=BLUE)
        tb_m = s1.shapes.add_textbox(x + Inches(0.1), Inches(4.45), Inches(2.4), Inches(1.3))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        pm1 = tf_m.paragraphs[0]
        pm1.text = head.upper()
        pm1.font.size = Pt(10)
        pm1.font.bold = True
        pm1.font.color.rgb = BLUE
        pm1.font.name = "Calibri"
        
        pm2 = tf_m.add_paragraph()
        pm2.text = val
        pm2.font.size = Pt(12)
        pm2.font.bold = True
        pm2.font.color.rgb = DARK_TEXT
        pm2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 2: Introduction & Project Overview
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Introduction & Overview")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.3), bg_color=CARD_BG, border_color=BORDER)
    tb_i1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.2), Inches(3.9))
    tf_i1 = tb_i1.text_frame
    tf_i1.word_wrap = True
    pi1 = tf_i1.paragraphs[0]
    pi1.text = "📌 What is Video Activity Recognition?"
    pi1.font.size = Pt(17)
    pi1.font.bold = True
    pi1.font.color.rgb = NAVY
    pi1.font.name = "Calibri"

    intro_pts = [
        "Automated understanding of human physical actions (e.g. Walking, Running, Jumping, Sitting) from video streams.",
        "Combines spatial understanding (posture, objects, body parts) with temporal progression (motion trajectory over time).",
        "Crucial for real-world applications in smart surveillance, healthcare patient monitoring, sports analytics, and autonomous systems."
    ]
    for pt in intro_pts:
        p = tf_i1.add_paragraph()
        p.text = "•  " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_before = Pt(8)

    add_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(4.3), bg_color=CARD_BG, border_color=BORDER)
    tb_i2 = s2.shapes.add_textbox(Inches(7.1), Inches(1.75), Inches(5.2), Inches(3.9))
    tf_i2 = tb_i2.text_frame
    tf_i2.word_wrap = True
    pi2 = tf_i2.paragraphs[0]
    pi2.text = "🎯 Core Project Goals"
    pi2.font.size = Pt(17)
    pi2.font.bold = True
    pi2.font.color.rgb = BLUE
    pi2.font.name = "Calibri"

    goals = [
        "Spatiotemporal Modeling: Build a native 3D-CNN capable of jointly learning motion and spatial features.",
        "Explainable AI Integration: Implement 3D Grad-CAM to visualize spatiotemporal attention heatmaps.",
        "Motion-Calibrated Real-Time Inference: Build a 30 FPS live webcam engine that distinguishes static postures (Sitting) from dynamic actions.",
        "Localhost Deployment: Provide an intuitive web dashboard and native desktop interface."
    ]
    for g in goals:
        p = tf_i2.add_paragraph()
        p.text = "✔  " + g
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_before = Pt(8)

    add_card(s2, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.75), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_i3 = s2.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_i3 = tb_i3.text_frame
    p_i3 = tf_i3.paragraphs[0]
    p_i3.text = "💡 Value Proposition: Bridging high-accuracy spatiotemporal deep learning with transparent visual explainability for local CPU deployment."
    p_i3.font.size = Pt(12)
    p_i3.font.bold = True
    p_i3.font.color.rgb = BLUE
    p_i3.font.name = "Calibri"

    # =========================================================================
    # SLIDE 3: Problem Statement
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement: 2D CNN vs. 3D CNN")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.3), bg_color=RGBColor(254, 242, 242), border_color=BORDER)
    tb_p1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.2), Inches(3.9))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    pp1 = tf_p1.paragraphs[0]
    pp1.text = "❌ Why Traditional 2D CNNs Fail"
    pp1.font.size = Pt(17)
    pp1.font.bold = True
    pp1.font.color.rgb = RGBColor(220, 38, 38)
    pp1.font.name = "Calibri"

    p2d = [
        "Processes video frames as independent 2D spatial images (Height x Width).",
        "Extracts static appearance ('What is in the frame') but completely misses motion trajectory ('How actions unfold').",
        "Confuses actions with identical static postures (e.g. Standing Still vs. Walking, Opening vs. Closing a door).",
        "Requires heavy, separate optical flow computations that introduce latency."
    ]
    for pt in p2d:
        p = tf_p1.add_paragraph()
        p.text = "•  " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_before = Pt(8)

    add_card(s3, Inches(6.9), Inches(1.6), Inches(5.6), Inches(4.3), bg_color=RGBColor(240, 253, 244), border_color=BORDER)
    tb_p2 = s3.shapes.add_textbox(Inches(7.1), Inches(1.75), Inches(5.2), Inches(3.9))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    pp2 = tf_p2.paragraphs[0]
    pp2.text = "✅ The 3D-CNN Advantage (Our Approach)"
    pp2.font.size = Pt(17)
    pp2.font.bold = True
    pp2.font.color.rgb = GREEN
    pp2.font.name = "Calibri"

    p3d = [
        "Applies 3D convolutional kernels across both space and time (H x W x Time).",
        "Preserves temporal continuity across sequential video frames in a unified model.",
        "Learns combined posture features, limb movements, and directional velocity.",
        "Achieves compact, high-speed inference suitable for local CPU execution."
    ]
    for pt in p3d:
        p = tf_p2.add_paragraph()
        p.text = "•  " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_before = Pt(8)

    add_card(s3, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.75), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_p3 = s3.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_p3 = tb_p3.text_frame
    p_p3 = tf_p3.paragraphs[0]
    p_p3.text = "💡 Core Conclusion: True action semantics reside in temporal transitions across consecutive frames, making 3D convolution essential for video classification."
    p_p3.font.size = Pt(12)
    p_p3.font.bold = True
    p_p3.font.color.rgb = BLUE
    p_p3.font.name = "Calibri"

    # =========================================================================
    # SLIDE 4: Literature Survey (Part 1 - Papers 1 to 5)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Literature Survey: Foundational Action Recognition (Papers 1–5)")

    t_s4 = s4.shapes.add_table(6, 4, Inches(0.8), Inches(1.55), Inches(11.73), Inches(5.2))
    tbl4 = t_s4.table
    tbl4.columns[0].width = Inches(0.8)
    tbl4.columns[1].width = Inches(2.9)
    tbl4.columns[2].width = Inches(4.5)
    tbl4.columns[3].width = Inches(3.53)

    h4 = ["No.", "Author & Year", "Methodology & Architecture", "Key Findings & Limitations"]
    for c_idx, h in enumerate(h4):
        cell = tbl4.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    lit1 = [
        ("1", "Simonyan & Zisserman (2014)", "Two-Stream CNN (Spatial + Optical Flow)", "Proved optical flow benefits; highly compute-heavy with separate flow extraction."),
        ("2", "Ji et al. (2013)", "Early 3D CNN for Human Action Recognition", "First applied 3D convolutions to video; limited depth due to computational constraints."),
        ("3", "Tran et al. (2015)", "C3D: Convolutional 3D Network", "Established 3x3x3 spatiotemporal kernels as standard; heavy parameter footprint (~60M)."),
        ("4", "Carreira & Zisserman (2017)", "I3D (Inflated 3D ConvNet) & Kinetics", "Inflated successful 2D ImageNet architectures into 3D; benchmarked modern video models."),
        ("5", "Tran et al. (2018)", "R(2+1)D Factorized Convolutions", "Split 3D conv into spatial 2D conv + temporal 1D conv; improved optimization stability.")
    ]
    for r_idx, r in enumerate(lit1):
        bg = CARD_BG if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(r):
            cell = tbl4.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if c_idx <= 1:
                p.font.bold = True

    # =========================================================================
    # SLIDE 5: Literature Survey (Part 2 - Papers 6 to 10)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Survey: 3D Advances & Attention (Papers 6–10)")

    t_s5 = s5.shapes.add_table(6, 4, Inches(0.8), Inches(1.55), Inches(11.73), Inches(5.2))
    tbl5 = t_s5.table
    tbl5.columns[0].width = Inches(0.8)
    tbl5.columns[1].width = Inches(2.9)
    tbl5.columns[2].width = Inches(4.5)
    tbl5.columns[3].width = Inches(3.53)

    for c_idx, h in enumerate(h4):
        cell = tbl5.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    lit2 = [
        ("6", "Hara et al. (2018)", "3D ResNet Architectures (ResNet-18/3D)", "Systematically demonstrated 3D residual connections enhance deeper spatiotemporal models."),
        ("7", "Wang et al. (2018)", "Non-local Neural Networks", "Introduced self-attention mechanisms to capture long-range spatiotemporal dependencies."),
        ("8", "Feichtenhofer et al. (2019)", "SlowFast Networks for Video Recognition", "Dual pathways: Slow (spatial detail) and Fast (rapid temporal motion); state-of-the-art accuracy."),
        ("9", "Bertasius et al. (2021)", "TimeSformer (Space-Time Attention)", "First pure video transformer using divided space-time attention; requires substantial training data."),
        ("10", "Arnab et al. (2021)", "ViViT: A Video Vision Transformer", "Spatial and temporal transformer factorizations; computationally demanding for edge deployment.")
    ]
    for r_idx, r in enumerate(lit2):
        bg = CARD_BG if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(r):
            cell = tbl5.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if c_idx <= 1:
                p.font.bold = True

    # =========================================================================
    # SLIDE 6: Literature Survey (Part 3 - Papers 11 to 15)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Literature Survey: Explainable AI & Benchmarks (Papers 11–15)")

    t_s6 = s6.shapes.add_table(6, 4, Inches(0.8), Inches(1.55), Inches(11.73), Inches(5.2))
    tbl6 = t_s6.table
    tbl6.columns[0].width = Inches(0.8)
    tbl6.columns[1].width = Inches(2.9)
    tbl6.columns[2].width = Inches(4.5)
    tbl6.columns[3].width = Inches(3.53)

    for c_idx, h in enumerate(h4):
        cell = tbl6.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    lit3 = [
        ("11", "Zhou et al. (2016)", "Class Activation Mapping (CAM)", "Pioneered visual localization using global average pooling; requires specific network architecture."),
        ("12", "Selvaraju et al. (2017)", "Grad-CAM (Gradient-Weighted CAM)", "Universal visual explanation framework applicable to any CNN without architectural retraining."),
        ("13", "Chattopadhay et al. (2018)", "Grad-CAM++ (Generalized CAM)", "Improved multiple-instance localization; mathematically generalized gradient weights."),
        ("14", "Soomro et al. (2012)", "UCF101 Benchmark Dataset", "Standardized 101 action classes in the wild; gold-standard benchmark for action recognition."),
        ("15", "Stergiou & Poppe (2019)", "Survey on Spatiotemporal Deep Learning", "Comprehensive analysis highlighting the necessity of combining explainability with 3D CNNs.")
    ]
    for r_idx, r in enumerate(lit3):
        bg = CARD_BG if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(r):
            cell = tbl6.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if c_idx <= 1:
                p.font.bold = True

    # =========================================================================
    # SLIDE 7: Synthesis of Literature Survey & Research Gaps
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Synthesis of Literature Survey & Research Gaps")

    gaps = [
        ("1. Computational Heaviness", 
         "Existing models (C3D, I3D, ViViT) require multi-GPU clusters and cannot achieve real-time 30 FPS inference on standard laptops/CPUs.",
         AMBER),
        ("2. Black-Box Opacity", 
         "Most literature focuses strictly on Top-1 classification accuracy while ignoring explainability; predictions lack visual justification.",
         RGBColor(220, 38, 38)),
        ("3. Static Posture Misclassification", 
         "Standard models often falsely classify sitting still as running or walking due to camera sensor jitter and lack of idle calibration.",
         BLUE),
        ("4. Deployment Complexity", 
         "Two-stream optical flow architectures require pre-processing pipelines that prevent seamless standalone desktop/web deployment.",
         GREEN)
    ]
    for i, (title, desc, clr) in enumerate(gaps):
        x = Inches(0.8 + i * 3.0)
        add_card(s7, x, Inches(1.7), Inches(2.75), Inches(4.0), bg_color=CARD_BG, border_color=clr)
        
        tb_g = s7.shapes.add_textbox(x + Inches(0.15), Inches(1.85), Inches(2.45), Inches(3.7))
        tf_g = tb_g.text_frame
        tf_g.word_wrap = True
        
        pg1 = tf_g.paragraphs[0]
        pg1.text = title
        pg1.font.size = Pt(14)
        pg1.font.bold = True
        pg1.font.color.rgb = clr
        pg1.font.name = "Calibri"

        pg2 = tf_g.add_paragraph()
        pg2.text = desc
        pg2.font.size = Pt(12)
        pg2.font.color.rgb = DARK_TEXT
        pg2.font.name = "Calibri"
        pg2.space_before = Pt(10)

    # Solution Banner
    add_card(s7, Inches(0.8), Inches(5.95), Inches(11.73), Inches(0.85), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_sol = s7.shapes.add_textbox(Inches(1.0), Inches(6.02), Inches(11.3), Inches(0.7))
    tf_sol = tb_sol.text_frame
    p_sol = tf_sol.paragraphs[0]
    p_sol.text = "🎯 Our Contribution: A streamlined 3D-CNN architecture integrated with 3D Grad-CAM, motion energy idle calibration, and an asynchronous 30 FPS live webcam engine running locally."
    p_sol.font.size = Pt(12)
    p_sol.font.bold = True
    p_sol.font.color.rgb = BLUE
    p_sol.font.name = "Calibri"

    # =========================================================================
    # SLIDE 8: Proposed System Architecture & Pipeline
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Proposed System Architecture & End-to-End Pipeline")

    steps = [
        ("1. Ingestion", "Webcam / MP4 Video (30 FPS)", BLUE),
        ("2. Buffer", "16 Frames @ 112x112 RGB", BLUE),
        ("3. 3D-CNN", "Spatiotemporal Convolutions", GREEN),
        ("4. Softmax", "Action Classification", AMBER),
        ("5. Grad-CAM", "Attention Heatmap Overlay", RGBColor(220, 38, 38))
    ]
    for i, (head, sub, clr) in enumerate(steps):
        x = Inches(0.8 + i * 2.4)
        add_card(s8, x, Inches(1.8), Inches(2.2), Inches(3.8), bg_color=CARD_BG, border_color=clr)
        
        # Step Circle
        badge = s8.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.8), Inches(2.1), Inches(0.6), Inches(0.6))
        badge.fill.solid()
        badge.fill.fore_color.rgb = clr
        badge.line.color.rgb = clr
        tf_c = badge.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = str(i+1)
        p_c.font.size = Pt(14)
        p_c.font.bold = True
        p_c.font.color.rgb = WHITE
        p_c.alignment = PP_ALIGN.CENTER

        tb_s = s8.shapes.add_textbox(x + Inches(0.15), Inches(2.9), Inches(1.9), Inches(2.5))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        ps1 = tf_s.paragraphs[0]
        ps1.text = head
        ps1.font.size = Pt(15)
        ps1.font.bold = True
        ps1.font.color.rgb = NAVY
        ps1.font.name = "Calibri"
        ps1.alignment = PP_ALIGN.CENTER

        ps2 = tf_s.add_paragraph()
        ps2.text = sub
        ps2.font.size = Pt(11.5)
        ps2.font.color.rgb = DARK_TEXT
        ps2.font.name = "Calibri"
        ps2.space_before = Pt(8)
        ps2.alignment = PP_ALIGN.CENTER

    add_card(s8, Inches(0.8), Inches(5.8), Inches(11.73), Inches(0.95), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_tpipe = s8.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.8))
    tf_tpipe = tb_tpipe.text_frame
    pt1 = tf_tpipe.paragraphs[0]
    pt1.text = "Spatiotemporal Tensor Flow:"
    pt1.font.bold = True
    pt1.font.size = Pt(12)
    pt1.font.color.rgb = BLUE
    pt1.font.name = "Calibri"

    pt2 = tf_tpipe.add_paragraph()
    pt2.text = "Raw Video Stream ➔ Frame Buffer [1, 3, 16, 112, 112] ➔ Conv3D Layers [1, 128, 8, 28, 28] ➔ Flatten [1, 802816] ➔ Linear [1, num_classes] ➔ Heatmap"
    pt2.font.size = Pt(11.5)
    pt2.font.color.rgb = DARK_TEXT
    pt2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 9: 3D CNN Model Design & Mathematical Formulation
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "3D CNN Architecture & Layer Specifications")

    t_s9 = s9.shapes.add_table(8, 4, Inches(0.8), Inches(1.6), Inches(11.73), Inches(4.3))
    tbl9 = t_s9.table
    tbl9.columns[0].width = Inches(2.2)
    tbl9.columns[1].width = Inches(3.6)
    tbl9.columns[2].width = Inches(3.2)
    tbl9.columns[3].width = Inches(2.73)

    h9 = ["Layer Name", "Kernel & Parameters", "Output Tensor Shape", "Role & Function"]
    for c_idx, h in enumerate(h9):
        cell = tbl9.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    rows9 = [
        ("Input Tensor", "16 RGB Frames @ 112x112", "(Batch, 3, 16, 112, 112)", "Standardized spatiotemporal video clip"),
        ("Conv3D Layer 1", "64 filters, kernel (3,3,3), pad=1", "(Batch, 64, 16, 112, 112)", "Extracts initial spatial edges & local motion"),
        ("MaxPool3D 1", "kernel=(1,2,2), stride=(1,2,2)", "(Batch, 64, 16, 56, 56)", "Spatial downsampling; preserves 16 frame temporal depth"),
        ("Conv3D Layer 2", "128 filters, kernel (3,3,3), pad=1", "(Batch, 128, 16, 56, 56)", "Target Layer for Grad-CAM (high-level feature maps)"),
        ("MaxPool3D 2", "kernel=(2,2,2), stride=(2,2,2)", "(Batch, 128, 8, 28, 28)", "Spatiotemporal pooling; pools time down to 8 frames"),
        ("Linear FC1", "Flatten(128x8x28x28) ➔ 256", "(Batch, 256)", "Dense representation with ReLU activation"),
        ("Linear FC2", "Linear(256, num_classes)", "(Batch, num_classes)", "Class logit output for Softmax categorization")
    ]
    for r_idx, r in enumerate(rows9):
        bg = CARD_BG if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(r):
            cell = tbl9.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if c_idx == 0:
                p.font.bold = True

    add_card(s9, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.75), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_n9 = s9.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_n9 = tb_n9.text_frame
    p_n9 = tf_n9.paragraphs[0]
    p_n9.text = "Mathematical Operation: v_ij^xyz = ReLU( b_ij + Σ_m Σ_p Σ_q Σ_r w_ijm^pqr * v_(i-1)m^(x+p)(y+q)(z+r) ) where kernel weights connect across both 2D space (x,y) and temporal time (z)."
    p_n9.font.size = Pt(11)
    p_n9.font.color.rgb = BLUE
    p_n9.font.name = "Calibri"

    # =========================================================================
    # SLIDE 10: Video Preprocessing & Data Engineering
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Video Preprocessing & Data Engineering")

    p_cards = [
        ("1. Temporal Sampling", "Uses OpenCV VideoCapture to read frames.\nUniform sampling using np.linspace(0, total_frames-1, 16) extracts exactly 16 evenly spaced frames regardless of original video length or FPS.", BLUE),
        ("2. Geometric Standardization", "Resizes every frame to standard 112x112 resolution.\nConverts default OpenCV BGR color channels to RGB for PyTorch tensor compatibility.", GREEN),
        ("3. Normalization", "Scales uint8 pixel values [0, 255] to float32 [0.0, 1.0].\nTensors reshaped to (Channels, Time, Height, Width) for batch feeding into Conv3D layers.", AMBER)
    ]
    for i, (title, content, clr) in enumerate(p_cards):
        x = Inches(0.8 + i * 4.0)
        add_card(s10, x, Inches(1.8), Inches(3.73), Inches(3.8), bg_color=CARD_BG, border_color=clr)
        
        tb_pc = s10.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.33), Inches(3.4))
        tf_pc = tb_pc.text_frame
        tf_pc.word_wrap = True
        
        p1 = tf_pc.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = clr
        p1.font.name = "Calibri"

        p2 = tf_pc.add_paragraph()
        p2.text = content
        p2.font.size = Pt(12)
        p2.font.color.rgb = DARK_TEXT
        p2.font.name = "Calibri"
        p2.space_before = Pt(12)

    add_card(s10, Inches(0.8), Inches(5.8), Inches(11.73), Inches(0.95), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_ds10 = s10.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.8))
    tf_ds10 = tb_ds10.text_frame
    pds1 = tf_ds10.paragraphs[0]
    pds1.text = "Dataset Organization Standard: dataset/<activity_class>/<video_sample>.mp4"
    pds1.font.bold = True
    pds1.font.size = Pt(12)
    pds1.font.color.rgb = BLUE
    pds1.font.name = "Calibri"

    pds2 = tf_ds10.add_paragraph()
    pds2.text = "Modular folder structure compatible with UCF101 benchmark actions and custom webcam clips across Sitting/Idle, Walking, Running, and Jumping."
    pds2.font.size = Pt(11.5)
    pds2.font.color.rgb = DARK_TEXT
    pds2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 11: Explainable AI with 3D Grad-CAM
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Explainable AI (XAI) using 3D Grad-CAM")

    add_card(s11, Inches(0.8), Inches(1.7), Inches(7.2), Inches(4.9), bg_color=CARD_BG, border_color=BLUE)
    tb_gc11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(6.8), Inches(4.5))
    tf_gc11 = tb_gc11.text_frame
    tf_gc11.word_wrap = True
    
    pg11 = tf_gc11.paragraphs[0]
    pg11.text = "Step-by-Step 3D Grad-CAM Workflow:"
    pg11.font.size = Pt(17)
    pg11.font.bold = True
    pg11.font.color.rgb = BLUE
    pg11.font.name = "Calibri"

    gc_pts = [
        ("1. Target Layer Selection:", "Hooks into conv2, the final 3D convolutional layer preserving high-level spatiotemporal semantic representations."),
        ("2. Gradient Computation:", "Calculates gradient of predicted class logit score (y^c) with respect to 3D feature activation maps (A^k)."),
        ("3. Global Average Pooling:", "Pools gradients across time and space to obtain channel importance weights alpha_k^c."),
        ("4. Weighted Linear Combination & ReLU:", "Computes L_Grad-CAM = ReLU( Σ_k alpha_k^c * A^k ), isolating only features positively supporting the predicted action."),
        ("5. Heatmap Superimposition:", "Normalizes activation map to [0, 1] and superimposes onto RGB video frames using OpenCV COLORMAP_JET.")
    ]
    for h, desc in gc_pts:
        p = tf_gc11.add_paragraph()
        p.text = f"•  {h} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(6)

    add_card(s11, Inches(8.3), Inches(1.7), Inches(4.23), Inches(4.9), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_gcr11 = s11.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.83), Inches(4.5))
    tf_gcr11 = tb_gcr11.text_frame
    tf_gcr11.word_wrap = True
    
    pgr11 = tf_gcr11.paragraphs[0]
    pgr11.text = "🎯 Visual Attention Verification"
    pgr11.font.size = Pt(16)
    pgr11.font.bold = True
    pgr11.font.color.rgb = NAVY
    pgr11.font.name = "Calibri"

    why_xai11 = [
        "Eliminates the 'Black Box' problem in neural network classification.",
        "Confirms the network focuses on moving body limbs (legs during walking, arms during jumping) rather than background noise.",
        "Guarantees model accountability for surveillance, safety, and healthcare deployments.",
        "Provides visual proof for project viva evaluation."
    ]
    for pt in why_xai11:
        p = tf_gcr11.add_paragraph()
        p.text = "✔  " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: Experimental Setup & Hyperparameter Optimization
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Experimental Setup & Training Configuration")

    hparams12 = [
        ("Loss Function", "CrossEntropyLoss", "Standard multi-class categorical cross-entropy loss function."),
        ("Optimizer", "Adam (lr = 0.001)", "Adaptive gradient estimation for fast and stable loss convergence."),
        ("Batch Size", "4 to 8 clips", "Optimized to prevent RAM exhaustion during local CPU execution."),
        ("Temporal Window", "16 Frames", "Optimal trade-off between motion context and frame processing latency.")
    ]
    for i, (hp_title, hp_val, hp_desc) in enumerate(hparams12):
        x = Inches(0.8 + i * 3.0)
        add_card(s12, x, Inches(1.8), Inches(2.75), Inches(2.5), bg_color=CARD_BG, border_color=BLUE)
        
        tb_hp = s12.shapes.add_textbox(x + Inches(0.15), Inches(1.95), Inches(2.45), Inches(2.2))
        tf_hp = tb_hp.text_frame
        tf_hp.word_wrap = True
        
        ph1 = tf_hp.paragraphs[0]
        ph1.text = hp_title.upper()
        ph1.font.size = Pt(11)
        ph1.font.bold = True
        ph1.font.color.rgb = BLUE
        ph1.font.name = "Calibri"
        
        ph2 = tf_hp.add_paragraph()
        ph2.text = hp_val
        ph2.font.size = Pt(15)
        ph2.font.bold = True
        ph2.font.color.rgb = NAVY
        ph2.font.name = "Calibri"
        ph2.space_before = Pt(4)

        ph3 = tf_hp.add_paragraph()
        ph3.text = hp_desc
        ph3.font.size = Pt(11)
        ph3.font.color.rgb = DARK_TEXT
        ph3.font.name = "Calibri"
        ph3.space_before = Pt(6)

    add_card(s12, Inches(0.8), Inches(4.6), Inches(11.73), Inches(2.1), bg_color=WHITE, border_color=BORDER)
    tb_opt12 = s12.shapes.add_textbox(Inches(1.0), Inches(4.75), Inches(11.3), Inches(1.8))
    tf_opt12 = tb_opt12.text_frame
    tf_opt12.word_wrap = True
    
    po1 = tf_opt12.paragraphs[0]
    po1.text = "CPU Optimization Strategies for ThinkPad i7 / Local Execution:"
    po1.font.size = Pt(15)
    po1.font.bold = True
    po1.font.color.rgb = NAVY
    po1.font.name = "Calibri"

    opts12 = [
        "Modular Category Subsetting: Core distinct action classes trained to ensure fast iterative development on CPU.",
        "Model Weight Checkpointing: Saves optimal model weights based on minimum validation loss (outputs/model_final.pth).",
        "DirectShow Video Driver: OpenCV CAP_DSHOW enabled on Windows for zero-latency camera capture.",
        "Asynchronous Decoupled Threading: Display runs at 30 FPS while 3D CNN computes in a background worker thread."
    ]
    for opt in opts12:
        p = tf_opt12.add_paragraph()
        p.text = "•  " + opt
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 13: Results & Evaluation Metrics
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Performance Evaluation Framework")

    t_s13 = s13.shapes.add_table(5, 4, Inches(0.8), Inches(1.7), Inches(11.73), Inches(3.6))
    tbl13 = t_s13.table
    tbl13.columns[0].width = Inches(2.2)
    tbl13.columns[1].width = Inches(2.5)
    tbl13.columns[2].width = Inches(4.5)
    tbl13.columns[3].width = Inches(2.53)

    eval_heads = ["Evaluation Metric", "Mathematical Formula", "Significance in Action Recognition", "Target Threshold"]
    for c_idx, h_text in enumerate(eval_heads):
        c = tbl13.cell(0, c_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = BLUE
        p = c.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    eval_rows = [
        ("Accuracy", "(TP + TN) / Total", "Overall proportion of correctly classified video clips.", "> 90%"),
        ("Precision", "TP / (TP + FP)", "Quantifies exactness; minimizes false action alarms (e.g. false running).", "> 88%"),
        ("Recall (Sensitivity)", "TP / (TP + FN)", "Measures ability to detect all actual action occurrences.", "> 89%"),
        ("F1-Score", "2 * (P * R) / (P + R)", "Harmonic balance between Precision and Recall under imbalanced clip counts.", "> 88%")
    ]
    for r_idx, r_data in enumerate(eval_rows):
        bg_row = CARD_BG if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(r_data):
            cell = tbl13.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_row
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if c_idx == 0:
                p.font.bold = True

    add_card(s13, Inches(0.8), Inches(5.6), Inches(11.73), Inches(1.1), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_ev13 = s13.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.9))
    tf_ev13 = tb_ev13.text_frame
    tf_ev13.word_wrap = True
    pe1 = tf_ev13.paragraphs[0]
    pe1.text = "Validation & Reporting Methodology:"
    pe1.font.size = Pt(12)
    pe1.font.bold = True
    pe1.font.color.rgb = BLUE
    pe1.font.name = "Calibri"

    pe2 = tf_ev13.add_paragraph()
    pe2.text = "Evaluated via scikit-learn classification_report alongside multi-class confusion matrix heatmaps to inspect action boundaries (e.g. Walking vs. Running classification thresholds)."
    pe2.font.size = Pt(11.5)
    pe2.font.color.rgb = DARK_TEXT
    pe2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 14: Real-Time Live Camera Predictor & Idle Posture Calibration
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Real-Time Live Camera Predictor & Motion Calibration")

    live_cards = [
        ("1. 30 FPS Multithreading", "Native camera acquisition decoupled from neural forward pass.\nZero video stutter or camera delay during inference.\nReal-time mirrored selfie preview with on-screen Heads-Up Display (HUD).", BLUE),
        ("2. Motion Energy Analyzer", "Solves idle sitting posture calibration.\nEvaluates frame-difference pixel velocity.\nPrevents subtle camera sensor noise from triggering false 'running' states when user is sitting.", GREEN),
        ("3. Real-Time 3D Grad-CAM", "Superimposes jet colormap heatmaps live.\nConfirms attention on moving limbs.\nSide-by-side or single overlay display modes toggleable with keyboard shortcuts.", RGBColor(220, 38, 38))
    ]
    for i, (title, text, clr) in enumerate(live_cards):
        x = Inches(0.8 + i * 4.0)
        add_card(s14, x, Inches(1.8), Inches(3.73), Inches(3.8), bg_color=CARD_BG, border_color=clr)
        
        tb_o = s14.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.33), Inches(3.4))
        tf_o = tb_o.text_frame
        tf_o.word_wrap = True
        
        po1 = tf_o.paragraphs[0]
        po1.text = title
        po1.font.size = Pt(16)
        po1.font.bold = True
        po1.font.color.rgb = clr
        po1.font.name = "Calibri"
        
        po2 = tf_o.add_paragraph()
        po2.text = text
        po2.font.size = Pt(12)
        po2.font.color.rgb = DARK_TEXT
        po2.font.name = "Calibri"
        po2.space_before = Pt(12)

    add_card(s14, Inches(0.8), Inches(5.8), Inches(11.73), Inches(0.95), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_del14 = s14.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.8))
    tf_del14 = tb_del14.text_frame
    p_dl1 = tf_del14.paragraphs[0]
    p_dl1.text = "Two Live Deployment Interfaces Ready:"
    p_dl1.font.bold = True
    p_dl1.font.size = Pt(12)
    p_dl1.font.color.rgb = BLUE
    p_dl1.font.name = "Calibri"

    p_dl2 = tf_del14.add_paragraph()
    p_dl2.text = "1. Streamlit Web Dashboard at http://localhost:8501  |  2. High-Speed Native Desktop Window (python live_predictor.py)"
    p_dl2.font.size = Pt(11.5)
    p_dl2.font.color.rgb = DARK_TEXT
    p_dl2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 15: Conclusion & Future Scope
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Conclusion & Future Research Scope")

    add_card(s15, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.2), bg_color=RGBColor(240, 253, 244), border_color=GREEN)
    tb_cl15 = s15.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_cl15 = tb_cl15.text_frame
    tf_cl15.word_wrap = True
    
    pcl1 = tf_cl15.paragraphs[0]
    pcl1.text = "🏆 Key Project Accomplishments"
    pcl1.font.size = Pt(18)
    pcl1.font.bold = True
    pcl1.font.color.rgb = GREEN
    pcl1.font.name = "Calibri"

    acc_list = [
        "End-to-End 3D-CNN Pipeline: Designed and validated a Conv3D architecture capturing spatiotemporal features without external optical flow.",
        "Transparent Explainability: Successfully integrated 3D Grad-CAM for frame-by-frame visual heatmaps.",
        "Zero-Latency Live Predictor: Built an asynchronous multithreaded engine delivering 30 FPS webcam predictions.",
        "Accurate Sitting/Idle Calibration: Eliminated sensor-jitter false positives during desk use.",
        "Fully Reproducible Open-Source Code: Pushed to GitHub with complete documentation and presentation assets."
    ]
    for acc in acc_list:
        p = tf_cl15.add_paragraph()
        p.text = "✔  " + acc
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(6)

    add_card(s15, Inches(6.9), Inches(1.7), Inches(5.6), Inches(4.2), bg_color=RGBColor(239, 246, 255), border_color=BLUE)
    tb_cr15 = s15.shapes.add_textbox(Inches(7.1), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_cr15 = tb_cr15.text_frame
    tf_cr15.word_wrap = True
    
    pcr1 = tf_cr15.paragraphs[0]
    pcr1.text = "🚀 Future Research Scope"
    pcr1.font.size = Pt(18)
    pcr1.font.bold = True
    pcr1.font.color.rgb = BLUE
    pcr1.font.name = "Calibri"

    scope_list = [
        "Video Transformers: Incorporate Video Swin Transformers / TimeSformer for long-range global spatiotemporal attention.",
        "SlowFast Networks: Integrate dual-rate frame sampling (Slow spatial detail + Fast temporal motion).",
        "Edge Hardware Deployment: Quantize model via TensorRT / ONNX for deployment on NVIDIA Jetson and Raspberry Pi devices.",
        "Multi-Modal Sensor Fusion: Combine video feeds with environmental audio for robust multi-sensory activity classification."
    ]
    for sc in scope_list:
        p = tf_cr15.add_paragraph()
        p.text = "➔  " + sc
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(8)

    add_card(s15, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.75), bg_color=NAVY, border_color=NAVY)
    tb_ty = s15.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_ty = tb_ty.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "Thank You!  |  Questions & Discussion  |  Department of AI & ML"
    p_ty.font.size = Pt(16)
    p_ty.font.bold = True
    p_ty.font.color.rgb = WHITE
    p_ty.font.name = "Calibri"
    p_ty.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 16: References (Part 1 - Papers 1 to 8)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "References & Bibliography (Part 1)")

    add_card(s16, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.1), bg_color=CARD_BG, border_color=BORDER)
    tb_ref1 = s16.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(4.7))
    tf_ref1 = tb_ref1.text_frame
    tf_ref1.word_wrap = True

    p_rf1 = tf_ref1.paragraphs[0]
    p_rf1.text = "Key Academic References (1–8):"
    p_rf1.font.size = Pt(14)
    p_rf1.font.bold = True
    p_rf1.font.color.rgb = BLUE
    p_rf1.font.name = "Calibri"

    refs1 = [
        "[1] K. Simonyan and A. Zisserman, 'Two-Stream Convolutional Networks for Action Recognition in Videos,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 27, 2014, pp. 568-576.",
        "[2] S. Ji, W. Xu, M. Yang, and K. Yu, '3D Convolutional Neural Networks for Human Action Recognition,' IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), vol. 35, no. 1, pp. 221-231, 2013.",
        "[3] D. Tran, L. Bourdev, R. Fergus, L. Torresani, and M. Paluri, 'Learning Spatiotemporal Features with 3D Convolutional Networks,' in IEEE International Conference on Computer Vision (ICCV), 2015, pp. 4489-4497.",
        "[4] J. Carreira and A. Zisserman, 'Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset,' in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 6299-6308.",
        "[5] D. Tran, H. Wang, L. Torresani, J. Ray, Y. LeCun, and M. Paluri, 'A Closer Look at Spatiotemporal Convolutions for Action Recognition,' in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 6450-6459.",
        "[6] K. Hara, H. Kataoka, and Y. Satoh, 'Can Spatiotemporal 3D CNNs Retrace the History of 2D CNNs and ImageNet?,' in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 6546-6555.",
        "[7] X. Wang, R. Girshick, A. Gupta, and K. He, 'Non-local Neural Networks,' in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 7794-7803.",
        "[8] C. Feichtenhofer, H. Fan, J. Malik, and K. He, 'SlowFast Networks for Video Recognition,' in IEEE International Conference on Computer Vision (ICCV), 2019, pp. 6202-6211."
    ]
    for r in refs1:
        p = tf_ref1.add_paragraph()
        p.text = r
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 17: References (Part 2 - Papers 9 to 15)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "References & Bibliography (Part 2)")

    add_card(s17, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.1), bg_color=CARD_BG, border_color=BORDER)
    tb_ref2 = s17.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(4.7))
    tf_ref2 = tb_ref2.text_frame
    tf_ref2.word_wrap = True

    p_rf2 = tf_ref2.paragraphs[0]
    p_rf2.text = "Key Academic References (9–15):"
    p_rf2.font.size = Pt(14)
    p_rf2.font.bold = True
    p_rf2.font.color.rgb = BLUE
    p_rf2.font.name = "Calibri"

    refs2 = [
        "[9] G. Bertasius, H. Wang, and L. Torresani, 'Is Space-Time Attention All You Need for Video Understanding?,' in International Conference on Machine Learning (ICML), 2021, pp. 813-824.",
        "[10] A. Arnab, M. Dehghani, G. Heigold, C. Sun, M. Lučić, and C. Schmid, 'ViViT: A Video Vision Transformer,' in IEEE International Conference on Computer Vision (ICCV), 2021, pp. 6836-6846.",
        "[11] B. Zhou, A. Khosla, A. Lapedriza, A. Oliva, and A. Torralba, 'Learning Deep Features for Discriminative Localization,' in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 2921-2929.",
        "[12] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, 'Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization,' in IEEE International Conference on Computer Vision (ICCV), 2017, pp. 618-626.",
        "[13] A. Chattopadhay, A. Sarkar, P. Howlader, and V. N. Balasubramanian, 'Grad-CAM++: Generalized Gradient-Based Visual Explanations for Deep Convolutional Networks,' in IEEE Winter Conference on Applications of Computer Vision (WACV), 2018, pp. 839-847.",
        "[14] K. Soomro, A. R. Zamir, and M. Shah, 'UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild,' Center for Research in Computer Vision (CRCV), Tech. Rep. CRCV-TR-12-01, 2012.",
        "[15] A. Stergiou and R. Poppe, 'Analyzing Human-Human Interactions: A Survey on Spatiotemporal Deep Learning Methods,' Computer Vision and Image Understanding (CVIU), vol. 188, p. 102799, 2019."
    ]
    for r in refs2:
        p = tf_ref2.add_paragraph()
        p.text = r
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_before = Pt(6)

    prs.save(output_path)
    print(f"Enhanced 17-slide Presentation PPTX saved successfully at: {output_path}")

if __name__ == "__main__":
    out = "C:\\Users\\T14\\.gemini\\antigravity\\scratch\\activity-recognition\\presentation_final.pptx"
    build_presentation(out)
