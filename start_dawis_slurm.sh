#!/usr/bin/env bash
#!/bin/bash
#SBATCH --job-name=lsb_fornax
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output /n08data/ellien/Euclid_Fornax/logs/fornax.%x.%j.out 
#SBATCH --error  /n08data/ellien/Euclid_Fornax/logs/fornax.%x.%j.err

source /home/ellien/.bashrc
conda activate dawis

python -W"ignore" /home/ellien/Euclid_Fornax/Fornax_scripts/dawis_input.py

exit 0
EOT