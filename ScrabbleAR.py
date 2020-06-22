#!/usr/bin/env python3
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
										'BUTTON': ('black', '#d1d6d7'),
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

letras = {"a": os.path.join(PATH_FICHAS, "A.png"),
		"b": os.path.join(PATH_FICHAS, "B.png"),
		"c": os.path.join(PATH_FICHAS, "C.png"),
		"d": os.path.join(PATH_FICHAS, "D.png"),
		"e": os.path.join(PATH_FICHAS, "E.png"),
		"f": os.path.join(PATH_FICHAS, "F.png"),
		"g": os.path.join(PATH_FICHAS, "G.png"),
		"h": os.path.join(PATH_FICHAS, "H.png"),
		"i": os.path.join(PATH_FICHAS, "I.png"),
		"j": os.path.join(PATH_FICHAS, "J.png"),
		"k": os.path.join(PATH_FICHAS, "K.png"),
		"l": os.path.join(PATH_FICHAS, "L.png"),
		"m": os.path.join(PATH_FICHAS, "M.png"),
		"n": os.path.join(PATH_FICHAS, "N.png"),
		"o": os.path.join(PATH_FICHAS, "O.png"),
		"p": os.path.join(PATH_FICHAS, "P.png"),
		"q": os.path.join(PATH_FICHAS, "Q.png"),
		"r": os.path.join(PATH_FICHAS, "R.png"),
		"s": os.path.join(PATH_FICHAS, "S.png"),
		"t": os.path.join(PATH_FICHAS, "T.png"),
		"u": os.path.join(PATH_FICHAS, "U.png"),
		"v": os.path.join(PATH_FICHAS, "V.png"),
		"w": os.path.join(PATH_FICHAS, "W.png"),
		"x": os.path.join(PATH_FICHAS, "X.png"),
		"y": os.path.join(PATH_FICHAS, "Y.png"), 
		"z": os.path.join(PATH_FICHAS, "Z.png"),
		"?": os.path.join(PATH_FICHAS, "question_mark.png")}
	

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
	letra = choice(bolsa)
	bolsa.remove(letra)
	return letra
# fin sacar_letra

#def generar_tablero2(tj):        #Tablero 2 Medium mode 
	# tj = tiempo de juego
#	cambiando_fichas = False
#	_fichas_seleccionadas = 0
#	dic_debug = {"ficha_jugador_0": False, 
#				"ficha_jugador_1": False, 
#				"ficha_jugador_2": False, 
#				"ficha_jugador_3": False, 
#				"ficha_jugador_4": False,
#				"ficha_jugador_5": False,
#				"ficha_jugador_6": False}          
#	bolsa = generar_bolsa()


