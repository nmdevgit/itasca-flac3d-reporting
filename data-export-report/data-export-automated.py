# data-export-automated.py
# To be executed in FLAC3D Python Console

import itasca as it
import os

# ------------------------------
# Directories
# ------------------------------
base_dir = "./exports"
dirs = {
    "disp_x":  os.path.join(base_dir, "displacements",  "xslice"),
    "disp_y":  os.path.join(base_dir, "displacements",  "yslice"),
    "disp_z":  os.path.join(base_dir, "displacements",  "zslice"),
    "max_x":   os.path.join(base_dir, "max_principal",  "xslice"),
    "max_y":   os.path.join(base_dir, "max_principal",  "yslice"),
    "max_z":   os.path.join(base_dir, "max_principal",  "zslice"),
    "min_x":   os.path.join(base_dir, "min_principal",  "xslice"),
    "min_y":   os.path.join(base_dir, "min_principal",  "yslice"),
    "min_z":   os.path.join(base_dir, "min_principal",  "zslice"),
    "state_x": os.path.join(base_dir, "zone_state",     "xslice"),
    "state_y": os.path.join(base_dir, "zone_state",     "yslice"),
    "state_z": os.path.join(base_dir, "zone_state",     "zslice"),
    # σzz (effective) stress
    "zz_x":    os.path.join(base_dir, "zz_stress",      "xslice"),
    "zz_y":    os.path.join(base_dir, "zz_stress",      "yslice"),
    "zz_z":    os.path.join(base_dir, "zz_stress",      "zslice"),
}
for p in dirs.values():
    os.makedirs(p, exist_ok=True)

# ----------------------------------------------------
# Helper: plane parameters for a given axis and value
# ----------------------------------------------------
def _plane_params(axis, i):
    axis = axis.lower()
    if axis == "x":
        return f"({i},0,0)", "(1,0,0)", "90", "90"   # origin, normal, dip, dip_dir
    if axis == "y":
        return f"(0,{i},0)", "(0,1,0)", "90", "0"
    if axis == "z":
        # top-down view for horizontal slice
        return f"(0,0,{i})", "(0,0,1)", "0", "0"
    raise ValueError("axis must be 'x', 'y', or 'z'")

# ----------------------------------------------------
# Displacement Slices
# ----------------------------------------------------
def export_displacement_slices(axis="x", start=90, end=265, step=5):
    axis = axis.lower()
    for i in range(start, end + 1, step):
        origin, normal, dip, dip_dir = _plane_params(axis, i)
        filename = f"{axis}_slice_disp_{i}.bmp"
        filepath = os.path.join(dirs[f"disp_{axis}"], filename)

        it.command(f'''
            plot create "Disp {axis.upper()}-Slice @ {i}"
            plot clear
            plot background 'white'
            plot outline active on width 2 color 'black'

            plot item create zone active on ...
                contour displacement component magnitude log off ...
                ramp rainbow minimum automatic maximum automatic interval automatic ...
                polygons fill on outline active on width 1 ...
                cut active on type plane ...
                    surface on front off back off ...
                    origin {origin} normal {normal}

            plot view projection parallel
            plot view reset
            plot view dip {dip}
            plot view dip-direction {dip_dir}
            plot view roll 0

            plot export bitmap filename="{filepath}" dpi=300
        ''')

# ----------------------------------------------------
# Max Principal Effective Stress
# ----------------------------------------------------
def export_max_principal_slices(axis="x", start=90, end=265, step=5):
    axis = axis.lower()
    for i in range(start, end + 1, step):
        origin, normal, dip, dip_dir = _plane_params(axis, i)
        filename = f"{axis}_slice_max_principal_{i}.bmp"
        filepath = os.path.join(dirs[f"max_{axis}"], filename)

        it.command(f'''
            plot create "MaxEffStress_{axis.upper()}{i}"
            plot clear
            plot active on
            plot target active on
            plot background 'white'
            plot outline active on width 2 color 'black'

            plot item create zone active on ...
                contour stress-effective quantity maximum log off ...
                method average ...
                ramp rainbow minimum automatic maximum automatic interval automatic ...
                polygons fill on outline active on width 1 ...
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

            plot export bitmap filename="{filepath}" dpi=300
        ''')

