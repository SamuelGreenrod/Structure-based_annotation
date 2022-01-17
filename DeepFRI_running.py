import os
import subprocess
import shutil

# This runs DeepFRI on all proteins in directory, and hides the console output so there is less cluttering. 

def deepFRI(proteinID, input_pdb, deepfri_output_path, summary_file):

	output_folder = deepfri_output_path + "/" + proteinID + "_deepFRI"
	os.mkdir(output_folder)
	subprocess.run(["python","DeepFRI/predict.py","-pdb",input_pdb,"-ont","mf","-v","-o",proteinID])
	
	json_file = proteinID + "_MF_pred_scores.json"
	csv_file = proteinID + "_MF_predictions.csv"
	shutil.move(json_file, output_folder + "/" + json_file)
	shutil.move(csv_file, output_folder + "/" + csv_file)

	# Make a summary file that contains the top annotation hits for each protein
	with open(output_folder + "/" + csv_file, "r") as file: # This file contains annotation hits and details
		with open(summary_file,"a") as output:
			lines = file.readlines()
			if len(lines) < 3:
				output.write(proteinID+"na,na,na\n") # If the file has fewer than 3 lines it means it has no annotation results so label annotation as "none".
			else:
				new_line = lines[2].replace("query_prot",proteinID)
				output.write(new_line) # If file has annotation results then write the top annotation (best hit) to the summary file. 
