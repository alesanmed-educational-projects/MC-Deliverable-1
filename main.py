#-*-coding:utf-8-*-
import functions

import tkinter as tk
import ttk
from PIL import Image, ImageTk
from tkinter import filedialog

def process(root, function, savefile, parameter, *filename):
	options = { 'multiple': False, 'filetypes': [('Images', '.jpg .png')] }
	name = filedialog.askopenfilename(**options)

	if(name):
		process = getattr(functions, function)
		if function == 'median':
			try:
				k_size = int(parameter.get())
				if k_size % 2 == 0:
					return
				else:
					images = process(name, k_size)
			except ValueError:
				images = process(name)
		elif function == 'denoise':
			try:
				filter_strength = int(parameter.get())
				images = process(name, filter_strength)
			except ValueError:
				images = process(name)
		elif function == 'gammaCorrection':
			pow_transfsorm = parameter.get()
			if '/' in pow_transfsorm:
				fraction = pow_transfsorm.split('/')
				numerator = 1
				try:
					denominator = int(fraction[1])
				except ValueError:
					return
				images = process(name, numerator / denominator)
			else:
				try:
					pow_value = int(pow_transfsorm)
					images = process(name, pow_value)
				except ValueError:
					images = process(name)
		elif function == 'cannyEdge':
			try:
				t_1 = int(parameter[0])
				t_2 = int(parameter[1])
			except ValueError:
				return

			l2gradient = bool(int(parameter[2]))
			try:
				aperture = int(parameter[3])
				images = process(name, t_1=t_1, t_2=t_2, aperture=aperture, l2gradient=l2gradient)
			except ValueError:
				images = process(name, t_1=t_1, t_2=t_2, l2gradient=l2gradient)
		elif function == 'sobel':
			try:
				dx = int(parameter[0])
			except ValueError:
				dx = 1

			try:
				dy = int(parameter[1])
			except ValueError:
				dy = 1

			try:
				k_size = int(parameter[2])

				if k_size not in [1, 3, 5, 7]:
					k_size = 3
			except ValueError:
				k_size = 3

			try:
				delta = int(parameter[3])
			except ValueError:
				delta = 0

			images = process(name, dx, dy, k_size, delta)

		else:
			images = process(name)

		original_img = images[0]
		processed_img = images[1]

		original_window = tk.Toplevel(master=root, height=600, width=600)
		original_window.wm_title('Original')
		original_img = Image.fromarray(original_img)
		tk_or_img = ImageTk.PhotoImage(image=original_img)
		or_label = tk.Label(original_window, image=tk_or_img)
		or_label.image = tk_or_img
		or_label.pack()

		processed_window = tk.Toplevel(master=root, height=600, width=600)
		processed_window.wm_title('Procesada')
		processed_img = Image.fromarray(processed_img)
		tk_pr_img = ImageTk.PhotoImage(image=processed_img)
		pr_label = tk.Label(processed_window, image=tk_pr_img)
		pr_label.image = tk_pr_img
		pr_label.pack()

		if bool(savefile):
			if filename:
				processed_img.save('results/{0}.jpg'.format(filename))
			else:
				processed_img.save('results/{0}.jpg'.format(function))
	else:
		return
	
root = tk.Tk()
root.title('Procesamiento')

tabs = ttk.Notebook(root)

savefile = tk.IntVar()
savecheck = tk.Checkbutton(root, text="Guardar resultados", variable=savefile)

###Pestanya de suavizado####
suavizado = tk.Frame(tabs)

tk.Label(suavizado, text='Tamaño de la matriz (impar)').grid(row=0, column=0)
median_k_size = tk.StringVar()
tk.Entry(suavizado, textvariable=median_k_size).grid(row=0, column=1)
tk.Button(suavizado, text='Filtro mediana', command= lambda: process(root, 'median', savefile.get(), median_k_size)).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=10)

tk.Label(suavizado, text='Fuerza del filtro').grid(row=2, column=0)
filter_strength = tk.StringVar()
tk.Entry(suavizado, textvariable=filter_strength).grid(row=2, column=1)
tk.Button(suavizado, text='Supresión de ruido', command= lambda: process(root, 'denoise', savefile.get(), filter_strength)).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=10)

