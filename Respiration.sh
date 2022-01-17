#!/usr/bin/env bash
 
#SBATCH --job-name=Respiration
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=24:00:00
#SBATCH --output=%x-%j.log

python Main_python_script.py -i Respiration.fasta -o Respiration_prediction

