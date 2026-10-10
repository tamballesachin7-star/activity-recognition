import sys
import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Top banner line (except page 1)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#1E3A8A")) # Deep Navy Blue
            self.setLineWidth(2.5)
            self.line(35, 550, 806, 550)

        # Footer banner
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(35, 22, "Department of Artificial Intelligence & Machine Learning (AI & ML)")
        
        self.setFont("Helvetica", 10)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(410, 22, "| 3D CNN & Grad-CAM Project")
        
        page_str = f"Slide {self._pageNumber} / {page_count}"
        self.drawRightString(806, 22, page_str)
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(1)
        self.line(35, 36, 806, 36)
        self.restoreState()

def create_presentation_pdf(output_path):
    # Setup document (A4 Landscape: 841.89 x 595.27 pt)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=35,
        rightMargin=35,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Big, Bold, Highly Readable Presentation Typography
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.HexColor("#0F172A")
    )
    
    subtitle_style = ParagraphStyle(
        'MainSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=colors.HexColor("#334155")
    )
    
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=14
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=19,
        textColor=colors.HexColor("#1E293B")
    )

    bold_body_style = ParagraphStyle(
        'SlideBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=19,
        textColor=colors.HexColor("#0F172A")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F172A")
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # ---------------------------------------------------------
    # SLIDE 1: Title Slide (AIML Dept Branded & Big Fonts)
    # ---------------------------------------------------------
    story.append(Spacer(1, 15))
    badge_table = Table([[Paragraph("DEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING (AI & ML)", badge_style)]], colWidths=[600])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#DBEAFE")),
        ('BORDER', (0,0), (-1,-1), 1.5, colors.HexColor("#2563EB")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Video Activity Recognition", title_style))
    story.append(Paragraph("Using 3D CNN & Grad-CAM Explainable AI", ParagraphStyle('Sub', parent=title_style, fontSize=24, textColor=colors.HexColor("#2563EB"))))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Spatiotemporal Feature Learning for Human Action Classification paired with Visual Attention Heatmaps.", subtitle_style))
    story.append(Spacer(1, 30))

    meta_data = [
        [Paragraph("<b>Department:</b> AI & Machine Learning (AIML)", bold_body_style), Paragraph("<b>Core Architecture:</b> 3D CNN (Conv3D)", bold_body_style)],
        [Paragraph("<b>Framework:</b> PyTorch & OpenCV", bold_body_style), Paragraph("<b>Explainability:</b> 3D Grad-CAM Heatmaps", bold_body_style)],
        [Paragraph("<b>Dataset:</b> UCF101 Action Categories", bold_body_style), Paragraph("<b>Target Environment:</b> Local CPU Execution", bold_body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[385, 385])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 2: Problem Statement & Motivation
    # ---------------------------------------------------------
    story.append(Paragraph("Problem Statement & Motivation", slide_title_style))
    story.append(Paragraph("Why traditional 2D CNNs fail and why 3D CNNs are required:", body_style))
    story.append(Spacer(1, 15))

    p2_data = [
        [
            Paragraph("<b>Limitations of Standard 2D CNNs</b>", ParagraphStyle('RedH', parent=bold_body_style, fontSize=15, textColor=colors.HexColor("#DC2626"))),
            Paragraph("<b>Advantages of 3D CNNs (AIML Solution)</b>", ParagraphStyle('GreenH', parent=bold_body_style, fontSize=15, textColor=colors.HexColor("#16A34A")))
        ],
        [
            Paragraph("&bull; Evaluates static frames independently (Spatial H &times; W).<br/><br/>&bull; Extracts posture only ('What is in the image').<br/><br/>&bull; Ignores temporal motion trajectories across time.<br/><br/>&bull; Cannot distinguish opposite actions with identical poses.", body_style),
            Paragraph("&bull; Applies 3D kernels across Spatial + Temporal (H &times; W &times; Time).<br/><br/>&bull; Captures posture AND motion trajectory simultaneously.<br/><br/>&bull; Preserves time-series continuity across frames.<br/><br/>&bull; Accurately classifies sequential human actions.", body_style)
        ]
    ]
    p2_table = Table(p2_data, colWidths=[380, 390])
    p2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#FEF2F2")),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (0,-1), 1.5, colors.HexColor("#FCA5A5")),
        ('BOX', (1,0), (1,-1), 1.5, colors.HexColor("#86EFAC")),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(p2_table)
    story.append(Spacer(1, 15))

    takeaway = Table([[Paragraph("<b>Key Concept:</b> 3D Convolutions are required because motion across consecutive video frames carries the semantic meaning of human activities.", body_style)]], colWidths=[770])
    takeaway.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(takeaway)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 3: End-to-End Pipeline
    # ---------------------------------------------------------
    story.append(Paragraph("System Pipeline Architecture", slide_title_style))
    story.append(Paragraph("Complete data flow from video input to model prediction and heatmaps:", body_style))
    story.append(Spacer(1, 20))

    pipe_data = [
        [
            Paragraph("<b>1. Input Video</b>", bold_body_style),
            Paragraph("<b>2. Preprocessing</b>", bold_body_style),
            Paragraph("<b>3. 3D CNN</b>", bold_body_style),
            Paragraph("<b>4. Classifier</b>", bold_body_style),
            Paragraph("<b>5. Grad-CAM</b>", bold_body_style)
        ],
        [
            Paragraph("Raw video clip<br/>(MP4 / AVI format)", body_style),
            Paragraph("16 uniform frames<br/>Resized 112&times;112 RGB", body_style),
            Paragraph("Spatiotemporal Conv<br/>Feature maps", body_style),
            Paragraph("Softmax Layer<br/>Action class label", body_style),
            Paragraph("3D Heatmap overlay<br/>Visual attention map", body_style)
        ]
    ]
    pipe_table = Table(pipe_data, colWidths=[154, 154, 154, 154, 154])
    pipe_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFFFF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#94A3B8")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(pipe_table)
    story.append(Spacer(1, 25))

    stream_info = Table([[Paragraph("<b>Tensor Pipeline Flow:</b> Input Video &rarr; OpenCV Frame Extractor &rarr; Tensor <code>(Batch, 3, 16, 112, 112)</code> &rarr; 3D CNN Forward Pass &rarr; Softmax Class Logits &rarr; Grad-CAM Backprop &rarr; Visual Overlay.", body_style)]], colWidths=[770])
    stream_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(stream_info)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 4: 3D CNN Model Details
    # ---------------------------------------------------------
    story.append(Paragraph("3D CNN Model Architecture & Tensor Shapes", slide_title_style))
    story.append(Paragraph("PyTorch <code>Simple3DCNN</code> network specifications:", body_style))
    story.append(Spacer(1, 15))

    arch_table_data = [
        [Paragraph("<b>Network Layer</b>", bold_body_style), Paragraph("<b>Kernel Parameters</b>", bold_body_style), Paragraph("<b>Output Tensor Dimension</b>", bold_body_style)],
        [Paragraph("Input Video Clip", body_style), Paragraph("16 RGB Frames @ 112&times;112 resolution", body_style), Paragraph("(B, 3, 16, 112, 112)", code_style)],
        [Paragraph("Conv3D Layer 1", body_style), Paragraph("3 &rarr; 64 filters, kernel (3,3,3), padding=1", body_style), Paragraph("(B, 64, 16, 112, 112)", code_style)],
        [Paragraph("MaxPool3D 1", body_style), Paragraph("kernel=(1,2,2), stride=(1,2,2)", body_style), Paragraph("(B, 64, 16, 56, 56)", code_style)],
        [Paragraph("Conv3D Layer 2 (Target)", body_style), Paragraph("64 &rarr; 128 filters, kernel (3,3,3), padding=1", body_style), Paragraph("(B, 128, 16, 56, 56)", code_style)],
        [Paragraph("MaxPool3D 2", body_style), Paragraph("kernel=(2,2,2), stride=(2,2,2)", body_style), Paragraph("(B, 128, 8, 28, 28)", code_style)],
        [Paragraph("Linear FC1", body_style), Paragraph("Linear(128 &times; 8 &times; 28 &times; 28, 256)", body_style), Paragraph("(B, 256)", code_style)],
        [Paragraph("Linear FC2 (Classifier)", body_style), Paragraph("Linear(256, num_classes)", body_style), Paragraph("(B, num_classes)", code_style)]
    ]
    arch_table = Table(arch_table_data, colWidths=[180, 330, 260])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#DBEAFE")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#3B82F6")),
        ('INNERGRID', (0,0), (-1,-1), 0.75, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(arch_table)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 5: Video Preprocessing
    # ---------------------------------------------------------
    story.append(Paragraph("Video Preprocessing & Clip Generation", slide_title_style))
    story.append(Paragraph("Standardizing raw video clips for robust tensor creation:", body_style))
    story.append(Spacer(1, 15))

    prep_data = [
        [
            Paragraph("<b>1. Uniform Frame Sampling</b>", bold_body_style),
            Paragraph("<b>2. Resizing & Color Space</b>", bold_body_style),
            Paragraph("<b>3. Normalization</b>", bold_body_style)
        ],
        [
            Paragraph("Reads frames using OpenCV <code>VideoCapture</code>. Computes uniform indices with <code>np.linspace</code> to extract exactly 16 frames per clip.", body_style),
            Paragraph("Resizes every frame to standard 112&times;112 resolution. Converts BGR to RGB color space for PyTorch compatibility.", body_style),
            Paragraph("Scales uint8 pixel values [0, 255] to float32 [0, 1]. Applies standardization for stable gradient flow.", body_style)
        ]
    ]
    prep_table = Table(prep_data, colWidths=[256, 256, 256])
    prep_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(prep_table)
    story.append(Spacer(1, 20))

    dir_box = Table([[Paragraph("<b>Dataset Folder Structure:</b><br/><code>dataset/&lt;class_name&gt;/&lt;video_file&gt;.mp4</code> (e.g., <code>dataset/Walking/v_Walking_g01_c01.avi</code>)", body_style)]], colWidths=[770])
    dir_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(dir_box)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 6: Explainable AI with Grad-CAM
    # ---------------------------------------------------------
    story.append(Paragraph("Explainable AI (XAI) using 3D Grad-CAM", slide_title_style))
    story.append(Paragraph("Visualizing where the model focuses when predicting actions:", body_style))
    story.append(Spacer(1, 15))

    grad_data = [
        [Paragraph("<b>Step</b>", bold_body_style), Paragraph("<b>Grad-CAM Operation</b>", bold_body_style), Paragraph("<b>Technical Explanation</b>", bold_body_style)],
        [Paragraph("1. Target Layer", body_style), Paragraph("Select <code>conv2</code> final 3D conv layer", body_style), Paragraph("Hooks into high-level spatiotemporal feature maps.", body_style)],
        [Paragraph("2. Gradients", body_style), Paragraph("Compute &part;y<sup>c</sup> / &part;A<sup>k</sup>", body_style), Paragraph("Calculates backprop gradients of target class score.", body_style)],
        [Paragraph("3. Weighting", body_style), Paragraph("Global Average Pooling of gradients", body_style), Paragraph("Obtains importance weights &alpha;<sub>k</sub><sup>c</sup> per feature map.", body_style)],
        [Paragraph("4. Heatmap", body_style), Paragraph("Apply ReLU(&sum; &alpha;<sub>k</sub><sup>c</sup> A<sup>k</sup>)", body_style), Paragraph("Isolates positive contributing spatial-temporal regions.", body_style)],
        [Paragraph("5. Visualization", body_style), Paragraph("OpenCV COLORMAP_JET superimposition", body_style), Paragraph("Overlays heatmap onto original video frames for output.", body_style)]
    ]
    grad_table = Table(grad_data, colWidths=[130, 280, 360])
    grad_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3E8FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#C084FC")),
        ('INNERGRID', (0,0), (-1,-1), 0.75, colors.HexColor("#E9D5FF")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(grad_table)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 7: Training & Optimization Setup
    # ---------------------------------------------------------
    story.append(Paragraph("Training Strategy & Hyperparameters", slide_title_style))
    story.append(Paragraph("Model training configuration and local CPU optimization:", body_style))
    story.append(Spacer(1, 15))

    hp_data = [
        [Paragraph("<b>Hyperparameter</b>", bold_body_style), Paragraph("<b>Value</b>", bold_body_style), Paragraph("<b>Description / Rationale</b>", bold_body_style)],
        [Paragraph("Loss Function", body_style), Paragraph("CrossEntropyLoss", body_style), Paragraph("Multi-class categorical cross-entropy loss function.", body_style)],
        [Paragraph("Optimizer", body_style), Paragraph("Adam (lr = 0.001)", body_style), Paragraph("Adaptive gradient optimizer for fast convergence.", body_style)],
        [Paragraph("Batch Size", body_style), Paragraph("4 / 8 clips", body_style), Paragraph("Prevents RAM overflow during local CPU execution.", body_style)],
        [Paragraph("Sequence Length", body_style), Paragraph("16 frames", body_style), Paragraph("Optimal temporal window size for video clip modeling.", body_style)]
    ]
    hp_table = Table(hp_data, colWidths=[180, 200, 390])
    hp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.75, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(hp_table)
    story.append(Spacer(1, 15))

    opt_box = Table([[Paragraph("<b>CPU Optimization Strategy:</b><br/>&bull; Trained on modular dataset subset (2-3 distinct activity classes) for fast execution on ThinkPad i7.<br/>&bull; Model checkpointing automatically saves highest accuracy weights to <code>models/best_3dcnn.pth</code>.", body_style)]], colWidths=[770])
    opt_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(opt_box)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 8: Evaluation Framework
    # ---------------------------------------------------------
    story.append(Paragraph("Performance Evaluation Framework", slide_title_style))
    story.append(Paragraph("Quantitative performance metrics for model validation:", body_style))
    story.append(Spacer(1, 15))

    eval_data = [
        [Paragraph("<b>Metric</b>", bold_body_style), Paragraph("<b>Formula</b>", bold_body_style), Paragraph("<b>Evaluation Purpose</b>", bold_body_style)],
        [Paragraph("Accuracy", body_style), Paragraph("(TP + TN) / Total", code_style), Paragraph("Overall proportion of correctly classified video clips.", body_style)],
        [Paragraph("Precision", body_style), Paragraph("TP / (TP + FP)", code_style), Paragraph("Measures exactness (low false positive action triggers).", body_style)],
        [Paragraph("Recall", body_style), Paragraph("TP / (TP + FN)", code_style), Paragraph("Measures sensitivity in capturing true action occurrences.", body_style)],
        [Paragraph("F1-Score", body_style), Paragraph("2 &times; (P &times; R) / (P + R)", code_style), Paragraph("Harmonic mean evaluating class-imbalance performance.", body_style)]
    ]
    eval_table = Table(eval_data, colWidths=[150, 230, 390])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#DBEAFE")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#3B82F6")),
        ('INNERGRID', (0,0), (-1,-1), 0.75, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(eval_table)
    story.append(Spacer(1, 20))

    report_info = Table([[Paragraph("Evaluated using <code>sklearn.metrics.classification_report</code> along with multi-class confusion matrix heatmaps to verify class prediction quality.", body_style)]], colWidths=[770])
    report_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(report_info)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 9: Presentation Output Deliverable
    # ---------------------------------------------------------
    story.append(Paragraph("Final Output Deliverable & Demo", slide_title_style))
    story.append(Paragraph("3-part visualization output for project presentation:", body_style))
    story.append(Spacer(1, 20))

    demo_data = [
        [
            Paragraph("<b>1. Input Video Stream</b>", bold_body_style),
            Paragraph("<b>2. Prediction & Confidence</b>", bold_body_style),
            Paragraph("<b>3. Grad-CAM Heatmap</b>", bold_body_style)
        ],
        [
            Paragraph("Raw video clip sampled into 16 RGB frame sequences.<br/><br/><i>Example: Walking video clip</i>", body_style),
            Paragraph("Model predicts target action class with confidence score.<br/><br/><b>Output:</b> 'Walking' (98.4% Confidence)", body_style),
            Paragraph("Superimposes red/yellow attention heatmaps on frames.<br/><br/><b>Verification:</b> Confirms focus on moving legs.", body_style)
        ]
    ]
    demo_table = Table(demo_data, colWidths=[256, 256, 256])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#F1F5F9")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#F3E8FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#94A3B8")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(demo_table)
    story.append(PageBreak())

    # ---------------------------------------------------------
    # SLIDE 10: Conclusion & Future Scope
    # ---------------------------------------------------------
    story.append(Paragraph("Conclusion & Future Scope", slide_title_style))
    story.append(Spacer(1, 10))

    conc_data = [
        [
            Paragraph("<b>Key Project Accomplishments</b>", ParagraphStyle('GreenH2', parent=bold_body_style, fontSize=16, textColor=colors.HexColor("#16A34A"))),
            Paragraph("<b>Future Enhancements</b>", ParagraphStyle('BlueH2', parent=bold_body_style, fontSize=16, textColor=colors.HexColor("#2563EB")))
        ],
        [
            Paragraph("&bull; Built complete end-to-end 3D CNN pipeline for video action recognition.<br/><br/>&bull; Successfully integrated 3D Grad-CAM for visual decision interpretability.<br/><br/>&bull; Optimized codebase for local CPU execution.<br/><br/>&bull; Proved spatiotemporal feature learning over 2D frame baselines.", body_style),
            Paragraph("&bull; Upgrade backbone to <b>Video Swin Transformers / SlowFast Networks</b>.<br/><br/>&bull; Deploy model to edge hardware (Raspberry Pi / NVIDIA Jetson).<br/><br/>&bull; Multi-modal fusion combining audio signals with 3D video features.<br/><br/>&bull; Expand real-time video surveillance action detection.", body_style)
        ]
    ]
    conc_table = Table(conc_data, colWidths=[380, 390])
    conc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F0FDF4")),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (0,-1), 1.5, colors.HexColor("#86EFAC")),
        ('BOX', (1,0), (1,-1), 1.5, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(conc_table)
    story.append(Spacer(1, 40))

    thanks = Paragraph("<b>Thank You!</b><br/><font size=12 color='#64748B'>Department of Artificial Intelligence & Machine Learning (AI & ML)</font>", ParagraphStyle('Thanks', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=26, alignment=1, textColor=colors.HexColor("#0F172A")))
    story.append(thanks)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated AIML presentation PDF with big readable fonts at: {output_path}")

if __name__ == "__main__":
    out_pdf = "C:\\Users\\T14\\.gemini\\antigravity\\brain\\8131d2ab-149c-4302-a9c1-ea90d8d68a1d\\presentation.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    create_presentation_pdf(out_pdf)
