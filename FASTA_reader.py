#!/usr/bin/env python

def reader(file_obj):
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