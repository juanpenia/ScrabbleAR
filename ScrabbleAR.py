import PySimpleGUI as sg
import os
from sys import platform
from random import shuffle, choice
#from pattern.es import verbs, spelling, lexicon 

PATH_TABLERO = 'img/tablero'
PATH_FICHAS = 'img/fichas'

sg.LOOK_AND_FEEL_TABLE['Fachero'] = {'BACKGROUND': '#191970', # midnight blue
										'TEXT': '#D9B382', # BEIGE
										'INPUT': '#D9B382',
										'TEXT_INPUT': '#191970',
										'SCROLL': '#c7e78b',
										#'BUTTON': ('black', '#D9B382'),
										'BUTTON': ('black', '#F5F5F5'),
										'PROGRESS': ('#01826B', '#D0D0D0'),
										'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
									}

#terminar tablero commit de prueba

sg.theme('Fachero') # tiene que ser cambiado

# no se bo
TUPLA_MARRONES = ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14))
TUPLA_ROJOS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (1, 13), (2, 12), (3, 11), (4, 10), (5, 9), (9, 5), (10, 4), (11, 3), (12, 2), (13, 1), (13, 13), (12, 12), (11, 11), (10, 10), (9, 9))
TUPLA_AZULES = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13))
TUPLA_VERDES = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13), (0, 3), (0, 10), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))

#letras = {a:"a.png", b: "b.png",c: "c.png", d: "d.png",e: "e.png", f: "f.png",g: "g.png", h: "h.png",i: "i.png", j: "j.png",k: "k.png", l: "l.png",m: "m.png", n: "n.png",o: "o.png", p: "p.png",q: "q.png", r: "r.png",s: "s.png", t: "t.png",u: "u.png", v: "v.png",w: "w.png", x: "x.png",y: "y.png", z: "z.png"}

def ImagenSegunColor(x, y): # cambiar nombre
	# cambiar ruta, obviamente
	if (x, y) in TUPLA_MARRONES:
		return os.path.join(PATH_TABLERO, 'beta_marron.png')
    
	elif (x, y) in TUPLA_ROJOS:
		return os.path.join(PATH_TABLERO, "beta_rojo2.png")

	elif (x, y) in TUPLA_AZULES:
		return os.path.join(PATH_TABLERO, "beta_azul.png")

	elif (x, y) in TUPLA_VERDES:
		return os.path.join(PATH_TABLERO, "beta_verde.png")

	else:
		return os.path.join(PATH_TABLERO, "fondo.png") # nada


def GenerarBolsa():
	lista = list("aaaaaaaaaaabbbccccddddeeeeeeeeeeeffgghhiiiiiijjkllllmmmnnnnnooooooooppqrrrrsssssssttttuuuuuuvvwxyz")
	shuffle(lista)
	return lista

def generar_tablero():
	
	Bolsa = GenerarBolsa()

	matriz = []
	for i in range(15):
		matriz.append([])
		for j in range(15):
			matriz[i].append(sg.Button(image_filename=ImagenSegunColor(i, j), key=(i,j), pad=(0, 0)))

	col_derecha = matriz.copy()

	col_derecha.append([sg.Text()])
	col_derecha.append([sg.Button("test")])

	col_izquierda = [[sg.Listbox([], size=(30, 10), key='lista_puntos')],
					[sg.Text("Fichas restantes: {}".format(len(Bolsa)))],
					[sg.Text("Tiempo restante: 10 años")],
					[sg.Button("Cambiar Fichas")],
					[sg.Button("TERMINAR"), sg.Button("POSPONER")]]

	layout = [[sg.Column(col_izquierda), sg.Column(col_derecha)]]

	window = sg.Window("ScrabbleAR", layout).Finalize()
	window.Maximize()

	while True:

		# el "_" detras de una variable significa que no se usa, es para que no salte warning
		# cuando la usemos, le sacamos el "_"
		event, _values = window.Read()

		if event is None:
			break

		# test
		if event is "test":
			window.Element((7, 7)).Update(image_filename=os.path.join(PATH_FICHAS, "h.png"))
			window.Element((7, 8)).Update(image_filename=os.path.join(PATH_FICHAS, "e.png"))
			window.Element((7, 9)).Update(image_filename=os.path.join(PATH_FICHAS, "r.png"))
			window.Element((7, 10)).Update(image_filename=os.path.join(PATH_FICHAS, "n.png"))
			window.Element((7, 11)).Update(image_filename=os.path.join(PATH_FICHAS, "i.png"))

# fin generar_tablero()

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
	[sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), key="niveles")],
	[sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), key="tiempo")],
	[sg.Button("INICIAR")]]

window = sg.Window("ScrabbleAR", layout, size=(250, 250)).Finalize()

while True:
	event, values = window.Read()

	if event is None:
		break

	if event is "INICIAR":
		window.Close()
		generar_tablero()