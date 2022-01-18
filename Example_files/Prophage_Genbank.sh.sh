#!/usr/bin/env bash
 
#SBATCH --job-name=PHASTERYO002_1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=24:00:00
#SBATCH --output=%x-%j.log

python Structure-based_annotation.py -i Prophage_Genbank.gbk -p "Hypothetical" -o Prophage_hypothetical_annotation

