#!/usr/bin/env python

import sys

def main(l, bins=10):
	minx = min(l)
	maxx = max(l) + 0.001*(max(l)-minx)
	range_size = maxx-minx

	binsize = range_size/float(bins)
	l_bins = [(x-minx)//binsize for x in l]
	bars = dict(zip(range(bins), [0,]*bins))
	for b in l_bins:
		bars[int(b)] += 1

	plot_height = 10
	y_max = max(bars.values())
	y_ticksize = y_max / float(plot_height)
	for b in bars.keys():
		bars[b] //= y_ticksize

	# Generate plot
	l_pad = len("{:> 0.2f}".format(y_max))
	for i in range(plot_height):
		nl = "{0:> {1}.2f}|".format(y_max - y_ticksize*i, l_pad)
		for j in range(bins):
			if bars[j] >= (plot_height - i):
				nl += "#"
			elif (i == (plot_height-1)) and (j in l_bins):
				nl += "."
			else:
				nl += " "
		print nl
	print "{0:> {1}.2f}".format(0, l_pad) + "+" + "-"*(bins-1) + "+"
	nl = str(minx)+"{}"
	len_nl = len(nl)
	print " "*l_pad + nl.format(" "*(bins-len_nl)) + str(maxx)

if __name__ == '__main__':
	import sys
	# Read info from command line
	f = open(sys.argv[1])
	if len(sys.argv) > 2:
		bins = int(sys.argv[2])
	else:
		bins = 10

	# Load and process data
	l = [float(x.strip()) for x in f if x.strip()]
	main(l, bins)