# Quick Start Guide - RecycLens

## 5-Minute Setup

### Windows

```powershell
# 1. Navigate to project directory
cd C:\Users\russ\Desktop\RecycLens

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install Flask Pillow numpy werkzeug

# 5. Run the application
python app.py

# 6. Open browser
# Visit: http://localhost:5000
```

### macOS/Linux

```bash
# 1. Navigate to project directory
cd ~/Desktop/RecycLens

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install Flask Pillow numpy werkzeug

# 5. Run the application
python app.py

# 6. Open browser
# Visit: http://localhost:5000
```

---

## Testing the Application

1. **Start the server**: Run `python app.py`
2. **Open your browser**: Go to `http://localhost:5000`
3. **Upload a test image**:
   - Drag and drop an image, or
   - Click to select from your computer
4. **View results**: See the predicted plastic type and information

---

## Project Structure Overview

```
RecycLens/
├── app.py                    ← Main Flask application
├── config.py                 ← Configuration settings
├── train_model.py           ← Model training script
├── requirements.txt         ← Python dependencies
├── README.md                ← Full documentation
├── QUICKSTART.md            ← This file
│
├── models/
│   ├── __init__.py
│   ├── classifier.py        ← Classifier implementation
│   └── plastic_classifier.h5 (generated after training)
│
├── templates/
│   ├── index.html           ← Home page
│   └── about.html           ← About page
│
└── static/
    ├── css/
    │   └── style.css        ← Styling
    ├── js/
    │   └── main.js          ← Frontend logic
    └── uploads/             ← Uploaded images
```

---

## Integrating Your Trained Model

### Step 1: Train Your Model
Use `train_model.py` as a reference or use your own training script.

### Step 2: Save the Model
```python
model.save('models/plastic_classifier.h5')
```

### Step 3: Update `models/classifier.py`
Replace the placeholder `predict()` method with:
```python
def predict(self, image_array):
    import tensorflow as tf
    predictions = self.model.predict(np.expand_dims(image_array, axis=0))
    class_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][class_idx])
    class_name = self.class_labels[class_idx]
    # ... return results
```

### Step 4: Test the Integration
```bash
python app.py
```

---

## Troubleshooting

**Port already in use?**
```bash
# Change port in app.py line:
app.run(host='127.0.0.1', port=5001)
```

**Module not found?**
```bash
# Make sure venv is activated:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies:
pip install -r requirements.txt
```

**Images not uploading?**
- Check file format (PNG, JPG, JPEG, GIF, BMP)
- Ensure file size < 16MB
- Try a different browser
- Check browser console (F12) for errors

---

## Next Steps

1. ✅ **Run the app** with placeholder model
2. 📊 **Prepare your dataset** (TrashNet or Kaggle)
3. 🤖 **Train your model** using `train_model.py`
4. 🔄 **Integrate trained model** into `models/classifier.py`
5. 🚀 **Deploy to production** (optional)

---

## Resources

- **Datasets**: https://github.com/garythung/trashnet
- **Kaggle**: https://www.kaggle.com/datasets (search "plastic waste")
- **TensorFlow Docs**: https://www.tensorflow.org/guide
- **Flask Docs**: https://flask.palletsprojects.com

---

For full documentation, see `README.md`
