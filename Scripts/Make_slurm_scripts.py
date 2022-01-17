#input file

def alphafold_sbatch_skeleton_edit(path_to_skeleton, fasta_id, single_fasta_file,path_to_alphafold_output,path_to_edited_skeleton):


		skeleton = open(path_to_skeleton, "r")

		edited_skeleton = ""
		for line in skeleton:
				stripped_line = line.strip()
				new_line = stripped_line.replace("jobid", fasta_id).replace("input_file", single_fasta_file).replace("output_folder", path_to_alphafold_output)
				edited_skeleton += new_line +"\n"
		skeleton.close()

		writing_file = open(path_to_edited_skeleton, "w")
		writing_file.write(edited_skeleton)
		writing_file.close()
