import os
import cv2
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class NoisyImageDataset(Dataset):
    def __init__(self, clean_dir, noisy_dir, transform=None):
        self.clean_dir = clean_dir
        self.noisy_dir = noisy_dir
        self.transform = transform
        
        # Get list of filenames that exist in both folders
        self.image_files = []
        for f in os.listdir(clean_dir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                if os.path.exists(os.path.join(noisy_dir, f)):
                    self.image_files.append(f)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        
        # Paths
        clean_path = os.path.join(self.clean_dir, img_name)
        noisy_path = os.path.join(self.noisy_dir, img_name)
        
        # Read Images
        clean_img = cv2.imread(clean_path)
        noisy_img = cv2.imread(noisy_path)
        
        # If an image fails to load, randomly pick another one to prevent crashing
        if clean_img is None or noisy_img is None:
            import random
            return self.__getitem__(random.randint(0, len(self.image_files) - 1))
        
        # Convert BGR (OpenCV) to RGB
        clean_img = cv2.cvtColor(clean_img, cv2.COLOR_BGR2RGB)
        noisy_img = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2RGB)
        
        # Apply Transforms (Resize & Convert to Tensor)
        if self.transform:
            clean_img = self.transform(clean_img)
            noisy_img = self.transform(noisy_img)
            
        return noisy_img, clean_img