# ----------------------------------------------------
# Min Principal Effective Stress
# ----------------------------------------------------
def export_min_principal_slices(axis="x", start=90, end=265, step=5):
    axis = axis.lower()
    for i in range(start, end + 1, step):
        origin, normal, dip, dip_dir = _plane_params(axis, i)
        filename = f"{axis}_slice_min_principal_{i}.bmp"
        filepath = os.path.join(dirs[f"min_{axis}"], filename)

        it.command(f'''
            plot create "MinEffStress_{axis.upper()}{i}"
            plot clear
            plot active on
            plot target active on
            plot background 'white'
            plot outline active on width 2 color 'black'

            plot item create zone active on ...
                contour stress-effective quantity minimum log off ...
                method average ...
                ramp rainbow minimum automatic maximum automatic interval automatic ...
                polygons fill on outline active on width 1 ...
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

            plot export bitmap filename="{filepath}" dpi=300
        ''')

# ----------------------------------------------------
# Zone State
# ----------------------------------------------------
def export_zone_state_slices(axis="x", start=90, end=265, step=5):
    axis = axis.lower()
    for i in range(start, end + 1, step):
        origin, normal, dip, dip_dir = _plane_params(axis, i)
        filename = f"{axis}_slice_state_{i}.bmp"
        filepath = os.path.join(dirs[f"state_{axis}"], filename)

        it.command(f'''
            plot create "ZoneState_{axis.upper()}{i}"
            plot clear
            plot background 'white'
            plot outline active on width 2 color 'black'

            plot item create zone active on ...
                label State Average ...
                polygons fill on outline active on width 1 ...
                cut active on type plane ...
                    surface on front off back off ...
                    origin {origin} normal {normal}

            plot view projection parallel
            plot view reset
            plot view dip {dip}
            plot view dip-direction {dip_dir}
            plot view roll 0

            plot export bitmap filename="{filepath}" dpi=300
        ''')

# ----------------------------------------------------
# σzz (Effective) Stress
# ----------------------------------------------------
def export_zz_stress_slices(axis="x", start=90, end=265, step=5):
    """
    Exports slices of effective vertical stress (sigma_zz).
    """
    axis = axis.lower()
    for i in range(start, end + 1, step):
        origin, normal, dip, dip_dir = _plane_params(axis, i)
        filename = f"{axis}_slice_zz_{i}.bmp"
        filepath = os.path.join(dirs[f"zz_{axis}"], filename)

        it.command(f'''
            plot create "ZZStress_{axis.upper()}{i}"
            plot clear
            plot active on
            plot target active on
            plot background 'white'
            plot outline active on width 2 color 'black'

            plot item create zone active on ...
                contour stress-effective quantity zz log off ...
                method average ...
                ramp rainbow minimum automatic maximum automatic interval automatic ...
                polygons fill on outline active on width 1 ...
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

            plot export bitmap filename="{filepath}" dpi=300
        ''')

# -----------------
# Run all exports
# -----------------
# X and Y (vertical slices)
export_displacement_slices("x"); export_displacement_slices("y")
export_max_principal_slices("x"); export_max_principal_slices("y")
export_min_principal_slices("x"); export_min_principal_slices("y")
export_zone_state_slices("x");    export_zone_state_slices("y")
export_zz_stress_slices("x");     export_zz_stress_slices("y")

# Z (horizontal slices)
export_displacement_slices("z", start=980, end=1080, step=5)
export_max_principal_slices("z",  start=980, end=1080, step=5)
export_min_principal_slices("z",  start=980, end=1080, step=5)
export_zone_state_slices("z",     start=980, end=1080, step=5)
export_zz_stress_slices("z",      start=980, end=1080, step=5)
