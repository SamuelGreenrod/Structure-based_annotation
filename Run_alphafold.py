import os
import subprocess

def alphafold_run_multifasta(single_fasta_dict,alphafold_dir_path):
		alphafold_folders = []

		for key,value in single_fasta_dict:
				Alphafold_output = key +"_alphafold"
				Alphafold_output_path = os.path.join(alphafold_dir_path, Alphafold_output)
				alphafold_folders.append(Alphafold_output_path)

				run_alphafold = "srun --time=2:00:00 --cpus-per-task=10 --gres=gpu:1 --partition=gpu alphafold --fasta_paths=" + value + "--max_template_date=2020-05-14 --preset=full_dbs --output_dir=" + Alphafold_output_path + "--model_names=model_1,model_2,model_3,model_4,model_5"
				
				process = subprocess.Popen(run_alphafold.split(), stdout=subprocess.PIPE)

				

def alphafold_run_singlefasta(single_fasta_path,single_fasta_name,alphafold_dir_path):
		alphafold_folders = []
		Alphafold_output = single_fasta_name +"_alphafold"
		Alphafold_output_path = os.path.join(alphafold_dir_path, Alphafold_output)
		alphafold_folders.append(Alphafold_output_path)

		run_alphafold = "srun --time=2:00:00 --cpus-per-task=10 --gres=gpu:1 --partition=gpu alphafold --fasta_paths=" + single_fasta_path + "--max_template_date=2020-05-14 --preset=full_dbs --output_dir=" + Alphafold_output_path + "--model_names=model_1,model_2,model_3,model_4,model_5"
				
		process = subprocess.Popen(run_alphafold.split(), stdout=subprocess.PIPE)

		return process

