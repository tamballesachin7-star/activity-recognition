import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset

class VideoDataset(Dataset):
    def __init__(self, root_dir, num_frames=16, transform=None):
        self.root_dir = root_dir
        self.num_frames = num_frames
        self.transform = transform
        self.classes = sorted(os.listdir(root_dir))
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        
        self.samples = []
        for cls in self.classes:
            cls_dir = os.path.join(root_dir, cls)
            if not os.path.isdir(cls_dir): continue
            for vid_name in os.listdir(cls_dir):
                if vid_name.endswith(('.mp4', '.avi')):
                    self.samples.append((os.path.join(cls_dir, vid_name), self.class_to_idx[cls]))

    def __len__(self):
        return len(self.samples)

    def _extract_frames(self, video_path):
        cap = cv2.VideoCapture(video_path)
        v_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample num_frames evenly
        if v_len < self.num_frames:
            indices = np.arange(v_len)
        else:
            indices = np.linspace(0, v_len - 1, self.num_frames, dtype=int)
            
        frames = []
        for i in range(v_len):
            ret, frame = cap.read()
            if not ret: break
            if i in indices:
                frame = cv2.resize(frame, (112, 112))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
        cap.release()
        
        # Padding if needed
        while len(frames) < self.num_frames:
            frames.append(np.zeros((112, 112, 3), dtype=np.uint8))
            
        # Convert to tensor: (Frames, H, W, C) -> (C, Frames, H, W)
        frames = np.array(frames)
        video_tensor = torch.from_numpy(frames).permute(3, 0, 1, 2).float() / 255.0
        return video_tensor

    def __getitem__(self, idx):
        video_path, label = self.samples[idx]
        video_tensor = self._extract_frames(video_path)
        return video_tensor, label

if __name__ == "__main__":
    # Test dataset
    if os.path.exists('dataset'):
        ds = VideoDataset('dataset')
        if len(ds) > 0:
            v, l = ds[0]
            print(f"Video shape: {v.shape}, Label: {l}")
        else:
            print("Dataset empty. Run download_data.py first.")
