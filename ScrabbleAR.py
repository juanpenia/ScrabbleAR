import PySimpleGUI as sg
import os
from json import load, dump
from sys import platform
from random import shuffle, choice
from time import time as now
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
TUPLA_VERDES = ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))

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


def generar_tablero(tj):
	# tj = tiempo de juego
	
	Bolsa = GenerarBolsa()

	matriz = []
	for i in range(15):
		matriz.append([])
		for j in range(15):
			matriz[i].append(sg.Button(image_filename=ImagenSegunColor(i, j), key=(i,j), pad=(0, 0)))

	col_derecha = matriz.copy()

	col_derecha.append([sg.Text()])
	col_derecha.append([sg.Button("test")])

	col_izquierda = [[sg.Text("Puntajes: ")],
					[sg.Listbox([], size=(30, 10), key='lista_puntos')],
					[sg.Text("Fichas restantes: {}".format(len(Bolsa)), key="bolsa")],
					[sg.Text("Tiempo restante: ?", key="cronometro")],
					[sg.Button("Cambiar Fichas")],
					[sg.Button("TERMINAR"), sg.Button("POSPONER")]]

	layout = [[sg.Column(col_izquierda), sg.Column(col_derecha)]]

	window = sg.Window("ScrabbleAR", layout).Finalize()
	window.Maximize()

	# cronometro related

	fin = now() + (tj * 60)

	while True:

		# el "_" detras de una variable significa que no se usa, es para que no salte warning
		# cuando la usemos, le sacamos el "_"
		event, _values = window.Read(timeout=10)

		if event is None:
			break

		# test
		if event is "test":

			# jejejeje
			window.Element((7, 7)).Update(image_filename=os.path.join(PATH_FICHAS, "h.png"))
			window.Element((7, 8)).Update(image_filename=os.path.join(PATH_FICHAS, "e.png"))
			window.Element((7, 9)).Update(image_filename=os.path.join(PATH_FICHAS, "r.png"))
			window.Element((7, 10)).Update(image_filename=os.path.join(PATH_FICHAS, "n.png"))
			window.Element((7, 11)).Update(image_filename=os.path.join(PATH_FICHAS, "i.png"))

			window.Element((6, 8)).Update(image_filename=os.path.join(PATH_FICHAS, "p.png"))
			window.Element((8, 8)).Update(image_filename=os.path.join(PATH_FICHAS, "n.png"))
			window.Element((9, 8)).Update(image_filename=os.path.join(PATH_FICHAS, "i.png"))
			window.Element((10, 8)).Update(image_filename=os.path.join(PATH_FICHAS, "a.png"))

			window.Element((4, 11)).Update(image_filename=os.path.join(PATH_FICHAS, "f.png"))
			window.Element((5, 11)).Update(image_filename=os.path.join(PATH_FICHAS, "e.png"))
			window.Element((6, 11)).Update(image_filename=os.path.join(PATH_FICHAS, "l.png"))

		# cronometro

		if now() < fin:
			# para mayor legibilidad
			min_restantes = int((fin - now()) // 60)
			seg_restantes = int((fin - now()) % 60)
			window["cronometro"].Update(value="Tiempo: {:02d}:{:02d}".format(min_restantes, seg_restantes))

# fin generar_tablero()

def mostrar_top10(puntajes):
	ancho_columnas = (10, 10)
	headings = ("Jugador", "Puntaje")
	layout = [[sg.Table(puntajes, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
	window = sg.Window("TOP 10", layout, resizable=True, finalize=True).Finalize()
	while True:
		event, _values = window.read()
		if event is None:
			break

# fin mostrar_top10

def popup_top10_vacio():
	#sg.Popup("No hay puntajes registrados.", title=":(")
	sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(") # cambiar despues jeje

# fin pop_top10_vacio

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
		[sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), default_value="Facil", key="niveles")],
		[sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), default_value=20, key="tiempo")],
		[sg.Button("TOP 10"),sg.Button("OPCIONES AVANZADAS")],
		[sg.Button("INICIAR")]]


window = sg.Window("ScrabbleAR", layout, size=(250, 250)).Finalize()

while True:
	event, values = window.Read()

	if event is None:
		break

	if event is "INICIAR":
		window.Close()
		generar_tablero(values["tiempo"])

	if event is "TOP 10":
		if(os.path.isfile("puntajes.json")):
			with open("puntajes.json") as arc:
				datos = load(arc)
				if not datos:
					popup_top10_vacio()
				else:
					puntajes = sorted(datos.items(), reverse=True, key=lambda x:x[1])
					mostrar_top10(puntajes)

		else:
			popup_top10_vacio()