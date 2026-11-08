# OCR X-Ray Visualizer 🔍

An interactive diagnostic tool that visualizes **Tesseract OCR** output using **Graphviz*
Turns a static image into an **zoomable, searchable, hoverable SVG map** showing exactly *what* Tesseract read, *where* it read it, and *how confident* it was.

> **Pipeline:** `Image` → **Tesseract** (Structured Data) → **Python** (Coord Transform) → **Graphviz** (SVG) → **Browser** (Visual Debugging)

---

## 🧠 What Each Library Does

| Library | Role in Pipeline | Core Responsibility |
| :--- | :--- | :--- |
| **Tesseract (via `pytesseract`)** | **The "Reader"** | Performs OCR. Extracts **words, bounding boxes (x,y,w,h), confidence scores (0-100), and layout hierarchy** (block/paragraph/line/word numbers) via
`image_to_data`. |
| **Graphviz (via `graphviz` Python pkg)** | **The "Cartographer"** | Takes the structured data (coordinates + text + confidence) and renders a **vector diagram (SVG)**. Uses the `neato` engine to pin
nodes to **exact absolute positions** (`pos="x,y!"`). |
| **Pillow (`PIL`)** | **The "Loader"** | Opens the image file, provides dimensions (Width/Height in pixels) required for coordinate system conversion. |
| **Python Standard Lib** | **The "Glue"** | Coordinate math (Pixels → Inches, Y-axis fliscaping for tooltips, CLI argument parsing. |

---

## 🤝 What Each Contributes to the Final Output

| Contribution | Source | Result in `output_xray.svg` |
| :--- | :--- | :--- |
| **Word Text** | Tesseract | The label inside each box (searchable via `Ctrl+F`). |
| **Bounding Box Geometry** | Tesseract → Python Math | Exact position/size of boxes overlaid on logical coordinates. |
| **Confidence Score (0-100)** | Tesseract | **Color Coding**: 🟢 Green (≥90), 🟠 Orange
| **Layout Hierarchy** | Tesseract | **Tooltip Metadata**: Block, Paragraph, Line, Word index. |
| **Vector Rendering** | Graphviz | Infinite zoom without blur; native SVG tooltips (`<ti
| **Coordinate System Fix** | Python | Corrects PIL (Top-Left origin) → Graphviz (Bottom-Left origin). |

---

## 🛠 Prerequisites (Install Once)

### 1. System Dependencies (Required for binaries)
macOS (Homebrew):
brew install tesseract graphviz
Ubuntu/Debian:
sudo apt update && sudo apt install tesseract-ocr graphviz
Windows:
- Install Tesseract Installer (https://github.com/UB-Mannheim/tesseract/wiki) (Add to PAT
- Install Graphviz Installer (https://graphviz.org/download/) (Add to PATH).

2. Python Environment & Packages

# 1. Navigate to project
cd path/to/ocr-xray-visualizer

# 2. Create & Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install Python Packages
pip install pytesseract graphviz pillow

---

▶️ How to Run

Basic Usage (Default: receipt.png)

# Ensure venv is active
source .venv/bin/activate

# Run
python3 ocr_xray.py

Custom Image

python3 ocr_xray.py path/to/your/image.png
Supports .png, .jpg, .jpeg, .tiff, .bmp.

---

📤 The Output

1. Terminal Feedback

🔍 Loading image: receipt.png
   Image size: 1240x1754 pixels
🧠 Running Tesseract OCR (image_to_data)...
🎨 Building Graphviz SVG (engine='neato')...
   Processed 87 words.
💾 Rendering SVG to: receipt_xray.svg
✅ SUCCESS! Open this file in your browser:
   file:///Users/you/project/receipt_xray.svg

2. The Artifact: receipt_xray.svg

Open this file in any modern browser (Chrome, Firefox, Safari, Edge) or VS Code Preview.

Visual Features

┌────────────────────┬──────────────────────────────────────────────────────────────────────────────────────┐
│      Feature       │                                     Description
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 🟢 Green Boxes     │ High Confidence (≥90%). Clean text, reliable.
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 🟠 Orange Boxes    │ Medium Confidence (60-89%). Noisy, blurred, or unusual fonts.
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 🔴 Red Boxes       │ Low Confidence (<60%). Likely garbage, lines mistaken for text, or
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 🔍 Infinite Zoom   │ Vector graphics (SVG) — zoom 5000% with zero pixelation.
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 🖱 Hover Tooltips   │ Hover any box → See Text, Confidence %, Block/Line/Word Index.
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 🔎 Searchable      │ Press Ctrl/Cmd + F in browser → Type "TOTAL" → Box highlights.
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│ 📋 Selectable Text │ Copy text labels directly from the diagram.
└────────────────────┴──────────────────────────────────────────────────────────────────────────────────────┘

❌ What It CANNOT Do (Limitations)

┌──────────────────────┬───────────────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────┐
│      Limitation      │                                        Reason                                                   Workaround / Note                                    │
├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ No Background Image  │ Graphviz neato with pos pins nodes but doesn't natively support e SVG shows boxes floating on white/transparent background. Mentally align with      │
│                      │ layer in the SVG output easily without complex image attributes per node.             │ original image, or use VS Code split view (Image left, SVG right).                     │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ No Handwriting       │ Tesseract LSTM models are trained on printed fonts.                                   │ Use TrOCR (Transformer-based) or cloud APIs (Google Vision, AWS Textract) for          │
│ Support              │                                                                 ndwriting.                                                                           │
├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ No Table Structure   │ Outputs words/lines; does not output <table>, rows, cols, or mere pymupdf (pdfplumber) for PDF tables, or specialized Table Transformers             │
│ Recovery             │                                                                                       │ (TableFormer).                                                                         │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Reading Order        │ Tesseract image_to_data returns linear word list. Reading order (Col1→Col2) must be   │ Post-process: Sort by block_num then top then left.                                    │
│ (Multi-column)       │ inferred from block_num/x coords.                                                                                                                    │
├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ Rotation / Skew      │ Fails silently or produces garbage on rotated images (> ±5°).   e-process with OpenCV: cv2.minAreaRect / pytesseract.image_to_osd for auto-rotation. │
│ Correction           │                                                                                       │                                                                                        │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Non-Latin Scripts    │ Default eng model only.                                                               │ Install tesseract-ocr-script-latn, chi_sim, ara, etc. Run: tesseract --list-langs.     │
│ (Default)            │                                                                                                                                                      │
├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
│ Real-time / Video    │ Architecturally batch-oriented (Disk I/O + Process Spawn).      e tesseract C++ API directly or tesserocr (Python C-binding) for in-memory speed.    │
└──────────────────────┴───────────────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘

---

📁 Project Structure

ocr-xray-visualizer/
├── .venv/                 # Virtual Environment (ignored by git)
├── ocr_xray.py            # Main Pipeline Script
├── receipt.png            # Sample Input Image
├── receipt_xray.svg       # Generated Output (ignored by git*)
├── requirements.txt       # pip freeze > requirements.txt
├── .gitignore
└── README.md              # You are here
Add *_xray.svg to .gitignore if you don't want to commit generated artifacts.

---

📜 License

MIT License — Free to use, modify, distribute.

---

🙏 Acknowledgments

- Tesseract OCR by Google / UB Mannheim.
- Graphviz by AT&T Labs / Open Source Community.
- Pillow by Alex Clark & Contributors.
