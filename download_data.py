import os
import urllib.request

def download_file(url, folder, filename):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, path)
        print(f"Done: {path}")
    else:
        print(f"File already exists: {path}")

def setup_sample_dataset():
    # We'll use 2 sample videos from Intel's open repo for a quick demo
    samples = [
        {
            "url": "https://github.com/intel-iot-devkit/sample-videos/raw/master/face-demographics-walking-and-pause.mp4",
            "class": "Walking",
            "name": "walking_1.mp4"
        },
        {
            "url": "https://github.com/intel-iot-devkit/sample-videos/raw/master/bottle-detection.mp4",
            "class": "BottleAction",
            "name": "bottle_1.mp4"
        }
    ]
    
    base_dir = "dataset"
    for item in samples:
        class_dir = os.path.join(base_dir, item["class"])
        download_file(item["url"], class_dir, item["name"])

if __name__ == "__main__":
    setup_sample_dataset()
    print("\nSample dataset ready in 'dataset/' folder.")
