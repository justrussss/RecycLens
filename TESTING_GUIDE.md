# RecycLens - Testing Guide

## Testing the Application

### Quick Test (2 minutes)

1. **Start the app**:
   ```powershell
   python app.py
   ```

2. **Open browser**:
   ```
   http://localhost:5000
   ```

3. **Upload a test image**:
   - Any image file works (photos, screenshots, etc.)
   - The placeholder classifier will return predictions based on image brightness

4. **View results**:
   - Plastic type (PET, HDPE, PVC, LDPE, PP, PS, or Other)
   - Confidence score (0.75-0.95 with placeholder)
   - Recyclability status
   - Environmental information

---

## Testing Checklist

### Functionality Tests

- [ ] **Upload Page**
  - [ ] Drag and drop upload works
  - [ ] Click-to-select works
  - [ ] File preview shows correctly
  - [ ] Classify button enables after upload

- [ ] **Classification**
  - [ ] Placeholder classifier returns predictions
  - [ ] Confidence bar displays correctly
  - [ ] Recyclability shows (✓ or ✗)
  - [ ] Environmental impact displays

- [ ] **Results Display**
  - [ ] Image preview shows uploaded image
  - [ ] Plastic type displays with code
  - [ ] Confidence percentage shown
  - [ ] Description accurate
  - [ ] Results section scrolls into view

- [ ] **Reset Functionality**
  - [ ] Reset button clears results
  - [ ] Upload area resets to initial state
  - [ ] Can upload new image after reset

- [ ] **Navigation**
  - [ ] Home link works
  - [ ] About link works
  - [ ] Navbar visible on all pages

### Error Handling Tests

- [ ] **Invalid File Upload**
  - Try uploading: `.txt`, `.pdf`, `.zip`
  - Should show error message

- [ ] **Large File Upload**
  - Try uploading file > 16MB
  - Should show size limit error

- [ ] **Drag and Drop**
  - Drag non-image file
  - Should show format error

### Responsive Design Tests

- [ ] **Desktop** (1920x1080)
  - All elements visible
  - Layout looks good

- [ ] **Tablet** (768x1024)
  - Single column layout for results
  - Navigation adjusts

- [ ] **Mobile** (375x667)
  - Text readable
  - Upload area clickable
  - Results display correctly
  - No horizontal scrolling

---

## File Upload Tests

### Valid Files (Should Work)
```
✅ photo.jpg          - JPEG image
✅ waste.png          - PNG image
✅ plastic.gif        - GIF image
✅ bottle.bmp         - BMP image
✅ screenshot.jpeg    - JPEG image
```

### Invalid Files (Should Show Error)
```
❌ document.pdf       - Wrong format
❌ data.csv           - Wrong format
❌ music.mp3          - Wrong format
❌ archive.zip        - Wrong format
❌ image.jpg.exe      - Suspicious file
```

### Large Files (Should Show Error)
```
❌ huge_image.jpg (20MB)  - Exceeds 16MB limit
```

---

## Browser Compatibility Tests

Test in these browsers:

- [ ] **Google Chrome** (Recommended)
- [ ] **Firefox**
- [ ] **Microsoft Edge**
- [ ] **Safari** (if on Mac)

All should work identically.

---

## Placeholder Classifier Behavior

The placeholder classifier returns predictions based on **image brightness**:

| Image Brightness | Prediction | Confidence |
|-----------------|-----------|-----------|
| Very Dark       | PS (Type 6) | ~75-95% |
| Dark            | PVC (Type 3) | ~75-95% |
| Medium Dark     | LDPE (Type 4) | ~75-95% |
| Medium          | HDPE (Type 2) | ~75-95% |
| Bright          | PET (Type 1) | ~75-95% |
| Very Bright     | PP (Type 5) | ~75-95% |

**This is normal!** The placeholder uses image properties to simulate different predictions. When you integrate your trained model, predictions will be based on actual plastic features.

---

## Loading Time Expectations

| Action | Expected Time |
|--------|---------------|
| Page load | < 1 second |
| Image upload | < 2 seconds |
| Classification | 1-2 seconds (placeholder) |
| Page navigation | < 1 second |

