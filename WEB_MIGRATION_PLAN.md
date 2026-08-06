# Web Platform Migration Plan

We are going to migrate the Clear-Vision user interface from Streamlit to a custom, modern web platform using HTML, CSS, JavaScript, and a Python backend API.

## Proposed Flow

1. **Frontend (User Interface)**: The user visits a beautiful, responsive web page (`index.html`) featuring modern design aesthetics (glassmorphism, animations).
2. **Interaction (JavaScript)**: The user selects a corrupted image. `script.js` handles the file selection and instantly shows a preview of the image.
3. **API Request**: When the user clicks "Restore Image", `script.js` sends the image file via an HTTP POST request to our local Python server.
4. **Backend (FastAPI/Flask)**: A lightweight Python web server (`server.py`) receives the image.
5. **Inference**: The server runs the image through the PyTorch `DenoisingAutoencoder` (reusing the logic from `app.py`).
6. **Response**: The server sends the restored image back to the frontend.
7. **Display**: The JavaScript receives the restored image and dynamically updates the UI to show the final result side-by-side with the original.

## Proposed File Structure

```text
clear-vision/
├── frontend/                 [NEW]
│   ├── index.html            [NEW] - Main web page
│   ├── style.css             [NEW] - Premium styling and animations
│   └── app.js                [NEW] - Logic for uploading and fetching results
├── server.py                 [NEW] - FastAPI/Flask backend
├── model.py                  [UNCHANGED]
├── train.py                  [UNCHANGED]
├── dataset.py                [UNCHANGED]
├── corrupt_image.py          [UNCHANGED]
├── denoising_model.pth       [UNCHANGED]
└── WEB_MIGRATION_PLAN.md     [NEW] - This document
```
