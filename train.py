import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from models.cnn3d import Simple3DCNN
from dataset import VideoDataset
import os

def train():
    # 1. Setup Data
    if not os.path.exists('dataset'):
        print("Error: 'dataset/' folder not found. Run 'python download_data.py' first.")
        return

    dataset = VideoDataset('dataset')
    if len(dataset) == 0:
        print("Error: No videos found in 'dataset/'. Please add videos to the class folders (walking, running, etc.).")
        return
        
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    num_classes = len(dataset.classes)
    
    # 2. Setup Model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Simple3DCNN(num_classes=num_classes).to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 3. Training Loop
    epochs = 10 # Short for demo
    print(f"Starting training on {device} for {epochs} epochs...")
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for videos, labels in dataloader:
            videos, labels = videos.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(videos)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(dataloader):.4f}")
    
    # 4. Save Model
    os.makedirs('outputs', exist_ok=True)
    torch.save(model.state_dict(), 'outputs/model_final.pth')
    print("Training complete. Model saved to outputs/model_final.pth")

if __name__ == "__main__":
    train()