###Pestanya de contraste###
contraste = tk.Frame(tabs)
tk.Button(contraste, text='Ecualización del histograma', command= lambda: process(root, 'equalizeHist', savefile.get(), None)).pack(anchor='w', padx=10, pady=10)
tk.Button(contraste, text='Ecualización adaptativa del histograma', command= lambda: process(root, 'CLAHE', savefile.get(), None)).pack(anchor='w', padx=10, pady=10)


###Pestanya de intensidad###
intensidad = tk.Frame(tabs)
tk.Button(intensidad, text='Trasnformación logarítmica', command= lambda: process(root, 'logTransform', savefile.get(), None)).grid(sticky='w', row=0, column=0, columnspan=2, pady=10)

tk.Label(intensidad, text='Potencia (n o 1/n)').grid(sticky='w', row=1, column=0)
pow_transfsorm = tk.StringVar()
tk.Entry(intensidad, textvariable=pow_transfsorm).grid(sticky='w', row=1, column=1)
tk.Button(intensidad, text='Trasnformación por potencias', command= lambda: process(root, 'gammaCorrection', savefile.get(), pow_transfsorm)).grid(sticky='w', row=2, column=0, columnspan=2, pady=10)


###Pestanya de bordes###
bordes = tk.Frame(tabs)
tk.Label(bordes, text='Umbral 1').grid(sticky='w', row=0, column=0)
t_1 = tk.StringVar()
tk.Entry(bordes, textvariable=t_1).grid(sticky='w', row=0, column=1)

tk.Label(bordes, text='Umbral 2').grid(sticky='w', row=1, column=0)
t_2 = tk.StringVar()
tk.Entry(bordes, textvariable=t_2).grid(sticky='w', row=1, column=1)

tk.Label(bordes, text='Tamaño de la matriz').grid(sticky='w', row=2, column=0)
aperture = tk.StringVar()
tk.Entry(bordes, textvariable=aperture).grid(sticky='w', row=2, column=1)

l2gradient = tk.IntVar()
tk.Checkbutton(bordes, text="Función gradiente sofisticada", variable=l2gradient).grid(sticky='w', columnspan=2, row=3, column=0)
tk.Button(bordes, text='Detector Canny', command= lambda: process(root, 'cannyEdge', savefile.get(), [t_1.get(), t_2.get(), l2gradient.get(), aperture.get()])).grid(sticky='w', columnspan=2, row=4, column=0, pady=10)


tk.Label(bordes, text='Orden derivada X').grid(sticky='w', row=5, column=0)
dx = tk.StringVar()
tk.Entry(bordes, textvariable=dx).grid(sticky='w', row=5, column=1)

tk.Label(bordes, text='Orden derivada Y').grid(sticky='w', row=6, column=0)
dy = tk.StringVar()
tk.Entry(bordes, textvariable=dy).grid(sticky='w', row=6, column=1)

tk.Label(bordes, text='Tamaño de la matriz (1, 3, 5, 7)').grid(sticky='w', row=7, column=0)
aperture = tk.StringVar()
tk.Entry(bordes, textvariable=aperture).grid(sticky='w', row=7, column=1)

tk.Label(bordes, text='Delta').grid(sticky='w', row=8, column=0)
delta = tk.StringVar()
tk.Entry(bordes, textvariable=delta).grid(sticky='w', row=8, column=1)

tk.Button(bordes, text='Detector Sobel', command= lambda: process(root, 'sobel', savefile.get(), [dx.get(), dy.get(), aperture.get(), delta.get()])).grid(sticky='w', columnspan=2, row=9, column=0, pady=10)




tabs.add(suavizado, text = "Suavizado")
tabs.add(contraste, text = "Contraste")
tabs.add(intensidad, text = "Intensidad")
tabs.add(bordes, text = "Bordes")
tabs.pack()

savecheck.pack(anchor='w')
tk.Button(master = root, text='Exit', command = lambda: exit()).pack(side = tk.LEFT)
tk.mainloop()