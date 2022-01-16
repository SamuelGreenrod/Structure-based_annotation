## Structure-based_annotation

# Program overview
This repository contains scripts required to annotate coding sequences based on their predicted 3d structures. The pipeline takes predicted protein sequences as input, either extracted from a Genbank file or in a multifasta or single fasta file. Protein sequences are then run through Alphafold 2.0 to determine their predicted structures. Predicted protein structures are then run through DeepFRI, a structure-function prediction tool, to predict their potential function. 

If you find this tool useful and use it in your own publications then please reference the original publication which this program was written for and tested in: https://www.biorxiv.org/content/10.1101/2021.10.20.465097v1.full. Thank you!

If you have any problems using these scripts then please create a GitHub issue. Also, if you have any advice or comments to improve the scripts then please also add an issue and we can discuss updating the scripts. Thank you and I hope this is useful!

# Dependencies
* [Python](https://www.python.org/) v3.7
* Access to a Slurm scheduler (for sbatch script submissions) - Alphafold takes a long time to Slurm submission is recommended.
* Alphafold v2.0 (https://github.com/kuixu/alphafold)
* DeepFRI (https://github.com/flatironinstitute/DeepFRI)

# Installation
1. Download scripts to working directory:
```
# Download scripts
git clone https://github.com/SamuelGreenrod/Structure-based_annotation

# Move to working directory
cp Structure-based_annotation/*.py .
cp Structure-based_annotation/*.sh .
```
2. Install Alphafold 2.0
3. Install DeepFRI:
```
# Create conda environment to install DeepFRI dependencies
conda create -n Structure-based_annotation python=3.7
conda activate Structure-based_annotation

# Download DeepFRI scripts
git clone https://github.com/flatironinstitute/DeepFRI
cd DeepFRI/

# Install DeepFRI dependencies
pip install .
cd ..
```

# File edits before running
For the program to run correctly, the "Alphafold_sbatch_skeleton.sh" slurm script must be edited to include the Alphafold loading and running commands used by your own cluster. This will include:

* Modifying the --gres and --partition commands to decide which gpus should be used, or removed if only cpus are used.
* Modify the --time command to account for how long the longest structure-prediction will take (will take longer depending on cpus or gpus used, and how many cpus used.
* Optionally insert a loading command to load Alphafold as a module.
* Insert a path to the Alphafold databases. 
* Modify command to run Alphafold - original command is an adaptation of the traditional Alphafold command for my local cluster. Note: --output_dir=output_folder must be kept the same for the program to function properly.


# Running Structure-based_annotation
To generate predicted protein functions, create an sbatch script and run the `Structure-based_annotation.py` script with the following options:
* `-i, --input` str, Genbank, multifasta, or single fasta file containing proteins of interest.
* `-p, --protein_label` str, if Genbank provided a string must be provided which is searched for. CDS with annotations containing string will be annotated.
* `-o, --output` str, name of output folder containing results.

Generated output folders/files:
* `Multifasta_files` folder, contains multifasta file either of selected amino acid sequences from Genbank or just input multifasta, if provided.
* `Singlefasta_files` folder, contains single fasta files of selected amino acid sequences from Genbank or of fasta sequences in multifasta or single fasta, if provided.
* `Slurm scripts` folder, contains Slurm sbatch scripts for submitting each single fasta to Alphafold 2.0. Adapted from Alphafold_sbatch_skeleton.sh file.
* `Alphafold_output` folder, contains folders with results from Alphafold for each single fasta. Output used in DeepFRI is ranked_0.pdb structure file which is the best model generated in the Alphafold run.
* `DeepFRI_output` folder, contains folders with results from DeepFRI for each single fasta pdb file from Alphafold output folder. Each DeepFRI_output folder contains:
  * `#NAME_MF_pred_scores.json` file, contains predicted goterms and gonames for each chain in pdb file
  * `#NAME_MF_predictions.csv` file, contains protein_id, predicted GO term, DeepFRI score (>0.5 considered significant true hit), and GO term name.
`DeepFRI_output folder` also contains:
  * `Best_deepfri_hits.csv` file, summary file containing top hits for each protein run compiled into one file for easy analysis.
