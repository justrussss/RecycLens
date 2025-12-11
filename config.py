# RecycLens Configuration

## Application Settings

# Flask
DEBUG = True
SECRET_KEY = 'your-secret-key-change-in-production'
JSON_SORT_KEYS = False

# Upload Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Model Configuration
MODEL_PATH = 'models/plastic_classifier.h5'
MODEL_INPUT_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.5

# Server Configuration
HOST = '127.0.0.1'
PORT = 5000
WORKERS = 4
