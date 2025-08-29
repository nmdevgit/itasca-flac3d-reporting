from PIL import Image
from docx import Document
from docx.shared import Inches
import io
import os
import re

print("Generating report...")

# Resize image to under 500 KB
def resize_image_to_limit(filepath, max_bytes=512000, min_quality=10):
    with Image.open(filepath) as img:
        quality = 95
        while quality >= min_quality:
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            size = buffer.tell()
            if size <= max_bytes:
                with open(filepath, 'wb') as f:
                    f.write(buffer.getvalue())
                return True
            quality -= 5
    return False

# Get numeric slice value from filename for sorting


def extract_slice_number(filename):
    match = re.search(r"(\d+)", filename)
    return int(match.group(1)) if match else -1


# Word doc generator for X or Y slices
def generate_report(axis="x"):
    from docx.enum.section import WD_ORIENT
    from docx.shared import Inches, Pt
    from docx.oxml.ns import qn

    axis = axis.lower()
    if axis not in ["x", "y"]:
        print("Invalid axis. Use 'x' or 'y'.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))

    folders = {
        "disp":  os.path.join(script_dir, "exports", "displacements", f"{axis}slice"),
        "max":   os.path.join(script_dir, "exports", "max_principal", f"{axis}slice"),
        "min":   os.path.join(script_dir, "exports", "min_principal", f"{axis}slice"),
        "state": os.path.join(script_dir, "exports", "zone_state", f"{axis}slice"),
    }

    filename_templates = {
        "disp":  f"{axis}_slice_disp_{{}}.bmp",
        "max":   f"{axis}_slice_max_principal_{{}}.bmp",
        "min":   f"{axis}_slice_min_principal_{{}}.bmp",
        "state": f"{axis}_slice_state_{{}}.bmp",
    }
    labels = {
        "disp":  "Displacement Magnitude",
        "max":   "Max Principal Effective Stress",
        "min":   "Min Principal Effective Stress",
        "state": "Zone State",
    }

    # exactly two per page for X; try for Y if files exist
    keys_x = ["disp", "max"]
    keys_y = ["disp", "max"]
    keys_to_include = keys_x if axis == "x" else keys_y

    doc_filename = os.path.join(script_dir, "exports", f"{axis}slice_figures.docx")
    document = Document()

    # Page setup (A4 portrait, tight margins)
    section = document.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.top_margin = section.bottom_margin = section.left_margin = section.right_margin = Inches(0.7)

    # Tighten caption style so two figures fit
    caption = document.styles["Caption"]
    caption.font.size = Pt(9)
    caption.paragraph_format.space_before = Pt(0)
    caption.paragraph_format.space_after  = Pt(6)  # just a little gap

    # (optional) also tweak Normal if you want tighter spacing everywhere:
    normal = document.styles["Normal"]
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after  = Pt(0)

    # Collect slice numbers from displacement folder
    if not os.path.exists(folders["disp"]):
        print(f"Missing folder: {folders['disp']}")
        return
    slice_files = [f for f in os.listdir(folders["disp"]) if f.lower().endswith(".bmp")]
    slice_numbers = sorted([extract_slice_number(f) for f in slice_files if extract_slice_number(f) >= 0])
    if not slice_numbers:
        print("No valid BMP slice files found.")
        return

    IMG_W = Inches(5.5)
    IMG_H = Inches(4)  # tweak if needed; 3.0–3.4" fits well

    for slice_val in slice_numbers:
        slice_str = str(slice_val)

        # Two pages per slice, each with exactly two figures (if available)
        page_pairs = [
            ("disp", "max"),   # Page A
            ("min",  "state"), # Page B
        ]

        for page_idx, (k1, k2) in enumerate(page_pairs, start=1):
            # Heading per page (helps when pages get separated in review)
            document.add_heading(f"{axis.upper()} Slice @ {slice_str}  ({page_idx}/2)", level=1)

            # Table block keeps both figures on the same page
            table = document.add_table(rows=0, cols=1)
            table.autofit = False

            for key in (k1, k2):
                bmp_name = filename_templates[key].format(slice_str)
                bmp_path = os.path.join(folders[key], bmp_name)
                if not os.path.exists(bmp_path):
                    print(f"⚠️  Missing: {bmp_path}")
                    continue

                # BMP → JPG (smaller + Word friendly)
                jpg_path = bmp_path.replace(".bmp", ".jpg")
                with Image.open(bmp_path) as im:
                    im.convert("RGB").save(jpg_path, "JPEG", quality=95)
                resize_image_to_limit(jpg_path)

                # Image row
                row_img = table.add_row().cells[0]
                p = row_img.paragraphs[0]
                run = p.add_run()
                run.add_picture(jpg_path, width=IMG_W, height=IMG_H)

                # Caption row
                row_cap = table.add_row().cells[0]
                row_cap.text = f"{labels[key]} – Slice {slice_str}"
                row_cap.paragraphs[0].style = "Caption"

                os.remove(jpg_path)

            # Page break after each page (so two pages per slice)
            document.add_page_break()

    document.save(doc_filename)
    print(f"\nWord document saved as: {os.path.abspath(doc_filename)}")




# Run for both X and Y slices
generate_report("x")
generate_report("y")
