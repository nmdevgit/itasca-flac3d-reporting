# ---------------------------------------------
# zz_slice_topview.py  (run in FLAC3D Python console)
# Export a top-down cut-plane view of Zone ZZ Effective Stress at z.
# ---------------------------------------------
import itasca as it
import os

def export_zz_top(z_value,
                  out_dir="./exports/zz_stress/topview",
                  out_name=None,
                  cmin=-3.0e6, cmax=0.0,
                  interval=1.5e6,
                  dpi=300,
                  export_dat=False):
    """
    Export a top-down view of effective σzz on a horizontal cut plane.

    Parameters
    ----------
    z_value : float
        Elevation (z-coordinate) of the cut plane.
    out_dir : str
        Directory where the export will be saved.
    out_name : str or None
        Output filename for the PNG (auto-named if None).
    cmin, cmax : float
        Contour scale minimum and maximum.
    interval : float
        Contour interval between ticks.
    dpi : int
        Resolution for the exported bitmap.
    export_dat : bool
        If True, also export a reloadable plot-data (.dat) file.
    """
    os.makedirs(out_dir, exist_ok=True)
    if out_name is None:
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

    print(f"Exported σzz top-view slice at z={z_value}: {outfile_png}")
    if export_dat:
        print(f"Also exported plot data: {outfile_dat}")


export_zz_top(1035.0)                  # PNG only
# export_zz_top(1035.0, export_dat=True) # PNG + .dat
