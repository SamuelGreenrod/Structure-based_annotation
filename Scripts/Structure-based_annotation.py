# Author - Samuel Greenod (samuel.greenrod@magd.ox.ac.uk)
# Main script used to predict protein structures with Alphafold 2.0 and determine their potential function using DeepFRI.

from Bio import SeqIO
from datetime import date
import argparse
import subprocess
import os
import timeit
import shutil
import extract_genbank_to_multifasta
from Split_multifasta import multifasta_to_fasta
from Make_slurm_scripts import alphafold_sbatch_skeleton_edit
from Run_alphafold import alphafold_run_multifasta, alphafold_run_singlefasta
from DeepFRI_running import deepFRI

# This makes the arguments that can be used when running the python script
parser = argparse.ArgumentParser(description = "Annotation pipeline for unannotated or poorly annotated proteins")
parser.add_argument("-i", "--input", help="Input file to run through pipeline (single fasta, multifasta, or genbank")
parser.add_argument("-p", "--protein_label", help="Protein ID string to search for in Genbank file")
parser.add_argument("-o", "--output", help="Label for output directory")

args = parser.parse_args()
path = os.getcwd()

start = timeit.default_timer() # Starts a timer to see how long the code runs for

# Specifies argument paths
input_path = str(path)+ "/"+ str(args.input)
protein_label_path = str(path)+ "/"+ str(args.protein_label)
output_path = str(path)+ "/"+ str(args.output)

genbank_file_extensions = [".gbk"]
fasta_file_extensions = [".fna", ".fa", ".faa", ".fasta"]

## Prepare output folders
# Overall output foldrr
Main_output = str(path) +"/" + str(args.output)
os.mkdir(Main_output)

# Folder for multifasta file - either from genbank or multifasta input
Multifasta_output = "Multifasta_files"
Multifasta_output_path = os.path.join(Main_output, Multifasta_output)
os.mkdir(Multifasta_output_path)

# Folder for single fasta files from splitting multifasta or single fasta input
Singlefasta_output = "Singlefasta_files"
Singlefasta_output_path = os.path.join(Main_output, Singlefasta_output)
os.mkdir(Singlefasta_output_path)

# Folder for slurm scripts for running alphafold
Slurm_scripts = "Slurm_scripts"
Slurm_scripts_path = os.path.join(Main_output, Slurm_scripts)
os.mkdir(Slurm_scripts_path)

# Folder for Alphafold_outputs
Alphafold_output = "Alphafold_output/"
Alphafold_output_path = os.path.join(Main_output, Alphafold_output)
os.mkdir(Alphafold_output_path)

# Folder for Alphafold_outputs
deepfri_output = "DeepFRI_output/"
deepfri_output_path = os.path.join(Main_output, deepfri_output)
os.mkdir(deepfri_output_path)
# 
# MODULE 1 FUNCTION: Extract user-specified proteins from genbank and add to a multifasta

# Stop program if a Genbank is used with no protein ID label.
if any(x in input_path for x in genbank_file_extensions) and str(args.protein_label) == "None":
	print("Protein ID string (-p) required if using Genbank file")
	exit()

# Program continues if both a GenBank and a protein ID are submitted.
elif any(x in input_path for x in genbank_file_extensions) and str(args.protein_label) != "None":
	print("Genbank submitted")
	protein_name = str(args.protein_label)

	# Function which uses Bio.SeqIO to extract protein id, organism name, protein label, amino acid sequence) from a genbank and outputs a multi-fasta
	multifasta_file = extract_genbank_to_multifasta.extract_genbank_to_multifasta(input_path,str(args.input),protein_name,Multifasta_output_path)


