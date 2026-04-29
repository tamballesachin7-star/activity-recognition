import os
import sys
import torch
import cv2

def check_env():
    print("--- Environment Check ---")
    print(f"Python Version: {sys.version}")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"OpenCV Version: {cv2.__version__}")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device being used: {device.upper()}")
    
    if device == "cpu":
        print("Note: Running on CPU. Training might be slow, so we will use a small dataset subset.")
    
    # Check directory structure
    dirs = ['dataset', 'models', 'utils', 'outputs']
    print("\nChecking Project Folders:")
    for d in dirs:
        if os.path.exists(d):
            print(f"  [OK]  {d}/")
        else:
            print(f"  [ERR] {d}/ is missing!")

if __name__ == "__main__":
    check_env()
