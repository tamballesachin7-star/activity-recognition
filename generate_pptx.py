import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = Presentation()
    # 16:9 Widescreen layout (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Color Palette (Clean Modern Tech)
    NAVY = RGBColor(15, 23, 42)       # Slate 900
    BLUE = RGBColor(37, 99, 235)      # Royal Blue
    LIGHT_BLUE = RGBColor(239, 246, 255) # Light Blue BG
    DARK_TEXT = RGBColor(30, 41, 59)   # Slate 800
    MUTED_TEXT = RGBColor(100, 116, 139) # Slate 500
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(248, 250, 252) # Slate 50
    BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200
    GREEN = RGBColor(22, 163, 74)     # Success Green
    RED = RGBColor(220, 38, 38)       # Alert Red
    PURPLE = RGBColor(147, 51, 234)

    def add_header(slide, title_text, category_text="DEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING (AI & ML)"):
        # Top banner category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE
        p_cat.font.name = "Calibri"

        # Main slide title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.font.name = "Calibri"

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.73), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE
        line.line.color.rgb = BLUE

        # Footer
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.73), Inches(0.015))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = BORDER_COLOR
        footer_line.line.color.rgb = BORDER_COLOR

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.02), Inches(11.7), Inches(0.35))
        tf_foot = foot_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Video Activity Recognition with 3D CNN & Grad-CAM  |  AIML Project Presentation"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = MUTED_TEXT
        p_foot.font.name = "Calibri"

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Background accent card
    add_card(s1, Inches(0.8), Inches(0.8), Inches(11.73), Inches(5.9), bg_color=WHITE, border_color=BLUE)
    
    # Department badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(6.5), Inches(0.45))
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

    # Title & Subtitle
    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.9), Inches(1.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Video Activity Recognition"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.font.name = "Calibri"

    p2 = tf1.add_paragraph()
    p2.text = "Using 3D Convolutional Neural Networks (3D-CNN) & Explainable AI (Grad-CAM)"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = BLUE
    p2.font.name = "Calibri"

    p3 = tf1.add_paragraph()
    p3.text = "Real-time spatiotemporal human action classification with visual attention heatmaps."
    p3.font.size = Pt(14)
    p3.font.color.rgb = MUTED_TEXT
    p3.font.name = "Calibri"

    # Meta cards
    labels = [
        ("Core Architecture", "3D-CNN (Conv3D + MaxPool3D)"),
        ("Explainability (XAI)", "3D Grad-CAM Attention Heatmaps"),
        ("Computer Vision", "PyTorch 2.1 & OpenCV"),
        ("Live Execution", "Real-Time 30 FPS Camera Stream")
    ]
    for i, (head, val) in enumerate(labels):
        x = Inches(1.2 + i * 2.75)
        card = add_card(s1, x, Inches(4.3), Inches(2.6), Inches(1.6), bg_color=LIGHT_BLUE, border_color=BLUE)
        tb_m = s1.shapes.add_textbox(x + Inches(0.1), Inches(4.4), Inches(2.4), Inches(1.4))
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
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Motivation: Why 3D CNN?")

    # Left Column: 2D CNN Limitation
    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.2), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(248, 113, 113))
    tb_l = s2.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    pl1 = tf_l.paragraphs[0]
    pl1.text = "❌ Limitations of Traditional 2D CNNs"
    pl1.font.size = Pt(18)
    pl1.font.bold = True
    pl1.font.color.rgb = RED
    pl1.font.name = "Calibri"

    points_l = [
        "Processes isolated spatial images (Height x Width) frame-by-frame.",
        "Captures posture / visual appearance ('What is in the frame') but misses motion trajectories ('How actions unfold').",
        "Fails on sequential actions with identical static body poses (e.g., Sitting Down vs. Standing Up, Opening vs. Closing a door).",
        "Requires complex two-stream optical flow architectures that are slow and computationally expensive."
    ]
    for pt in points_l:
        p = tf_l.add_paragraph()
        p.text = "•  " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(8)

    # Right Column: 3D CNN Solution
    add_card(s2, Inches(6.9), Inches(1.7), Inches(5.6), Inches(4.2), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(134, 239, 172))
    tb_r = s2.shapes.add_textbox(Inches(7.1), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    pr1 = tf_r.paragraphs[0]
    pr1.text = "✅ The 3D-CNN Advantage (AIML Solution)"
    pr1.font.size = Pt(18)
    pr1.font.bold = True
    pr1.font.color.rgb = GREEN
    pr1.font.name = "Calibri"

    points_r = [
        "Applies 3D convolutional kernels across both space and time (Height x Width x Time).",
        "Preserves temporal continuity across sequential video frames in a single unified model.",
        "Simultaneously captures body posture, limb movements, and directional velocity.",
        "Lightweight & deployable on edge devices without requiring pre-computed optical flow."
    ]
    for pt in points_r:
        p = tf_r.add_paragraph()
        p.text = "•  " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(8)

    # Key takeaway bottom card
    add_card(s2, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.75), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_tk = s2.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_tk = tb_tk.text_frame
    p_tk = tf_tk.paragraphs[0]
    p_tk.text = "💡 Key Principle: Video actions cannot be understood by single frames alone. Motion dynamics across adjacent frames constitute the semantic identity of human behavior."
    p_tk.font.size = Pt(12)
    p_tk.font.bold = True
    p_tk.font.color.rgb = BLUE
    p_tk.font.name = "Calibri"

    # =========================================================================
    # SLIDE 3: System Pipeline Architecture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "End-to-End System Pipeline Architecture")

    steps = [
        ("1. Video Capture", "Raw Video Stream (MP4/AVI) or Live Webcam Feed (30 FPS).", BLUE),
        ("2. Preprocessing", "16-frame temporal buffer sampled uniformly, resized to 112x112 RGB.", BLUE),
        ("3. 3D-CNN Core", "Spatiotemporal convolutions extract movement & posture features.", PURPLE),
        ("4. Classifier", "Softmax probability distribution across human activity categories.", GREEN),
        ("5. 3D Grad-CAM", "Gradient-weighted class activation map overlaid as visual heatmap.", RED)
    ]

    for i, (title, desc, clr) in enumerate(steps):
        x = Inches(0.8 + i * 2.4)
        add_card(s3, x, Inches(1.8), Inches(2.2), Inches(3.8), bg_color=CARD_BG, border_color=clr)
        
        # Step number badge
        badge_step = s3.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.8), Inches(2.1), Inches(0.6), Inches(0.6))
        badge_step.fill.solid()
        badge_step.fill.fore_color.rgb = clr
        badge_step.line.color.rgb = clr
        tf_s = badge_step.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.text = str(i+1)
        p_s.font.size = Pt(14)
        p_s.font.bold = True
        p_s.font.color.rgb = WHITE
        p_s.alignment = PP_ALIGN.CENTER

        tb_step = s3.shapes.add_textbox(x + Inches(0.15), Inches(2.9), Inches(1.9), Inches(2.5))
        tf_step = tb_step.text_frame
        tf_step.word_wrap = True
        p_st = tf_step.paragraphs[0]
        p_st.text = title
        p_st.font.size = Pt(14)
        p_st.font.bold = True
        p_st.font.color.rgb = NAVY
        p_st.font.name = "Calibri"
        p_st.alignment = PP_ALIGN.CENTER
        
        p_sd = tf_step.add_paragraph()
        p_sd.text = desc
        p_sd.font.size = Pt(11)
        p_sd.font.color.rgb = DARK_TEXT
        p_sd.font.name = "Calibri"
        p_sd.space_before = Pt(8)
        p_sd.alignment = PP_ALIGN.CENTER

    # Pipeline summary box
    add_card(s3, Inches(0.8), Inches(5.8), Inches(11.73), Inches(0.95), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_pipe = s3.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.8))
    tf_pipe = tb_pipe.text_frame
    p_pf = tf_pipe.paragraphs[0]
    p_pf.text = "Tensor Transformation Pipeline:"
    p_pf.font.bold = True
    p_pf.font.size = Pt(12)
    p_pf.font.color.rgb = BLUE
    p_pf.font.name = "Calibri"
    
    p_pf2 = tf_pipe.add_paragraph()
    p_pf2.text = "Video Input (T x H x W x C)  ➔  Tensor Batch [B, 3, 16, 112, 112]  ➔  Conv3D Layers [B, 128, 8, 28, 28]  ➔  Logits [B, num_classes]  ➔  Grad-CAM [B, 16, 112, 112]"
    p_pf2.font.size = Pt(11.5)
    p_pf2.font.color.rgb = DARK_TEXT
    p_pf2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 4: 3D CNN Model Architecture & Tensor Flow
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3D CNN Architecture (Simple3DCNN Specifications)")

    # Architecture Table
    table_shape = s4.shapes.add_table(8, 4, Inches(0.8), Inches(1.7), Inches(11.73), Inches(4.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.6)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(2.73)

    headers = ["Layer", "Kernel & Hyperparameters", "Output Tensor Shape", "Function / Role"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    rows = [
        ("Input Clip", "16 RGB Frames @ 112x112", "(Batch, 3, 16, 112, 112)", "Spatiotemporal video sample"),
        ("Conv3D Layer 1", "64 filters, kernel (3,3,3), padding=1", "(Batch, 64, 16, 112, 112)", "Low-level spatial/motion edge detection"),
        ("MaxPool3D 1", "kernel=(1,2,2), stride=(1,2,2)", "(Batch, 64, 16, 56, 56)", "Spatial downsampling, keeps 16 frames"),
        ("Conv3D Layer 2", "128 filters, kernel (3,3,3), padding=1", "(Batch, 128, 16, 56, 56)", "High-level spatiotemporal representation (Grad-CAM target)"),
        ("MaxPool3D 2", "kernel=(2,2,2), stride=(2,2,2)", "(Batch, 128, 8, 28, 28)", "Temporal & spatial pooling (downsamples to 8 frames)"),
        ("Linear FC1", "Flatten(128 x 8 x 28 x 28 = 802,816) -> 256", "(Batch, 256)", "Dense feature abstraction with ReLU"),
        ("Linear FC2", "Linear(256, num_classes)", "(Batch, num_classes)", "Class logit output for Softmax cross-entropy")
    ]

    for row_idx, data in enumerate(rows):
        bg = CARD_BG if row_idx % 2 == 0 else WHITE
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if col_idx == 0:
                p.font.bold = True

    # Note below table
    note_box = s4.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.73), Inches(0.6))
    tf_nb = note_box.text_frame
    p_nb = tf_nb.paragraphs[0]
    p_nb.text = "Architectural Design Note: MaxPool1 selectively shrinks spatial dimensions while keeping temporal frame depth intact; MaxPool2 downsamples both time and space to control fully-connected parameter volume for fast CPU inference."
    p_nb.font.size = Pt(11)
    p_nb.font.color.rgb = MUTED_TEXT
    p_nb.font.name = "Calibri"

    # =========================================================================
    # SLIDE 5: Video Preprocessing & Data Engineering
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Video Preprocessing & Data Engineering")

    prep_cards = [
        ("1. Temporal Frame Extraction", 
         "OpenCV VideoCapture reads clips frame-by-frame.\nUniform step spacing computed using np.linspace(0, total_frames-1, 16) to ensure consistent temporal duration regardless of source video FPS.",
         BLUE),
        ("2. Geometric Standardization", 
         "Every extracted frame is resized to standard 112x112 spatial resolution.\nBGR channels converted to RGB color space for PyTorch tensor compatibility.",
         GREEN),
        ("3. Normalization & Tensor Batching", 
         "Pixel intensity values scaled from uint8 [0, 255] to float32 [0.0, 1.0].\nTensors reshaped to (Channels, Time, Height, Width) for 3D convolution processing.",
         PURPLE)
    ]

    for i, (title, content, clr) in enumerate(prep_cards):
        x = Inches(0.8 + i * 4.0)
        add_card(s5, x, Inches(1.8), Inches(3.73), Inches(3.8), bg_color=CARD_BG, border_color=clr)
        
        tb_c = s5.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.33), Inches(3.4))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True
        
        pc1 = tf_c.paragraphs[0]
        pc1.text = title
        pc1.font.size = Pt(16)
        pc1.font.bold = True
        pc1.font.color.rgb = clr
        pc1.font.name = "Calibri"
        
        pc2 = tf_c.add_paragraph()
        pc2.text = content
        pc2.font.size = Pt(12)
        pc2.font.color.rgb = DARK_TEXT
        pc2.font.name = "Calibri"
        pc2.space_before = Pt(12)

    # Dataset structure box
    add_card(s5, Inches(0.8), Inches(5.8), Inches(11.73), Inches(0.95), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_ds = s5.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.8))
    tf_ds = tb_ds.text_frame
    p_ds = tf_ds.paragraphs[0]
    p_ds.text = "Dataset Organization Standard: dataset/<activity_class>/<video_sample>.mp4"
    p_ds.font.bold = True
    p_ds.font.size = Pt(12)
    p_ds.font.color.rgb = BLUE
    p_ds.font.name = "Calibri"

    p_ds2 = tf_ds.add_paragraph()
    p_ds2.text = "Compatible with UCF101 benchmark splits and custom webcam video recordings across target categories: Walking, Running, Jumping, and Sitting/Idle."
    p_ds2.font.size = Pt(11.5)
    p_ds2.font.color.rgb = DARK_TEXT
    p_ds2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 6: Explainable AI with 3D Grad-CAM
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Explainable AI (XAI) using 3D Grad-CAM")

    # Left: Explanation steps
    add_card(s6, Inches(0.8), Inches(1.7), Inches(7.2), Inches(4.9), bg_color=CARD_BG, border_color=BLUE)
    tb_gc = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(6.8), Inches(4.5))
    tf_gc = tb_gc.text_frame
    tf_gc.word_wrap = True
    
    pgc1 = tf_gc.paragraphs[0]
    pgc1.text = "How 3D Grad-CAM Visualizes Model Attention:"
    pgc1.font.size = Pt(18)
    pgc1.font.bold = True
    pgc1.font.color.rgb = BLUE
    pgc1.font.name = "Calibri"

    gc_steps = [
        ("1. Target Layer Hook:", "Hooks into conv2, the final 3D convolutional layer capturing rich spatiotemporal features before classification."),
        ("2. Gradient Computation:", "Computes gradient of predicted class logit score (y^c) with respect to 3D feature activation maps (A^k)."),
        ("3. Global Importance Weighting:", "Applies Global Average Pooling across spatial and temporal dimensions to determine channel importance alpha_k^c."),
        ("4. ReLU Activation:", "Combines weighted feature maps through a ReLU activation to isolate only features positively supporting the predicted action."),
        ("5. Heatmap Superimposition:", "Normalizes activation map to [0, 1] and overlays it onto the original RGB frames using OpenCV COLORMAP_JET.")
    ]
    for h, desc in gc_steps:
        p = tf_gc.add_paragraph()
        p.text = f"•  {h} {desc}"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(6)

    # Right: Importance / Verification Box
    add_card(s6, Inches(8.3), Inches(1.7), Inches(4.23), Inches(4.9), bg_color=RGBColor(243, 232, 255), border_color=PURPLE)
    tb_gc_r = s6.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.83), Inches(4.5))
    tf_gc_r = tb_gc_r.text_frame
    tf_gc_r.word_wrap = True
    
    pgr1 = tf_gc_r.paragraphs[0]
    pgr1.text = "🎯 Why XAI is Essential for Defense & Viva"
    pgr1.font.size = Pt(16)
    pgr1.font.bold = True
    pgr1.font.color.rgb = PURPLE
    pgr1.font.name = "Calibri"

    why_xai = [
        "Defeats the 'Black Box' problem in Deep Learning.",
        "Proves model attends to moving human legs/arms rather than static background textures (like walls or shadows).",
        "Assures accountability for security, healthcare, and surveillance deployment.",
        "Provides judges with visual interpretability alongside numerical classification metrics."
    ]
    for pt in why_xai:
        p = tf_gc_r.add_paragraph()
        p.text = "✔  " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: Training & Optimization Setup
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Training Strategy & Hyperparameter Configuration")

    # Hyperparameter cards
    hparams = [
        ("Loss Function", "Cross-Entropy Loss", "Standard categorical cross-entropy for multi-class classification."),
        ("Optimizer", "Adam (lr = 0.001)", "Adaptive gradient estimation ensuring stable and fast convergence."),
        ("Batch Size", "4 to 8 clips", "Configured to fit into standard CPU memory without RAM overflow."),
        ("Temporal Window", "16 Frames", "Optimal trade-off between temporal motion context and frame processing latency.")
    ]

    for i, (hp_title, hp_val, hp_desc) in enumerate(hparams):
        x = Inches(0.8 + i * 3.0)
        add_card(s7, x, Inches(1.8), Inches(2.75), Inches(2.5), bg_color=CARD_BG, border_color=BLUE)
        
        tb_hp = s7.shapes.add_textbox(x + Inches(0.15), Inches(1.95), Inches(2.45), Inches(2.2))
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

    # Optimization strategies card
    add_card(s7, Inches(0.8), Inches(4.6), Inches(11.73), Inches(2.1), bg_color=WHITE, border_color=BORDER_COLOR)
    tb_opt = s7.shapes.add_textbox(Inches(1.0), Inches(4.75), Inches(11.3), Inches(1.8))
    tf_opt = tb_opt.text_frame
    tf_opt.word_wrap = True
    
    po1 = tf_opt.paragraphs[0]
    po1.text = "CPU Optimization Strategies for ThinkPad i7 / Localhost Execution:"
    po1.font.size = Pt(15)
    po1.font.bold = True
    po1.font.color.rgb = NAVY
    po1.font.name = "Calibri"

    opts = [
        "Modular Category Subsetting: Trained on core distinct activity categories to enable rapid experimentation on CPU.",
        "Model Checkpointing: Checkpoints save weights based on lowest validation loss (outputs/model_final.pth).",
        "DirectShow Video Acceleration: OpenCV CAP_DSHOW enabled on Windows for zero-latency camera frame grab.",
        "Multithreaded Inference Decoupling: Frame rendering runs at 30 FPS while 3D CNN computes asynchronously."
    ]
    for opt in opts:
        p = tf_opt.add_paragraph()
        p.text = "•  " + opt
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 8: Evaluation Framework & Metrics
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Performance Evaluation Framework")

    # Metrics Table
    tbl_shape2 = s8.shapes.add_table(5, 4, Inches(0.8), Inches(1.7), Inches(11.73), Inches(3.6))
    tbl2 = tbl_shape2.table
    tbl2.columns[0].width = Inches(2.2)
    tbl2.columns[1].width = Inches(2.5)
    tbl2.columns[2].width = Inches(4.5)
    tbl2.columns[3].width = Inches(2.53)

    eval_heads = ["Evaluation Metric", "Formula", "Purpose & Significance", "Target Threshold"]
    for c_idx, h_text in enumerate(eval_heads):
        c = tbl2.cell(0, c_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = BLUE
        p = c.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"

    eval_rows = [
        ("Accuracy", "(TP + TN) / Total", "Measures overall proportion of correctly predicted video clips.", "> 90%"),
        ("Precision", "TP / (TP + FP)", "Quantifies exactness; minimizes false action alarms (e.g., false running).", "> 88%"),
        ("Recall (Sensitivity)", "TP / (TP + FN)", "Measures ability to detect all actual action occurrences.", "> 89%"),
        ("F1-Score", "2 * (P * R) / (P + R)", "Harmonic balance between Precision and Recall under imbalanced clip counts.", "> 88%")
    ]

    for r_idx, r_data in enumerate(eval_rows):
        bg_row = CARD_BG if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(r_data):
            cell = tbl2.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_row
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_TEXT
            p.font.name = "Calibri"
            if c_idx == 0:
                p.font.bold = True

    # Analysis methodology card
    add_card(s8, Inches(0.8), Inches(5.6), Inches(11.73), Inches(1.1), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_ev = s8.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.9))
    tf_ev = tb_ev.text_frame
    tf_ev.word_wrap = True
    pe1 = tf_ev.paragraphs[0]
    pe1.text = "Validation & Reporting Methodology:"
    pe1.font.size = Pt(12)
    pe1.font.bold = True
    pe1.font.color.rgb = BLUE
    pe1.font.name = "Calibri"

    pe2 = tf_ev.add_paragraph()
    pe2.text = "Evaluated via scikit-learn classification_report alongside confusion matrix heatmaps to inspect inter-class confusion patterns (e.g. Walking vs. Running boundary detection)."
    pe2.font.size = Pt(11.5)
    pe2.font.color.rgb = DARK_TEXT
    pe2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 9: Real-Time Live Camera Predictor & Visual Output
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Real-Time Live Camera Predictor & Dashboard Output")

    # 3-Part Output Cards
    out_cards = [
        ("1. Live Video Stream", "Native 30 FPS camera capture via OpenCV.\nReal-time 16-frame sliding spatiotemporal buffer.\nMirrored selfie preview with on-screen Heads-Up Display (HUD).", BLUE),
        ("2. Motion Energy Analyzer", "Solves idle sitting posture calibration.\nEvaluates frame-differencing pixel velocity.\nPrevents subtle camera sensor noise from triggering false 'running' states.", GREEN),
        ("3. 3D Grad-CAM Attention Heatmap", "Superimposes jet colormap heatmaps in real-time.\nConfirms attention on moving limbs.\nSide-by-side or single overlay display modes toggleable with key shortcuts.", RED)
    ]

    for i, (title, text, clr) in enumerate(out_cards):
        x = Inches(0.8 + i * 4.0)
        add_card(s9, x, Inches(1.8), Inches(3.73), Inches(3.8), bg_color=CARD_BG, border_color=clr)
        
        tb_o = s9.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.33), Inches(3.4))
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

    # Deliverables banner
    add_card(s9, Inches(0.8), Inches(5.8), Inches(11.73), Inches(0.95), bg_color=LIGHT_BLUE, border_color=BLUE)
    tb_deliv = s9.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.3), Inches(0.8))
    tf_deliv = tb_deliv.text_frame
    p_dl = tf_deliv.paragraphs[0]
    p_dl.text = "Two Deployment Interfaces Ready:"
    p_dl.font.bold = True
    p_dl.font.size = Pt(12)
    p_dl.font.color.rgb = BLUE
    p_dl.font.name = "Calibri"

    p_dl2 = tf_deliv.add_paragraph()
    p_dl2.text = "1. Streamlit Web Dashboard at http://localhost:8501  |  2. High-Speed Native Desktop Window (python live_predictor.py)"
    p_dl2.font.size = Pt(11.5)
    p_dl2.font.color.rgb = DARK_TEXT
    p_dl2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 10: Conclusion & Future Scope
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion & Future Research Directions")

    # Left: Accomplishments
    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.2), bg_color=RGBColor(240, 253, 244), border_color=GREEN)
    tb_c_l = s10.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_c_l = tb_c_l.text_frame
    tf_c_l.word_wrap = True
    
    pcl1 = tf_c_l.paragraphs[0]
    pcl1.text = "🏆 Key Project Accomplishments"
    pcl1.font.size = Pt(18)
    pcl1.font.bold = True
    pcl1.font.color.rgb = GREEN
    pcl1.font.name = "Calibri"

    acc_list = [
        "End-to-End 3D-CNN Pipeline: Successfully implemented Conv3D architecture for spatiotemporal human action recognition.",
        "Integrated Explainable AI: Leveraged 3D Grad-CAM to confirm model focus on active human limbs rather than background textures.",
        "Real-Time Live Predictor: Asynchronous multithreaded engine delivering 30 FPS webcam predictions with on-screen HUD.",
        "Motion-Aware Idle Calibration: Eliminated false-positive predictions when sitting still at a desk.",
        "Open-Source GitHub Repository: Clean codebase, docs, and reproducible workflow."
    ]
    for acc in acc_list:
        p = tf_c_l.add_paragraph()
        p.text = "✔  " + acc
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(6)

    # Right: Future Scope
    add_card(s10, Inches(6.9), Inches(1.7), Inches(5.6), Inches(4.2), bg_color=RGBColor(239, 246, 255), border_color=BLUE)
    tb_c_r = s10.shapes.add_textbox(Inches(7.1), Inches(1.85), Inches(5.2), Inches(3.8))
    tf_c_r = tb_c_r.text_frame
    tf_c_r.word_wrap = True
    
    pcr1 = tf_c_r.paragraphs[0]
    pcr1.text = "🚀 Future Research Scope"
    pcr1.font.size = Pt(18)
    pcr1.font.bold = True
    pcr1.font.color.rgb = BLUE
    pcr1.font.name = "Calibri"

    scope_list = [
        "Video Transformers: Upgrade backbone to Video Swin Transformer (TimeSformer) for global attention modeling.",
        "SlowFast Networks: Integrate two-pathway networks capturing fine spatial details (Slow) and rapid motions (Fast).",
        "Edge Hardware Deployment: Quantize model (TensorRT / ONNX) for NVIDIA Jetson and Raspberry Pi edge devices.",
        "Multi-Modal Sensor Fusion: Combine synchronized audio streams with video features for enhanced activity classification."
    ]
    for sc in scope_list:
        p = tf_c_r.add_paragraph()
        p.text = "➔  " + sc
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Calibri"
        p.space_after = Pt(8)

    # Thank you footer card
    add_card(s10, Inches(0.8), Inches(6.05), Inches(11.73), Inches(0.75), bg_color=NAVY, border_color=NAVY)
    tb_ty = s10.shapes.add_textbox(Inches(1.0), Inches(6.12), Inches(11.3), Inches(0.6))
    tf_ty = tb_ty.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "Thank You!  |  Questions & Discussion  |  Department of AI & ML"
    p_ty.font.size = Pt(16)
    p_ty.font.bold = True
    p_ty.font.color.rgb = WHITE
    p_ty.font.name = "Calibri"
    p_ty.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Presentation PPTX saved successfully at: {output_path}")

if __name__ == "__main__":
    out = "C:\\Users\\T14\\.gemini\\antigravity\\scratch\\activity-recognition\\presentation.pptx"
    build_presentation(out)
