# ✨ Clear-Vision: Image Denoising Autoencoder

Clear-Vision is a Deep Learning application designed to restore low-quality images. It uses a **Convolutional Autoencoder** with skip connections to remove Gaussian noise and blur from images, restoring them to clarity.

The project includes a full pipeline: a data corruption script to generate training data, a PyTorch training loop, and a user-friendly web interface built with Streamlit.

---

## 📂 Project Structure

```text
├── backend/               # Python server (optional separation)
├── frontend/              # Web platform assets
│   ├── index.html         # Main web page
│   ├── style.css          # UI Styling
│   └── app.js             # API interaction logic
├── server.py              # FastAPI server for inference
├── corrupt_image.py       # Script to generate noisy/blurred data from clean images
├── dataset.py             # Custom PyTorch Dataset loader
├── model.py               # Neural Network Architecture (Autoencoder)
├── train.py               # Training loop to save 'denoising_model.pth'
├── dataset/               # Folder containing image data
│   ├── clean_images/      # Place your original high-quality images here
│   └── corrupted_images/  # Generated automatically by corrupt_image.py
└── denoising_model.pth    # The trained model weights (generated after training)

Run the following command to install the required packages:
pip install torch torchvision opencv-python numpy pillow fastapi uvicorn python-multipart

Run the corruption script to generate the "bad" versions of these images:
python corrupt_image.py

Now, train the Neural Network to map the "Corrupted" images back to the "Clean" ones.
python train.py

### Launching the Web Platform

Once the model is trained, start the API server:
```bash
uvicorn server:app --reload
```

Then, simply open `frontend/index.html` in your favorite web browser (e.g. Chrome, Safari).