def generar_tablero1(tj):        #Tablero 1 Easy mode 
	# tj = tiempo de juego
	cambiando_fichas = False
	dic_debug = {"ficha_jugador_0": False, 
				"ficha_jugador_1": False, 
				"ficha_jugador_2": False, 
				"ficha_jugador_3": False, 
				"ficha_jugador_4": False,
				"ficha_jugador_5": False,
				"ficha_jugador_6": False}           # deberia haber una clase ficha mepa, digoooooooooooooooooooo
	bolsa = generar_bolsa()

	matriz = []
	for i in range(15):
		matriz.append([])
		for j in range(15):
			matriz[i].append(sg.Button(image_filename=casillero_segun_color(i, j), key=(i,j), pad=(0, 0))) 

	col_derecha = matriz.copy()

	lista_selec = []
	#col_derecha.append([sg.Text()])
	col_derecha.append([sg.Button("test")])
	col_derecha.append([sg.Text("Letras seleccionadas: ", key="letras_selecc", size=(180, None))])

	letras_jugador = []
	for i in range(0, 7):
		l = sacar_letra(bolsa) # deberia devolver un objeto y no una letra
		#letras_jugador.append(sg.Button(l, font="Arial 1", image_filename=letras[l], button_color=('black', '#191970'), border_width=0, key="ficha_jugador_{}".format(i)))
		letras_jugador.append(sg.Button(l, font="Arial 1", image_filename=letras[l], key="ficha_jugador_{}".format(i)))

	col_derecha.append(letras_jugador)

	headings_tabla = ("Jugador", "Puntaje")
	col_izquierda = [[sg.Text("Puntajes: ", size=(70,0))],
					[sg.Table([], headings_tabla, select_mode="browse", col_widths=(10, 10), num_rows=10, auto_size_columns=False, key="tabla_puntos")],
					[sg.Text("Fichas restantes: {}".format(len(bolsa)), key="bolsa_fichas")],
					[sg.Text("Tiempo restante: ?", key="cronometro")],
					[sg.Button("Cambiar Fichas", button_color=('black', '#D9B382'), pad=((0, 0), (530, 0)), key="cambiar_fichas")],
					[sg.Button("TERMINAR", button_color=('black', '#D9B382'), pad=((0, 0), (25, 0))), sg.Button("POSPONER", button_color=('black', '#D9B382'), pad=((20, 0), (25, 0)))]]


	layout = [[sg.Column(col_izquierda), sg.Column(col_derecha, pad=(0,0))]]

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


		if event is "TERMINAR": #cuando finaliza :   En ese momento se muestran las fichas que posee cada jugador y se recalcula el puntaje restando al mismo el valor de dichas fichas
			sg.PopupOKCancel("¿Esta seguro que desea salir?", title="!")
			break
		if event is "POSPONER": #  Al elegir esta opción se podrá guardar la partida para continuarla luego. En este caso, se podrá guardar la partida actual teniendo en cuenta la información del tablero y el tiempo restante. Al momento de iniciar el juego, se pedirá si se desea continuar con la partida guardada (si es que hay una) o iniciar una nueva. En cualquier caso siempre habrá una única partida guardada.

			pass


	
		if event is "cambiar_fichas": # si se le asigna una key, no se lo puede llamar por el contenido del boton
			if((cambiando_fichas) and len(lista_selec)):
				salida = sg.PopupOKCancel("Esta seguro que desea cambiar las fichas?", title="!!")
				if(salida == "OK"):
					bolsa.extend(lista_selec)
					shuffle(bolsa)
					for _x in lista_selec:
						l = sacar_letra(bolsa)
						for i in range(7): #debug, deberia ser mejor y mas prolijo
							if(dic_debug["ficha_jugador_{}".format(i)]):
								window["ficha_jugador_{}".format(i)].Update(text=l, image_filename=letras[l])
								dic_debug["ficha_jugador_{}".format(i)] = False
								break
				lista_selec = []
				window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(lista_selec).upper()))
			cambiando_fichas = not cambiando_fichas
			if(cambiando_fichas):
				window["cambiar_fichas"].Update(button_color=('white', '#008000'))
			else:
				window["cambiar_fichas"].Update(button_color=('black', '#D9B382'))

		if event in ("ficha_jugador_0", "ficha_jugador_1", "ficha_jugador_2", "ficha_jugador_3", "ficha_jugador_4", "ficha_jugador_5", "ficha_jugador_6"):
			if(cambiando_fichas):
				# terminar
				if(not dic_debug[event]):
					#window[event].Update(border_width=3)
					lista_selec.append(window[event].GetText())
					window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(lista_selec).upper()))
				else:
					lista_selec.remove(window[event].GetText())
					window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(lista_selec).upper()))
				dic_debug[event] = not dic_debug[event]

		# test
		if event is "test":

			# jejejeje
			window.Element((7, 7)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["h"])
			window.Element((7, 8)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["e"])
			window.Element((7, 9)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["r"])
			window.Element((7, 10)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["n"])
			window.Element((7, 11)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["i"])

			window.Element((6, 8)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["p"])
			window.Element((8, 8)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["n"])
			window.Element((9, 8)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["i"])
			window.Element((10, 8)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["a"])
			window.Element((11, 8)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["?"])

			window.Element((4, 11)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["f"])
			window.Element((5, 11)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["e"])
			window.Element((6, 11)).Update(button_color=('black', '#d1d6d7'), image_filename=letras["l"])
			try:
				sacar_letra(bolsa)
			except IndexError:
				sg.Popup("No bro, no hay mas fixas") #debug, este boton ni va a existir

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
		
		[sg.Button('CONTINUAR PARTIDA',button_color=('black', '#D9B382'),pad=((45, 0),(30, 0)))],
		[sg.Button('INICIAR',button_color=('black', '#D9B382'),pad=((80, 0),(30, 0)))]]


window = sg.Window("ScrabbleAR", layout, size=(250, 250)).Finalize()

while True:
	event, values = window.Read()

	if event is None:
		break

	if event is "INICIAR":
		window.Close()
		#aca hay que hacer if,para preguntar que nivel es y asi mostrar el tablero correspondiente a cada nivel
		generar_tablero1(values["tiempo"])

	if event is "CONTINUAR PARTIDA": #Se debe  poder seguir la partida que fue pospuesta anteriormente.
			pass

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

