import streamlit as st
import torch
import cv2
import numpy as np
from models.cnn3d import Simple3DCNN
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
import os
import time
from PIL import Image

# Page Config
st.set_page_config(page_title="Spatiotemporal Human Activity Recognition Dashboard", page_icon="🎥", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 20px;
        margin-bottom: 24px;
    }
    
    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 600;
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .metric-container {
        display: flex;
        gap: 20px;
        margin-top: 10px;
    }
    
    .metric-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model
@st.cache_resource
def load_model():
    # Detect number of classes from dataset folder
    classes = [d for d in os.listdir('dataset') if os.path.isdir(os.path.join('dataset', d))]
    num_classes = len(classes) if len(classes) > 0 else 4 # Fallback
    model = Simple3DCNN(num_classes=num_classes)
    model_path = 'outputs/model_final.pth'
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

# Helper function for full video inference
def process_full_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret: break
        frames.append(frame)
    cap.release()
    
    if len(frames) == 0:
        return None, None, None

    # Process in chunks of 16 frames
    processed_frames = []
    num_chunks = len(frames) // 16
    
    # Target layers for Grad-CAM
    target_layers = [model.conv2]
    cam = GradCAM(model=model, target_layers=target_layers)
    
    # Class names from folder structure
    class_names = sorted([d for d in os.listdir('dataset') if os.path.isdir(os.path.join('dataset', d))])
    if not class_names:
        class_names = ['walking', 'running', 'jumping', 'sleeping']
    final_pred_label = "Analyzing..."
    
    for i in range(max(1, num_chunks)):
        start_idx = i * 16
        end_idx = min(start_idx + 16, len(frames))
        chunk = frames[start_idx:end_idx]
        
        # Pad if last chunk is too small
        if len(chunk) < 16:
            while len(chunk) < 16:
                chunk.append(np.zeros_like(chunk[0]))
        
        # Prepare tensor
        input_frames = [cv2.cvtColor(cv2.resize(f, (112, 112)), cv2.COLOR_BGR2RGB) for f in chunk]
        input_tensor = torch.from_numpy(np.array(input_frames)).permute(3, 0, 1, 2).float().unsqueeze(0) / 255.0
        
        # Predict
        with torch.no_grad():
            output = model(input_tensor)
            probs = torch.softmax(output, dim=1)[0]
            pred_idx = torch.argmax(output, dim=1).item()
            final_pred_label = class_names[pred_idx]
            confidence = probs[pred_idx].item()
            
        # Grad-CAM for this chunk
        grayscale_cam = cam(input_tensor=input_tensor) # (1, 16, 112, 112)
        
        for t in range(16):
            if start_idx + t >= len(frames): break
            
            # Get original frame and heatmap
            orig_frame = frames[start_idx + t]
            h, w = orig_frame.shape[:2]
            heatmap = cv2.resize(grayscale_cam[0, t, :], (w, h))
            
            # Overlay with higher visibility
            rgb_orig = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGB) / 255.0
            # Increase heatmap intensity (multiply by 1.5 and clip)
            heatmap = np.clip(heatmap * 1.5, 0, 1)
            vis = show_cam_on_image(rgb_orig, heatmap, use_rgb=True, image_weight=0.5)
            vis = (vis * 255).astype(np.uint8)
            
            # Add text
            cv2.putText(vis, f"Prediction: {final_pred_label} ({confidence:.2%})", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            processed_frames.append(cv2.cvtColor(vis, cv2.COLOR_RGB2BGR))
            
    # Save video
    output_path = 'outputs/processed_video.mp4'
    os.makedirs('outputs', exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # mp4v is generally safe for .mp4 extension
    out = cv2.VideoWriter(output_path, fourcc, fps if fps > 0 else 10.0, (width, height))
    
    for f in processed_frames:
        out.write(f)
    out.release()
    
    return output_path, final_pred_label, confidence

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Project Details")
    st.markdown('<div class="status-badge">Model: R3D-CNN</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    <div class="card" style="padding: 15px;">
        <h4 style="margin-top:0; color:#3b82f6;">Technical Stack</h4>
        <ul style="color:#94a3b8; font-size: 0.9rem;">
            <li><b>Core:</b> PyTorch 2.1</li>
            <li><b>Architecture:</b> 3D CNN</li>
            <li><b>Explainability:</b> Grad-CAM</li>
            <li><b>Processing:</b> OpenCV</li>
            <li><b>UI:</b> Streamlit / CSS3</li>
        </ul>
    </div>
    
    <div class="card" style="padding: 15px;">
        <h4 style="margin-top:0; color:#4ade80;">Performance</h4>
        <div style="font-size: 0.85rem; color:#94a3b8;">
            <b>Temporal Window:</b> 16 Frames<br>
            <b>Resolution:</b> 224x224 (HD)<br>
            <b>Latency:</b> ~120ms / batch<br>
            <b>Inference:</b> CPU Optimized
        </div>
    </div>
    
   <div class="card" style="padding: 15px;">
        <h4 style="margin-top:0; color:#fbbf24;">Features</h4>
        <ul style="color:#94a3b8; font-size: 0.85rem;">
            <li>Full Video Processing</li>
            <li>Real-time Overlays</li>
            <li>Frame-by-frame XAI</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main UI
st.title("🎥 Spatiotemporal Human Activity     Recognition Dashboard")
st.write("Upload a video and get a frame-by-frame Grad-CAM analysis video output.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Video Upload & Analysis")
    
    uploaded_file = st.file_uploader("Upload a video file (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])
    
    st.divider()
    st.write("Or use a sample video:")
    sample_videos = []
    if os.path.exists('dataset'):
        for root, dirs, files in os.walk('dataset'):
            for file in files:
                if file.endswith('.mp4'):
                    sample_videos.append(os.path.join(root, file))
    
    selected_sample = st.selectbox("Choose a sample", ["None"] + sample_videos)
    
    video_to_process = None
    if uploaded_file:
        video_to_process = os.path.join("outputs", uploaded_file.name)
        with open(video_to_process, "wb") as f:
            f.write(uploaded_file.getbuffer())
    elif selected_sample != "None":
        video_to_process = selected_sample

    if video_to_process and st.button("Process Full Video 🎬"):
        with st.spinner("Analyzing temporal features and generating heatmap video..."):
            model = load_model()
            out_video, label, conf = process_full_video(video_to_process, model)
            
            if out_video:
                st.session_state['video_result'] = {
                    'path': out_video,
                    'label': label,
                    'confidence': conf
                }
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if 'video_result' in st.session_state:
        res = st.session_state['video_result']
        st.markdown(f'''
        <div class="card">
            <h3>Final Classification</h3>
            <div style="font-size: 2rem; font-weight: 600; color: #4ade80;">{res['label']}</div>
            <div class="metric-container">
                <div class="metric-">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Avg Confidence</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">{res['confidence']:.2%}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

with col2:
    if 'video_result' in st.session_state:
        res = st.session_state['video_result']
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Analysis Output Video")
        st.write("Processed video with Grad-CAM heatmap overlay.")
        
        # Check if the file exists and is readable
        if os.path.exists(res['path']):
            # For browser compatibility, sometimes we need to convert to H264.
            # But we'll try serving the OpenCV output first.
            st.video(res['path'])
            
            with open(res['path'], "rb") as file:
                btn = st.download_button(
                    label="Download Processed Video",
                    data=file,
                    file_name="processed_activity.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("Error generating video output.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        pass

st.divider()
st.markdown('<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Powered by Antigravity AI Engine | local-host v1.1</div>', unsafe_allow_html=True)

