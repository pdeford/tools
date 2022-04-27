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
		print( nl)
	print( "{0:> {1}.2f}".format(0, l_pad) + "+" + "-"*(bins-1) + "+")
	nl = str(minx)+"{}"
	len_nl = len(nl)
	print( " "*l_pad + nl.format(" "*(bins-len_nl)) + str(maxx))

if __name__ == '__main__':
	import argparse
	import sys
	parser = argparse.ArgumentParser(
		description="""\
			Generate an ASCII based histogram from a one column file.
			""",
		)
	parser.add_argument('-b', '--bins', type=int, default=10,
		help="The number of bins across the x-axis. (Default: 10)"
		)
	parser.add_argument('input', type=argparse.FileType('r'), 
		default=sys.stdin, nargs='?',
		help='A file with one column of numbers. Defaults to STDIN if not specified.')
	args = parser.parse_args()

	l = [float(x.strip()) for x in args.input if x.strip()]


	main(l, args.bins)