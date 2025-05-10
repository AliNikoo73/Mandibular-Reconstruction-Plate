#!/usr/bin/env python3
"""
DICOM to NIfTI conversion utility for the mandibular reconstruction plate project.
Converts DICOM image series to NIfTI format for easier processing.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_dicom_to_nifti(input_dir, output_file=None):
    """
    Convert DICOM series to NIfTI format.
    
    Args:
        input_dir (str): Directory containing DICOM files
        output_file (str): Output NIfTI file path (optional)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import SimpleITK as sitk
        
        if not os.path.isdir(input_dir):
            logger.error(f"Input directory not found: {input_dir}")
            return False
        
        if output_file is None:
            output_file = os.path.join(os.path.dirname(input_dir), 
                                     os.path.basename(input_dir) + ".nii.gz")
        
        logger.info(f"Reading DICOM series from {input_dir}")
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(input_dir)
        
        if not dicom_names:
            logger.error(f"No DICOM series found in {input_dir}")
            return False
        
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        
        logger.info(f"Writing NIfTI file to {output_file}")
        sitk.WriteImage(image, output_file)
        
        logger.info("Conversion completed successfully")
        return True
        
    except ImportError:
        logger.error("SimpleITK not found. Make sure it is installed: pip install SimpleITK")
        return False
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return False

def find_dicom_directories(base_dir):
    """Find directories containing DICOM files."""
    try:
        import SimpleITK as sitk
        dicom_dirs = []
        
        for root, dirs, files in os.walk(base_dir):
            if any(file.lower().endswith(('.dcm', '.ima')) for file in files):
                try:
                    # Check if this is a valid DICOM series
                    reader = sitk.ImageSeriesReader()
                    series_IDs = reader.GetGDCMSeriesIDs(root)
                    if series_IDs:
                        dicom_dirs.append(root)
                except:
                    pass
        
        return dicom_dirs
    except ImportError:
        logger.error("SimpleITK not found. Make sure it is installed: pip install SimpleITK")
        return []

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Convert DICOM series to NIfTI format")
    parser.add_argument("input", help="Input DICOM directory or base directory to search for DICOM series")
    parser.add_argument("-o", "--output", help="Output NIfTI file path")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search recursively for DICOM directories")
    args = parser.parse_args()
    
    if args.recursive:
        dicom_dirs = find_dicom_directories(args.input)
        if not dicom_dirs:
            logger.error(f"No DICOM directories found in {args.input}")
            return 1
        
        logger.info(f"Found {len(dicom_dirs)} DICOM directories")
        success = True
        for dicom_dir in dicom_dirs:
            output_file = None
            if args.output:
                base_name = Path(args.output).stem
                ext = Path(args.output).suffix
                dir_name = os.path.basename(dicom_dir)
                output_file = os.path.join(os.path.dirname(args.output), 
                                         f"{base_name}_{dir_name}{ext}")
            
            success = convert_dicom_to_nifti(dicom_dir, output_file) and success
        
        return 0 if success else 1
    else:
        success = convert_dicom_to_nifti(args.input, args.output)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 