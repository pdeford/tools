#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

try:
	from tkinter import *
	from tkinter import scrolledtext as tkst
except:
	from Tkinter import *
	import ScrolledText as tkst
import PWM_logo
from PIL import Image, ImageTk

if __name__ == '__main__':

	pwm = """0.00 4000.00  27.00 3887.00 3550.00 799.00 
0.00   0.00  29.00   0.00   4.00 681.00 
4000.00   0.00 109.00   6.00 383.00 2296.00 
0.00   0.00 3835.00 107.00  63.00 224.00"""
	PWM_logo.main(pwm, 'logo.png')

	window = Tk()
	window.title("PWM to logo")
	window.geometry('400x300')
	scrollbar = Scrollbar(window)
	# scrollbar.pack(side=BOTTOM, fill=X)
	input_txt = tkst.ScrolledText(window, width=50, height=5, xscrollcommand=scrollbar.set)
	input_txt.insert(INSERT, 'Enter your PWM here\n'+pwm)
	# scrollbar.config(command=input_txt.xview)
	image = Image.open('logo.png')
	image = image.resize((400,200), Image.ANTIALIAS)
	photo = ImageTk.PhotoImage(image)
	label = Label(image=photo)
	label.image = photo
	# label.pack()
	def clicked():
		pwm = input_txt.get(1.0, END)
		print(pwm)
		PWM_logo.main(pwm)
		image = Image.open('logo.png')
		image = image.resize((400,200), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(image)
		label.configure(image=photo)
		label.image = photo

	btn = Button(window, text='Submit PWM', command=clicked)
	input_txt.grid(column=0, row=0)
	label.grid(column=0, row=2)
	btn.grid(column=0, row=1)
	input_txt.focus()
	def selectall(event):
		event.widget.tag_add("sel","1.0","end")
	window.bind_class("Text", "<Control-a>", selectall)
	window.bind_class("Text", "<Command-a>", selectall)
	window.mainloop()
