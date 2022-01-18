#!/usr/bin/env bash
 
#SBATCH --job-name=Transporters
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=24:00:00
#SBATCH --output=%x-%j.log

python Structure-based_annotation.py -i Transporters.fasta -o Transporters_annotation

