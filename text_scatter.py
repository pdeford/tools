import numpy as np

def main(x, y, plot_type='scatter', plot_height=20):

	x = np.asarray(x)
	y = np.asarray(y)

	plot_width = int(plot_height*2.5)

	minx = min(x)
	miny = min(y)
	maxx = max(x)
	maxx += (maxx-minx)*0.001
	maxy = max(y)
	maxy += (maxy-miny)*0.001

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
		short_ramp = " .:-=+*#%@"
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
				nl += short_ramp[int((val-minramp)//binsizeramp)]

			if i < len(short_ramp):
				nl += ("  " + cbar.format(short_ramp[-(1+i)], maxramp - i*binsizeramp))
			print nl


	print "{0:> {1}.2f}".format(miny, l_pad) + "+" + "-"*(plot_width-1) + "+" 
	nl = str(minx)+"{}"
	len_nl = len(nl)
	print " "*l_pad + nl.format(" "*(plot_width-len_nl)) + str(maxx)




if __name__ == '__main__':
	import sys
	x,y = [],[]
	for line in open(sys.argv[1]):
		valx, valy = [float(val) for val in line.split()]
		x.append(valx)
		y.append(valy)

	plot_type = sys.argv[2]

	if len(sys.argv) > 3:
		plot_height = int(sys.argv[3])
	else:
		plot_height = 20


	
	main(x, y, plot_height=plot_height, plot_type=plot_type)