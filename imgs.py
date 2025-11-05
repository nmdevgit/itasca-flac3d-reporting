import itasca as it
import os
import math

# --- SETTINGS ---
PLOT_NAME = "MyPlot"                  # name of existing plot in FLAC3D
OUT_DIR = "./exports/rotation_z"      # folder for exported PNGs
AXIS = "z"                            # rotation axis: 'x', 'y', or 'z'
N_FRAMES = 36                         # number of rotation frames
os.makedirs(OUT_DIR, exist_ok=True)

# --- CAMERA SETTINGS (from your .dat file) ---
CENTER = (195.51961, 176.49878, 1024.5232)
EYE = (81.121306, -198.60634, 1152.4)
ROLL = 358.79797

def rotate_vector(x, y, z, angle_deg, axis):
    a = math.radians(angle_deg)
    if axis == "z":
        return (x * math.cos(a) - y * math.sin(a),
                x * math.sin(a) + y * math.cos(a),
                z)
    elif axis == "y":
        return (x * math.cos(a) + z * math.sin(a),
                y,
                -x * math.sin(a) + z * math.cos(a))
    elif axis == "x":
        return (x,
                y * math.cos(a) - z * math.sin(a),
                y * math.sin(a) + z * math.cos(a))
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")

for i in range(N_FRAMES):
    angle = i * 360 / N_FRAMES
    dx, dy, dz = EYE[0] - CENTER[0], EYE[1] - CENTER[1], EYE[2] - CENTER[2]
    rx, ry, rz = rotate_vector(dx, dy, dz, angle, AXIS)
    ex, ey, ez = CENTER[0] + rx, CENTER[1] + ry, CENTER[2] + rz

    filename = os.path.join(OUT_DIR, f"rotation_{i:03d}.png")

    it.command(f"""
        plot view projection perspective magnification 1 ...
            center ({CENTER[0]},{CENTER[1]},{CENTER[2]}) ...
            eye ({ex},{ey},{ez}) ...
            roll {ROLL} ...
            clip-front -1e10 clip-back 1e10
        plot export bitmap filename="{filename}" dpi=300
    """)

    print(f"[{i+1}/{N_FRAMES}] Saved {filename}")

print(f"\nRotation complete. Files saved in: {OUT_DIR}\n")
