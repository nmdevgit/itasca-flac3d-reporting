# ---------------------------------------------
# zz_slice_topview_batch.py   (run in FLAC3D Python console)
# Export top-down cut-plane views of Zone ZZ Effective Stress at multiple RLs.
# ---------------------------------------------
import itasca as it
import os
from math import isfinite

# =========================================================
# ============== USER CONFIG – EDIT THIS BLOCK ============
# Where do you want the files?
OUT_DIR = "./exports/zz_stress/topview"
DPI     = 300
EXPORT_DAT = False          # set True to also export *.dat for each image

# >>> PASTE YOUR RL / Z VALUES HERE (millimetres or metres as per your model) <<<
# You can separate by commas or keep as a Python list—both work.
RL_VALUES = """
987.34, 1002.54, 1012.34, 1019.49,
1023.315, 1025.34, 1034.72, 1044.415,
1053.81, 1062.27, 1072.3, 1075.245
"""

# Contour scaling for σzz (effective) [Pa]
# cmin: lower bound (more compressive if negative); cmax: upper bound (usually 0 for effective σzz at crown);
# interval: spacing between contour ticks. As a rule of thumb:
#   - Choose cmin so the lowest colors appear where you expect peak compression.
#   - Keep cmax at 0.0 for σzz if you only want compressive (negative) to 0.
#   - Set interval to 1/2–1/4 of |cmin| to get ~4–8 bands (e.g., cmin=-1.5e6 → interval≈0.75e6).
CMIN = -3e6
CMAX =  0.0
INTERVAL = 1.5e6
# ============ END USER CONFIG – STOP EDITING =============
# =========================================================


def _parse_rl_values(maybe_text_or_list):
    """Accept a list OR a comma/space separated string and return a clean list of floats."""
    if isinstance(maybe_text_or_list, str):
        raw = maybe_text_or_list.replace("\n", " ").split(",")
        vals = []
        for chunk in raw:
            for t in chunk.split():
                try:
                    vals.append(float(t))
                except ValueError:
                    pass
        return vals
    # already a list/tuple
    return [float(v) for v in maybe_text_or_list]


def export_zz_top(z_value,
                  out_dir=OUT_DIR,
                  out_name=None,
                  cmin=CMIN, cmax=CMAX,
                  interval=INTERVAL,
                  dpi=DPI,
                  export_dat=EXPORT_DAT):
    """
    Export a top-down view of effective σzz on a horizontal cut plane at z_value.

    Parameters
    ----------
    z_value : float      Elevation (z-coordinate) of the cut plane.
    out_dir : str        Directory for export.
    out_name : str|None  Optional filename; if None, uses 'zz_effective_topview_z{int(z)}.png'
    cmin, cmax : float   Contour min/max. Keep cmax=0.0 for compressive-only effective σzz.
    interval : float     Distance between contour ticks (choose ~1/2–1/4 of |cmin|).
    dpi : int            Export resolution.
    export_dat : bool    Also export plot data (*.dat) if True.
    """
    # Basic sanity
    if not (isfinite(cmin) and isfinite(cmax) and isfinite(interval) and interval > 0):
        raise ValueError("cmin/cmax/interval must be finite; interval > 0.")
    if cmin >= cmax:
        raise ValueError("CMIN must be < CMAX (e.g., -1.5e6 < 0.0).")

    os.makedirs(out_dir, exist_ok=True)
    if out_name is None:
        # keep original style: integer-rounded Z in the name
        out_name = f"zz_effective_topview_z{int(round(z_value))}.png"

    outfile_png = os.path.join(out_dir, out_name).replace("\\", "/")
    outfile_dat = outfile_png.rsplit(".", 1)[0] + ".dat"

    it.command(f"""
    plot create
    plot clear
    plot active on
    plot target active on
    plot background 'white'
    plot outline active on width 2 color 'black'

    plot legend active true heading size 94 color 'black' copyright size 40 color 'black' \
        placement left size 25,50 \
        step active false time-real active false time-model active false \
        title-customer active false view-info active false
    plot title-job active false
    plot title active false

    plot view projection parallel
    plot view reset
    plot view dip 0
    plot view dip-direction 0
    plot view roll 0

    plot item create zone active on \
        contour stress-effective quantity zz log off \
            method average null fluid off mechanical on thermal off \
        ramp rainbow minimum {cmin} maximum {cmax} interval {interval} \
            reversed off above 'red' below 'blue' \
        polygons fill on outline active on width 1 color 'black' \
            polygon-transparency 0 outline-transparency 80 lighting on offset 0.5 2 \
        null-faces-only off \
        map axis xyz rotate (0,0,0) translate (0,0,0) scale (1,1,1) \
        deformation-factor active off \
        hide-null mechanical on thermal off fluid off \
        transparency 0 \
        cut active on type plane \
            surface on front off back off \
            origin (0,0,{z_value}) normal (0,0,1) \
        clip active off \
        legend active on \
            title active true text "" size 55 family 'Times New Roman' style bold color 'black' \
            cut title active true size 44 family 'Arial' style normal color 'black' \
            map active true  size 44 family 'Arial' style normal color 'black' \
            hide-null active false \
            deformation-factor active true size 44 family 'Arial' style normal color 'black' \
            count active false \
            contour labels active true size 44 family 'Arial' style normal color 'black' \
            labels-maximum 20 format 0 precision 2 \
            method active true size 44 family 'Arial' style normal color 'black'

    plot item create axes active on \
        axis-x color 'red'  draw-positive on draw-negative off label-positive 'X' \
        axis-y color 'lime' draw-positive on draw-negative off label-positive 'Y' \
        axis-z color 'blue' draw-positive on draw-negative off label-positive 'Z' \
        screen 10 10 scale 5 \
        font size 10 family 'Arial' style bold \
        transparency 0 \
        legend active off

    plot export bitmap filename="{outfile_png}" dpi={dpi}
    """)

    if export_dat:
        it.command(f'plot export data filename "{outfile_dat}"')

    print(f"[OK] Exported σzz top-view slice @ z = {z_value:.3f}  →  {outfile_png}")
    if export_dat:
        print(f"     ↳ also exported data: {outfile_dat}")


# -----------------------------
# Batch run
# -----------------------------
def run_batch():
    rl_list = _parse_rl_values(RL_VALUES)
    if not rl_list:
        raise RuntimeError("No RL values found. Edit RL_VALUES in the CONFIG block.")
    print(f"Exporting {len(rl_list)} slices to: {OUT_DIR}")
    print(f"Contour range = [{CMIN:g}, {CMAX:g}], interval = {INTERVAL:g}, dpi = {DPI}")
    for z in rl_list:
        export_zz_top(z)

# kick off
run_batch()
