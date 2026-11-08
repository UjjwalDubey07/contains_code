import sys
import os
from PIL import Image
import pytesseract
from pytesseract import Output
from graphviz import Digraph

def main(image_path):
    # ---------------------------------------------------------
    # 1. VALIDATE INPUT
    # ---------------------------------------------------------
    if not os.path.exists(image_path):
        print(f"❌ ERROR: File not found at '{image_path}'")
        print(f"   Current folder: {os.getcwd()}")
        print(f"   Files here: {os.listdir('.')}")
        return

    print(f"🔍 Loading image: {image_path}")
    try:
        img = Image.open(image_path)
        img_w, img_h = img.size
        print(f"   Image size: {img_w}x{img_h} pixels")
    except Exception as e:
        print(f"❌ ERROR: Could not open image: {e}")
        return

    # ---------------------------------------------------------
    # 2. TESSERACT: Extract Structured Data (The "Doctor")
    # ---------------------------------------------------------
    print("🧠 Running Tesseract OCR (image_to_data)...")
    try:
        # output_type=Output.DICT gives us: left, top, width, height, conf, text, block_num, line_num...
        data = pytesseract.image_to_data(img, output_type=Output.DICT)
    except pytesseract.TesseractNotFoundError:
        print("❌ ERROR: Tesseract binary not found.")
        print("   Run: brew install tesseract")
        return
    except Exception as e:
        print(f"❌ ERROR during OCR: {e}")
        return

    # ---------------------------------------------------------
    # 3. GRAPHVIZ: Build the Visualization Graph (The "Artist")
    # ---------------------------------------------------------
    print("🎨 Building Graphviz SVG (engine='neato')...")

    # 'neato' allows absolute positioning via 'pos' attribute.
    # Graphviz uses INCHES (72 DPI) for 'pos'.
    # PIL uses PIXELS (Top-Left origin).
    # Graphviz 'neato' uses INCHES (Bottom-Left origin).
    # Conversion: x_inch = x_px / 72.0
    #             y_inch = (img_h_px - y_px) / 72.0  <-- FLIP Y AXIS

    dot = Digraph(name='OCR_XRay', format='svg', engine='neato', graph_attr={
        'overlap': 'false',      # Don't move nodes, keep exact coords
        'splines': 'false',      # No edges/lines connecting words
        'outputorder': 'nodesfirst', # Draw nodes on top
        'dpi': '72',             # Match our coordinate math (1 inch = 72 pts)
        'bgcolor': 'transparent' # Let browser background show
    })

    # Default node styling
    dot.attr('node', shape='plaintext', fontname='Helvetica', fontsize='8', margin='0')

    words_processed = 0
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        # Filter: Confidence > 0 AND text not empty
        conf = int(data['conf'][i])
        text = data['text'][i].strip()

        if conf < 0 or not text:
            continue

        words_processed += 1

        # --- Coordinates ---
        x_px = data['left'][i]
        y_px = data['top'][i]
        w_px = data['width'][i]
        h_px = data['height'][i]

        # Convert to Graphviz Inches (Bottom-Left Origin)
        pos_x = x_px / 72.0
        pos_y = (img_h - y_px) / 72.0  # FLIP Y

        # --- Color by Confidence ---
        if conf >= 90:      color = "#27ae60"  # Green
        elif conf >= 60:    color = "#f39c12"  # Orange
        else:               color = "#c0392b"  # Red

        # --- Tooltip / Label (HTML-like) ---
        # Escaping quotes for DOT language
        safe_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

        tooltip = (f"Text: {safe_text}\\n"
                   f"Confidence: {conf}%\\n"
                   f"Block: {data['block_num'][i]} | Par: {data['par_num'][i]} | Line: {data['line_num'][i]} | Word: {data['word_num'][i]}")

        # HTML-like label allows formatting + tooltip via <title> in SVG output
        label = f'''<
            <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="2" BGCOLOR="white" COLOR="{color}">
                <TR><TD><B>{safe_text}</B></TD></TR>
                <TR><TD><FONT POINT-SIZE="7" COLOR="#555555">Conf: {conf}%</FONT></TD></TR>
            </TABLE>
        >'''

        node_id = f"w_{i}"
        # 'pos="x,y!"' -> '!' means "pinned/fixed position"
        dot.node(node_id, label=label, pos=f"{pos_x},{pos_y}!", tooltip=tooltip)

    if words_processed == 0:
        print("⚠️ WARNING: No text detected with confidence > 0.")
        print("   Image might be blank, upside down, or non-text.")
        return

    print(f"   Processed {words_processed} words.")

    # ---------------------------------------------------------
    # 4. RENDER & SAVE
    # ---------------------------------------------------------
    output_base = os.path.splitext(os.path.basename(image_path))[0] + "_xray"
    output_path = os.path.join(os.getcwd(), output_base)

    try:
        print(f"💾 Rendering SVG to: {output_base}.svg")
        dot.render(output_base, cleanup=True, quiet=True)
        print(f"✅ SUCCESS! Open this file in your browser:")
        print(f"   file://{output_path}.svg")
    except Exception as e:
        print(f"❌ ERROR rendering Graphviz: {e}")

if __name__ == "__main__":
    # Allow dragging file onto script or passing as arg
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Default fallback to your receipt
        target_file = "receipt.png"
        print(f"No filename provided. Defaulting to: {target_file}")

    main(target_file)

