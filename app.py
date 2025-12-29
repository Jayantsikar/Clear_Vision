import streamlit as st
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from model import DenoisingAutoencoder  # Importing your model structure

# --- Configuration ---
MODEL_PATH = "denoising_model.pth"
IMAGE_SIZE = 128  # Must match the size used in training

# --- 1. Load the Model ---
@st.cache_resource  # Caches the model so it doesn't reload on every click
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Initialize the architecture
    model = DenoisingAutoencoder().to(device)
    
    # Load the trained weights
    # map_location ensures it works even if you trained on GPU but run on CPU
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(MODEL_PATH))
    else:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
        
    model.eval()  # Set to evaluation mode (turns off training specific layers)
    return model, device

# --- 2. Image Processing Helper ---
def process_image(image_file, device):
    # Open image
    img = Image.open(image_file).convert("RGB")
    
    # Transform: Resize -> ToTensor
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
    ])
    
    # Prepare for model: Add batch dimension (1, 3, 128, 128)
    input_tensor = transform(img).unsqueeze(0).to(device)
    
    return input_tensor, img

# --- 3. The Streamlit UI ---
def main():
    st.set_page_config(page_title="Clear-Vision", page_icon="✨")
    
    st.title("✨ Clear-Vision: Image Restoration")
    st.write("Upload a noisy or blurry image, and the AI will attempt to restore it.")

    # Sidebar for extra info
    with st.sidebar:
        st.header("About")
        st.write("This project uses a **Convolutional Autoencoder** to remove noise and restore image quality.")
        st.write("Built with PyTorch & Streamlit.")

    # Load Model
    try:
        model, device = load_model()
        st.success("System Ready: Model Loaded Successfully!")
    except FileNotFoundError:
        st.error(f"Error: '{MODEL_PATH}' not found. Please run 'train.py' first!")
        return

    # File Uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Layout: Two columns (Input vs Output)
        col1, col2 = st.columns(2)

        # Process Input
        input_tensor, original_pil = process_image(uploaded_file, device)

        with col1:
            st.subheader("Original Input")
            st.image(original_pil, use_column_width=True)

        # Run Inference (Prediction)
        if st.button("Restore Image ✨"):
            with st.spinner("Restoring..."):
                with torch.no_grad():
                    output_tensor = model(input_tensor)
                
                # Convert output back to Image
                output_tensor = output_tensor.squeeze(0).cpu() # Remove batch dim
                restored_img = transforms.ToPILImage()(output_tensor)
            
            with col2:
                st.subheader("Restored Output")
                st.image(restored_img, use_column_width=True)
                
            # Optional: Add download button for result
            # st.download_button("Download Result", data=...)

if __name__ == "__main__":
    main()