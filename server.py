import io
import torch
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image
from torchvision import transforms
from model import DenoisingAutoencoder
import logging

app = FastAPI(title="Clear-Vision API")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "denoising_model.pth"
IMAGE_SIZE = 128

# Set up device for Mac support (mps) if available
device = torch.device("mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu"))
logging.info(f"Using device: {device}")

# Load model globally when server starts
model = DenoisingAutoencoder().to(device)
try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}. Please ensure you have run train.py")

@app.post("/api/restore")
async def restore_image(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess
        transform = transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
        ])
        input_tensor = transform(img).unsqueeze(0).to(device)
        
        # Inference
        with torch.no_grad():
            output_tensor = model(input_tensor)
            
        # Postprocess (convert tensor back to PIL Image)
        output_tensor = output_tensor.squeeze(0).cpu()
        restored_img = transforms.ToPILImage()(output_tensor)
        
        # Convert PIL Image back to bytes to send in response
        img_byte_arr = io.BytesIO()
        restored_img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return Response(content=img_byte_arr, media_type="image/jpeg")
        
    except Exception as e:
        return Response(content=f"Error processing image: {str(e)}", status_code=500)
