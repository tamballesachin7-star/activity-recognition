import cv2
import numpy as np
import os

def create_video(output_path, activity_type, num_frames=16, size=(112, 112)):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 10.0, size)
    
    # Starting point
    x, y = size[0]//2, size[1]//2
    
    for t in range(num_frames):
        frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        cv2.rectangle(frame, (0, 0), size, (20, 20, 20), -1) # Dark background
        
        # Motion simulation
        if activity_type == 'Walking':
            x = (x + 3) % size[0]
            color = (0, 255, 0)
            cv2.circle(frame, (x, y), 8, color, -1)
        elif activity_type == 'Running':
            x = (x + 10) % size[0]
            color = (0, 255, 255)
            cv2.circle(frame, (x, y), 8, color, -1)
        elif activity_type == 'Jumping':
            y_offset = int(20 * np.sin(t * 0.5))
            color = (255, 0, 0)
            cv2.circle(frame, (x, y + y_offset), 8, color, -1)
        elif activity_type == 'Sleeping':
            color = (100, 100, 100)
            cv2.circle(frame, (x, y), 8, color, -1) # No motion
        elif activity_type == 'Flying':
            x = (x + np.random.randint(-5, 15)) % size[0]
            y = (y + np.random.randint(-10, 10)) % size[1]
            color = (255, 255, 255)
            cv2.circle(frame, (x, y), 8, color, -1)
        
        out.write(frame)
        
    out.release()

def generate_dataset():
    base_dir = 'dataset'
    classes = ['Walking', 'Running', 'Jumping', 'Sleeping', 'Flying']
    
    for cls in classes:
        cls_dir = os.path.join(base_dir, cls)
        if os.path.exists(cls_dir):
            import shutil
            shutil.rmtree(cls_dir)
        os.makedirs(cls_dir, exist_ok=True)
        print(f"Generating videos for {cls}...")
        for i in range(5): # 5 samples each for fast training
            video_path = os.path.join(cls_dir, f'video_{i}.mp4')
            create_video(video_path, cls)

if __name__ == "__main__":
    generate_dataset()
    print("Sample dataset generated successfully.")
