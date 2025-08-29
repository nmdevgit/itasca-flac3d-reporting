# FLAC3D Slice Export → Word Report

This repository provides a two-step workflow to automate the generation of Word reports from FLAC3D slice outputs. The first script (`data-export-automated.py`) is designed to run inside the FLAC3D Python Console and exports bitmap slice images for displacement magnitude, maximum principal effective stress, minimum principal effective stress, and zone state. 

Images are written to structured folders under `./exports/**/<xslice|yslice>/` with filenames like `x_slice_disp_100.bmp`. The second script (`create-docx-summary.py`) is run with standard Python and scans these exported folders, converts the BMP files to JPG (with size control), and compiles them into formatted Word documents. 

Each slice is represented across two pages: one with displacement and max principal stress, and another with min principal stress and zone state. The output files are `exports/xslice_figures.docx` and `exports/yslice_figures.docx`. 

The workflow requires FLAC3D with the Python console, plus Python 3.9+ with the `python-docx` and `Pillow` libraries (`pip install python-docx Pillow`). To use, first open FLAC3D and run `data-export-automated.py` to create the image exports, then from your shell run `python create-docx-summary.py` to generate the Word reports. Slice range and step can be adjusted in the export script, while page layout and image sizing can be tuned in the docx script. Missing image sets are handled gracefully with warnings. The result is a repeatable process for producing consistent reviewer-ready Word reports of FLAC3D model slice results.
