#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

example_pwm = """1423.00 708.00 2782.00   0.00 4000.00  27.00 3887.00 3550.00 799.00 1432.00 1487.00
560.00 1633.00  31.00   0.00   0.00  29.00   0.00   4.00 681.00 897.00 829.00
1242.00 1235.00  10.00 4000.00   0.00 109.00   6.00 383.00 2296.00 1360.00 1099.00
775.00 424.00 1177.00   0.00   0.00 3835.00 107.00  63.00 224.00 311.00 585.00"""

def main(pwm, outname='logo.png'):
	lines = pwm.split('\n')
	to_pop = []
	for i,l in enumerate(lines):
		if l == '':
			to_pop.append(i)
	for i in to_pop[::-1]:
		lines.pop(i)

	pwm_ar = np.vstack([np.fromstring(l, dtype=float, sep=' ') for l in lines])

	# Make sure it is the right shape
	if pwm_ar.shape[0] != 4:
		pwm_ar = pwm_ar.T
	if pwm_ar.shape[0] != 4:
		print("Array is the wrong shape. Should be of size `k` by 4")
		quit()
	k = pwm_ar.shape[1]

	# Add pseudo counts
	pwm_ar += 0.00001
	pwm_ar /= np.sum(pwm_ar, axis=0)

	# Find information content at each position
	ic = np.log2(pwm_ar)* pwm_ar
	ic = np.sum(ic, axis=0) + 2.0

	# Create logo
	nucs = [plot_A, plot_C, plot_G, plot_T]

	fig = plt.figure(figsize=[k,4])
	ax = fig.add_subplot(111)
	
	for x in range(k):
		y = 0
		idx = np.argsort(pwm_ar[:,x],)
		for i in idx:
			height = pwm_ar[i,x]*ic[x]
			nucs[i](ax, x, y, height)
			y += height

	plt.xlim([0,k])
	plt.ylim([0,2])
	fig.tight_layout()
	plt.savefig(outname)



def plot_A(ax, x, y, height, width=1):
	xs = [0.0, 0.5, 1.0, 0.85, 0.65, 0.35, 0.15, 0.0]
	ys = [0.0, 1.0, 0.0, 0.0, 0.4, 0.4, 0.0, 0.0]

	xs = [i*width+x for i in xs]
	ys = [i*height+y for i in ys]
	ax.add_patch(patches.Polygon(xy=list(zip(xs,ys)), fill=True, facecolor='green'))

	xs = [0.4, 0.5, 0.6, 0.4]
	ys = [0.55, 0.8, 0.55, 0.55]
	xs = [i*width+x for i in xs]
	ys = [i*height+y for i in ys]
	ax.add_patch(patches.Polygon(xy=list(zip(xs,ys)), fill=True, facecolor='white'))

def plot_C(ax, x, y, height, width=1):
	cx = x + width/2.
	cy = y + height/2.

	ax.add_patch(patches.Ellipse((cx,cy), width, height, facecolor='blue'))
	ax.add_patch(patches.Ellipse((cx,cy), width*0.7, height*0.7, facecolor='white'))
	ax.add_patch(patches.Rectangle((cx,cy-0.15*height), width*0.5, 0.3*height, facecolor='white'))

def plot_G(ax, x, y, height, width=1):
	cx = x + width/2.
	cy = y + height/2.

	ax.add_patch(patches.Ellipse((cx,cy), width, height, facecolor='gold'))
	ax.add_patch(patches.Ellipse((cx,cy), width*0.7, height*0.7, facecolor='white'))
	ax.add_patch(patches.Rectangle((cx,cy-0.15*height), width*0.5, 0.3*height, facecolor='white'))
	ax.add_patch(patches.Rectangle((cx,cy-0.15*height), width*0.5, 0.15*height, facecolor='gold'))

def plot_T(ax, x, y, height, width=1):
	xs = [0, 1, 1, 0.6, 0.6, 0.4, 0.4, 0, 0 ]
	ys = [1, 1, 0.8, 0.8, 0, 0, 0.8, 0.8, 1]

	xs = [i*width+x for i in xs]
	ys = [i*height+y for i in ys]
	ax.add_patch(patches.Polygon(xy=list(zip(xs,ys)), fill=True, facecolor='red'))

if __name__ == '__main__':
	main(example_pwm)