With your trained model, classification time may increase to 2-5 seconds depending on model complexity.

---

## Visual Elements to Verify

### Home Page
- [ ] Green gradient header with title
- [ ] Upload area with dashed border
- [ ] "Drag & Drop" instructions clear
- [ ] File format info visible
- [ ] Classify button disabled initially
- [ ] Info cards at bottom with icons
- [ ] Footer with links

### Results Page
- [ ] Image preview on left (or top on mobile)
- [ ] Results cards on right (or bottom on mobile)
- [ ] Plastic type with code circle
- [ ] Confidence bar fills correctly
- [ ] Recyclability status with check/cross icon
- [ ] Reset button at bottom

### About Page
- [ ] Plastic types table displays
- [ ] Codes and recyclability shown
- [ ] Steps grid visible
- [ ] Technology stack listed
- [ ] Environmental impact info readable

---

## Performance Tests

### Measurement

1. **Open DevTools** (F12)
2. **Go to Network tab**
3. **Reload page**
4. **Upload image**
5. **Check metrics**:
   - **Initial page load**: < 2 seconds
   - **Image upload**: < 2 seconds
   - **Classification**: 1-2 seconds
   - **Total request**: < 5 seconds

### Acceptable Performance
- ✅ Home page loads in < 1 second
- ✅ Styles fully applied (no flash)
- ✅ Images load correctly
- ✅ Smooth animations (60 FPS)

---

## Database/Storage Tests

### Upload Directory
- Verify `static/uploads/` exists
- Uploaded images saved with timestamp
- Old uploads don't interfere with new ones
- Images display correctly from storage path

### Configuration Tests
- Change `MAX_CONTENT_LENGTH` in `app.py`
- Change `UPLOAD_FOLDER` path
- Change `ALLOWED_EXTENSIONS`
- Verify changes take effect

---

## API Response Tests

### Health Check Endpoint
```bash
curl http://localhost:5000/health
```

**Expected Response**:
```json
{"status": "healthy", "app": "RecycLens"}
```

### Classification Endpoint
Upload a file via form:
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/classify
```

**Expected Response**:
```json
{
    "success": true,
    "filename": "20250203_151045_image.jpg",
    "prediction": "PET",
    "confidence": 0.87,
    "description": "Type 1 plastic...",
    "environmental_impact": "Takes 450+ years...",
    "recyclable": true
}
```

---

## Common Test Scenarios

### Scenario 1: First Time User
1. Opens app
2. Sees home page
3. Drags image onto upload area
4. Clicks Classify
5. Views results
6. Clicks About for more info

✅ **Expected**: Everything works smoothly

### Scenario 2: Upload Error
1. Tries to upload `.txt` file
2. Sees error message
3. Message auto-hides after 5 seconds
4. Can retry with valid file

✅ **Expected**: Error handled gracefully

### Scenario 3: Reset After Classification
1. Uploads image and classifies
2. Clicks Reset button
3. Upload area resets
4. Can upload new image immediately

✅ **Expected**: Full reset works correctly

### Scenario 4: Mobile User
1. Opens app on phone
2. Sees mobile-optimized layout
3. Can tap upload area
4. Can view results in single column
5. Navigation works on mobile

✅ **Expected**: Fully responsive design

---

## Automated Testing (Optional)

Create `test_app.py`:
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'RecycLens' in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_invalid_file_upload(client):
    response = client.post('/classify', data={})
    assert response.status_code == 400

# Run tests: pytest test_app.py
```

---

## Issue Reporting

If you find a problem:

1. **Note the steps** to reproduce
2. **Check the console** (F12 for browser, terminal for server)
3. **Copy error messages**
4. **Check README.md** Troubleshooting section
5. **Open an issue** on GitHub with details

---

## Success Indicators

Your app is working correctly if:

- ✅ Loads without errors
- ✅ Accepts image uploads
- ✅ Displays predictions
- ✅ Shows results clearly
- ✅ Handles errors gracefully
- ✅ Works on mobile
- ✅ Responsive to interactions
- ✅ About page has information

---

**Ready to test? Start with `python app.py` and visit `http://localhost:5000`!**
