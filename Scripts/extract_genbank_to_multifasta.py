from Bio import SeqIO

def extract_genbank_to_multifasta(input_file,file_name,protein_label,multifasta_dir_path):
		multifasta_file = file_name.replace(".gbk","") + "_specified_genes.fasta" # Make multifasta name by keeping GenBank name, remove extension, add extra label.
		multifasta_file_path = str(multifasta_dir_path) + "/" + multifasta_file

		for record in SeqIO.parse(input_file, "gb"): # Looks at SeqRecords in the genbank (number of contigs/samples)
			#acc = record.annotations['accessions'][0] # Remove hash and add extra number to line 45 if contig/sample accession needed.
			organism = record.annotations['organism'] # Outputs the organism information

		for feature in record.features: # Looks at each feature in each SeqRecord (each feature represents a putative protein sequence)

			for key, val in feature.qualifiers.items(): # feature qualifiers contain protein information for each protein including the protein name (val)
				
				if any(protein_label in s for s in val): # if name of any of the items in the qualifiers (contains protein name) contains user-specified string
					
					with open(multifasta_file_path, "a") as ofile: # create a new file and insert the protein id, organism name, protein label, and amino acid sequence						
						ofile.write(">{0}| {1}| {2}| \n{3}\n\n".format(feature.qualifiers['protein_id'][0], organism,val[0], feature.qualifiers['translation'][0])) #Writes genbank information to multifasta
		
		with open(multifasta_file_path, "r") as ofile:
			
			if ">" in ofile.read(): # If multifasta file contains headers then it is likely a multifasta so continue.
				print("String-specific protein multi-fasta generated")
		
		return multifasta_file_path