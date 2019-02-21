#!/usr/bin/env python

import numpy as np

def main(x, y, plot_type='scatter', plot_height=20, sharesize=False):

	x = np.asarray(x)
	y = np.asarray(y)

	plot_width = int(plot_height*2.5)

	minx = min(x)
	miny = min(y)
	maxx = max(x)
	maxx += (maxx-minx)*0.001
	maxy = max(y)
	maxy += (maxy-miny)*0.001

	if sharesize:
		minx = miny = min(minx, miny)
		maxx = maxy = max(maxx, maxy)

	rangex = maxx-minx
	rangey = maxy-miny

	binsizex = rangex/plot_width
	binsizey = rangey/plot_height

	x_bins = np.asarray((x-minx) // binsizex, dtype=int)
	y_bins = np.asarray((y-miny) // binsizey, dtype=int)

	plot = np.zeros((plot_height, plot_width))
	for i in range(len(x_bins)):
		plot[y_bins[i], x_bins[i]] += 1
	plot = plot[::-1]


	l_pad = len("{:> 0.2f}".format(maxy))
	if plot_type == 'scatter':
		for i in xrange(plot_height):
			nl = ""
			if i == 0:
				nl += "{0:> {1}.2f}+".format(maxy, l_pad)
			else:
				nl += " "*l_pad + "|"
			for val in plot[i]:
				if val > 0:
					nl += "*"
				else:
					nl += " "
			print nl
	elif plot_type == 'density':
		cbar = '\x1b[1;36;40m{} {:> 5.2e}\x1b[0m'
		short_ramp = ".:-=+*#%@"
		pmax = np.max(plot)
		if pmax < len(short_ramp):
			short_ramp = short_ramp[:int(pmax)]
		minramp = np.min(plot)
		maxramp = np.max(plot)
		maxramp += (maxramp - minramp)*0.001
		binsizeramp = (maxramp - minramp)/len(short_ramp)

		for i in xrange(plot_height):
			nl = ""
			if i == 0:
				nl += "{0:> {1}.2f}+".format(maxy, l_pad)
			else:
				nl += " "*l_pad + "|"
			for val in plot[i]:
				if val > 0:
					nl += short_ramp[int((val-minramp)//binsizeramp)]
				else:
					nl += " "

			if i < len(short_ramp):
				nl += ("  " + cbar.format(short_ramp[-(1+i)], maxramp - i*binsizeramp))
			print nl


	print "{0:> {1}.2f}".format(miny, l_pad) + "+" + "-"*(plot_width-1) + "+" 
	nl = str(minx)+"{}"
	len_nl = len(nl)
	print " "*l_pad + nl.format(" "*(plot_width-len_nl)) + str(maxx)


if __name__ == '__main__':
	import argparse
	import sys
	parser = argparse.ArgumentParser(
		description="""\
			Generate an ASCII based scatterplot from a two column file.
			"""
		)
	parser.add_argument('-y', '--height', type=int, default=20,
		help="The number of characters tall the plot will be. Determines the plot size. (Default: 20)"
		)
	parser.add_argument('-t', '--type', choices=['scatter', 'density'], type=str, default='scatter',
		help="Whether to generate a scatter plot or a density plot. (Default: scatter)"
		)
	parser.add_argument('--xy-lim', action='store_true',
		help='make the x and y limits have the same axis limits.')
	parser.add_argument('input', type=argparse.FileType('r'), 
		default=sys.stdin, nargs='?',
		help='A file with two columns of numbers separated by whitespace. Defaults to STDIN if not specified.')
	args = parser.parse_args()

	x,y = [],[]
	for line in args.input:
		valx, valy = [float(val) for val in line.split()]
		x.append(valx)
		y.append(valy)

	main(x, y, plot_height=args.height, plot_type=args.type, sharesize=args.xy_lim)