import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
from models.cnn3d import Simple3DCNN
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
import os

def run_inference(video_path):
    device = torch.device("cpu") # Keep on CPU for simplicity
    
    # 1. Load Model
    # Note: We need to know the number of classes. In our demo, it's 2.
    num_classes = 2 # Demo: Walking, BottleAction
    model = Simple3DCNN(num_classes=num_classes)
    
    model_path = 'outputs/model_final.pth'
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
        print("Loaded trained model weights.")
    else:
        print("Warning: Model weights not found. Using random initialization for demo.")
    
    model.eval()

    # 2. Preprocess Video
    from dataset import VideoDataset
    ds = VideoDataset('dataset') # To get class names
    class_names = ds.classes
    
    cap = cv2.VideoCapture(video_path)
    frames = []
    original_frames = []
    for _ in range(16):
        ret, frame = cap.read()
        if not ret: break
        original_frames.append(cv2.resize(frame, (224, 224)))
        f = cv2.resize(frame, (112, 112))
        f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        frames.append(f)
    cap.release()
    
    input_tensor = torch.from_numpy(np.array(frames)).permute(3, 0, 1, 2).float().unsqueeze(0) / 255.0

    # 3. Predict
    with torch.no_grad():
        output = model(input_tensor)
        pred_idx = torch.argmax(output, dim=1).item()
        confidence = torch.softmax(output, dim=1)[0][pred_idx].item()
    
    pred_label = class_names[pred_idx] if pred_idx < len(class_names) else f"Class {pred_idx}"
    print(f"Prediction: {pred_label} ({confidence:.2%})")

    # 4. Grad-CAM
    # Target the last convolutional layer (conv2 in our Simple3DCNN)
    target_layers = [model.conv2]
    cam = GradCAM(model=model, target_layers=target_layers)
    
    # Generate heatmap
    grayscale_cam = cam(input_tensor=input_tensor)
    # grayscale_cam shape is (Batch, Frames, H, W) -> (1, 16, 112, 112)
    
    # Save a comparison image (Middle frame)
    mid_idx = 8
    heatmap_frame = grayscale_cam[0, mid_idx, :]
    rgb_frame = frames[mid_idx] / 255.0
    
    visualization = show_cam_on_image(rgb_frame, heatmap_frame, use_rgb=True)
    
    # Save output
    os.makedirs('outputs', exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title(f"Original Frame ({pred_label})")
    plt.imshow(rgb_frame)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.title("Grad-CAM Heatmap")
    plt.imshow(visualization)
    plt.axis('off')
    
    plt.savefig('outputs/gradcam_result.png')
    print("Grad-CAM result saved to outputs/gradcam_result.png")
    plt.show()

if __name__ == "__main__":
    # Test on one of the downloaded videos
    test_video = 'dataset/MovingCircle/video_0.mp4'
    if os.path.exists(test_video):
        run_inference(test_video)
    else:
        print(f"Test video {test_video} not found. Run download_data.py first.")
