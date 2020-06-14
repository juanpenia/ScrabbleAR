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

letras = {"a": os.path.join(PATH_FICHAS, "a.png"),
		"b": os.path.join(PATH_FICHAS, "b.png"),
		"c": os.path.join(PATH_FICHAS, "c.png"),
		"d": os.path.join(PATH_FICHAS, "d.png"),
		"e": os.path.join(PATH_FICHAS, "e.png"),
		"f": os.path.join(PATH_FICHAS, "f.png"),
		"g": os.path.join(PATH_FICHAS, "g.png"),
		"h": os.path.join(PATH_FICHAS, "h.png"),
		"i": os.path.join(PATH_FICHAS, "i.png"),
		"j": os.path.join(PATH_FICHAS, "j.png"),
		"k": os.path.join(PATH_FICHAS, "k.png"),
		"l": os.path.join(PATH_FICHAS, "l.png"),
		"m": os.path.join(PATH_FICHAS, "m.png"),
		"n": os.path.join(PATH_FICHAS, "n.png"),
		"o": os.path.join(PATH_FICHAS, "o.png"),
		"p": os.path.join(PATH_FICHAS, "p.png"),
		"q": os.path.join(PATH_FICHAS, "q.png"),
		"r": os.path.join(PATH_FICHAS, "r.png"),
		"s": os.path.join(PATH_FICHAS, "s.png"),
		"t": os.path.join(PATH_FICHAS, "t.png"),
		"u": os.path.join(PATH_FICHAS, "u.png"),
		"v": os.path.join(PATH_FICHAS, "v.png"),
		"w": os.path.join(PATH_FICHAS, "w.png"),
		"x": os.path.join(PATH_FICHAS, "x.png"),
		"y": os.path.join(PATH_FICHAS, "y.png"), 
		"z": os.path.join(PATH_FICHAS, "z.png")}

def casillero_segun_color(x, y): # cambiar nombre
	# cambiar ruta, obviamente
	if (x, y) in TUPLA_MARRONES:
		return os.path.join(PATH_TABLERO, 'beta_marron.png')
    
	elif (x, y) in TUPLA_ROJOS:
		return os.path.join(PATH_TABLERO, "beta_rojo3.png")

	elif (x, y) in TUPLA_AZULES:
		return os.path.join(PATH_TABLERO, "beta_azul2.png")

	elif (x, y) in TUPLA_VERDES:
		return os.path.join(PATH_TABLERO, "beta_verde2.png")

	else:
		return os.path.join(PATH_TABLERO, "fondo3.png") # nada


def generar_bolsa():
	lista = list("aaaaaaaaaaabbbccccddddeeeeeeeeeeeffgghhiiiiiijjkllllmmmnnnnnooooooooppqrrrrsssssssttttuuuuuuvvwxyz")
	shuffle(lista)
	return lista

def sacar_letra(bolsa): 
	#print("before:", bolsa) #debug
	letra = choice(bolsa)
	bolsa.remove(letra)
	#print("after:", bolsa) #debug
	return letra
# fin sacar_letra


def generar_tablero(tj):
	# tj = tiempo de juego
	
	bolsa = generar_bolsa()

	matriz = []
	for i in range(15):
		matriz.append([])
		for j in range(15):
			matriz[i].append(sg.Button(image_filename=casillero_segun_color(i, j), key=(i,j), pad=(0, 0)))

	col_derecha = matriz.copy()

	col_derecha.append([sg.Text()])
	col_derecha.append([sg.Button("test")])
	letras_jugador = []
	for i in range(0, 5):
		l = sacar_letra(bolsa)
		letras_jugador.append(sg.Button(image_filename=letras[l]))

	col_derecha.append(letras_jugador)

	col_izquierda = [[sg.Text("Puntajes: ")],
					[sg.Listbox([], size=(30, 10), key='lista_puntos')],
					[sg.Text("Fichas restantes: {}".format(len(bolsa)), key="bolsa_fichas")],
					[sg.Text("Tiempo restante: ?", key="cronometro")],
					[sg.Button("Cambiar Fichas" ,button_color=('black','#D9B382'), pad=((0,0),(420,0)))],
					[sg.Button("TERMINAR", button_color=('black','#D9B382'),pad=((0, 0),(25, 0))), sg.Button("POSPONER",button_color=('black', '#D9B382'), pad=((20, 0),(25, 0)))]]


	layout = [[sg.Column(col_izquierda), sg.Column(col_derecha, element_justification="right")]]

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
			window.Element((7, 7)).Update(image_filename=letras["h"])
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
			print(sacar_letra(bolsa))

		window["bolsa_fichas"].Update(value="Fichas restantes: {}".format(len(bolsa)))

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
		[sg.Button("TOP 10", button_color=('black', '#D9B382')), sg.Button("OPCIONES AVANZADAS", button_color=('black', '#D9B382'))],
		[sg.Button('INICIAR',button_color=('black', '#D9B382'),pad=((85, 0),(85, 0)))]]


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
