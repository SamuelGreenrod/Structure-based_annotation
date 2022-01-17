#!/usr/bin/env bash
 
#SBATCH --job-name=jobid
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu
#SBATCH --time=5:00:00
#SBATCH --wait
#SBATCH --output=%x-%j.log
 
# Load AlphaFold module - CHANGE TO MODULE ON LOCAL CLUSTER
module load bio/AlphaFold/2.0.0-fosscuda-2020b
 
# Path to genetic databases - CHANGE TO DATABASE PATHS FOR LOCAL CLUSTER
export ALPHAFOLD_DATA_DIR=/mnt/bb/striped/alphafold_db/20210908/
 
# Optional: uncomment to change number of CPU cores to use for hhblits/jackhmmer
# export ALPHAFOLD_HHBLITS_N_CPU=8
# export ALPHAFOLD_JACKHMMER_N_CPU=8
 
# Run AlphaFold - CHANGE TO ALPHAFOLD COMMAND FOR LOCAL CLUSTER (don't change: --fasta_paths=input_file and --output_dir=output_folder)
alphafold --fasta_paths=input_file --max_template_date=2020-05-14 --preset=full_dbs --output_dir=output_folder --model_names=model_1,model_2,model_3,model_4,model_5