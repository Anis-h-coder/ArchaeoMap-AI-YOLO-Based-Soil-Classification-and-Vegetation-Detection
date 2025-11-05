from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

app = Flask(__name__)

# ---------------------------------------------------
# ✅ FLASK CONFIG
# ---------------------------------------------------

app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['RESULTS_FOLDER'] = "static/results"
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp', 'avif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# ---------------------------------------------------
# ✅ LOAD YOLO MODELS
# ---------------------------------------------------

VEG_MODEL = YOLO("models/best.pt")
SOIL_MODEL = YOLO("models/soil_best.pt")

# ---------------------------------------------------
# ✅ HELPERS
# ---------------------------------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_upload(file):
    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    new_filename = f"{timestamp}_{filename}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    file.save(save_path)

    # ✅ Convert AVIF → PNG (YOLO cannot read AVIF)
    if ext == "avif":
        try:
            img = Image.open(save_path).convert("RGB")
            png_name = f"{timestamp}_{filename.rsplit('.', 1)[0]}.png"
            png_path = os.path.join(app.config['UPLOAD_FOLDER'], png_name)
            img.save(png_path, format="PNG")
            os.remove(save_path)
            return f"uploads/{png_name}"
        except Exception as e:
            print("AVIF conversion failed:", e)

    return f"uploads/{new_filename}"


# ---------------------------------------------------
# ✅ YOLO DETECTION
# ---------------------------------------------------

def run_yolo(input_path, output_path, kind, conf_threshold=0.5, iou_threshold=0.5):

    model = VEG_MODEL if kind == "vegetation" else SOIL_MODEL
    results = model(input_path, conf=conf_threshold, iou=iou_threshold)[0]

    img = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    detections = 0
    boxes = []
    class_names = []
    confidences = []

    for box in results.boxes:
        conf = float(box.conf)

        if conf < conf_threshold:
            continue

        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cls = int(box.cls)
        label = results.names[cls]

        detections += 1
        boxes.append((x1, y1, x2, y2))
        confidences.append(conf)
        class_names.append(label)

        text = f"{label} {conf:.2f}"

        # ✅ BIG, VISIBLE FONT
        try:
            font = ImageFont.truetype("arial.ttf", 42)   # bigger text
        except:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)

        # ✅ OUTLINE (black shadow)
        draw.text((x1 + 7, y1 + 7), text, font=font, fill="black")
        draw.text((x1 + 9, y1 + 9), text, font=font, fill="black")

        # ✅ MAIN TEXT (bright lime)
        draw.text((x1 + 8, y1 + 8), text, font=font, fill="lime")

        # ✅ Bounding box remains
        draw.rectangle([x1, y1, x2, y2], outline="lime", width=4)


    img.save(output_path)

    top6 = sorted(confidences, reverse=True)[:6]
    highest_conf = max(confidences) if confidences else 0

    return detections, highest_conf, top6, boxes, class_names


# ---------------------------------------------------
# ✅ SEGMENTATION MASK
# ---------------------------------------------------

def create_seg_mask(input_path, output_path, boxes):

    base_img = Image.open(input_path).convert("RGBA")
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for (x1, y1, x2, y2) in boxes:
        draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255, 130))

    final = Image.alpha_composite(base_img, overlay)

    base, _ = os.path.splitext(output_path)
    final_path = base + ".png"
    final.save(final_path)

    return f"results/{os.path.basename(final_path)}"


# ---------------------------------------------------
# ✅ RUN FULL DETECTION
# ---------------------------------------------------

def run_detection(image_path, kind, conf_threshold, iou_threshold):

    fname = os.path.basename(image_path)
    base, _ = os.path.splitext(fname)

    full = os.path.join("static", image_path)
    det_path = os.path.join(app.config['RESULTS_FOLDER'], f"{base}_detected.jpg")
    mask_path = os.path.join(app.config['RESULTS_FOLDER'], f"{base}_mask.png")

    detections, highest_conf, top6, boxes, class_names = run_yolo(
        full, det_path, kind,
        conf_threshold=conf_threshold,
        iou_threshold=iou_threshold
    )

    segmentation_rel = create_seg_mask(full, mask_path, boxes)

    return (
        f"results/{os.path.basename(det_path)}",
        segmentation_rel,
        {
            "detections": detections,
            "highest_confidence": highest_conf,
            "top6": top6,
            "class_names": class_names,
            "model_used": f"{kind.capitalize()} YOLO Model",
            "conf_threshold": conf_threshold,
            "iou_threshold": iou_threshold
        }
    )


