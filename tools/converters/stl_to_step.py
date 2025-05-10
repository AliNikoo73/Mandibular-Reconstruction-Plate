#!/usr/bin/env python3
"""
STL to STEP conversion utility for the mandibular reconstruction plate project.
Uses FreeCAD for the conversion process.
"""

import os
import sys
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_stl_to_step(input_file, output_file=None, tolerance=0.01):
    """
    Convert STL mesh file to STEP CAD format using FreeCAD.
    
    Args:
        input_file (str): Path to input STL file
        output_file (str): Path to output STEP file (optional)
        tolerance (float): Conversion tolerance (default: 0.01)
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return False
    
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".step"
    
    try:
        # Import FreeCAD modules
        import FreeCAD
        import Import
        import Part
        import Mesh
        
        logger.info(f"Converting {input_file} to {output_file}")
        
        # Import STL
        mesh_obj = Mesh.Mesh(input_file)
        
        # Create shape from mesh
        shape = Part.Shape()
        shape.makeShapeFromMesh(mesh_obj.Topology, tolerance)
        
        # Export to STEP
        Part.export([shape], output_file)
        
        logger.info("Conversion completed successfully")
        return True
        
    except ImportError:
        logger.error("FreeCAD Python modules not found. Make sure FreeCAD is installed and in Python path.")
        return False
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return False

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Convert STL files to STEP format")
    parser.add_argument("input", help="Input STL file path")
    parser.add_argument("-o", "--output", help="Output STEP file path")
    parser.add_argument("-t", "--tolerance", type=float, default=0.01, help="Conversion tolerance (default: 0.01)")
    args = parser.parse_args()
    
    success = convert_stl_to_step(args.input, args.output, args.tolerance)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 