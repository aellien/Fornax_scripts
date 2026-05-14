#!/usr/bin/env bash
#!/bin/bash
#SBATCH --job-name=fornax_synth
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --output /n08data/ellien/Euclid_Fornax/logs/%x.%j.out
#SBATCH --error  /n08data/ellien/Euclid_Fornax/logs/%x.%j.err

source /home/ellien/.bashrc
conda activate dawis
python -W"ignore" /home/ellien/Euclid_Fornax/Fornax_scripts/make_synthesis_euc_edfn.py

exit 0
