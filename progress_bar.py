#!/usr/bin/env python

import sys

class progress_bar(object):
	"""docstring for progress_bar"""
	def __init__(self, length=50):
		self.length = length
	def updateProgress(self, progress, total):
		"""Write the progress to screen as a bar and a percent."""
		l = int(self.length)
		percent = progress*100.0/total
		bars = int(percent//(100.0/l))
		bar = "[" + "="*bars + " "*(l-bars) + "] %0.2f%%" % percent + "\r"
		sys.stdout.write(bar)
		sys.stdout.flush()
		sys.stdout.flush()
		if percent >= 100.0:
			print(bar[:-1])
