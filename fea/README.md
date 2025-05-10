# FEA Directory

This directory contains all Finite Element Analysis (FEA) materials for the mandibular reconstruction plate project.

## Contents

- `models/`: FEA model definitions
  - `healthy/`: Models of healthy mandibles for baseline comparison
  - `reconstructed/`: Models of reconstructed mandibles with fixation plates
- `simulations/`: Simulation configurations
  - `bite_forces/`: Different bite force scenarios (incisal, molar, etc.)
  - `healing_stages/`: Models representing different healing periods post-surgery
- `results/`: Simulation outputs and visualizations

## Software

- Primary FEA software: ANSYS Mechanical
- Preprocessing: ANSYS SpaceClaim, Mimics
- File formats: .dat, .scdoc, .msh, .out, .vtk

## Analysis Guidelines

1. Mesh quality checks required before running simulations
2. Document all material properties used in each simulation
3. Standard load cases should be applied consistently across all models
4. Save raw results and processed visualizations separately
5. Include a summary report with each simulation run 