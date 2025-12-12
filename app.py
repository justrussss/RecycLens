"""
RecycLens - Plastic Waste Sorting Web Application
A Flask-based web app for classifying plastic waste images using machine learning.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from datetime import datetime

# Import the classifier
from models.classifier import PlasticClassifier

# Flask App Configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Enable CORS for frontend communication
try:
    from flask_cors import CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}, r"/classify": {"origins": "*"}})
except ImportError:
    pass

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the classifier (will load Keras model if available)
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'plastic_classifier_model.keras')
classifier = PlasticClassifier(model_path=MODEL_PATH)


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model input.
    
    Args:
        image_path: Path to the image file
        target_size: Target size for resizing (default: 224x224 for MobileNetV2)
    
    Returns:
        Preprocessed image array
    """
    try:
        # Open image
        img = Image.open(image_path).convert('RGB')
        
        # Resize image
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize
        img_array = np.array(img) / 255.0
        
        # Expand dimensions for batch processing
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        raise


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify_image():
    """
    Handle image upload and classification.
    
    Returns:
        JSON response with classification results
    """
    try:
        # Check if image was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP'}), 400
        
        # Save uploaded file
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Predict
        try:
            prediction = classifier.predict(filepath)
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Classification failed: {str(e)}'}), 500
        
        # Prepare response
        response = {
            'success': True,
            'filename': filename,
            'filepath': f"/{filepath}",
            'prediction': prediction['class'],
            'code': prediction['code'],
            'confidence': prediction['confidence'],
            'description': prediction['description'],
            'environmental_impact': prediction['environmental_impact'],
            'recyclable': prediction['recyclable']
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        print(f"Error during classification: {str(e)}")
        return jsonify({'error': f'Classification failed: {str(e)}'}), 500


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'app': 'RecycLens'}), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File is too large. Maximum size: 16MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development vs Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
