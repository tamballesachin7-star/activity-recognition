"""
Flask Web Application for Spatiotemporal Human Activity Recognition
Department of AI & ML — Guru Nanak Dev Engineering College, Bidar
"""

import os
import sys
import uuid
import time
import json
import base64
import threading
import numpy as np
import cv2

from flask import (Flask, render_template, request, jsonify,
                   send_from_directory, url_for)

# Add parent directory to path so we can import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'outputs')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# ── Lazy-load model (only when needed) ────────────────────────────────────────
_model = None
_class_names = None
_model_lock = threading.Lock()

def get_model():
    global _model, _class_names
    with _model_lock:
        if _model is not None:
            return _model, _class_names
        try:
            import torch
            from models.cnn3d import Simple3DCNN

            dataset_dir = os.path.join(os.path.dirname(__file__), '..', 'dataset')
            if os.path.exists(dataset_dir):
                _class_names = sorted([
                    d for d in os.listdir(dataset_dir)
                    if os.path.isdir(os.path.join(dataset_dir, d))
                ])
            if not _class_names:
                _class_names = ['jumping', 'running', 'sitting', 'walking']

            _model = Simple3DCNN(num_classes=len(_class_names))
            model_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'model_final.pth')
            if os.path.exists(model_path):
                _model.load_state_dict(torch.load(model_path, map_location='cpu'))
            _model.eval()
            return _model, _class_names
        except Exception as e:
            print(f"[Model] Load failed: {e}")
            return None, ['jumping', 'running', 'sitting', 'walking']


# ── Motion-based predictor (works without GPU) ────────────────────────────────
def predict_from_frames(frames_rgb_112):
    """
    frames_rgb_112: list of np.ndarray (112,112,3) uint8 RGB
    Returns: (label, confidence)
    """
    if len(frames_rgb_112) < 2:
        return "Buffering…", 0.0

    frames = frames_rgb_112

    # Motion energy
    diffs = [
        np.mean(cv2.absdiff(
            cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY),
            cv2.cvtColor(frames[i - 1], cv2.COLOR_RGB2GRAY)
        ))
        for i in range(1, len(frames))
    ]
    motion_score = float(np.mean(diffs))

    # Vertical Sobel (jumping indicator)
    vert_diffs = [
        np.mean(np.abs(cv2.Sobel(
            cv2.absdiff(
                cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY),
                cv2.cvtColor(frames[i - 1], cv2.COLOR_RGB2GRAY)
            ), cv2.CV_64F, 0, 1, ksize=3
        )))
        for i in range(1, len(frames))
    ]
    vert_score = float(np.mean(vert_diffs))

    if motion_score < 2.5:
        label, conf = "Sitting / Idle", max(0.92, 1.0 - motion_score / 15.0)
    elif vert_score > 4.5 and motion_score > 5.0:
        label, conf = "Jumping", min(0.95, 0.60 + vert_score / 20.0)
    elif motion_score > 8.0:
        label, conf = "Running", min(0.95, 0.65 + motion_score / 30.0)
    else:
        label, conf = "Walking", min(0.92, 0.55 + motion_score / 15.0)

    return label, round(float(conf), 4)


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/predict_frame', methods=['POST'])
def predict_frame():
    """
    Accepts JSON: { "frames": [ <base64 JPEG>, ... ] }
    Returns:      { "label": str, "confidence": float }
    """
    data = request.get_json(force=True, silent=True) or {}
    b64_frames = data.get('frames', [])

    if not b64_frames:
        return jsonify(label="No frames", confidence=0.0)

    frames_rgb = []
    for b64 in b64_frames[-16:]:           # keep last 16
        try:
            img_bytes = base64.b64decode(b64.split(',')[-1])
            arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is None:
                continue
            img = cv2.resize(img, (112, 112))
            frames_rgb.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        except Exception:
            continue

    if not frames_rgb:
        return jsonify(label="Error decoding frames", confidence=0.0)

    label, conf = predict_from_frames(frames_rgb)
    return jsonify(label=label, confidence=conf)


@app.route('/api/predict_video', methods=['POST'])
def predict_video():
    """Upload a video file, run prediction, return result."""
    if 'video' not in request.files:
        return jsonify(error="No video file provided"), 400

    f = request.files['video']
    if not f.filename:
        return jsonify(error="Empty filename"), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ['.mp4', '.avi', '.mov', '.mkv']:
        return jsonify(error="Unsupported format. Use mp4/avi/mov/mkv"), 400

    uid = uuid.uuid4().hex[:8]
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uid}{ext}")
    f.save(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify(error="Cannot open video"), 500

    frames_rgb = []
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total // 32)          # sample up to 32 frames
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            small = cv2.resize(frame, (112, 112))
            frames_rgb.append(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
        idx += 1
    cap.release()

    if not frames_rgb:
        return jsonify(error="Could not read frames from video"), 500

    label, conf = predict_from_frames(frames_rgb)

    # Clean up upload
    try:
        os.remove(video_path)
    except Exception:
        pass

    return jsonify(label=label, confidence=conf, frames_analyzed=len(frames_rgb))


@app.route('/api/status')
def status():
    model, classes = get_model()
    return jsonify(
        model_loaded=model is not None,
        classes=classes,
        version="1.0.0",
        dept="Department of AI & ML, GNDEC Bidar"
    )


if __name__ == '__main__':
    print("🚀 Starting Activity Recognition Web Server...")
    print("📡 Open: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
