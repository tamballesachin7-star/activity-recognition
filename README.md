# 🎥 Spatiotemporal Human Activity Recognition (3D-CNN)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)

A high-performance spatiotemporal activity recognition system utilizing **3D Convolutional Neural Networks (R3D-CNN)** and **Grad-CAM** for explainable video analysis. This project features a premium interactive dashboard for real-time inference and visualization.

## ✨ Features

-   **Deep 3D-CNN Architecture**: Leverages spatiotemporal features from video sequences for accurate activity classification.
-   **Explainable AI (XAI)**: Integrated **Grad-CAM** heatmaps to visualize which temporal and spatial regions the model focuses on.
-   **Premium Dashboard**: A sleek, modern Streamlit UI with glassmorphism effects and real-time processing feedback.
-   **Full Video Inference**: Process entire video files and generate downloadable results with heatmap overlays.
-   **Synthetic Data Support**: Includes a built-in generator for rapid testing and movement simulation.
-   **CPU Optimized**: Designed to run efficiently on local machines without requiring high-end GPUs.

## 🚀 Tech Stack

-   **Deep Learning**: PyTorch
-   **Computer Vision**: OpenCV, torchvision
-   **Visualization**: Grad-CAM, Matplotlib
-   **UI/UX**: Streamlit, Custom CSS3
-   **Data Management**: NumPy, Scikit-learn

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tamballesachin7-star/activity-recognition.git
   cd activity-recognition
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Sample Data (Optional)**:
   ```bash
   python generate_sample_data.py
   ```

## 📈 Usage

### 1. Training the Model
To train the 3D-CNN on your dataset:
```bash
python train.py
```

### 2. Launching the Dashboard
To start the interactive web interface:
```bash
streamlit run dashboard.py
```

## 🎥 Dashboard Preview
The dashboard allows users to upload videos, view frame-by-frame classification, and download a processed version with spatiotemporal heatmaps highlighting the recognized actions.

## 📁 Project Structure

```text
activity-recognition/
├── dashboard.py           # Streamlit Web Application
├── train.py               # Model Training Script
├── dataset.py             # PyTorch Dataset Loaders
├── models/                # 3D-CNN Model Definitions
├── inference_gradcam.py   # XAI & Heatmap Logic
├── generate_sample_data.py# Synthetic Data Generator
├── requirements.txt       # Project Dependencies
└── outputs/               # Saved Models and Processed Videos
```

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

---
**Developed with ❤️ by [tamballesachin7-star](https://github.com/tamballesachin7-star)**
