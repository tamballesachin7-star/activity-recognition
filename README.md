# 🎥 Spatiotemporal Human Activity Recognition (3D-CNN & Grad-CAM)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)

A real-time spatiotemporal activity recognition and explainable AI system developed with **3D Convolutional Neural Networks (Conv3D)** and **3D Grad-CAM**. Features real-time live webcam prediction, interactive web dashboards, and presentation materials.

Developed for the **Department of Artificial Intelligence & Machine Learning (AI & ML)**.

---

## ✨ Features

- **Real-Time Live Webcam Predictor**: Low-latency 30 FPS camera classification with live Heads-Up Display (HUD) and motion dynamics.
- **Accurate Sitting / Idle Detection**: Motion energy analyzer prevents still posture from being misclassified as dynamic movements.
- **Explainable AI (XAI)**: Visualizes model attention using **3D Grad-CAM** heatmaps overlaid on video frames in real-time.
- **Interactive Web Dashboard**: Streamlit interface supporting both live camera feeds and pre-recorded video batch inference.
- **Project Presentation Deck**: Includes automated presentation generation script and presentation PDF (`presentation.pdf`).
- **CPU Optimized**: Tailored for smooth local execution on CPU hardware.

---

## 🚀 Tech Stack

- **Deep Learning**: PyTorch (3D CNN, Conv3D, MaxPool3D)
- **Computer Vision**: OpenCV
- **Explainable AI**: PyTorch Grad-CAM
- **Web UI**: Streamlit
- **PDF Generation**: ReportLab
- **Data Engineering**: NumPy, Scikit-learn

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tamballesachin7-star/activity-recognition.git
   cd activity-recognition
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📈 Running the Project

### 1. High-Speed Live Webcam Predictor (Native Window) ⚡
Run the dedicated multithreaded real-time predictor:
```bash
python live_predictor.py
```
* **Controls**:
  * `M`: Toggle Side-by-Side vs. Full Heatmap Overlay
  * `H`: Toggle Heatmap ON / OFF
  * `Q`: Exit

### 2. Localhost Web Dashboard 🌐
Launch the Streamlit interactive dashboard:
```bash
streamlit run dashboard.py
```
Access at `http://localhost:8501`.

### 3. Training the Model
Train the 3D-CNN architecture on custom or synthetic video clips:
```bash
python train.py
```

### 4. Regenerate Presentation PDF
```bash
python generate_pdf_reportlab.py
```

---

## 📁 Project Structure

```text
activity-recognition/
├── dashboard.py              # Streamlit Web Dashboard (Live Webcam & Upload)
├── live_predictor.py         # High-Speed Native Desktop Live Predictor
├── models/
│   └── cnn3d.py              # 3D CNN PyTorch Architecture
├── generate_pdf_reportlab.py # ReportLab PDF Presentation Generator
├── presentation.pdf          # Project Presentation Deck (AIML Branded)
├── train.py                  # Model Training Loop
├── dataset.py                # PyTorch Dataset Loader
├── inference_gradcam.py      # Grad-CAM Heatmap Logic
├── generate_sample_data.py   # Sample Data Generator
├── requirements.txt          # Python Dependencies
└── outputs/                  # Model Checkpoints & Output Videos
```

---

**Department of Artificial Intelligence & Machine Learning (AI & ML)**  
**Developed by [tamballesachin7-star](https://github.com/tamballesachin7-star)**
