#!/usr/bin/env python3
"""
Stress distribution analysis tool for mandibular reconstruction plate project.
Processes ANSYS result files to calculate stress distribution statistics.
"""

import os
import sys
import argparse
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_fea_results(result_file):
    """
    Load FEA results from file.
    
    Args:
        result_file (str): Path to result file (supports .csv, .vtk formats)
        
    Returns:
        dict: Dictionary containing result data
    """
    try:
        ext = os.path.splitext(result_file)[1].lower()
        
        if ext == '.csv':
            df = pd.read_csv(result_file)
            return {
                'node_ids': df['Node'].values if 'Node' in df else np.arange(len(df)),
                'coordinates': df[['X', 'Y', 'Z']].values if all(x in df for x in ['X', 'Y', 'Z']) else None,
                'von_mises': df['von_Mises'].values if 'von_Mises' in df else None,
                'max_principal': df['S1'].values if 'S1' in df else None,
                'min_principal': df['S3'].values if 'S3' in df else None,
                'displacement': df['USum'].values if 'USum' in df else None
            }
            
        elif ext == '.vtk':
            import pyvista as pv
            mesh = pv.read(result_file)
            result = {
                'node_ids': np.arange(mesh.n_points),
                'coordinates': mesh.points
            }
            
            # Extract available point data
            point_data = mesh.point_data
            for key in ['von_Mises', 'S1', 'S3', 'USum']:
                if key in point_data:
                    result[key.lower()] = point_data[key]
                
            return result
            
        else:
            logger.error(f"Unsupported file format: {ext}")
            return None
            
    except Exception as e:
        logger.error(f"Error loading FEA results: {str(e)}")
        return None

def analyze_stress_distribution(result_data, material='bone', output_dir=None):
    """
    Analyze stress distribution in the model.
    
    Args:
        result_data (dict): Result data dictionary
        material (str): Material type ('bone', 'plate', 'screw')
        output_dir (str): Directory for output files
        
    Returns:
        dict: Dictionary containing analysis results
    """
    try:
        # Define material yield/ultimate stress for comparison
        material_limits = {
            'bone': {'yield': 80, 'ultimate': 120},  # MPa
            'titanium': {'yield': 800, 'ultimate': 900},  # MPa
            'niti': {'yield': 195, 'ultimate': 754},  # MPa
            'screw': {'yield': 800, 'ultimate': 900}  # MPa
        }
        
        limits = material_limits.get(material.lower(), material_limits['bone'])
        
        # Extract stress values
        vm_stress = result_data.get('von_mises')
        if vm_stress is None:
            logger.error("No von Mises stress data found in results")
            return None
            
        # Calculate statistics
        stats = {
            'mean': np.mean(vm_stress),
            'median': np.median(vm_stress),
            'std_dev': np.std(vm_stress),
            'max': np.max(vm_stress),
            'min': np.min(vm_stress),
            'percentile_95': np.percentile(vm_stress, 95),
            'yield_ratio': np.max(vm_stress) / limits['yield'],
            'ultimate_ratio': np.max(vm_stress) / limits['ultimate'],
            'nodes_exceeding_yield': np.sum(vm_stress > limits['yield']),
            'percent_exceeding_yield': 100 * np.sum(vm_stress > limits['yield']) / len(vm_stress)
        }
        
        # Generate plots if output directory is provided
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            # Histogram of stress distribution
            plt.figure(figsize=(10, 6))
            plt.hist(vm_stress, bins=50, alpha=0.7, color='steelblue')
            plt.axvline(limits['yield'], color='red', linestyle='--', label=f"Yield Stress ({limits['yield']} MPa)")
            plt.axvline(limits['ultimate'], color='darkred', linestyle='--', label=f"Ultimate Stress ({limits['ultimate']} MPa)")
            plt.axvline(stats['percentile_95'], color='green', linestyle=':', label=f"95th Percentile ({stats['percentile_95']:.2f} MPa)")
            plt.xlabel('von Mises Stress (MPa)')
            plt.ylabel('Frequency')
            plt.title(f'Stress Distribution - {material.capitalize()}')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.savefig(os.path.join(output_dir, f'stress_histogram_{material}.png'), dpi=300)
            
            # Save statistics to CSV
            pd.DataFrame([stats]).to_csv(os.path.join(output_dir, f'stress_stats_{material}.csv'), index=False)
        
        return stats
        
    except Exception as e:
        logger.error(f"Error analyzing stress distribution: {str(e)}")
        return None

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Analyze stress distribution from FEA results")
    parser.add_argument("result_file", help="Path to FEA result file (.csv or .vtk)")
    parser.add_argument("-m", "--material", choices=['bone', 'titanium', 'niti', 'screw'], 
                        default='bone', help="Material type for stress limits")
    parser.add_argument("-o", "--output", help="Output directory for results")
    args = parser.parse_args()
    
    # Load results
    result_data = load_fea_results(args.result_file)
    if result_data is None:
        return 1
    
    # Analyze stress distribution
    stats = analyze_stress_distribution(result_data, args.material, args.output)
    if stats is None:
        return 1
    
    # Print summary to console
    print(f"\nStress Analysis Summary for {args.material.capitalize()}:")
    print(f"  Mean Stress: {stats['mean']:.2f} MPa")
    print(f"  Maximum Stress: {stats['max']:.2f} MPa")
    print(f"  95th Percentile: {stats['percentile_95']:.2f} MPa")
    print(f"  Yield Ratio: {stats['yield_ratio']:.3f}")
    print(f"  Elements Exceeding Yield: {stats['nodes_exceeding_yield']} ({stats['percent_exceeding_yield']:.2f}%)")
    
    if args.output:
        print(f"\nDetailed results saved to: {args.output}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 