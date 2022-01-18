# Structure-based_annotation

## Program overview
This repository contains Python scripts required to annotate coding sequences based on their predicted 3d structures. The pipeline takes predicted protein sequences as input, either extracted from a Genbank file, multifasta, or single fasta file format. Protein sequences are then extracted and run through Alphafold 2.0 to determine their predicted structures. Predicted protein structures are then run through DeepFRI, a structure-function prediction tool, to predict their potential function. 

If you find this tool useful and use it in your own publications then please reference the original publication which this program was written for and tested in: https://www.biorxiv.org/content/10.1101/2021.10.20.465097v1.full. Thank you!

If you have any problems using these scripts then please create a GitHub issue. Also, if you have any advice or comments to improve the scripts then please also add an issue and we can discuss updating the scripts. Thank you and I hope this is useful!

## Dependencies
* [Python](https://www.python.org/) v3.7
* Access to a Slurm scheduler (for sbatch script submissions) - Alphafold takes a long time so Slurm submission is recommended.
* Alphafold v2.0 (https://github.com/kuixu/alphafold)
* DeepFRI (https://github.com/flatironinstitute/DeepFRI)

## Installation
1. Create conda environment to install dependencies
```
conda create -n Structure-based_annotation python=3.7
conda activate Structure-based_annotation
```
2. Download scripts to working directory:
```
# Download scripts
git clone https://github.com/SamuelGreenrod/Structure-based_annotation

# Move scripts to working directory
cp Structure-based_annotation/Scripts/*.py .
cp Structure-based_annotation/Scripts/*.sh .
```
3. Install Alphafold 2.0 (See here: https://github.com/kuixu/alphafold)
4. Install DeepFRI and trained models:
```
# Download DeepFRI scripts
git clone https://github.com/flatironinstitute/DeepFRI
cd DeepFRI/

# Install DeepFRI dependencies
pip install .
cd ..

# Install trained models
wget https://users.flatironinstitute.org/vgligorijevic/public_www/DeepFRI_data/newest_trained_models.tar.gz
tar xvzf newest_trained_models.tar.gz
```

## File edits before running
For the program to run correctly, the "Alphafold_sbatch_skeleton.sh" slurm script must be edited to include the Alphafold loading and running commands used by your own cluster. This will include:

* Modifying the --gres and --partition commands to decide which gpus should be used, or removed if only cpus are used.
* Modify the --time command to account for how long the longest structure-prediction will take (will take longer depending on cpus or gpus used, and how many cpus used.
* Optionally insert a loading command to load Alphafold as a module.
* Insert a path to the Alphafold databases. 
* Modify command to run Alphafold - original command is an adaptation of the traditional Alphafold command for my local cluster. Note: `--job-name=jobid`; `--fasta_paths=input_file`; `--output_dir=output_folder`; commands must be kept the same for the program to function properly.


## Running Structure-based_annotation
To generate predicted protein functions, create an sbatch script and run the `Structure-based_annotation.py` script with the following options:
* `-i, --input` str, Genbank, multifasta, or single fasta file containing proteins of interest. If fasta file used, headers must have an identifer at the start e.g "A"
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
  * `Best_deepfri_hits.csv` file, present in the `DeepFRI_output` folder, summary file containing top hits for each protein run compiled into one file for easy analysis.

## Example run
To test if the installations have been successful, the structure-based annotation tool can be tested on a very short protein (TRP-CAGE - labelled Short_protein.fasta in the Example folder) which should run relatively quickly (< 45 mins). To run use either submit the Short_protein.sh slurm script or create a new script and run this command:
```
python Structure-based_annotation.py -i Short_protein.fasta -o Short_protein_annotation
```

Whilst the tool was unable to predict a function, the final summary results should look like:
```txt
Protein,GO_term/EC_number,Score,GO_term/EC_number name
Ana,na,na
```

Structure-based_annotation was tested on four types of known function genes, acquired from the R. solanacearum GMI1000 gbff file (downloaded from: https://www.ncbi.nlm.nih.gov/genome/490?genome_assembly_id=300190). These included genes involved in: Bacterial respiration; Type III effectors; Membrane transporters; Transcriptional regulators. 

These can be found in the Respiration.fasta; T3E.fasta; Transporters.fasta; and Transcriptional_regulators.fasta files in this repository. 

The tests were done using the Respiration.sh; T3E.sh; Transporters.sh; and Transcriptional_regulators.sh scripts with variations of the command:
```
python Structure-based_annotation.py -i Respiration.fasta -o Respiration_annotation
```

For the Respiration dataset, the summary output (Best_deepfri_hits.csv) looked like:
```txt
Protein,GO_term/EC_number,Score,GO_term/EC_number name
A,GO:0015318,0.99955,inorganic molecular entity transmembrane transporter activity
B,GO:0015318,0.99890,inorganic molecular entity transmembrane transporter activity
C,GO:0003955,0.24991,NAD(P)H dehydrogenase (quinone) activity
D,GO:0051540,0.44101,metal cluster binding
E,GO:0016655,0.99390,"oxidoreductase activity, acting on NAD(P)H, quinone or similar compound as acceptor"
F,GO:0050136,0.99999,NADH dehydrogenase (quinone) activity
G,GO:0016651,0.51225,"oxidoreductase activity, acting on NAD(P)H"
H,GO:0016853,0.78599,isomerase activity
I,GO:0008270,0.99974,zinc ion binding
J,GO:0005215,0.50252,transporter activity
```

The tools was also tested on hypothetical proteins acquired from annotated prophage elements (see https://www.biorxiv.org/content/10.1101/2021.10.20.465097v1.full). This allowed the tool's power to be determined. This was done using the command:
```
python Structure-based_annotation.py -i Prophage_Genbank.gbk -p "Hypothetical" -o Prophage_hypothetical_annotation
```

An example summary output (Best_deepfri_hits.csv) from this is:
```txt
Protein,GO_term/EC_number,Score,GO_term/EC_number name
LOC_1_1,GO:0016757,0.15871,"transferase activity, transferring glycosyl groups"
LOC_1_2,GO:0016788,0.21507,"hydrolase activity, acting on ester bonds"
LOC_1_4,GO:0016788,0.13886,"hydrolase activity, acting on ester bonds"
LOC_1_7na,na,na
LOC_1_8na,na,na
LOC_1_9,GO:0005215,0.94041,transporter activity
LOC_1_12na,na,na
LOC_1_15,GO:0003677,0.19199,DNA binding
LOC_1_18,GO:0003723,0.20913,RNA binding
LOC_1_19,GO:0016895,0.91022,"exodeoxyribonuclease activity, producing 5'-phosphomonoesters"
LOC_1_20,GO:0003677,0.30268,DNA binding
LOC_1_24,GO:0003677,0.63090,DNA binding
LOC_1_25,GO:0003677,0.91422,DNA binding
LOC_1_26,GO:0022857,0.17785,transmembrane transporter activity
LOC_1_27na,na,na
LOC_1_30,GO:0005198,0.92011,structural molecule activity
LOC_1_31,GO:0003677,0.82856,DNA binding
LOC_1_32,GO:0017076,0.77057,purine nucleotide binding
LOC_1_33na,na,na
LOC_1_34,GO:0046914,0.25447,transition metal ion binding
LOC_1_35,GO:0016829,0.20727,lyase activity
LOC_1_36,GO:0003677,0.17416,DNA binding
LOC_1_38,GO:0016788,0.34641,"hydrolase activity, acting on ester bonds"
LOC_1_39,GO:0032553,0.65813,ribonucleotide binding
LOC_1_40,GO:0008233,0.83821,peptidase activity
LOC_1_41,GO:0016772,0.57553,"transferase activity, transferring phosphorus-containing groups"
LOC_1_42,GO:0016829,0.50003,lyase activity
LOC_1_43,GO:0030246,0.12414,carbohydrate binding
```



