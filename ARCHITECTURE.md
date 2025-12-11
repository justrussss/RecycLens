# RecycLens - Application Architecture & Data Flow

## Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Frontend (HTML + CSS + JS)              │   │
│  │  - index.html (Upload Interface)                     │   │
│  │  - about.html (Information Page)                     │   │
│  │  - style.css (Responsive Design)                     │   │
│  │  - main.js (Event Handling)                          │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────┬───────────────────────────────────────────────┘
               │ HTTP Requests (JSON)
               │
┌──────────────┴───────────────────────────────────────────────┐
│                    FLASK SERVER (Python)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              app.py (Routes & Logic)                 │   │
│  │  ├─ GET / → index.html                              │   │
│  │  ├─ GET /about → about.html                         │   │
│  │  ├─ POST /classify → Process & Classify             │   │
│  │  ├─ GET /health → Health Check                      │   │
│  │  └─ Error Handlers (404, 413, 500)                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                        ↓                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Image Processing (Pillow + NumPy)            │   │
│  │  - Load Image → Resize (224x224) → Normalize        │   │
│  └──────────────────────────────────────────────────────┘   │
│                        ↓                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      ML Classifier (models/classifier.py)           │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │ Placeholder: Returns dummy predictions        │  │   │
│  │  │ (Based on image brightness)                   │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │ Production: Loads trained TensorFlow model    │  │   │
│  │  │ (After you train and integrate)               │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  Returns: Class, Confidence, Description, Impact    │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────┬───────────────────────────────────────────────┘
               │ JSON Response
               ↓
        Display Results
        Update UI with:
        - Plastic Type
        - Confidence Score
        - Recyclability
        - Environmental Info
```

---

## Image Upload & Classification Flow

```
USER UPLOADS IMAGE
     ↓
[Browser]
  - User drags image or clicks to select
  - File validation (JavaScript)
  - Image preview shown
     ↓
[POST /classify request]
  - Multipart form-data with image
  - Sent to Flask server
     ↓
[Flask - app.py]
  1. Validate file
     - Check extension (PNG, JPG, etc.)
     - Check file size (< 16MB)
  2. Save uploaded file
     - Generate timestamp filename
     - Save to static/uploads/
  3. Preprocess image
     - Load with Pillow
     - Resize to 224x224
     - Normalize to 0-1
  4. Classify image
     - Create PlasticClassifier instance
     - Call predict(image_array)
     - Get results dict
  5. Return JSON response
     ↓
[Browser JavaScript]
  - Parse JSON response
  - Display plastic type
  - Show confidence bar
  - List environmental impact
  - Update UI with results
     ↓
USER SEES RESULTS
```

---

## Data Structure: Classification Result

```
POST /classify Request
├── File: image.jpg (multipart/form-data)
└── Max Size: 16MB

↓

Response (JSON)
{
  "success": true,
  "filename": "20250305_120000_image.jpg",
  "filepath": "/static/uploads/20250305_120000_image.jpg",
  "prediction": "PET",
  "confidence": 0.8742,
  "description": "Type 1 plastic, commonly used for drinks...",
  "environmental_impact": "Takes 450+ years to decompose...",
  "recyclable": true,
  "name": "PET (Polyethylene Terephthalate)",
  "recycle_code": 1,
  "common_uses": "Beverage bottles, food containers"
}

↓

Display in Browser
┌─────────────────────────┐
│  Plastic Type: PET      │
│  Code: 1                │
│  Confidence: 87%        │
│  █████████░░░░░░░░░░░░  │
│  Recyclable: ✓ Yes      │
│  Impact: Takes 450+...  │
└─────────────────────────┘
```

---

## Directory Structure & File Relationships

```
RecycLens/
│
├── app.py ◄──────────────────┐
│   └── imports:             │
│       - Flask              │
│       - Pillow             │
│       - NumPy              │
│       - models/classifier  │
│
├── models/
│   ├── classifier.py ◄──────┤────── Imported by app.py
│   │   └── Contains:        │
│   │       - PlasticClassifier class
│   │       - PLASTIC_TYPES dict
│   │       - predict() method
│   │
│   └── plastic_classifier.h5 (YOUR MODEL)
│       └── Loaded by classifier.py
│
├── templates/
│   ├── index.html ◄─────────┤────── Served by app.py
│   │   └── References:
│   │       - style.css
│   │       - main.js
│   │
│   └── about.html ◄─────────┤────── Served by app.py
│       └── References:
│           - style.css
│
├── static/
│   ├── css/
│   │   └── style.css ◄──────┤────── Loaded by HTML
│   │       └── Styles all pages
│   │
│   ├── js/
│   │   └── main.js ◄────────┤────── Loaded by HTML
│   │       └── Handles:
│   │           - File upload
│   │           - API calls
│   │           - UI updates
│   │
│   └── uploads/
│       └── image files (stored here)
│
└── train_model.py
    └── Reference for training
        - Shows data loading
        - Shows model building
        - Shows training loop
```

---

## Supported Plastic Types

```
Classification Output:
┌──────────────────────────────────────────────────┐
│ Plastic Type Code                                │
├──────────────────────────────────────────────────┤
│ 1 = PET  (Polyethylene Terephthalate)  ♻ YES    │
│ 2 = HDPE (High-Density Polyethylene)   ♻ YES    │
│ 3 = PVC  (Polyvinyl Chloride)          ♻ NO     │
│ 4 = LDPE (Low-Density Polyethylene)    ♻ YES    │
│ 5 = PP   (Polypropylene)               ♻ YES    │
│ 6 = PS   (Polystyrene)                 ♻ NO     │
│ 7 = Other (Mixed/Unknown)              ♻ NO     │
└──────────────────────────────────────────────────┘
```

---

## Image Processing Pipeline

```
Raw Image File
    ↓
