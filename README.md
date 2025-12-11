# RecycLens - Plastic Waste Sorting Web Application

## Overview

RecycLens is an AI-powered web application for classifying plastic waste images using machine learning. It helps users identify different plastic types, understand their environmental impact, and make informed recycling decisions.

**Current Status**: The app runs with a placeholder classification model. Ready for integration with your trained TensorFlow/Keras model.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [Usage](#usage)
7. [Model Integration Guide](#model-integration-guide)
8. [API Endpoints](#api-endpoints)
9. [Dataset Resources](#dataset-resources)
10. [Environmental Impact](#environmental-impact)
11. [Troubleshooting](#troubleshooting)
12. [Future Enhancements](#future-enhancements)

---

## Features

### Current Implementation
- ✅ **Image Upload**: Drag & drop or click to upload plastic waste images
- ✅ **Real-time Classification**: Instant plastic type identification
- ✅ **Confidence Scores**: Visual confidence metrics for predictions
- ✅ **Recyclability Info**: Clear recyclability status for each plastic type
- ✅ **Environmental Impact**: Detailed information about decomposition and recycling
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile devices
- ✅ **Placeholder Model**: Ready for real model integration

### Supported Plastic Types
- **PET (Type 1)**: Beverage bottles, food containers
- **HDPE (Type 2)**: Milk bottles, detergent containers
- **PVC (Type 3)**: Pipes, vinyl siding
- **LDPE (Type 4)**: Plastic wrap, squeeze bottles
- **PP (Type 5)**: Yogurt containers, bottle caps
- **PS (Type 6)**: Foam cups, takeout containers
- **Other (Type 7)**: Mixed plastic materials

---

## Project Structure

```
RecycLens/
├── app.py                          # Flask application main file
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── models/
│   ├── classifier.py              # Placeholder classifier with integration guide
│   └── plastic_classifier.h5      # (Optional) Trained Keras model
│
├── templates/
│   ├── index.html                 # Home page with upload and results
│   └── about.html                 # About and documentation page
│
├── static/
│   ├── css/
│   │   └── style.css              # Main stylesheet (responsive design)
│   ├── js/
│   │   └── main.js                # Frontend JavaScript functionality
│   └── uploads/
│       └── (uploaded images stored here)
│
└── datasets/
    └── (Optional) Plastic waste image datasets
```

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- A modern web browser (Chrome, Firefox, Edge, Safari)
- **Git** (optional, for cloning the repository)

---

## Installation

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/RecycLens.git
cd RecycLens
```

Or download the ZIP file and extract it.

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies included:**
- Flask: Web framework
- Pillow: Image processing
- NumPy: Numerical computing
- Werkzeug: Utilities for WSGI applications
- TensorFlow/Keras: (Optional, for model integration)

---

## Running the Application

### Start the Flask Development Server

```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

### Access the Web Application

Open your browser and navigate to:
```
http://localhost:5000
```

### Stop the Server

Press `Ctrl+C` in the terminal.

---

## Usage

### Basic Workflow

1. **Upload an Image**
   - Drag and drop an image onto the upload area
   - Or click to browse and select an image
   - Supported formats: PNG, JPG, JPEG, GIF, BMP
   - Maximum file size: 16MB

2. **Classify the Image**
   - Click the "Classify Image" button
   - Wait for the analysis to complete (1-2 seconds with placeholder model)

3. **View Results**
   - See the predicted plastic type
   - Check confidence score
   - Review recyclability status
   - Read environmental impact information

4. **Take Action**
   - Use the recycling guidance to sort your plastic
   - Share the information to educate others

### Example Images for Testing

You can find test images of plastic waste from:
- **TrashNet Dataset**: https://github.com/garythung/trashnet
- **Kaggle Plastic Datasets**: https://www.kaggle.com/datasets (search "plastic waste")

---

## Model Integration Guide

### Current State

The application currently uses a **placeholder classifier** that returns dummy predictions based on image brightness. This is intentional—it allows you to test the full web application workflow before your ML model is ready.

### Step 1: Prepare Your Model

Train a deep learning model on plastic waste images:

```python
import tensorflow as tf
from tensorflow import keras

# Build your model (example: simple CNN)
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(7, activation='softmax')  # 7 plastic types
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train your model
history = model.fit(train_data, train_labels, epochs=50, validation_data=(val_data, val_labels))

# Save the model
model.save('models/plastic_classifier.h5')
```

### Step 2: Update the Classifier

Edit `models/classifier.py` to replace the placeholder with your trained model:

```python
import tensorflow as tf

class PlasticClassifier:
    def __init__(self):
        # Load your trained model
        self.model = tf.keras.models.load_model('models/plastic_classifier.h5')
        self.class_labels = ['PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS', 'Other']
        print("Model loaded successfully!")
    
    def predict(self, image_array):
        # Add batch dimension
        input_array = np.expand_dims(image_array, axis=0)
        
        # Make prediction
        predictions = self.model.predict(input_array)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        class_name = self.class_labels[class_idx]
        
        # Get plastic info
        plastic_info = self.PLASTIC_TYPES[class_name].copy()
        
        return {
            'class': class_name,
            'name': plastic_info['name'],
            'confidence': round(confidence, 4),
            'description': plastic_info['description'],
            'environmental_impact': plastic_info['environmental_impact'],
            'recyclable': plastic_info['recyclable'],
            'recycle_code': plastic_info['recycle_code'],
            'common_uses': plastic_info['common_uses']
        }
```

### Step 3: Install TensorFlow (if not already installed)

```bash
pip install tensorflow
```

### Step 4: Test Your Model

```bash
python app.py
```

Upload test images and verify classifications are working correctly.

### Step 5: Optimize for Production

For deployment, consider:
- Using `model.save('models/plastic_classifier.tflite')` for TFLite models (faster inference)
- Implementing batch processing for multiple images
- Adding GPU support if available
- Setting up model caching for faster predictions

---

## API Endpoints

### 1. **GET `/`**
- **Description**: Render the home page
- **Response**: HTML page with upload interface

### 2. **POST `/classify`**
- **Description**: Classify an uploaded image
- **Request Body**: `multipart/form-data` with file upload
- **Response**:
```json
{
    "success": true,
    "filename": "20250203_151045_plastic.jpg",
    "filepath": "/static/uploads/20250203_151045_plastic.jpg",
    "prediction": "PET",
    "confidence": 0.87,
    "description": "Type 1 plastic, commonly used for drinks and food packaging.",
    "environmental_impact": "Takes 450+ years to decompose...",
    "recyclable": true
}
```

### 3. **GET `/about`**
- **Description**: Render the about page
- **Response**: HTML page with documentation

### 4. **GET `/health`**
- **Description**: Health check endpoint
- **Response**:
```json
{
    "status": "healthy",
    "app": "RecycLens"
}
```

---

## Dataset Resources

### TrashNet Dataset
- **Source**: https://github.com/garythung/trashnet
- **Contents**: 2,527 images across 6 categories (glass, paper, cardboard, plastic, metal, trash)
- **Format**: JPG images, ~500x500 pixels
- **License**: Open Source

### Kaggle Plastic Waste Datasets
- **Plastic Waste Classification**: https://www.kaggle.com/datasets/piatetradiashvili/plastic-waste-classification
- **Garbage Segregation**: https://www.kaggle.com/datasets/samkshan/garbage-segregation
- **Trash Images**: https://www.kaggle.com/datasets/brsdincer/garbage-classification

### Using Datasets Locally

1. **Download datasets** from the sources above
2. **Extract to `datasets/` folder**:
   ```
   datasets/
   ├── trashnet/
   ├── kaggle_plastic/
   └── custom_images/
   ```

3. **Create a preprocessing script** (`preprocess_datasets.py`):
```python
import os
import cv2
import numpy as np
from sklearn.train_test_split import train_test_split

# Load and normalize images
def load_dataset(data_path, target_size=(224, 224)):
    images, labels = [], []
    
    for label, category in enumerate(['PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS', 'Other']):
        category_path = os.path.join(data_path, category)
        for img_name in os.listdir(category_path):
            img = cv2.imread(os.path.join(category_path, img_name))
            img = cv2.resize(img, target_size)
            img = img / 255.0  # Normalize
            images.append(img)
            labels.append(label)
    
    return np.array(images), np.array(labels)

# Data augmentation example
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)
```

---

## Environmental Impact

### How Automated Sorting Helps

**1. Reduce Contamination**
- Manual sorting errors contaminate recycling streams
- Automated sorting achieves 95%+ accuracy
- Cleaner materials → higher quality recycled products

**2. Improve Efficiency**
- Faster processing (100+ items/minute vs 10-20 manual)
- Lower labor costs
- Increased facility throughput

**3. Enable Circular Economy**
- Better sorted plastics = wider reuse applications
- High-quality HDPE recycled into food containers
- PET bottles reused for fiber and new bottles

**4. Reduce Environmental Burden**
- Each ton of properly recycled plastic saves 5-6 tons of CO2
- Prevents 450+ years of landfill decomposition
- Protects marine ecosystems from ocean plastic

### Decomposition Timeline
- PET, HDPE, PVC, LDPE: **400-450 years**
- PP: **20-30 years**
- PS: **500+ years**

---

## Troubleshooting

### Problem: Port 5000 is Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or use a different port in app.py
app.run(host='127.0.0.1', port=5001)
```

### Problem: "ModuleNotFoundError: No module named 'flask'"
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Problem: Images Not Uploading
- Check file format (PNG, JPG, JPEG, GIF, BMP)
- Verify file size is under 16MB
- Check browser console for JavaScript errors (F12)
- Ensure `static/uploads/` directory exists and is writable

### Problem: Model Not Loading
```bash
# Verify model file exists
ls models/plastic_classifier.h5

# Install TensorFlow if missing
pip install tensorflow

# Check model compatibility
python -c "import tensorflow as tf; model = tf.keras.models.load_model('models/plastic_classifier.h5')"
```

### Problem: CORS Issues in Production
Add CORS headers to `app.py`:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

---

## Future Enhancements

### Short Term
- [ ] Batch image processing
- [ ] Image history/previous classifications
- [ ] Export results as PDF report
- [ ] Multi-language support

### Medium Term
- [ ] Real-time camera/webcam support
- [ ] Mobile app (React Native/Flutter)
- [ ] Community dataset contributions
- [ ] Advanced statistics dashboard

### Long Term
- [ ] Edge deployment (on-device inference)
- [ ] Integration with recycling facilities
- [ ] Blockchain for waste tracking
- [ ] AR visualization of plastic decomposition

---

## File Manifest

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with routes and error handling |
| `models/classifier.py` | Placeholder and production classifier implementation |
| `templates/index.html` | Home page with upload interface |
| `templates/about.html` | About page and documentation |
| `static/css/style.css` | Responsive styling (mobile-first design) |
| `static/js/main.js` | Frontend logic (upload, drag-drop, form handling) |
| `static/uploads/` | Directory for uploaded images |
| `datasets/` | Directory for training datasets |
| `requirements.txt` | Python package dependencies |

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@recyclelens.app
- Documentation: https://recyclelens.app/docs

---

## Acknowledgments

- **TrashNet Dataset**: Gary Thung, Mindy Renfro
- **Kaggle Community**: For plastic waste datasets
- **Flask Community**: For the excellent web framework
- **TensorFlow Team**: For deep learning tools

---

## Changelog

### v1.0.0 (2025-03-05)
- Initial release
- Placeholder classifier implementation
- Full web interface with upload and results display
- Responsive design for all devices
- Documentation and integration guide

---

**Last Updated**: March 5, 2025

For the latest updates, visit: https://github.com/yourusername/RecycLens
