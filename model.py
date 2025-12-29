import torch
import torch.nn as nn

class DenoisingAutoencoder(nn.Module):
    def __init__(self):
        super(DenoisingAutoencoder, self).__init__()
        
        # --- Encoder (Compressing) ---
        self.enc1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)  
        self.enc2 = nn.Conv2d(64, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.relu = nn.ReLU()
        
        # --- Decoder (Restoring) ---
        # Note: We use Upsample + Conv instead of ConvTranspose2d to fix checkerboard artifacts
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.dec1 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.dec2 = nn.Conv2d(64, 3, kernel_size=3, padding=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # Encoder
        # x shape: [Batch, 3, 128, 128]
        e1 = self.relu(self.enc1(x))
        # e1 shape: [Batch, 64, 128, 128]
        
        e2 = self.relu(self.enc2(e1))
        # e2 shape: [Batch, 32, 128, 128]
        
        compressed = self.pool(e2)
        # compressed shape: [Batch, 32, 64, 64]
        
        # Decoder
        restored = self.up(compressed)
        # restored shape: [Batch, 32, 128, 128]
        
        restored = self.relu(self.dec1(restored))
        
        # --- SKIP CONNECTION TRICK ---
        # We add the details from the encoder (e1) back to the decoder.
        # This helps the model "remember" the sharp edges.
        restored = restored + e1  
        
        restored = self.sigmoid(self.dec2(restored))
        return restored