elif any(x in input_path for x in fasta_file_extensions): # If file is a fasta file (has fasta extension)
	multifasta_file = ""
	singlefasta_file = ""
	with open(input_path,"r") as file:
		list_of_lists = []

  		# Turn all sequences in fasta into a string and if they only contain "ACTG" characters then it's a nucleotide sequence so exit
		for line in file:
			if ">" not in line:
				strip_line = line.strip()
				split_strip_line = strip_line.split()
				list_of_lists.append(split_strip_line)
		fasta_list = [item for sublist in list_of_lists for item in sublist]
		fasta_string = "".join(fasta_list)
		if set(fasta_string) == set("ACTG"):
			print("This is a nucleotide fasta file, please input a protein fasta file.")
			exit()
	with open(input_path,"r") as file:
		count = 0
		for line in file:	
				if ">" in line:
					count += 1 # For each line in the fasta if it contains a header then add 1

		# Determines whether a multifasta or a single fasta was input based on number of headers.
		if count > 1: # If there are more than one ">" then it is a multifasta
			multifasta_file = shutil.copy(input_path, Multifasta_output_path)
			print("Multi-fasta submitted")
		elif count == 1: # If there is only one ">" then it is a single fasta file
			singlefasta_file = shutil.copy(input_path, Singlefasta_output_path)
			print("Single fasta submitted")
		elif count < 1:
			print("No fasta header detected, please enter a valid fasta file.") # If there is no ">" then the file is likely empty or not a fasta file so reject.
			exit()


# Module 2 - Split multifastas

# Runs python script that splits multifastas into single fasta files, and puts them into the single fasta folder
if multifasta_file != "":
	protein_names, single_fastas = multifasta_to_fasta(multifasta_file,Singlefasta_output_path)

	# Converts single fasta files into a dictionary with the fasta file prefix as key and full path as value
	single_fasta_dictionary = {}
	for name in protein_names:
		for fasta in single_fastas:
				single_fasta_dictionary[name] = fasta
				single_fastas.remove(fasta)
				break  



# Module 3 - Create alphafold sbatch files and run, then pipe output into DeepFRI

# Specifies the skeleton sbatch file that can be copied and edited
sbatch_skeleton = str(path) + "/Alphafold_sbatch_skeleton.sh"

# If multifasta is available then create an edited sbatch script, where the jobid, input file, and output folder is altered.
if multifasta_file != "":

	# Create summary file for DeepFRI output
	summary_filename = 	deepfri_output_path + "/Best_deepfri_hits.csv"
	with open(summary_filename,"a") as output:
		output.write("Protein,GO_term/EC_number,Score,GO_term/EC_number name\n")

	# Create sbatch script and run alphafold, looping through each single fasta
	for key, value in single_fasta_dictionary.items():
		edited_slurm_script = Slurm_scripts_path + "/" + key + "_alphafold_slurm.sh" # Adds single fasta prefix to sbatch file name
		create_sbatch = alphafold_sbatch_skeleton_edit(sbatch_skeleton, key, value, Alphafold_output_path,edited_slurm_script) # Copies skeleton sbatch, edits variable strings and then moves to script folder
		subprocess.run(["sbatch",edited_slurm_script]) # Runs sbatch files in the sbatch folder

		# Run DeepFRI on alphafold output and upload results to the summary file
		alphafold_pdb = Alphafold_output_path + key + "/" + "ranked_0.pdb"
		deepfri = deepFRI(key,alphafold_pdb,deepfri_output_path,summary_filename)

# If single fasta is used as input then run on its own
else:

	# Create summary file for DeepFRI output
	summary_filename = 	deepfri_output_path + "/Best_deepfri_hits.csv"
	with open(summary_filename,"a") as output:
		output.write("Protein,GO_term/EC_number,Score,GO_term/EC_number name\n")

	# Create sbatch script and run alphafold
	fasta_id = str(args.input).replace(".fasta","")
	edited_slurm_script = Slurm_scripts_path + "/" + fasta_id + "_alphafold_slurm.sh" # Note fasta_id is used instead of key
	create_sbatch = alphafold_sbatch_skeleton_edit(sbatch_skeleton, fasta_id, singlefasta_file, Alphafold_output_path,edited_slurm_script)
	subprocess.run(["sbatch",edited_slurm_script])

	# Run DeepFRI on alphafold output and upload results to the summary file
	alphafold_pdb = Alphafold_output_path + fasta_id + "/" + "ranked_0.pdb"
	deepfri = deepFRI(fasta_id,alphafold_pdb,deepfri_output_path,summary_filename)
