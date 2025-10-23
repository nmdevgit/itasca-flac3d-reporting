# ================================================================
# make_video_from_images.py
# ------------------------------------------------
# Combines exported FLAC3D slice images into a single .mp4 video.
# Run this AFTER your export scripts have generated all images.
# ================================================================

import cv2
import os
import natsort

# ------------------------------
# User configuration
# ------------------------------
IMAGE_FOLDER = "./exports/max_principal/zslice"  # folder with your BMPs/PNGs
OUTPUT_VIDEO = "./exports/max_principal/zslice/video_slices.mp4"

FPS = 5               # frames per second (adjust for speed)
EXTENSION = ".bmp"    # change to ".png" if you export PNGs

# ------------------------------
# Collect and sort image files
# ------------------------------
images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(EXTENSION)]
images = natsort.natsorted(images)  # natural sort: vert_slice_001, vert_slice_002, ...

if not images:
    raise FileNotFoundError(f"No {EXTENSION} files found in {IMAGE_FOLDER}")

# Read first image to get frame size
first_image_path = os.path.join(IMAGE_FOLDER, images[0])
frame = cv2.imread(first_image_path)
height, width, _ = frame.shape

# ------------------------------
# Create video writer
# ------------------------------
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec
video_writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (width, height))

# ------------------------------
# Write frames
# ------------------------------
print(f"Creating video from {len(images)} images...")

for img_name in images:
    img_path = os.path.join(IMAGE_FOLDER, img_name)
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"⚠️ Skipping unreadable image: {img_name}")
        continue
    video_writer.write(frame)
    print(f"Added {img_name}")

video_writer.release()
print(f"\n Video saved as: {OUTPUT_VIDEO}")
