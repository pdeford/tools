#!/usr/bin/env python

"""
################################################################################
#                             pubmed_PMC_querier.py                            #
#                                 Peter DeFord                                 #
#                           Johns Hopkins University                           #
#                                     2015                                     #
################################################################################

pubmed_PMC_querier is a tool that allows you to query NCBI's PubMed database,
and download the full-text for articles that are available as part of the open
access subset of PMC articles. It dumps the XML for all files into one file that
can then be processed as you wish.

The usage is as follows:

    $ pubmed_PMC_querier.py outputFileBasename "your search query[&additional=options]"

The additional options should be added to the end of your query without a space
in the format descibed on the NCBI's E-utilities website:
http://www.ncbi.nlm.nih.gov/books/NBK25500/

The program works in the following way:
1. Queries PubMed and downloads matching PMIDs
2. Converts PMIDs to PMCIDs
3. Accesses full text through the PMC-OAI

"""

import time
import subprocess
import sys

search_base      = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s&retstart=%d&retmax=%d&&tool=enhancer_parser&email=pdeford1%%40jhu.edu"
convert_base     = "http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=%s&format=csv&versions=no&tool=enhancer_parser&email=pdeford1%%40jhu.edu"
download_base    = "http://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:%s&metadataPrefix=pmc"
download_base_fm = "http://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:%s&metadataPrefix=pmc_fm"

retmax = 100000
max_rate = 1.0/3 # NCBI requests no more than 3 url posts per second

query = ""

f_base = "out"

if len(sys.argv) > 2:
	query = "+".join(sys.argv[2:])
	query.replace(" ", "+")
	f_base = sys.argv[1]
else:
	print( "Usage: %s f_out your search query" % sys.argv[0] )
	quit()

count = 0
print( "Querying PMC for '%s'" % query )
while True:
	time.sleep(max_rate)
	subprocess.call('wget -a parser_log -O - "%s" >> accessions.txt' % search_base % (query, count, retmax),shell=True)
	subprocess.call('grep "</RetStart><IdList/>" accessions.txt > tmp_grep', shell=True)
	with open("tmp_grep") as f:
		l = f.readline()
		if l != "":
			break
	count += retmax

IDs = []
with open("accessions.txt") as f:
	for line in f:
		if line.strip().startswith("<Id>"):
			PMID = line.strip()[4:-5]
			if PMID not in IDs:
				IDs.append(PMID)
print( "PMIDs:", len(IDs) )

print( "Converting PMIDs to PMCIDs" )
for i in range(len(IDs)//200+1):
	end = i + 200
	if end > len(IDs):
		end = len(IDs)
	csv = ",".join(IDs[i:end])
	#print( csv )
	time.sleep(max_rate)
	subprocess.call('wget -a parser_log -O - "%s" >> conversions.txt' % convert_base % csv, shell=True)

IDs = []
with open("conversions.txt") as f:
	f.readline()
	for line in f:
		PMCID = line.split(",")[1][1:-1]
		if PMCID == "PMCID":
			pass
		elif PMCID != "":
			if PMCID[3:] not in IDs:
				IDs.append(PMCID[3:])
print( "PMCIDs:", len(IDs) )

exp_time = len(IDs) * max_rate / 60.0
print( "Downloading full text of articles. Minimum time = %0.1f minutes" % exp_time )
for PMCID in IDs:
	time.sleep(max_rate)
	subprocess.call('wget -a parser_log -O - "%s" >> %s.articles.txt' % (download_base % PMCID, f_base), shell=True)

count = 0
subprocess.call('grep "/body" %s.articles.txt > tmp_grep' % f_base, shell=True)
with open("tmp_grep") as f:
	for line in f:
		count += 1

print( "Full text retrieved for %d articles" % count )

subprocess.call('rm tmp_grep', shell=True)
subprocess.call('rm accessions.txt', shell=True)
subprocess.call('rm conversions.txt', shell=True)