[Load with Pillow]
    - Open file
    - Ensure RGB format
    ↓
[Resize]
    - Convert to 224x224 pixels
    - Use high-quality resampling
    ↓
[Normalize]
    - Convert to NumPy array
    - Divide by 255 (scale 0-1)
    ↓
[Ready for Model]
    - Shape: (224, 224, 3)
    - Values: [0.0 to 1.0]
    - Type: numpy.ndarray
    ↓
[Send to Classifier]
    - predict(image_array)
    - Returns classification
    ↓
Result: Plastic Type + Confidence
```

---

## Request/Response Flow Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       │ 1. GET /
       ▼
    [Flask]
       │
       │ Return index.html
       │
       ▼
┌─────────────┐
│  Homepage   │
│  - Upload   │
│  - Info     │
└──────┬──────┘
       │
       │ 2. User uploads image (Drag/Drop)
       │
       │ 3. POST /classify
       ▼
    [Flask]
       │
       │ • Validate file
       │ • Save file
       │ • Preprocess
       │ • Classify
       │
       ├─ Success ─────┐
       │               │
       │               ▼
       │            [JSON Response]
       │            {
       │              "success": true,
       │              "prediction": "PET",
       │              "confidence": 0.87,
       │              ...
       │            }
       │               │
       │               │
       │ Failure ─┐    │
       │          │    │
       │          ▼    ▼
       │      [JSON]  [JSON]
       │      Error   Results
       │          │    │
       └──────────┴────┴─────┐
                             │
       ┌─────────────────────┘
       │
       ▼
┌─────────────┐
│  JavaScript │
│  - Parse    │
│  - Display  │
│  - Update   │
└─────────────┘
       │
       ▼
┌─────────────┐
│  Results    │
│  - Type     │
│  - Score    │
│  - Impact   │
└─────────────┘
```

---

## Classifier Decision Tree (Placeholder)

```
Input: Image Array
       (224x224x3, values 0-1)
       ↓
Calculate Mean Brightness
       ↓
   Is it < 0.2?  ─Yes─→ Predict: PS (Type 6)
       │
       No
       ↓
   Is it < 0.3?  ─Yes─→ Predict: PVC (Type 3)
       │
       No
       ↓
   Is it < 0.4?  ─Yes─→ Predict: LDPE (Type 4)
       │
       No
       ↓
   Is it < 0.5?  ─Yes─→ Predict: HDPE (Type 2)
       │
       No
       ↓
   Is it < 0.7?  ─Yes─→ Predict: PET (Type 1)
       │
       No
       ↓
       Predict: PP (Type 5)

Generate Random Confidence: 0.75-0.95
       ↓
Return: {
  "class": "PET",
  "confidence": 0.87,
  "description": "...",
  "environmental_impact": "...",
  "recyclable": True
}
```

---

## Production Model Integration

```
Current (Placeholder):
┌──────────────────┐
│ Image Array      │
└────────┬─────────┘
         │
         ▼
    [Dummy Logic]
    • Calculate brightness
    • Return fake prediction
         │
         ▼
    [Result Dict]


Future (Your Model):
┌──────────────────┐
│ Image Array      │
└────────┬─────────┘
         │
         ▼
    [Load Model]
    classifier.model = tf.keras.models.load_model(...)
         │
         ▼
    [Expand Dims]
    input = np.expand_dims(image_array, axis=0)
         │
         ▼
    [Predict]
    predictions = model.predict(input)
         │
         ▼
    [Extract Results]
    • class_idx = np.argmax(predictions[0])
    • confidence = predictions[0][class_idx]
    • class_name = self.class_labels[class_idx]
         │
         ▼
    [Result Dict]
    • class
    • confidence
    • description
    • environmental_impact
    • recyclable
```

---

## Environment Setup

```
System
  ↓
Python 3.8+
  ↓
Virtual Environment (venv)
  ├─ Flask 3.0.0
  ├─ Pillow 10.1.0
  ├─ NumPy 1.24.3
  ├─ Werkzeug 3.0.1
  └─ (Optional) TensorFlow 2.13.0
  ↓
RecycLens App ← Ready to run!
```

---

## Deployment Architecture (Optional)

```
For Local Development:
Browser ↔ Flask Dev Server (127.0.0.1:5000)

For Production:
┌──────────┐
│ Nginx    │ (Reverse Proxy)
└────┬─────┘
     │
     ▼
┌──────────────────────────────┐
│ Gunicorn                     │
│ - Multiple workers           │
│ - WSGI application server    │
└────────────┬─────────────────┘
             │
             ▼
        app.py
        (Flask Application)
```

---

## Security Architecture

```
User Input
    ↓
[Validation Layer]
    ├─ File type check
    ├─ File size limit
    ├─ Extension validation
    └─ Mime type check
    ↓
[Processing Layer]
    ├─ Secure filename generation
    ├─ Path traversal prevention
    └─ Isolated upload directory
    ↓
[Response Layer]
    ├─ No sensitive info in errors
    ├─ Rate limiting (ready)
    └─ CORS headers (ready)
    ↓
Safe Output
```

---

## Monitoring & Logging Points

```
Application Flow:
┌──────────────────┐
│ Request received │ ← Log: endpoint, method
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ File validation  │ ← Log: file size, extension
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Image processing │ ← Log: dimensions, normalization
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Classification   │ ← Log: prediction, confidence
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Response sent    │ ← Log: status code, response time
└──────────────────┘
```

---

**This architecture ensures:**
- Clear separation of concerns
- Easy to understand data flow
- Simple to integrate real model
- Production-ready code quality
- Comprehensive documentation
