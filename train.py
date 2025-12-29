import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from dataset import NoisyImageDataset
from model import DenoisingAutoencoder
import os

# --- Configuration ---
CLEAN_PATH = "dataset/clean_images"
NOISY_PATH = "dataset/corrupted_images"
MODEL_SAVE_PATH = "denoising_model.pth"
BATCH_SIZE = 16
LEARNING_RATE = 0.001
EPOCHS = 20  # You can increase this if you have time
IMAGE_SIZE = 128 # Resize images to 128x128 for speed

def train():
    # 1. Setup Device (Use GPU if available, else CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on: {device}")

    # 2. Prepare Data Transforms
    # Resize to fixed size and convert to Tensor (0-1 range)
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
    ])

    # 3. Load Dataset
    dataset = NoisyImageDataset(CLEAN_PATH, NOISY_PATH, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    print(f"Loaded {len(dataset)} image pairs.")

    # 4. Initialize Model, Loss, and Optimizer
    model = DenoisingAutoencoder().to(device)
    criterion = nn.MSELoss() # Measures Mean Squared Error
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 5. Training Loop
    for epoch in range(EPOCHS):
        total_loss = 0
        
        for noisy_imgs, clean_imgs in dataloader:
            # Move data to GPU/CPU
            noisy_imgs = noisy_imgs.to(device)
            clean_imgs = clean_imgs.to(device)
            
            # Forward Pass: Feed bad image to model
            outputs = model(noisy_imgs)
            
            # Calculate Loss: Compare Output vs Clean Image
            loss = criterion(outputs, clean_imgs)
            
            # Backward Pass: Update weights
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {avg_loss:.6f}")

    # 6. Save the Model
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    # Ensure dataset exists before running
    if not os.path.exists(CLEAN_PATH) or not os.path.exists(NOISY_PATH):
        print("Error: Dataset folders not found. Please run corruption.py first.")
    else:
        train()