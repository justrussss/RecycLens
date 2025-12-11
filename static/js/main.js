/**
 * RecycLens - JavaScript functionality for image upload and classification
 */

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const classifyBtn = document.getElementById('classifyBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const resetBtn = document.getElementById('resetBtn');
const previewImage = document.getElementById('previewImage');
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

// Camera elements
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const startCameraBtn = document.getElementById('startCameraBtn');
const stopCameraBtn = document.getElementById('stopCameraBtn');
const captureBtn = document.getElementById('captureBtn');
const cameraVideo = document.getElementById('cameraVideo');
const cameraPreviewContainer = document.getElementById('cameraPreviewContainer');
const captureCanvas = document.getElementById('captureCanvas');

// Global variables
let selectedFile = null;
let cameraStream = null;

/**
 * Initialize event listeners
 */
function initEventListeners() {
    // Navigation toggle
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', toggleNavMenu);
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => closeNavMenu());
        });
    }

    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', handleTabSwitch);
    });

    // Camera controls
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', startCamera);
    }
    if (stopCameraBtn) {
        stopCameraBtn.addEventListener('click', stopCamera);
    }
    if (captureBtn) {
        captureBtn.addEventListener('click', capturePhoto);
    }

    if (uploadArea) {
        // Drag and drop events
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);

        // Click on upload area to trigger file input
        uploadArea.addEventListener('click', () => fileInput && fileInput.click());
    }

    // File input change
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }

    // Classify button
    if (classifyBtn) {
        classifyBtn.addEventListener('click', classifyImage);
    }

    // Reset button
    if (resetBtn) {
        resetBtn.addEventListener('click', resetForm);
    }
}

/**
 * Toggle navigation visibility on mobile
 */
function toggleNavMenu() {
    if (!navToggle || !navLinks) {
        return;
    }
    const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', (!isExpanded).toString());
    navLinks.classList.toggle('open');
}

/**
 * Close navigation menu (after selection)
 */
function closeNavMenu() {
    if (!navToggle || !navLinks) {
        return;
    }
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
}

/**
 * Handle drag over event
 */
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = 'var(--primary-dark)';
    uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.15)';
}

/**
 * Handle drag leave event
 */
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = 'var(--primary-color)';
    uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';
}

/**
 * Handle drop event
 */
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = 'var(--primary-color)';
    uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

/**
 * Handle file selection from input or drop
 */
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFiles(files);
    }
}

/**
 * Process selected files
 */
