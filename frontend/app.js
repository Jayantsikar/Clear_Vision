document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const imageInput = document.getElementById('imageInput');
    const restoreBtn = document.getElementById('restoreBtn');
    const resultsSection = document.getElementById('resultsSection');
    const originalPreview = document.getElementById('originalPreview');
    const restoredPreview = document.getElementById('restoredPreview');
    const loader = document.getElementById('loader');

    let selectedFile = null;

    // --- File Input Handlers ---
    
    // Click to upload
    dropZone.addEventListener('click', () => {
        imageInput.click();
    });

    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // --- Process File ---
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (JPG/PNG).');
            return;
        }

        selectedFile = file;
        
        // Show original preview
        const reader = new FileReader();
        reader.onload = (e) => {
            originalPreview.src = e.target.result;
            resultsSection.style.display = 'flex';
            restoredPreview.style.display = 'none'; // Hide old result
            restoreBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // --- API Request ---
    restoreBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI State: Loading
        restoreBtn.disabled = true;
        restoreBtn.textContent = 'Restoring...';
        loader.style.display = 'block';
        restoredPreview.style.display = 'none';

        // Prepare Data
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // ⚠️ DEPLOYMENT INSTRUCTIONS ⚠️
            // When hosting on Vercel, change this API_URL to your Render/Railway backend URL.
            // Example: const API_URL = 'https://clear-vision-api.onrender.com/api/restore';
            const API_URL = 'http://127.0.0.1:8000/api/restore';

            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Server error: ' + await response.text());
            }

            // Get image blob
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);

            // Display Restored Image
            restoredPreview.src = imageUrl;
            restoredPreview.style.display = 'block';
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during restoration. Please check the server logs.');
        } finally {
            // UI State: Done
            loader.style.display = 'none';
            restoreBtn.textContent = 'Restore Image ✨';
            restoreBtn.disabled = false;
        }
    });
});
