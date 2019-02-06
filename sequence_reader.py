#!/usr/bin/env python

def FASTA_reader(file_obj):
	sequences = []
	currSeq = ""
	firstLine = True
	for line in file_obj:
		if line.startswith(">") or line.strip() == "":
			if firstLine:
				firstLine = False
			else:
				sequences.append(currSeq)
				currSeq = ""
		else:
			s = line.strip()
			currSeq += s
		if line.strip() == "":
			break
	if currSeq != "":
		sequences.append(currSeq)
	return sequences

def BED_reader(file_obj):
	sequences = []
	for line in file_obj:
		fields = line.split()
		chrom, start, end = fields[0], int(fields[1]), int(fields[2])
		sequences.append(get_sequence(chrom, start, end))
	return sequences

def get_sequence(chrom,start=None,end=None,chrom_path = ""):
	f_c = open(chrom_path + chrom + ".fa")
	f_c.readline() 											# Read past the header
	if start and end:									# If start and end coordinates provided, return sequence specified
		offset = f_c.tell()									# Position in file where sequence starts
		f_c.seek(start + offset + (start)//50)				# Count the right number of characters + newlines to the start of the sequence of interest
		lines = f_c.read(end-start + (end-start)//50 + 1) 	# Read the right number of characters + newlines to encompass target sequence
		f_c.close()
		sequence = "".join(lines.split("\n"))				# Join the sequence into one string, no newlines.
	else:												# If no start and end, return sequence of whole chromosome
		lines = f_c.read()									
		sequence = "".join(lines.split("\n"))
	return sequence
