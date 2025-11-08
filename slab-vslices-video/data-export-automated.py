# --------------------------------------------------------
# data-export-max-principal-zslice.py
# Exports horizontal (z-slice) plots of max principal
# effective stress from FLAC3D with fixed legend bounds.
# --------------------------------------------------------

import itasca as it
import os

# ------------------------------
# Directory setup
# ------------------------------
out_dir = "./exports-mn/max_principal/zslice"
os.makedirs(out_dir, exist_ok=True)

# ------------------------------
# Helper: plane parameters
# ------------------------------
def _plane_params_z(i):
    """Returns origin and orientation for horizontal z-slice."""
    origin = f"(0,0,{i})"
    normal = "(0,0,1)"
    dip, dip_dir = "0", "0"
    return origin, normal, dip, dip_dir

# ------------------------------
# Max Principal Stress (Z-slices)
# ------------------------------
def export_max_principal_z_slices(start=980, end=1080, step=0.5,
                                  min_val=0, max_val=10):
    """
    Exports horizontal slices of maximum principal effective stress
    with fixed legend bounds (positive-only range).
    """
    z_values = [round(start + j * step, 2) for j in range(int((end - start) / step) + 1)]

    for i in z_values:
        origin, normal, dip, dip_dir = _plane_params_z(i)
        filename = f"z_slice_max_principal_{i:.1f}.bmp"
        filepath = os.path.join(out_dir, filename)

        print(f"Exporting max principal stress slice at z = {i:.1f} m")

        it.command(f'''
            plot create "MaxEffStress_Z{i:.1f}"
            plot clear
            plot background 'white'
            plot outline active on width 2 color 'black'

            plot item create zone active on ...
                contour stress-effective quantity maximum log off ...
                method average ...
                ramp rainbow minimum {min_val} maximum {max_val} interval 10 ...
                polygons fill on ...
                outline active off ...
                cut active on type plane ...
                    surface on front off back off ...
                    origin {origin} normal {normal} ...
                null-faces-only off ...
                hide-null mechanical on thermal off fluid off ...
                transparency 0

            plot view projection parallel
            plot view reset
            plot view dip {dip}
            plot view dip-direction {dip_dir}

            plot export bitmap filename="{filepath}" dpi=250
        ''')

# ------------------------------
# Run export
# ------------------------------
# Adjust min_val/max_val as needed (e.g., MPa range)
export_max_principal_z_slices(min_val=0, max_val=350000)


























######################################################################
# ====================================================================
# FLAC3D Vertical Slice Automation Script (Reverse Direction)
# --------------------------------------------------------------------
# Automates export of vertical slices of maximum principal effective
# stress at 1 m spacing, moving opposite to the plane's normal vector.
# ====================================================================

import itasca as it
import os

# --------------------------------------------------------------------
# User configuration
# --------------------------------------------------------------------
OUT_DIR = "./exports/max_principal/vertical_1"
os.makedirs(OUT_DIR, exist_ok=True)

# Base plane definition (from your first manual plot)
ORIGIN_BASE = (63.918, 174.661, 980.0)
NORMAL = (-0.927184, 0.374607, 6.12323e-17)  # do NOT modify
SPACING = 0.5        # distance between slices (m)
NUM_SLICES = 260      # number of slices to generate

# Contour display settings
MIN_VAL = 0
MAX_VAL = 350000
INTERVAL = 50

# Camera / view settings (from your .dat)
CENTER = (118.6423, 186.62776, 970.54353)
EYE = (-344.4808, 253.49691, 977.97595)
ROLL = 359.79744


# --------------------------------------------------------------------
# Helper: offset the origin opposite the plane normal
# --------------------------------------------------------------------
def offset_origin(base, normal, distance):
    """Return a new origin offset *opposite* to the normal by 'distance'."""
    return tuple(base[i] - distance * normal[i] for i in range(3))  # ← negative direction


# --------------------------------------------------------------------
# Main export loop
# --------------------------------------------------------------------
for i in range(NUM_SLICES):
    origin = offset_origin(ORIGIN_BASE, NORMAL, i * SPACING)
    filename = os.path.join(OUT_DIR, f"vert_slice_{i+1:03d}.bmp")

    print(f"[{i+1}/{NUM_SLICES}] Exporting vertical slice at origin {origin}")

    it.command(f"""
        plot create "VertSlice_{i+1:03d}"
        plot clear
        plot active on
        plot target active on
        plot background 'white'
        plot outline active on width 2 color 'black'

        plot legend active true heading size 80 color 'black' copyright size 28 color 'black' ...
            placement left size 25,50 ...
            step active false ...
            time-real active false ...
            time-model active false ...
            title-customer active false ...
            view-info active false

        plot title-job active false
        plot title active false

        plot view projection parallel magnification 1 ...
            center ({CENTER[0]},{CENTER[1]},{CENTER[2]}) ...
            eye ({EYE[0]},{EYE[1]},{EYE[2]}) ...
            roll {ROLL} ...
            clip-front -1e10 clip-back 1e10

        plot item create zone active on ...
            contour stress-effective quantity maximum log off ...
                method average null fluid off mechanical on thermal off ...
            ramp rainbow ...
                minimum {MIN_VAL} maximum {MAX_VAL} interval {INTERVAL} ...
                reversed off above automatic below automatic ...
            polygons fill on outline active off ...
                polygon-transparency 0 ...
                outline-transparency 80 lighting on offset 0.5 2 ...
            cut-line width 1 selected-only false selected-highlight false selected-only false ...
            null-faces-only off ...
            map axis xyz rotate (0,0,0) translate (0,0,0) scale (1,1,1) ...
            deformation-factor active off ...
            hide-null mechanical on thermal off fluid off ...
            transparency 0 ...
            cut active on type plane ...
                 surface on front off back off ...
                 origin ({origin[0]:.3f},{origin[1]:.3f},{origin[2]:.3f}) ...
                 normal ({NORMAL[0]:.6f},{NORMAL[1]:.6f},{NORMAL[2]:.6f}) ...
            clip active off ...
            legend active on ...
                title active true text "" size 55 family 'Times New Roman' style bold color 'black' ...
                cut ...
                    title active true size 44 family 'Arial' style normal color 'black' ...
                    origin active false ...
                    normal active false ...
                    orientation active false ...
                map active true size 44 family 'Arial' style normal color 'black' ...
                hide-null active false ...
                deformation-factor active true size 44 family 'Arial' style normal color 'black' ...
                count active false ...
                contour labels active true size 44 family 'Arial' style normal color 'black' ...
                labels-maximum 20  format 0  precision 2 ...
                method active true size 44 family 'Arial' style normal color 'black'

        plot export bitmap filename="{filename}" dpi=300
    """)

