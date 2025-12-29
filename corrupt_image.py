import cv2
import numpy as np
import os
import random

def add_gaussian_noise(image, mean=0, sigma=25):
    """
    Adds Gaussian noise to an image.
    Args:
        image: Source image (numpy array).
        mean: Mean of the Gaussian noise.
        sigma: Standard deviation (higher = more noise).
    Returns:
        Noisy image.
    """
    # Generate Gaussian noise
    gauss = np.random.normal(mean, sigma, image.shape)

    # Add noise to the image
    noisy_image = image + gauss

    # Clip values to stay between 0 and 255 (valid pixel range)
    noisy_image = np.clip(noisy_image, 0, 255)

    # Convert back to uint8 format for image saving
    return noisy_image.astype(np.uint8)

def add_blur(image, kernel_size=(15, 15)):
    """
    Adds Gaussian Blur to an image.
    Args:
        image: Source image.
        kernel_size: Tuple (width, height). Must be odd numbers.
    Returns:
        Blurred image.
    """
    return cv2.GaussianBlur(image, kernel_size, 0)

def process_dataset(source_folder, dest_folder, mode='noise'):
    """
    Reads images from source_folder, applies corruption,
    and saves them to dest_folder.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # List all files in the source folder
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    print(f"Processing {len(files)} images...")

    for filename in files:
        # 1. Read the clean image
        img_path = os.path.join(source_folder, filename)
        image = cv2.imread(img_path)

        if image is None:
            continue

        # 2. Apply Corruption
        if mode == 'noise':
            corrupted_img = add_gaussian_noise(image)
        elif mode == 'blur':
            # Randomize blur intensity for variety
            k = random.choice([5, 9, 15])
            corrupted_img = add_blur(image, kernel_size=(k, k))
        elif mode == 'mixed':
            # Randomly apply either noise or blur
            if random.random() > 0.5:
                corrupted_img = add_gaussian_noise(image)
            else:
                k = random.choice([5, 9, 15])
                corrupted_img = add_blur(image, kernel_size=(k, k))

        # 3. Save the corrupted image (Bad_Image)
        save_path = os.path.join(dest_folder, filename)
        cv2.imwrite(save_path, corrupted_img)

    print(f"Done! Corrupted images saved to: {dest_folder}")

# --- CONFIGURATION ---
if __name__ == "__main__":
    # Create these folders manually or let the script do it
    # 'clean_images' should contain your original dataset
    CLEAN_PATH = "dataset/clean_images"
    CORRUPTED_PATH = "dataset/corrupted_images"

    # Create dummy folder for testing if it doesn't exist
    if not os.path.exists(CLEAN_PATH):
        os.makedirs(CLEAN_PATH)
        print(f"Please put some images in '{CLEAN_PATH}' and run again.")
    else:
        # Run the corruption
        # Options: 'noise', 'blur', or 'mixed'
        process_dataset(CLEAN_PATH, CORRUPTED_PATH, mode='mixed')