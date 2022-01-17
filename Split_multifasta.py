from Bio import SeqIO

def multifasta_to_fasta(multifasta_path, singlefasta_dir_path):

	single_fasta_files = []
	protein_names = []

	header_count = 0 # Number of headers in multifasta
	count = 0 # Number of single fasta generated
	with open(multifasta_path, "r") as multifasta:
		for line in multifasta.read():
			if ">" in line:
				header_count += 1 # Count the number of headers in multifasta

	with open(multifasta_path, "r") as multifasta:
		for rec in SeqIO.parse(multifasta, "fasta"): # Use Bio.SeqIO to separate the sequences in multifasta, extract the protein ids (id) and the sequences (seq)
			id = rec.id
			seq = rec.seq
			fasta_name = id.replace("|","") + ".fasta" # Label each single fasta based on the protein id
			fasta_name_noext = fasta_name.replace(".fasta","")
			full_fasta_path = str(singlefasta_dir_path) + "/" + fasta_name

			protein_names.append(fasta_name_noext) # Make list of protein names
			single_fasta_files.append(full_fasta_path) # Make list of protein paths

			with open(str(singlefasta_dir_path) + "/" + fasta_name, "a") as id_file:
				id_file.write(">"+str(id)+"\n"+str(seq)) # Make a new fasta file in the current directory for each sequence with the header (protein id) and sequence.
			with open(str(singlefasta_dir_path) + "/" + fasta_name, "r") as ofile:
				if ">" in ofile.read():
					count += 1 # Count how many single fastas (containing headers) are generated
	if count > 0 and count == header_count: # If the number of single fastas is equal to the number of fastas in the multifasta then the parse has been successful
		print("Multi-fasta successfully split")

	return protein_names, single_fasta_files