function handleFiles(files) {
    const file = files[0];

    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, BMP)');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File is too large. Maximum size is 16MB');
        return;
    }

    selectedFile = file;
    clearError();

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Enable classify button
    classifyBtn.disabled = false;

    // Update upload area text
    uploadArea.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <h3>Image Ready!</h3>
        <p>File: ${file.name}</p>
        <p class="file-info">${(file.size / 1024).toFixed(2)} KB</p>
    `;
}

/**
 * Classify the selected image
 */
async function classifyImage() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }

    // Create FormData and append file
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Show loading spinner
        showLoading();
        classifyBtn.disabled = true;

        // Send request to Flask backend
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Handle response
        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'Classification failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred during classification. Please try again.');
    } finally {
        hideLoading();
        classifyBtn.disabled = false;
    }
}

/**
 * Display classification results
 */
function displayResults(data) {
    // Hide upload section, show results
    resultsSection.style.display = 'block';
    uploadArea.parentElement.style.display = 'none';

    // Set plastic code
    const plasticCode = document.getElementById('plasticCode');
    plasticCode.textContent = data.prediction;

    // Set plastic name
    const plasticName = document.getElementById('plasticName');
    plasticName.textContent = data.description;

    // Set confidence bar
    const confidenceFill = document.getElementById('confidenceFill');
    const confidencePercent = Math.round(data.confidence * 100);
    confidenceFill.style.width = confidencePercent + '%';

    // Set confidence text
    const confidenceText = document.getElementById('confidenceText');
    confidenceText.textContent = `Confidence: ${confidencePercent}%`;

    // Set description
    const description = document.getElementById('description');
    description.textContent = data.description;

    // Set recyclability
    const recyclability = document.getElementById('recyclability');
    const recyclableStatus = data.recyclable ? 'Recyclable ✓' : 'Not Recyclable ✗';
    const recyclableClass = data.recyclable ? 'recyclable' : 'not-recyclable';
    recyclability.innerHTML = `<span class="${recyclableClass}">${recyclableStatus}</span>`;

    // Set environmental impact
    const environmentalImpact = document.getElementById('environmentalImpact');
    environmentalImpact.textContent = data.environmental_impact;

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show loading spinner
 */
function showLoading() {
    loadingSpinner.style.display = 'flex';
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    loadingSpinner.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';

    // Auto-hide error after 5 seconds
    setTimeout(() => {
        clearError();
    }, 5000);
}

/**
 * Clear error message
 */
function clearError() {
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
}

/**
 * Reset form to initial state
 */
function resetForm() {
    // Reset variables
    selectedFile = null;

    // Reset file input
    fileInput.value = '';

    // Reset UI
    previewImage.src = '';
    classifyBtn.disabled = true;
    resultsSection.style.display = 'none';
    uploadArea.parentElement.style.display = 'block';

    // Reset upload area
    uploadArea.innerHTML = `
        <i class="fas fa-cloud-upload-alt"></i>
        <h3>Drag & Drop Your Image Here</h3>
        <p>or <label for="fileInput" class="link">click to select a file</label></p>
        <p class="file-info">Supported formats: PNG, JPG, JPEG, GIF, BMP (Max 16MB)</p>
    `;

    // Re-attach event listener to new label
    document.querySelector('label[for="fileInput"]').addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.click();
    });

    // Clear errors
    clearError();

    // Scroll to top
    document.querySelector('.upload-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Handle tab switching between upload methods
 */
function handleTabSwitch(e) {
    const tabName = e.currentTarget.getAttribute('data-tab');

    // Remove active class from all buttons and contents
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));

    // Add active class to clicked button and corresponding content
    e.currentTarget.classList.add('active');
    document.getElementById(tabName).classList.add('active');

    // Stop camera if switching away from camera tab
    if (tabName !== 'camera-capture' && cameraStream) {
        stopCamera();
    }
}

/**
 * Start camera capture
 */
async function startCamera() {
    try {
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' },
            audio: false
        });

        // Set video stream
        cameraVideo.srcObject = cameraStream;
        cameraVideo.play();

        // Show camera preview, hide start button
        cameraPreviewContainer.style.display = 'flex';
        startCameraBtn.style.display = 'none';

        clearError();
    } catch (error) {
        showError('Unable to access camera. Please check permissions or try a different device.');
        console.error('Camera error:', error);
    }
}

/**
 * Stop camera capture
 */
function stopCamera() {
    if (cameraStream) {
        // Stop all tracks
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    // Reset UI
    cameraPreviewContainer.style.display = 'none';
    startCameraBtn.style.display = 'block';
    cameraVideo.srcObject = null;
}

/**
 * Capture photo from camera
 */
function capturePhoto() {
    try {
        // Get canvas context
        const context = captureCanvas.getContext('2d');

        // Set canvas size to match video
        captureCanvas.width = cameraVideo.videoWidth;
        captureCanvas.height = cameraVideo.videoHeight;

        // Draw video frame to canvas
        context.drawImage(cameraVideo, 0, 0);

        // Convert canvas to blob and create file
        captureCanvas.toBlob((blob) => {
            // Create a File object
            const timestamp = new Date().getTime();
            const file = new File(
                [blob],
                `camera_capture_${timestamp}.jpg`,
                { type: 'image/jpeg' }
            );

            selectedFile = file;

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
            };
            reader.readAsDataURL(blob);

            // Enable classify button
            classifyBtn.disabled = false;

            // Stop camera
            stopCamera();

            // Switch to results section notification
            showError('Photo captured! Click "Classify Image" to analyze.', 'success');
            clearError();

            // Scroll to classify button
            classifyBtn.scrollIntoView({ behavior: 'smooth' });
        }, 'image/jpeg', 0.9);
    } catch (error) {
        showError('Failed to capture photo. Please try again.');
        console.error('Capture error:', error);
    }
}

/**
 * Initialize on document ready
 */
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
});
