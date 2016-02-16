import functions

from tkinter import *
from tkinter import filedialog
from ttk import *

def process(function):
	options = { 'multiple': False, 'filetypes': [('Images', '.jpg .png')] }
	name = filedialog.askopenfilename(**options)

	if(name):
		process = getattr(functions, function)
		process(name)
	else:
		return
	
root = Tk()

tabs = Notebook(root)

suavizado = Frame(tabs)
Button(suavizado, text='Filtro mediana', command= lambda: process('median')).pack(anchor='w', padx=10, pady=10)
Button(suavizado, text='Supresión de ruido', command= lambda: process('denoise')).pack(anchor='w', padx=10, pady=10)

contraste = Frame(tabs)
Button(contraste, text='Ecualización del histograma', command= lambda: process('equalizeHist')).pack(anchor='w', padx=10, pady=10)
Button(contraste, text='Ecualización adaptativa del histograma', command= lambda: process('CLAHE')).pack(anchor='w', padx=10, pady=10)

intensidad = Frame(tabs)
Button(intensidad, text='Trasnformación logarítmica', command= lambda: process('logTransform')).pack(anchor='w', padx=10, pady=10)
Button(intensidad, text='Trasnformación por potencias', command= lambda: process('gammaCorrection')).pack(anchor='w', padx=10, pady=10)



tabs.add(suavizado, text = "Suavizado")
tabs.add(contraste, text = "Contraste")
tabs.add(intensidad, text = "Intensidad")
tabs.pack()

Button(master = root, text='Exit', command = lambda: exit()).pack(side = LEFT)
mainloop()