# ---------------------------------------------------
# ✅ ROUTES
# ---------------------------------------------------

@app.route("/")
def index():
    uploads = sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True)
    latest = uploads[0] if uploads else None
    return render_template("index.html", latest_image=latest)


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        file = request.files["file"]

        if not file or not allowed_file(file.filename):
            return "Invalid file", 400

        kind = request.form.get("kind", "vegetation")
        # ✅ Use lower threshold for soil
        default_conf = 0.3 if kind == "soil" else 0.5
        conf_threshold = float(request.form.get("conf_threshold", default_conf))
        iou_threshold = float(request.form.get("iou_threshold", 0.5))


        saved_rel = save_upload(file)

        det_rel, mask_rel, stats = run_detection(
            saved_rel, kind, conf_threshold, iou_threshold
        )

        return redirect(url_for(
            "results",
            original=saved_rel,
            result=det_rel,
            segmented=mask_rel,
            detections=stats["detections"],
            highest_confidence=stats["highest_confidence"],
            top6=",".join([str(x) for x in stats["top6"]]),
            class_names=",".join(stats["class_names"]),
            model_used=stats["model_used"],
            iou_threshold=iou_threshold,
            conf_threshold=conf_threshold
        ))

    return render_template("upload.html")


@app.route("/results")
def results():

    original = request.args.get("original")
    result = request.args.get("result")
    segmented = request.args.get("segmented")

    top6_raw = request.args.get("top6", "")
    top6_list = [float(x) for x in top6_raw.split(",") if x]

    stats = {
        "detections": int(request.args.get("detections", 0)),
        "highest_confidence": float(request.args.get("highest_confidence", 0)),
        "top6": top6_list,
        "model_used": request.args.get("model_used", ""),
        "class_names": request.args.get("class_names", "").split(","),
        "iou_threshold": float(request.args.get("iou_threshold", 0.5)),
        "conf_threshold": float(request.args.get("conf_threshold", 0.5)),
    }

    return render_template(
        "results.html",
        original=original,
        result=result,
        segmented=segmented,
        stats=stats
    )

@app.route("/compare", methods=["GET", "POST"])
def compare():

    if request.method == "POST":
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")
        kind = request.form.get("kind", "vegetation")

        # ✅ Soil uses lower threshold
        default_conf = 0.3 if kind == "soil" else 0.5
        conf_threshold = float(request.form.get("conf_threshold", default_conf))
        iou_threshold = float(request.form.get("iou_threshold", 0.5))


        if not file1 or not file2:
            return "Please upload both images.", 400

        if not allowed_file(file1.filename) or not allowed_file(file2.filename):
            return "Invalid file format", 400

        # ✅ Save files
        img1_rel = save_upload(file1)
        img2_rel = save_upload(file2)

        # ✅ Run detection on both images
        det1, mask1, stats1 = run_detection(img1_rel, kind, conf_threshold, iou_threshold)
        det2, mask2, stats2 = run_detection(img2_rel, kind, conf_threshold, iou_threshold)

        # ✅ Build final comparison dictionary
        comparison = {
            "model_used": stats1["model_used"],
            "model_version": "1.0",
            
            # ✅ Soil names (THIS FIXES YOUR ISSUE)
            "soil_name_1": stats1["class_names"][0] if stats1["class_names"] else "No detection",
            "soil_name_2": stats2["class_names"][0] if stats2["class_names"] else "No detection",
            
            # ✅ Highest confidences
            "highest_conf_1": stats1["highest_confidence"],
            "highest_conf_2": stats2["highest_confidence"],
            
            # ✅ Detection counts
            "detections_1": stats1["detections"],
            "detections_2": stats2["detections"],
            
            # ✅ Differences (required)
            "difference": stats2["detections"] - stats1["detections"],
            "detections_change": stats2["detections"] - stats1["detections"],
            
            # ✅ Confidence change
            "confidence_change": stats2["highest_confidence"] - stats1["highest_confidence"],
            
            "iou_threshold": iou_threshold,
            "conf_threshold": conf_threshold,
            
            "interpretation": (
                "Detection increased in the second image."
                if stats2["detections"] > stats1["detections"]
                else "Detection decreased in the second image."
                if stats2["detections"] < stats1["detections"]
                else "Both images have equal detection counts."
            )
        }

        return render_template(
            "compare_result.html",
            file1=img1_rel,
            file2=img2_rel,
            file1_detected=det1,
            file2_detected=det2,
            file1_mask=mask1,
            file2_mask=mask2,
            comparison=comparison,
            is_soil=(kind == "soil") 
        )


    return render_template("compare.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
