import torch
import torch.nn as nn

class Simple3DCNN(nn.Module):
    def __init__(self, num_classes):
        super(Simple3DCNN, self).__init__()

        # Input shape: (Batch, Channels, Frames, Height, Width) -> (B, 3, 16, 112, 112)
        
        self.conv1 = nn.Conv3d(3, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2)) # Spatially downsample

        self.conv2 = nn.Conv3d(64, 128, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2)) # Spatially and Temporally downsample

        # After pool1: (B, 64, 16, 56, 56)
        # After pool2: (B, 128, 8, 28, 28)
        
        self.flatten = nn.Flatten()
        
        # Calculate linear input size: 128 * 8 * 28 * 28 = 802,816
        self.fc1 = nn.Linear(128 * 8 * 28 * 28, 256)
        self.fc2 = nn.Linear(256, num_classes)

        self.relu = nn.ReLU()

    def forward(self, x):
        # Layer 1
        x = self.relu(self.conv1(x))
        x = self.pool1(x)
        
        # Layer 2
        x = self.relu(self.conv2(x))
        x = self.pool2(x)

        x = self.flatten(x)

        x = self.relu(self.fc1(x))
        x = self.fc2(x)

        return x

if __name__ == "__main__":
    # Test with dummy data (Batch=1, Channels=3, Frames=16, H=112, W=112)
    model = Simple3DCNN(num_classes=10)
    dummy_input = torch.randn(1, 3, 16, 112, 112)
    output = model(dummy_input)
    print(f"Model output shape: {output.shape}") # Should be [1, 10]
