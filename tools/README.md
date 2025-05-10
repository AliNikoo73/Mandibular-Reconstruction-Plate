# Tools Directory

This directory contains specialized tools and software-specific files for the mandibular reconstruction plate project.

## Contents

- `mimics/`: Materialise Mimics project files for medical image processing
  - `templates/`: Segmentation templates for consistent CT scan processing
  - `masks/`: Segmentation masks for different anatomical structures
- `3-matic/`: 3-matic design files for medical model manipulation
- `converters/`: Utility scripts for file format conversion

## Software Requirements

- Materialise Mimics (Version 24.0 or later)
- Materialise 3-matic (Version 16.0 or later)
- Python 3.8+ (for converter scripts)

## Usage Guidelines

### Mimics Workflow

1. Import DICOM data into Mimics
2. Apply appropriate segmentation template
3. Generate 3D model
4. Export to 3-matic for design modification

### File Conversion

For converting between file formats, use the scripts in the `converters/` directory:
- `stl_to_step.py`: Convert STL mesh to STEP CAD file
- `dicom_to_nifti.py`: Convert DICOM series to NIfTI format
- `ansys_to_vtk.py`: Convert ANSYS result files to VTK for visualization 