print(f"\n Export complete! Files saved in: {OUT_DIR}\n")


















# ====================================================================
# FLAC3D Vertical Slice Automation Script (Forward Direction)
# --------------------------------------------------------------------
# Automates export of vertical slices of maximum principal effective
# stress at 1 m spacing, moving along the plane's normal vector.
# ====================================================================

import itasca as it
import os

# --------------------------------------------------------------------
# User configuration
# --------------------------------------------------------------------
OUT_DIR = "./exports/max_principal/vertical_2"
os.makedirs(OUT_DIR, exist_ok=True)

# Base plane definition (from the new attached .dat)
ORIGIN_BASE = (51.7136, 96.7497, 980.0)
NORMAL = (0.390731, 0.920505, 6.12323e-17)  # forward direction
SPACING = 0.5        # distance between slices (m)
NUM_SLICES = 420      # number of slices to generate

# Contour display settings
MIN_VAL = 0
MAX_VAL = 350000
INTERVAL = 50

# Camera / view settings (from new .dat)
CENTER = (143.95518, 114.28977, 964.47347)
EYE = (51.765629, -298.42382, 1001.1944)
ROLL = 0.064852696


# --------------------------------------------------------------------
# Helper: offset the origin along the plane normal
# --------------------------------------------------------------------
def offset_origin(base, normal, distance):
    """Return a new origin offset *along* the normal by 'distance'."""
    return tuple(base[i] + distance * normal[i] for i in range(3))


# --------------------------------------------------------------------
# Main export loop
# --------------------------------------------------------------------
for i in range(NUM_SLICES):
    origin = offset_origin(ORIGIN_BASE, NORMAL, i * SPACING)
    filename = os.path.join(OUT_DIR, f"vert_slice_{i+1:03d}.bmp")

    print(f"[{i+1}/{NUM_SLICES}] Exporting vertical slice at origin {origin}")

    it.command(f"""
        plot create "VertSlice2_{i+1:03d}"
        plot clear
        plot active on
        plot target active on
        plot background 'white'
        plot outline active on width 2 color 'black'

        plot legend active true heading size 80 color 'black' copyright size 28 color 'black' ...
            placement left size 25,50 ...
            step active false ...
            time-real active false ...
            time-model active false ...
            title-customer active false ...
            view-info active false

        plot title-job active false
        plot title active false

        plot view projection parallel magnification 1 ...
            center ({CENTER[0]},{CENTER[1]},{CENTER[2]}) ...
            eye ({EYE[0]},{EYE[1]},{EYE[2]}) ...
            roll {ROLL} ...
            clip-front -1e10 clip-back 1e10

        plot item create zone active on ...
            contour stress-effective quantity maximum log off ...
                method average null fluid off mechanical on thermal off ...
            ramp rainbow ...
                minimum {MIN_VAL} maximum {MAX_VAL} interval {INTERVAL} ...
                reversed off above automatic below automatic ...
            polygons fill on outline active off ...
                polygon-transparency 0 ...
                outline-transparency 80 lighting on offset 0.5 2 ...
            cut-line width 1 selected-only false selected-highlight false selected-only false ...
            null-faces-only off ...
            map axis xyz rotate (0,0,0) translate (0,0,0) scale (1,1,1) ...
            deformation-factor active off ...
            hide-null mechanical on thermal off fluid off ...
            transparency 0 ...
            cut active on type plane ...
                 surface on front off back off ...
                 origin ({origin[0]:.3f},{origin[1]:.3f},{origin[2]:.3f}) ...
                 normal ({NORMAL[0]:.6f},{NORMAL[1]:.6f},{NORMAL[2]:.6f}) ...
            clip active off ...
            legend active on ...
                title active true text "" size 55 family 'Times New Roman' style bold color 'black' ...
                cut ...
                    title active true size 44 family 'Arial' style normal color 'black' ...
                    origin active false ...
                    normal active false ...
                    orientation active false ...
                map active true size 44 family 'Arial' style normal color 'black' ...
                hide-null active false ...
                deformation-factor active true size 44 family 'Arial' style normal color 'black' ...
                count active false ...
                contour labels active true size 44 family 'Arial' style normal color 'black' ...
                labels-maximum 20  format 0  precision 2 ...
                method active true size 44 family 'Arial' style normal color 'black'

        plot export bitmap filename="{filename}" dpi=300
    """)

print(f"\n Export complete! Files saved in: {OUT_DIR}\n")







