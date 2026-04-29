import os
import requests
import zipfile
import cv2
import numpy as np

# Configuration
DATASET_URL = "https://www.crcv.ucf.edu/data/UCF101/UCF101.rar" # This is the full dataset (6.5GB)
# For CPU testing, we might want to manually download just a few videos or use a smaller mirror.
# Since UCF101 is a .rar, we'd need 'rarfile' or 'unrar' installed.
# To keep it simple, I'll provide a script that expects you to have a few videos in dataset/ folder.

def extract_frames(video_path, num_frames=16, resize=(112, 112)):
    """Extracts exactly num_frames from a video, resized and normalized."""
    cap = cv2.VideoCapture(video_path)
    v_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Simple sampling: get num_frames evenly spaced
    indices = np.linspace(0, v_len - 1, num_frames, dtype=int)
    
    frames = []
    count = 0
    success, frame = cap.read()
    while success:
        if count in indices:
            frame = cv2.resize(frame, resize)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # PyTorch expects RGB
            frames.append(frame)
        count += 1
        success, frame = cap.read()
    cap.release()
    
    # Handle cases where video is shorter than num_frames
    while len(frames) < num_frames:
        frames.append(np.zeros((*resize, 3), dtype=np.uint8))
        
    return np.array(frames)

def prepare_dummy_data():
    """Creates a mock dataset structure if you don't have UCF101 yet."""
    classes = ['ApplyEyeMakeup', 'Archery']
    base_dir = 'dataset'
    for cls in classes:
        os.makedirs(os.path.join(base_dir, cls), exist_ok=True)
    print(f"Created dummy folders in {base_dir}/. Please place .avi or .mp4 files inside them.")

if __name__ == "__main__":
    prepare_dummy_data()
    print("Pre-processing utility ready.")
