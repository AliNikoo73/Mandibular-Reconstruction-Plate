# Project Structure

```
.
├── README.md                    # Project overview and documentation
├── data/                       
│   ├── ct_scans/                # Patient CT scan data (anonymized)
│   ├── measurements/            # Clinical measurements data
│   └── mandible_models/         # Base mandible models
│
├── cad/
│   ├── plate_designs/           # CAD models of fixation plates
│   │   ├── titanium/            # Traditional Ti-6Al-4V designs
│   │   ├── niti/                # Novel NiTi designs
│   │   └── patient_specific/    # Custom designs for case studies
│   ├── mandible_models/         # 3D models of mandibles
│   └── material_samples/        # Test samples for material validation
│
├── fea/
│   ├── models/                  # FEA model definitions
│   │   ├── healthy/             # Healthy mandible models
│   │   └── reconstructed/       # Reconstructed mandible models
│   ├── simulations/             # Simulation configurations
│   │   ├── bite_forces/         # Different bite force scenarios
│   │   └── healing_stages/      # Models for different healing periods
│   └── results/                 # Simulation outputs and visualizations
│
├── manufacturing/
│   ├── slm_parameters/          # SLM process parameters
│   ├── toolpaths/               # Manufacturing toolpaths
│   └── qc/                      # Quality control protocols
│
├── analysis/
│   ├── scripts/                 # Analysis scripts and code
│   ├── stress_distribution/     # Stress analysis results
│   └── reports/                 # Generated reports and figures
│
├── tools/                       # Helper tools and utilities
│   ├── mimics/                  # Mimics project files
│   │   ├── templates/           # Segmentation templates
│   │   └── masks/               # Segmentation masks
│   ├── 3-matic/                 # 3-matic project files for design
│   └── converters/              # File format conversion scripts
│
├── literature/                  # Relevant research papers and references
│
└── docs/                        # Project documentation
    ├── protocols/               # Experimental protocols
    ├── presentations/           # Slides and presentation materials
    └── figures/                 # Generated figures for publications
``` 