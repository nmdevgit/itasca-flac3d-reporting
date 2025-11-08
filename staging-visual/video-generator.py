# ================================================================
# make_video_from_images.py
# ------------------------------------------------
# Combines exported FLAC3D rotation images (in subfolders) into
# a single .mp4 video, preserving folder order (01, 02, 03, ...),
# with optional skipping (e.g., use every Nth image).
# ================================================================

import cv2
import os
import natsort

# ------------------------------
# User configuration
# ------------------------------
BASE_FOLDER = "./exports/rotation_z"   # parent folder containing 01, 02, ...
OUTPUT_VIDEO = "./exports/rotation_z/video.mp4"

FPS = 1
EXTENSION = ".png"
SKIP = 1   # use every Nth image (1 = use all, 2 = every 2nd, 3 = every 3rd, etc.)

# ------------------------------
# Collect subfolders and images
# ------------------------------
subfolders = [f for f in os.listdir(BASE_FOLDER)
              if os.path.isdir(os.path.join(BASE_FOLDER, f))]
subfolders = natsort.natsorted(subfolders)  # ensure 01, 02, 03, ...

all_images = []

for sub in subfolders:
    folder_path = os.path.join(BASE_FOLDER, sub)
    images = [f for f in os.listdir(folder_path)
              if f.lower().endswith(EXTENSION)]
    images = natsort.natsorted(images)
    # apply skip
    images = images[::SKIP]
    for img in images:
        all_images.append(os.path.join(folder_path, img))

if not all_images:
    raise FileNotFoundError(f"No {EXTENSION} files found in subfolders of {BASE_FOLDER}")

# ------------------------------
# Determine frame size
# ------------------------------
first_image = cv2.imread(all_images[0])
if first_image is None:
    raise RuntimeError(f"Unable to read the first image: {all_images[0]}")

height, width, _ = first_image.shape

# ------------------------------
# Create video writer
# ------------------------------
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (width, height))

# ------------------------------
# Write frames
# ------------------------------
print(f"Creating video from {len(all_images)} images... (skip={SKIP})")

for img_path in all_images:
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"Skipping unreadable image: {img_path}")
        continue
    video_writer.write(frame)
    print(f"Added {img_path}")

video_writer.release()
print(f"\nVideo saved as: {OUTPUT_VIDEO}")
