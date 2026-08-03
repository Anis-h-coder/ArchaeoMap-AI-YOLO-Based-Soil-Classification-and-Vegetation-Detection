# 🌍 ArchaeoMap AI – YOLO-Based Soil Classification & Vegetation Detection

ArchaeoMap AI is an AI-powered geospatial analysis platform built using **Flask** and **YOLOv8** for automatic **soil classification**, **vegetation detection**, and **side-by-side aerial image comparison**. The platform helps researchers, archaeologists, environmental scientists, and agricultural professionals analyze drone or satellite imagery through computer vision.

---

## 🚀 Key Features

### 🌱 Vegetation Detection
- Detects vegetation from aerial and ground imagery
- YOLOv8-powered object detection
- Bounding boxes with confidence scores
- Segmentation mask generation
- Environmental visualization

---

### 🧱 Soil Classification
- Identifies multiple soil types
- Supports:
  - Red Soil
  - Black Soil
  - Clay Soil
  - Sandy Soil
- Optimized confidence threshold for low-contrast images
- Detection count and confidence metrics

---

### 📊 AI Comparison Engine
Compare two aerial images side-by-side.

The comparison includes:

- Detection count
- Confidence score
- Soil type
- Vegetation percentage
- Moisture estimation
- YOLO model used
- IoU threshold
- AI-generated comparison summary

---

### 📈 Detection Analytics Dashboard

Interactive dashboard displaying:

- Original image
- Detection output
- Segmentation mask
- Terrain visualization
- AI interpretation
- Performance metrics
- Downloadable PDF report

---

### 🎯 Smart Threshold Optimization

Automatically adjusts detection thresholds based on analysis type.

| Analysis | Confidence |
|-----------|-----------:|
| Vegetation | 0.50 |
| Soil | 0.30 |

This reduces false negatives for difficult soil images.

---

### 🖼️ Segmentation & Visualization

- Semi-transparent segmentation masks
- Bounding-box overlay
- Terrain edge visualization
- AI-highlighted regions

---

### 🌐 Modern Web Interface

- Responsive design
- Tailwind CSS
- Clean dashboard
- Interactive comparison reports
- User-friendly upload workflow

---

# 📸 Platform Preview & UI Showcase

### 1. AI-Powered Landing Experience

Modern homepage introducing ArchaeoMap AI with intelligent aerial image analysis.

<img width="1913" height="1079" alt="Screenshot 2026-08-03 143154" src="https://github.com/user-attachments/assets/bedbde30-8094-4b74-825a-28b2e79bc595" />

---

### 2. About the Platform

Overview of the platform, AI capabilities, vegetation analysis, soil recognition, and aerial vision technologies.

<img width="1901" height="1079" alt="Screenshot 2026-08-03 143208" src="https://github.com/user-attachments/assets/7875e6f0-5d01-405e-a776-69982af0228c" />

---

### 3. Image Analysis Workspace

Upload imagery, configure detection settings, and launch AI-powered analysis.

<img width="1919" height="1079" alt="Screenshot 2026-08-03 143239" src="https://github.com/user-attachments/assets/330e3ae1-1c3d-4e65-9ef3-60f206f0ed55" />

---

### 4. Detection Results & Environmental Insights

Displays detection outputs, segmentation masks, terrain visualization, and environmental metrics.

<img width="1159" height="831" alt="Screenshot 2026-08-03 143438" src="https://github.com/user-attachments/assets/aa0e3f5d-4ac8-432d-805d-c8843d1cc074" />

---

### 5. AI Comparison Report

Compare two aerial images with automated AI insights.

<img width="1891" height="1079" alt="Screenshot 2026-08-03 143555" src="https://github.com/user-attachments/assets/5ab5aca2-6a86-41fe-aa18-cd8e4c4f1f0c" />

---

### 6. Real-Time YOLO Detection Preview

Visualization of detected vegetation and soil regions with confidence scores.

<img width="1888" height="1079" alt="Screenshot 2026-08-03 143648" src="https://github.com/user-attachments/assets/1285a96e-2ead-4bb7-b097-98ab64967b5a" />

---

### 7. Analytics Dashboard

Comprehensive dashboard presenting AI interpretations, segmentation masks, performance metrics, and downloadable reports.

<img width="1521" height="1079" alt="Screenshot 2026-08-03 143721" src="https://github.com/user-attachments/assets/1b211094-8b1a-4971-ad50-d6562aeea4df" />


---

# 🏗️ Project Architecture

```
ArchaeoMapAI/
│
├── app.py
├── models/
│   ├── best.pt
│   └── soil_best.pt
│
├── static/
│   ├── uploads/
│   ├── results/
│   ├── css/
│   └── screenshots/
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── results.html
│   ├── compare.html
│   └── compare_result.html
│
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

## Backend

- Flask
- Python

## AI & Computer Vision

- YOLOv8 (Ultralytics)
- OpenCV
- Pillow

## Frontend

- HTML5
- Tailwind CSS
- JavaScript
- Jinja2 Templates

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ArchaeoMapAI.git

cd ArchaeoMapAI
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask pillow ultralytics
```

---

## 4. Add YOLO Models

Place the trained models inside the `models` directory.

```
models/
├── best.pt
└── soil_best.pt
```

---

# ▶️ Running the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 💻 Usage

## Image Analysis

1. Upload an image.
2. Choose:
   - Vegetation Detection
   - Soil Classification
3. Click **Analyze**.
4. View:
   - Detection output
   - Segmentation mask
   - Terrain visualization
   - AI summary

---

## Image Comparison

1. Upload two images.
2. Select the analysis mode.
3. Compare:

- Soil type
- Detection count
- Confidence scores
- Moisture level
- AI summary
- Model information

---

# 📊 AI Pipeline

```
Input Image
      │
      ▼
Image Upload
      │
      ▼
YOLOv8 Inference
      │
      ▼
Detection + Segmentation
      │
      ▼
Confidence Analysis
      │
      ▼
Comparison Engine
      │
      ▼
Dashboard & PDF Report
```

---

# 📦 Requirements

- Python 3.9+
- Flask
- Pillow
- OpenCV
- Ultralytics YOLOv8

---

# 🔧 Troubleshooting

### Soil type not displayed

Ensure the comparison dictionary includes:

```python
"soil_name_1": stats1["class_names"][0],
"soil_name_2": stats2["class_names"][0],
```

---

### No detections

Lower the confidence threshold:

```python
default_conf = 0.3 if kind == "soil" else 0.5
```

---

### Images appear stretched

Use:

```html
class="w-full h-80 object-cover rounded-xl"
```

---

# 🚀 Future Enhancements

- Satellite imagery support
- GIS integration
- Heatmap generation
- Change detection over time
- Multi-image comparison
- GeoJSON export
- PDF & Excel report generation
- Cloud deployment
- User authentication
- Historical analysis dashboard

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👩‍💻 Author

**Anish Fathima**

AI & Data Science Student

GitHub: https://github.com/Anis-h-coder

---

# ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.
