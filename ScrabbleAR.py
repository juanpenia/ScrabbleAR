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
	'''Esta funcion lo que hace es poner en el tablero el
		color del casillero del tablero correspondiente segun las
		"coordenadas" de la tupla
	'''
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
	'''Esta funcion genera la bolsa 
		de 98 fichas
	'''
	lista = list("aaaaaaaaaaabbbccccddddeeeeeeeeeeeffgghhiiiiiijjkllllmmmnnnnnooooooooppqrrrrsssssssttttuuuuuuvvwxyz")
	shuffle(lista)
	return lista

def sacar_letra(bolsa): 
	'''Saca una letra random
		de la "bolsa" de letras.
	'''
	letra = choice(bolsa)
	bolsa.remove(letra)
	return letra
# fin sacar_letra

def dar_fichas_maquina(bolsa):
	return [sacar_letra(bolsa) for x in range(7)]

def cambiar_fichas_maquina(bolsa, fm, cambios): # deberia haber una funcion para cambiar fichas del usuario, asi esta mas organizado
	for _i in range(7):
		bolsa.extend(fm)
	shuffle(bolsa)
	fm = dar_fichas_maquina(bolsa)
	return fm, cambios+1
	
def cambiar_fichas_jugador():
	pass

def generar_tablero():
	'''genera el tablero utilizando la funcion 
	casillero_segun_color de una dimension de 
	15x15
	'''
	tablero = []
	for i in range(15):
		tablero.append([])
		for j in range(15):
			tablero[i].append(sg.Button(image_filename=casillero_segun_color(i, j), image_size=(32, 32), key=(i,j), pad=(0, 0)))
	return tablero

def generar_ventana_de_juego(tj): # tj = tiempo de juego
	# cambio de fichas
	'''Esta funcion es la que que inicia el juego,utilizando los procesos
	declarados anteriormente.Tambien se encarga de generar el cronometro.
	'''
	cambios_jugador = 0
	_cambios_maquina = 0 # todavia no se usa
	# la idea es que en algun momento de la logica del cpu se use asi:
	# fichas_maquina, cambios_maquina = cambiar_fichas_maquina(bolsa, fichas_maquina, cambios_maquina)

	cambiando_fichas = False
	estado_ficha = {"ficha_jugador_0": False, 
				"ficha_jugador_1": False, 
				"ficha_jugador_2": False, 
				"ficha_jugador_3": False, 
				"ficha_jugador_4": False,
				"ficha_jugador_5": False,
				"ficha_jugador_6": False}           # deberia haber una clase ficha mepa, digoooooooooooooooooooo

	# cronometro related
	fin = now() + (tj * 60)

	# bolsa de fichas
	bolsa = generar_bolsa()

	# fichas de la maquina:
	_fichas_maquina = dar_fichas_maquina(bolsa)

	# columnas: 
	# fichas computadora: 
	col_arriba = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18)),sg.Text(" "*10)]]
	for i in range(7):
		col_arriba[0].append(sg.Button(image_filename=letras["?"], border_width=0, pad =((9,0),(10,0)),button_color=('black', '#191970')))

	# tablero de juego:
	col_tablero = generar_tablero()

	# letras del jugador:
	lista_selec = []
	col_derecha = [[sg.Text(" "*45), sg.Text("Letras seleccionadas: ", key="letras_selecc",size=(180, None))]]

	letras_jugador = [sg.Text(" "*45)]
	for i in range(0, 7):
		l = sacar_letra(bolsa) # deberia devolver un objeto y no una letra
		letras_jugador.append(sg.Button(l, font="Arial 1", image_filename=letras[l], button_color=('black', '#191970'), border_width=0,key="ficha_jugador_{}".format(i)))
		#letras_jugador.append(sg.Button(l, font="Arial 1", image_filename=letras[l], key="ficha_jugador_{}".format(i)))

	col_derecha.append(letras_jugador)

	# panel izquierdo:
	headings_tabla = ("Jugador", "Puntaje")
	col_izquierda = [[sg.Text("Puntajes: ")],
					[sg.Table([], headings_tabla, select_mode="browse", col_widths=(10, 10), num_rows=10, auto_size_columns=False,key="tabla_puntos")],
					[sg.Text("Fichas restantes: {}".format(len(bolsa)), key="bolsa_fichas")],
					[sg.Text("Tiempo restante: ?", key="cronometro")],
					[sg.Button("Cambiar Fichas", button_color=('black', '#D9B382'), pad=((0, 0), (200, 0)), key="cambiar_fichas")],
					[sg.Button("TERMINAR", button_color=('black', '#D9B382'), pad=((0, 0), (25, 0))), sg.Button("POSPONER", button_color=('black', '#D9B382'), pad=((20, 0), (25, 0)))]]



	layout = [[sg.Column(col_arriba)],
			[sg.Column(col_izquierda), sg.Column(col_tablero, pad=(0,26), element_justification="right")],
			[sg.Column(col_derecha)]]

	window = sg.Window("ScrabbleAR", layout, size=(900, 700)).Finalize()
	#window.Maximize()

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
			# me gustaria hacer que esto sea una funcion, asi queda mejor y mas prolijo aca
			if(cambios_jugador >= 3):
				sg.Popup("f") # cambiar
			if((cambiando_fichas) and len(lista_selec)):
				salida = sg.PopupOKCancel("Esta seguro que desea cambiar las fichas?", title="!!")
				if(salida == "OK"):
					bolsa.extend(lista_selec)
					shuffle(bolsa)
					for _x in lista_selec:
						l = sacar_letra(bolsa)
						for i in range(7): #debug, deberia ser mejor y mas prolijo
							if(estado_ficha["ficha_jugador_{}".format(i)]):
								window["ficha_jugador_{}".format(i)].Update(text=l, image_filename=letras[l])
								estado_ficha["ficha_jugador_{}".format(i)] = False
								break
					cambios_jugador += 1
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
				if(not estado_ficha[event]):
					#window[event].Update(border_width=3)
					lista_selec.append(window[event].GetText())
					window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(lista_selec).upper()))
				else:
					lista_selec.remove(window[event].GetText())
					window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(lista_selec).upper()))
				estado_ficha[event] = not estado_ficha[event]

		window["bolsa_fichas"].Update(value="Fichas restantes: {}".format(len(bolsa)))

		# cronometro

		if now() < fin:
			# para mayor legibilidad
			min_restantes = int((fin - now()) // 60)
			seg_restantes = int((fin - now()) % 60)
			window["cronometro"].Update(value="Tiempo: {:02d}:{:02d}".format(min_restantes, seg_restantes))
			
	window.Close()


def mostrar_top10(puntajes):
	'''Esta funcion genera el boton "top 10"
	donde se puede visualizar un top 10 con los puntajes
	obtenidos del tipo: fecha + puntaje + nivel.

	'''
	ancho_columnas = (10, 10)
	headings = ("Jugador", "Puntaje")
	layout = [[sg.Table(puntajes, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
	window = sg.Window("TOP 10", layout, resizable=True, finalize=True).Finalize()
	while True:
		event, _values = window.read()
		if event is None:
			break


def popup_top10_vacio():
	'''Esta funcion muestra una imagen
	en caso de que el top 10 este vacio
	'''	
	#sg.Popup("No hay puntajes registrados.", title=":(")
	sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(") # cambiar despues jeje


# comienzo de "main"

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
		generar_ventana_de_juego(values["tiempo"])

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

window.Close()