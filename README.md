ArchaeoMap AI – YOLO-Based Soil Classification and Vegetation Detection

ArchaeoMap AI is an intelligent visual analysis system built with Flask and YOLOv8 for automatic soil classification, vegetation detection, and side-by-side image comparison.
It is designed for use in agriculture, archaeology, environmental assessment, and Earth-surface analytics.

<div align="center"> <img src="static/screenshots/banner.png" width="800"> </div>
✅ Features
🌱 Vegetation Detection

Detects vegetation from aerial or ground photography.

Shows bounding boxes, confidence scores, and segmentation masks.

🧱 Soil Classification

Classifies soil types (e.g., Red soil, Black soil, Sandy soil).

Works with low-contrast soil regions using optimized thresholds.

Provides detection count and confidence metrics.

📊 Comparison Engine

Upload any two images to compare:

Soil type

Detection count

Confidence change

YOLO model used

Thresholds

Includes a graphical confidence bar chart.

✨ Smart Thresholding

Automatically lowers the confidence threshold for soil images (0.3 instead of 0.5).

Prevents false “No detection” cases.

🖼️ Image Segmentation

Creates semi-transparent soil/vegetation masks.

Supports bounding-box detection in a clear overlay.

🌐 Web UI

Clean, responsive UI using TailwindCSS.

Modern aligned comparison cards.

User-friendly upload workflow.

📁 Project Structure
ArchaeoMapAI/
│
├── app.py                       # Main Flask backend
├── models/
│   ├── best.pt                  # Vegetation YOLO model
│   ├── soil_best.pt             # Soil classifier YOLO model
│
├── static/
│   ├── uploads/                 # Uploaded images
│   ├── results/                 # YOLO output images + masks
│   ├── css/
│   └── screenshots/             # README screenshots
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── results.html
│   ├── compare.html
│   └── compare_result.html
│
└── README.md
✅ Installation
1. Clone the repository
git clone https://github.com/yourusername/ArchaeoMapAI.git
cd ArchaeoMapAI

2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

3. Install dependencies
pip install -r requirements.txt

4. Place YOLO models

Place your .pt files here:

models/best.pt
models/soil_best.pt

✅ Running the Application
python app.py


Your app will run at:

👉 http://127.0.0.1:5000

✅ Using the Application
1. Upload Image Mode

Upload one image.

Select Vegetation or Soil mode.

YOLO detects objects and creates:

A detected image

A segmentation mask

Detection stats

2. Comparison Mode

Upload two images.

Select mode (Soil or Vegetation).

The system generates:

Image 1 analysis

Image 2 analysis

Side-by-side summary

Confidence change

Detection change

Model details

✅ Soil images include soil type names (e.g., Red Soil, Clay Soil).

✅ Technical Highlights
YOLO Processing

Uses ultralytics YOLOv8.

Auto-thresholding for soil classification.

Extracts:

bounding boxes

class names

confidence list

segmentation overlays

Rendering

All processed images saved inside /static/results/.

Jinja2 templates show metrics and comparison summaries.

✅ Requirements

Python 3.9+

Flask

Pillow

Ultralytics YOLOv8

TailwindCSS (via CDN)

Install everything:

pip install flask pillow ultralytics

✅ Troubleshooting
✅ Soil Type not showing?

Ensure comparison dictionary includes:

"soil_name_1": stats1["class_names"][0],
"soil_name_2": stats2["class_names"][0],

✅ Image shows “No detection”?

Lower threshold:

default_conf = 0.3 if kind == "soil" else 0.5

✅ Images not same size?

Use consistent fixed-height:

class="w-full h-80 object-cover rounded-xl"

📄 License

MIT License (recommended for public + academic use).

🤝 Contributing

Pull requests are welcome!

⭐ Support the Project

If you found ArchaeoMap AI useful, consider starring the repo ⭐ on GitHub.
